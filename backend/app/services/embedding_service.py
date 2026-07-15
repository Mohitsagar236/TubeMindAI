import asyncio

from ..config import Settings
from ..exceptions import ConfigurationError, ExternalServiceError


class EmbeddingService:
    def __init__(self, settings: Settings):
        self.settings = settings

    def _client(self, api_key: str | None = None):
        key = api_key or self.settings.openai_api_key
        if not key:
            raise ConfigurationError("An OpenAI API key is required to process this video.")
        try:
            from langchain_openai import OpenAIEmbeddings
        except ImportError as exc:
            raise ConfigurationError("OpenAI integration is not installed on the backend.") from exc
        return OpenAIEmbeddings(model=self.settings.openai_embedding_model, api_key=key)

    async def embed_documents(self, texts: list[str], api_key: str | None = None) -> list[list[float]]:
        try:
            return await self._client(api_key).aembed_documents(texts)
        except ConfigurationError:
            raise
        except Exception as exc:
            raise ExternalServiceError("Embedding service is temporarily unavailable.") from exc

    async def embed_query(self, text: str, api_key: str | None = None) -> list[float]:
        try:
            return await self._client(api_key).aembed_query(text)
        except ConfigurationError:
            raise
        except Exception as exc:
            raise ExternalServiceError("Embedding service is temporarily unavailable.") from exc
