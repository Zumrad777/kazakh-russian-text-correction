"""TilTüzету MVP: rule-based correction, MyMemory translation API, optional MongoDB history."""
import os, re, json
from pathlib import Path
from typing import Literal
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

# Small .env loader; python-dotenv is not required.
def load_dotenv():
    env_file = Path(__file__).with_name('.env')
    if env_file.exists():
        for raw in env_file.read_text(encoding='utf-8').splitlines():
            line = raw.strip()
            if not line or line.startswith('#') or '=' not in line: continue
            key, value = line.split('=', 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))
load_dotenv()

app = FastAPI(title='TilTüzету API', description='MVP for mixed Kazakh/Russian text correction and translation.', version='0.3.0')

class CorrectRequest(BaseModel):
    text: str = Field(min_length=1, max_length=5000)
class CorrectResponse(BaseModel):
    original_text: str
    corrected_text: str
    changes: list[str]
    mode: str
class TranslateRequest(BaseModel):
    text: str = Field(min_length=1, max_length=5000)
    source_language: Literal['kk', 'ru', 'en'] = 'ru'
    target_language: Literal['kk', 'ru', 'en']
class TranslateResponse(BaseModel):
    translated_text: str
    source_language: str
    target_language: str
    provider: str
    demo_mode: bool

CORRECTION_RULES = [
    (r'\bsalem\b', 'сәлем'), (r'\bсалем\b', 'сәлем'), (r'\bрахмет\b', 'рақмет'),
    (r'\bрахмат\b', 'рақмет'), (r'\bказакша\b', 'қазақша'), (r'\bказахша\b', 'қазақша'),
    (r'\bкалай\b', 'қалай'), (r'\bжаксы\b', 'жақсы'), (r'\bжок\b', 'жоқ'),
    (r'\бия\b', 'иә'), (r'\bуниверге\b', 'университетке'), (r'\ббу́гин\b', 'бүгін'),
    (r'\bбугин\b', 'бүгін'), (r'\bистемедим\b', 'істемедім'),
]
def correct_text(text: str):
    result, changes = text, []
    for pattern, replacement in CORRECTION_RULES:
        regex = re.compile(pattern, re.IGNORECASE)
        def replace_case(m):
            found = m.group(0)
            if found.isupper(): return replacement.upper()
            if found[:1].isupper(): return replacement[:1].upper() + replacement[1:]
            return replacement
        updated, count = regex.subn(replace_case, result)
        if count:
            changes.append(f'{pattern[2:-2]} → {replacement} ({count})')
            result = updated
    return result, changes

DEMO_TRANSLATIONS = {
    ('сәлем','en'):'Hello', ('Сәлем','en'):'Hello', ('hello','kk'):'Сәлем', ('Hello','kk'):'Сәлем',
    ('hello','ru'):'Привет', ('Hello','ru'):'Привет', ('привет','en'):'Hello', ('Привет','en'):'Hello',
    ('спасибо','kk'):'Рақмет', ('спасибо','en'):'Thank you', ('thank you','kk'):'Рақмет', ('thank you','ru'):'Спасибо',
    ('рақмет','en'):'Thank you', ('рақмет','ru'):'Спасибо', ('как дела?','en'):'How are you?', ('как дела?','kk'):'Қалайсың?',
}

def mongo_collection():
    uri = os.getenv('MONGODB_URI', '').strip()
    if not uri: return None
    try:
        from pymongo import MongoClient
        client = MongoClient(uri, serverSelectionTimeoutMS=1500)
        client.admin.command('ping')
        return client[os.getenv('MONGODB_DATABASE', 'tiltuzetu')]['history']
    except Exception:
        return None

def save_history(record: dict):
    collection = mongo_collection()
    if collection is not None:
        try: collection.insert_one(record)
        except Exception: pass

def translate_mymemory(text: str, source: str, target: str):
    # MyMemory Translation Memory API supports a simple GET endpoint; no key is required for basic requests.
    params = urlencode({'q': text, 'langpair': f'{source}|{target}', 'mt': '1'})
    request = Request('https://api.mymemory.translated.net/get?' + params, headers={'Accept': 'application/json', 'User-Agent': 'TilTuzetu-MVP/0.3'})
    try:
        with urlopen(request, timeout=18) as response:
            data = json.loads(response.read().decode('utf-8'))
    except HTTPError as exc:
        raise HTTPException(status_code=502, detail=f'MyMemory API returned HTTP {exc.code}. Please try again later.') from exc
    except (URLError, TimeoutError, ValueError) as exc:
        raise HTTPException(status_code=502, detail='Could not reach MyMemory translation API. Check your internet connection and try again.') from exc
    response_data = data.get('responseData') or {}
    translated = (response_data.get('translatedText') or '').strip()
    if not translated or data.get('responseStatus') not in (200, '200'):
        raise HTTPException(status_code=502, detail='Translation provider did not return a translation for this language pair. Try another source language or a shorter sentence.')
    return translated

@app.get('/api/health')
def health():
    mongo_enabled = bool(os.getenv('MONGODB_URI', '').strip())
    mongo_ok = mongo_collection() is not None if mongo_enabled else False
    return {'status':'ok','app':'TilTüzету','correction_mode':'rule-based-demo','translation_provider':'MyMemory','translation_configured':True,'database':'MongoDB connected' if mongo_ok else ('MongoDB not connected (history remains off)' if mongo_enabled else 'local/no database configured'),'database_connected':mongo_ok,'message':'MVP API is running. Translation uses MyMemory; correction uses sample rules.'}

@app.get('/api/config')
def config():
    return {'correction':{'mode':'rule-based-demo','note':'Transparent sample rules only; no trained ByT5/mT5 model is integrated.'},'translation':{'provider':'MyMemory Translation API','requires_api_key':False,'targets':['kk','ru','en']},'database':{'optional':'MongoDB Atlas','configured':bool(os.getenv('MONGODB_URI','').strip())}}

@app.post('/api/correct', response_model=CorrectResponse)
def correct(request: CorrectRequest):
    original = request.text.strip()
    if not original: raise HTTPException(status_code=400, detail='Text must not be empty.')
    corrected, changes = correct_text(original)
    save_history({'action':'correct','original_text':original,'result_text':corrected,'changes':changes,'mode':'rule-based-demo'})
    return CorrectResponse(original_text=original, corrected_text=corrected, changes=changes, mode='rule-based-demo')

@app.post('/api/translate', response_model=TranslateResponse)
def translate(request: TranslateRequest):
    text = request.text.strip()
    if not text: raise HTTPException(status_code=400, detail='Text must not be empty.')
    if request.source_language == request.target_language:
        raise HTTPException(status_code=400, detail='Choose different source and target languages.')
    # Exact short phrases are a fallback for a classroom demo if the external service has no match.
    try:
        translated = translate_mymemory(text, request.source_language, request.target_language)
        demo = False
        provider = 'MyMemory Translation API'
    except HTTPException as exc:
        demo_translation = DEMO_TRANSLATIONS.get((text, request.target_language)) or DEMO_TRANSLATIONS.get((text.lower(), request.target_language))
        if not demo_translation: raise exc
        translated, demo, provider = demo_translation, True, 'offline-demo fallback'
    save_history({'action':'translate','source_language':request.source_language,'target_language':request.target_language,'original_text':text,'result_text':translated,'provider':provider,'demo_mode':demo})
    return TranslateResponse(translated_text=translated, source_language=request.source_language, target_language=request.target_language, provider=provider, demo_mode=demo)

@app.get('/api/history')
def history():
    collection = mongo_collection()
    if collection is None: return {'enabled':False,'items':[],'message':'Optional MongoDB is not connected. The MVP works without database history.'}
    try:
        items = list(collection.find({}, {'_id':0}).sort('_id', -1).limit(20))
        return {'enabled':True,'items':items}
    except Exception:
        return {'enabled':False,'items':[],'message':'MongoDB history is temporarily unavailable.'}

@app.get('/')
def index(): return FileResponse(str(Path(__file__).parent / 'static' / 'index.html'))
app.mount('/static', StaticFiles(directory=str(Path(__file__).parent / 'static')), name='static')
