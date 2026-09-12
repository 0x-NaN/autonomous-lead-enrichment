import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    OLLAMA_HOST: str = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "qwen2.5:7b")
    
    BROWSER_TIMEOUT: int = int(os.getenv("BROWSER_TIMEOUT", "30000"))
    BROWSER_HEADLESS: bool = os.getenv("BROWSER_HEADLESS", "true").lower() == "true"
    
    MAX_SUBPAGES: int = int(os.getenv("MAX_SUBPAGES", "5"))
    MAX_TOKENS_PER_DOMAIN: int = int(os.getenv("MAX_TOKENS_PER_DOMAIN", "3000"))
    
    TARGET_DOMAINS: list[str] = os.getenv("TARGET_DOMAINS", "postman.com,supabase.com,vapi.ai").split(",")
    
    OUTPUT_DIR: str = os.getenv("OUTPUT_DIR", "output")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

settings = Settings()