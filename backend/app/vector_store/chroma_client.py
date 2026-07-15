import asyncio
from typing import Any

from ..config import Settings
from ..exceptions import ExternalServiceError


class ChromaStore:
    """Thin lazy wrapper; no client, files, or network services are touched on import."""

    def __init__(self, settings: Settings):
        self.settings = settings
        self._collection = None

    def _get_collection(self):
        if self._collection is None:
            try:
                import chromadb

                client = chromadb.PersistentClient(path=self.settings.chroma_path)
                self._collection = client.get_or_create_collection(
                    name=self.settings.chroma_collection_name,
                    metadata={"hnsw:space": "cosine"},
                )
            except Exception as exc:
                raise ExternalServiceError("Vector store is unavailable.") from exc
        return self._collection

    async def upsert(self, ids: list[str], documents: list[str], embeddings: list[list[float]], metadatas: list[dict]) -> None:
        def operation():
            self._get_collection().upsert(ids=ids, documents=documents, embeddings=embeddings, metadatas=metadatas)
        try:
            await asyncio.to_thread(operation)
        except ExternalServiceError:
            raise
        except Exception as exc:
            raise ExternalServiceError("Could not index transcript vectors.") from exc

    async def query(self, embedding: list[float], video_id: str, limit: int) -> list[dict[str, Any]]:
        def operation():
            return self._get_collection().query(
                query_embeddings=[embedding],
                n_results=limit,
                where={"youtubeVideoId": video_id},
                include=["documents", "metadatas", "distances"],
            )
        try:
            result = await asyncio.to_thread(operation)
            documents = (result.get("documents") or [[]])[0]
            metadatas = (result.get("metadatas") or [[]])[0]
            distances = (result.get("distances") or [[]])[0]
            return [
                {"text": document, "metadata": metadata or {}, "distance": distances[i] if i < len(distances) else None}
                for i, (document, metadata) in enumerate(zip(documents, metadatas))
            ]
        except ExternalServiceError:
            raise
        except Exception as exc:
            raise ExternalServiceError("Could not search transcript vectors.") from exc

    async def delete_video(self, video_id: str) -> None:
        try:
            await asyncio.to_thread(lambda: self._get_collection().delete(where={"youtubeVideoId": video_id}))
        except ExternalServiceError:
            raise
        except Exception as exc:
            raise ExternalServiceError("Could not replace existing transcript vectors.") from exc
