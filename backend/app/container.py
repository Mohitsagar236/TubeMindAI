from dataclasses import dataclass

from .config import Settings
from .services.chunking_service import ChunkingService
from .services.content_service import ContentService
from .services.embedding_service import EmbeddingService
from .services.llm_service import LLMService
from .services.rag_service import RAGService
from .services.transcript_service import TranscriptService
from .services.video_service import VideoService
from .vector_store.chroma_client import ChromaStore
from .vector_store.retriever import VideoRetriever


@dataclass
class ServiceContainer:
    videos: VideoService
    rag: RAGService
    content: ContentService


def build_container(settings: Settings) -> ServiceContainer:
    embeddings = EmbeddingService(settings)
    store = ChromaStore(settings)
    videos = VideoService(TranscriptService(), ChunkingService(), embeddings, store)
    llm = LLMService(settings)
    retriever = VideoRetriever(embeddings, store, settings)
    return ServiceContainer(videos=videos, rag=RAGService(videos, retriever, llm), content=ContentService(videos, llm, settings))
