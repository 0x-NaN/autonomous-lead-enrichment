from typing import List
from scraper.browser_handler import BrowserHandler
from llm.llm_client import OllamaClient
from agent.tools import process_domain
from llm.structured_output import CompanyEnrichment
from config.settings import settings
from utils.logger import get_logger

logger = get_logger(__name__)


class LeadEnrichmentAgent:
    def __init__(self):
        self.browser = BrowserHandler()
        self.llm_client = OllamaClient()

    async def initialize(self) -> bool:
        await self.browser.start()
        
        model_exists = await self.llm_client.check_model()
        if not model_exists:
            logger.info(f"Model {settings.OLLAMA_MODEL} not found, pulling...")
            success = await self.llm_client.pull_model()
            if not success:
                logger.error("Failed to pull model")
                return False
        
        logger.info("Agent initialized successfully")
        return True

    async def cleanup(self) -> None:
        await self.browser.stop()
        await self.llm_client.close()

    async def run(self, domains: List[str] = None) -> List[CompanyEnrichment]:
        if domains is None:
            domains = settings.TARGET_DOMAINS
        
        results = []
        
        for domain in domains:
            domain = domain.strip()
            if not domain:
                continue
            
            try:
                result = await process_domain(self.browser, self.llm_client, domain)
                results.append(result)
            except Exception as e:
                logger.error(f"Unexpected error processing {domain}: {e}")
                results.append(CompanyEnrichment(
                    domain=domain,
                    company_overview="Processing error",
                    target_audience="Unknown",
                    contact_points=[],
                    key_leadership=[],
                    data_confidence_score=0.0,
                    errors=[str(e)]
                ))
        
        return results