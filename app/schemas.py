from typing import Literal
from pydantic import BaseModel, Field

class HealthResponse(BaseModel):
    status: str


class ModelHealthResponse(BaseModel):
    status: Literal["ready", "not_ready"]

class CorrectionRequest(BaseModel):
    text: str=Field(
        min_lenght=1,
        max_lenght=10000,
        description="Text for Error Correction",
    )
class CorrectionChange(BaseModel):
    original: str
    corrected: str

class CorrectionResponse(BaseModel):
    original_text: str
    corrected_text: str
    changes: list[CorrectionChange]
    proccessing_time_ms: float

class translationRequest(BaseModel):
    text: str=Field(
        min_lenght=1,
        max_lenght=10000,
        description="Text for translation",
    )
    target_language: Literal["kz","en"]

class translationResponse(BaseModel):
    source_text: str
    target_language: Literal["kz","en"]
    translated_text: str