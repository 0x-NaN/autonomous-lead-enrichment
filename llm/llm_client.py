import json
import re
import httpx
from typing import Optional
from config.settings import settings
from utils.logger import get_logger
from llm.structured_output import CompanyEnrichment

logger=get_logger(__name__)

class OllamaClient:
    def __init__(self):
        self.host=settings.OLLAMA_HOST.rstrip("/")
        self.model=settings.OLLAMA_MODEL
        self.client=httpx.AsyncClient(timeout=300.0)

    async def close(self):
        await self.client.aclose()

    async def generate(self, prompt: str, schema: dict) -> Optional[CompanyEnrichment]:
        payload={
            "model": self.model,
            "prompt": prompt,
            "format": schema,
            "stream": False,
            "options": {
                "temperature": 0.1,
                "top_p": 0.9,
                "num_predict": 2048
            }
        }

        try:
            logger.info(f"Calling Ollama with model: {self.model}")
            response=await self.client.post(f"{self.host}/api/generate", json=payload)
            response.raise_for_status()
            
            result=response.json()
            raw_output=result.get("response", "")
            
            # Strip markdown code blocks if the local model adds them
            raw_output=re.sub(r'^```json\s*', '', raw_output, flags=re.MULTILINE)
            raw_output=re.sub(r'\s*```$', '', raw_output, flags=re.MULTILINE)
            raw_output=raw_output.strip()
            
            parsed=json.loads(raw_output)
            return CompanyEnrichment(**parsed)
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM JSON output: {e}")
            return None
        except httpx.HTTPStatusError as e:
            logger.error(f"Ollama HTTP error: {e.response.status_code}")
            return None
        except Exception as e:
            logger.error(f"Ollama error: {e}")
            return None

    async def check_model(self) -> bool:
        try:
            response=await self.client.get(f"{self.host}/api/tags")
            response.raise_for_status()
            models=response.json().get("models", [])
            model_names=[m["name"] for m in models]
            return self.model in model_names
        except Exception as e:
            logger.error(f"Failed to check Ollama models: {e}")
            return False

    async def pull_model(self) -> bool:
        try:
            logger.info(f"Pulling model {self.model}...")
            response=await self.client.post(
                f"{self.host}/api/pull",
                json={"name": self.model},
                timeout=300.0
            )
            response.raise_for_status()
            logger.info(f"Model {self.model} pulled successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to pull model: {e}")
            return False