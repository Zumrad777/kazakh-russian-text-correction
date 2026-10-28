from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str="Kazakh-Russian Text Correction API"
    app_version: str="0.1.0"
    debug: bool = False

    translation_api_url: str=""
    translation_api_key: str=""

    model_path: str="models/correction"
    model_config=SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
    
settings=Settings()
