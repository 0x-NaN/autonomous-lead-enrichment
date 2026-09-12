from typing import Optional

class ScraperError(Exception):
    def __init__(self, message: str, domain: str = "", error_type: str = "unknown"):
        self.message = message
        self.domain = domain
        self.error_type = error_type
        super().__init__(message)


def handle_scraper_error(error: Exception, domain: str) -> tuple[Optional[str], float]:
    from utils.logger import get_logger
    logger = get_logger(__name__)
    
    error_msg = str(error)
    error_type = "unknown"
    
    if "timeout" in error_msg.lower():
        error_type = "timeout"
    elif "404" in error_msg or "not found" in error_msg.lower():
        error_type = "not_found"
    elif "rate limit" in error_msg.lower() or "429" in error_msg:
        error_type = "rate_limit"
    elif "blocked" in error_msg.lower() or "captcha" in error_msg.lower() or "bot" in error_msg.lower():
        error_type = "bot_block"
    elif "connection" in error_msg.lower() or "dns" in error_msg.lower():
        error_type = "connection"
    
    logger.error(f"Scraper error for {domain} [{error_type}]: {error_msg}")
    return None, 0.0