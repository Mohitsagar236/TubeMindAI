from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore", case_sensitive=False)

    app_name: str = "TubeMind AI"
    app_env: str = "development"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    database_url: str = "sqlite:///./tubemind.db"
    chroma_persist_dir: str = "./chroma_data"
    chroma_collection_name: str = "youtube_transcripts"
    openai_api_key: str | None = None
    openai_chat_model: str = "gpt-4o-mini"
    openai_embedding_model: str = "text-embedding-3-small"
    cors_origins: str = "http://localhost:5173,chrome-extension://*"
    retrieval_top_k: int = 5
    max_transcript_chars: int = 120_000

    @property
    def chroma_path(self) -> str:
        return str(Path(self.chroma_persist_dir).resolve())

    @property
    def cors_origin_list(self) -> list[str]:
        return [item.strip() for item in self.cors_origins.split(",") if item.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
