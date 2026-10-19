import os
import re
import json
from pathlib import Path
from typing import Literal
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field



def load_dotenv():
    env_file = Path(__file__).with_name(".env")

    if env_file.exists():
        for raw in env_file.read_text(encoding="utf-8").splitlines():
            line = raw.strip()

            if not line or line.startswith("#") or "=" not in line:
                continue

            key, value = line.split("=", 1)

            os.environ.setdefault(
                key.strip(),
                value.strip().strip('"').strip("'")
            )


load_dotenv()


app = FastAPI(
    title="TilTüzету API",
    description="MVP for mixed Kazakh/Russian text correction and translation.",
    version="0.4.0",
)

class CorrectRequest(BaseModel):
    text: str = Field(min_length=1, max_length=5000)


class CorrectResponse(BaseModel):
    original_text: str
    corrected_text: str
    changes: list[str]
    mode: str


class TranslateRequest(BaseModel):
    text: str = Field(min_length=1, max_length=5000)
    source_language: Literal["kk", "ru", "en"] = "ru"
    target_language: Literal["kk", "ru", "en"]


class TranslateResponse(BaseModel):
    translated_text: str
    source_language: str
    target_language: str
    provider: str
    demo_mode: bool



CORRECTION_RULES = [
    (r"\bsalem\b", "сәлем"),
    (r"\bсалем\b", "сәлем"),
    (r"\bрахмет\b", "рақмет"),
    (r"\bрахмат\b", "рақмет"),
    (r"\bказакша\b", "қазақша"),
    (r"\bказахша\b", "қазақша"),
    (r"\bкалай\b", "қалай"),
    (r"\bжаксы\b", "жақсы"),
    (r"\bжок\b", "жоқ"),
    (r"\бия\b", "иә"),
    (r"\bуниверге\b", "университетке"),
    (r"\bбугин\b", "бүгін"),
    (r"\bистемедим\b", "істемедім"),
]


def correct_text(text: str):
    result = text
    changes = []

    for pattern, replacement in CORRECTION_RULES:
        regex = re.compile(pattern, re.IGNORECASE)

        def replace_case(match):
            found = match.group(0)

            if found.isupper():
                return replacement.upper()

            if found[:1].isupper():
                return replacement[:1].upper() + replacement[1:]

            return replacement

        updated, count = regex.subn(replace_case, result)

        if count:
            changes.append(
                f"{pattern[2:-2]} → {replacement} ({count})"
            )
            result = updated

    return result, changes



DEMO_TRANSLATIONS = {
    ("сәлем", "en"): "Hello",
    ("сәлем!", "en"): "Hello!",
    ("салем", "en"): "Hello",
    ("салем!", "en"): "Hello!",
    ("hello", "kk"): "Сәлем",
    ("hello", "ru"): "Привет",
    ("привет", "en"): "Hello",
    ("привет", "kk"): "Сәлем",
    ("привет!", "en"): "Hello!",
    ("спасибо", "kk"): "Рақмет",
    ("спасибо", "en"): "Thank you",
    ("thank you", "kk"): "Рақмет",
    ("thank you", "ru"): "Спасибо",
    ("рақмет", "en"): "Thank you",
    ("рақмет", "ru"): "Спасибо",
    ("как дела?", "en"): "How are you?",
    ("как дела?", "kk"): "Қалайсың?",
    ("сәлем", "ru"): "Привет",
    ("сәлем!", "ru"): "Привет!",
    ("салем!", "ru"): "Привет!",
    ("сәлеметсіз бе", "ru"): "Здравствуйте",
    ("қалайсың?", "ru"): "Как дела?",
    ("қайырлы таң", "ru"): "Доброе утро",
    ("мен жақсымын", "ru"): "У меня всё хорошо",
    (
        "сәлем, мен бүгін университетке бардым.",
        "en",
    ): "Hello, I went to university today.",
}



def mongo_collection():
    uri = os.getenv("MONGODB_URI", "").strip()

    if not uri:
        return None

    try:
        from pymongo import MongoClient

        client = MongoClient(
            uri,
            serverSelectionTimeoutMS=1500,
        )
        client.admin.command("ping")

        database_name = os.getenv(
            "MONGODB_DATABASE",
            "tiltuzetu",
        )

        return client[database_name]["history"]

    except Exception:
        return None


def save_history(record: dict):
    collection = mongo_collection()

    if collection is not None:
        try:
            collection.insert_one(record)
        except Exception:
            pass


def translate_mymemory(
    text: str,
    source: str,
    target: str,
):
    params = urlencode({
        "q": text,
        "langpair": f"{source}|{target}",
        "mt": "1",
    })

    request = Request(
        "https://api.mymemory.translated.net/get?" + params,
        headers={
            "Accept": "application/json",
            "User-Agent": "TilTuzetu-MVP/0.4",
        },
    )

    try:
        with urlopen(request, timeout=15) as response:
            data = json.loads(
                response.read().decode("utf-8")
            )

    except (HTTPError, URLError, TimeoutError, ValueError) as exc:
        raise RuntimeError(
            "MyMemory translation request failed."
        ) from exc

    response_data = data.get("responseData") or {}
    translated = (
        response_data.get("translatedText") or ""
    ).strip()

    if (
        not translated
        or data.get("responseStatus") not in (200, "200")
    ):
        raise RuntimeError(
            "MyMemory did not return a valid translation."
        )

    return translated

def translate_google(
    text: str,
    source: str,
    target: str,
):
    params = urlencode({
        "client": "gtx",
        "sl": source,
        "tl": target,
        "dt": "t",
        "q": text,
    })

    request = Request(
        "https://translate.googleapis.com/translate_a/single?"
        + params,
        headers={
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json",
        },
    )

    try:
        with urlopen(request, timeout=20) as response:
            data = json.loads(
                response.read().decode("utf-8")
            )

        translated = "".join(
            part[0]
            for part in data[0]
            if part and part[0]
        ).strip()

        if not translated:
            raise ValueError("Empty translation.")

        return translated

    except (
        HTTPError,
        URLError,
        TimeoutError,
        ValueError,
        IndexError,
        TypeError,
        KeyError,
    ) as exc:
        raise RuntimeError(
            "Google Translate is temporarily unavailable."
        ) from exc


@app.get("/api/health")
def health():
    mongo_enabled = bool(
        os.getenv("MONGODB_URI", "").strip()
    )
    mongo_ok = (
        mongo_collection() is not None
        if mongo_enabled
        else False
    )

    return {
        "status": "ok",
        "app": "TilTüzету",
        "correction_mode": "rule-based-demo",
        "translation_provider": (
            "MyMemory with Google Translate fallback "
            "and offline demo"
        ),
        "translation_configured": True,
        "database": (
            "MongoDB connected"
            if mongo_ok
            else "MongoDB not connected (history remains off)"
        ),
        "database_connected": mongo_ok,
        "message": "MVP API is running.",
    }


@app.get("/api/config")
def config():
    return {
        "correction": {
            "mode": "rule-based-demo",
            "note": (
                "Sample rules only; no trained model is integrated."
            ),
        },
        "translation": {
            "provider": (
                "MyMemory, Google Translate fallback, "
                "and offline demo"
            ),
            "requires_api_key": False,
            "targets": ["kk", "ru", "en"],
        },
        "database": {
            "optional": "MongoDB Atlas",
            "configured": bool(
                os.getenv("MONGODB_URI", "").strip()
            ),
        },
    }


# Correct text
@app.post(
    "/api/correct",
    response_model=CorrectResponse,
)
def correct(request: CorrectRequest):
    original = request.text.strip()

    if not original:
        raise HTTPException(
            status_code=400,
            detail="Text must not be empty.",
        )

    corrected, changes = correct_text(original)

    save_history({
        "action": "correct",
        "original_text": original,
        "result_text": corrected,
        "changes": changes,
        "mode": "rule-based-demo",
    })

    return CorrectResponse(
        original_text=original,
        corrected_text=corrected,
        changes=changes,
        mode="rule-based-demo",
    )


@app.post(
    "/api/translate",
    response_model=TranslateResponse,
)
def translate(request: TranslateRequest):
    text = request.text.strip()

    if not text:
        raise HTTPException(
            status_code=400,
            detail="Text must not be empty.",
        )

    if request.source_language == request.target_language:
        raise HTTPException(
            status_code=400,
            detail="Choose different source and target languages.",
        )

    translated = None
    provider = None
    demo = False

    try:
        translated = translate_mymemory(
            text,
            request.source_language,
            request.target_language,
        )
        provider = "MyMemory Translation API"

    except Exception:
        try:
            translated = translate_google(
                text,
                request.source_language,
                request.target_language,
            )
            provider = "Google Translate"

        except Exception:
            normalized = text.casefold().strip()
            demo_translation = DEMO_TRANSLATIONS.get(
                (normalized, request.target_language)
            )

            if demo_translation is None:
                raise HTTPException(
                    status_code=503,
                    detail=(
                        "Both online translation services are "
                        "temporarily unavailable. Please try again "
                        "later. Offline demo supports only selected "
                        "example phrases."
                    ),
                )

            translated = demo_translation
            provider = "offline-demo fallback"
            demo = True

    save_history({
        "action": "translate",
        "source_language": request.source_language,
        "target_language": request.target_language,
        "original_text": text,
        "result_text": translated,
        "provider": provider,
        "demo_mode": demo,
    })

    return TranslateResponse(
        translated_text=translated,
        source_language=request.source_language,
        target_language=request.target_language,
        provider=provider,
        demo_mode=demo,
    )


@app.get("/api/history")
def history():
    collection = mongo_collection()

    if collection is None:
        return {
            "enabled": False,
            "items": [],
            "message": (
                "MongoDB is not connected. History is disabled."
            ),
        }

    try:
        items = list(
            collection.find({}, {"_id": 0})
            .sort("_id", -1)
            .limit(20)
        )

        return {
            "enabled": True,
            "items": items,
        }

    except Exception:
        return {
            "enabled": False,
            "items": [],
            "message": (
                "MongoDB history is temporarily unavailable."
            ),
        }


@app.get("/")
def index():
    return FileResponse(
        str(
            Path(__file__).parent
            / "static"
            / "index.html"
        )
    )


app.mount(
    "/static",
    StaticFiles(
        directory=str(
            Path(__file__).parent / "static"
        )
    ),
    name="static",
)

