from ..config import Settings
from ..services.embedding_service import EmbeddingService
from .chroma_client import ChromaStore


class VideoRetriever:
    def __init__(self, embeddings: EmbeddingService, store: ChromaStore, settings: Settings):
        self.embeddings = embeddings
        self.store = store
        self.settings = settings

    async def retrieve(self, video_id: str, question: str, api_key: str | None = None) -> list[dict]:
        vector = await self.embeddings.embed_query(question, api_key)
        # The video filter is mandatory and enforced inside ChromaStore.query too.
        return await self.store.query(vector, video_id, self.settings.retrieval_top_k)
