import asyncio
from typing import Optional
from playwright.async_api import async_playwright, Browser, Page
from config.settings import settings
from utils.logger import get_logger

logger = get_logger(__name__)


class BrowserHandler:
    def __init__(self):
        self.browser: Optional[Browser] = None
        self.playwright = None

    async def start(self) -> None:
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(
            headless=settings.BROWSER_HEADLESS,
            args=["--disable-blink-features=AutomationControlled"]
        )
        logger.info("Browser started")

    async def stop(self) -> None:
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
        logger.info("Browser stopped")

    async def fetch_page(self, url: str) -> Optional[str]:
        if not self.browser:
            raise RuntimeError("Browser not started. Call start() first.")
        
        page: Page = await self.browser.new_page()
        page.set_default_timeout(settings.BROWSER_TIMEOUT)
        
        try:
            logger.info(f"Fetching: {url}")
            response = await page.goto(url, wait_until="networkidle", timeout=settings.BROWSER_TIMEOUT)
            
            if not response:
                logger.warning(f"No response for {url}")
                return None
            
            if response.status >= 400:
                logger.warning(f"HTTP {response.status} for {url}")
                return None
            
            await page.wait_for_timeout(2000)
            content = await page.content()
            logger.info(f"Successfully fetched {url} ({len(content)} chars)")
            return content
            
        except Exception as e:
            logger.error(f"Error fetching {url}: {e}")
            return None
        finally:
            await page.close()

    async def discover_subpages(self, base_url: str, html: str) -> list[str]:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, "html.parser")
        
        subpage_keywords = ["/about", "/team", "/company", "/contact", "/pricing", "/leadership", "/founders", "/careers"]
        subpages = set()
        
        for link in soup.find_all("a", href=True):
            href = link["href"]
            if not href or href.startswith("#") or href.startswith("mailto:") or href.startswith("tel:"):
                continue
            
            if href.startswith("/"):
                full_url = base_url.rstrip("/") + href
            elif href.startswith("http") and base_url in href:
                full_url = href
            else:
                continue
            
            for keyword in subpage_keywords:
                if keyword in full_url.lower() and full_url != base_url:
                    subpages.add(full_url)
                    break
        
        result = list(subpages)[:settings.MAX_SUBPAGES]
        logger.info(f"Discovered {len(result)} subpages for {base_url}")
        return result