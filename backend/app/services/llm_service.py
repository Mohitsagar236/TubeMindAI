from ..config import Settings
from ..exceptions import ConfigurationError, ExternalServiceError


class LLMService:
    def __init__(self, settings: Settings):
        self.settings = settings

    async def complete(self, prompt: str, api_key: str | None = None) -> str:
        key = api_key or self.settings.openai_api_key
        if not key:
            raise ConfigurationError("An OpenAI API key is required for this request.")
        try:
            from langchain_openai import ChatOpenAI

            response = await ChatOpenAI(
                model=self.settings.openai_chat_model,
                api_key=key,
                temperature=0,
            ).ainvoke(prompt)
            content = response.content
            if isinstance(content, list):
                content = "".join(str(part.get("text", "")) if isinstance(part, dict) else str(part) for part in content)
            return str(content).strip()
        except ConfigurationError:
            raise
        except ImportError as exc:
            raise ConfigurationError("OpenAI integration is not installed on the backend.") from exc
        except Exception as exc:
            raise ExternalServiceError("The language model is temporarily unavailable.") from exc
