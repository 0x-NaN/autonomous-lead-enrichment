import html2text
from bs4 import BeautifulSoup
import tiktoken
from config.settings import settings
from utils.logger import get_logger

logger = get_logger(__name__)


class ContentExtractor:
    def __init__(self):
        self.converter = html2text.HTML2Text()
        self.converter.ignore_links=False
        self.converter.ignore_images=True
        self.converter.ignore_emphasis=False
        self.converter.body_width=0
        self.encoding = tiktoken.get_encoding("cl100k_base")

    def extract(self, html: str) -> str:
        soup = BeautifulSoup(html, "html.parser")

        for tag in soup(["script", "style", "nav", "footer", "header", "aside", "noscript", "svg", "iframe"]):
            tag.decompose()

        for tag in soup.find_all(class_=lambda x: x and any(kw in str(x).lower() for kw in ["nav", "menu", "footer", "header", "sidebar", "cookie", "banner", "popup", "modal"])):
            tag.decompose()

        main_content = soup.find("main") or soup.find("article") or soup.find("div", class_=lambda x: x and "content" in str(x).lower()) or soup.body

        if main_content:
            html = str(main_content)
        else:
            html = str(soup)

        markdown = self.converter.handle(html)
        markdown = self._clean_markdown(markdown)

        return markdown

    def _clean_markdown(self, markdown: str) -> str:
        lines = markdown.split("\n")
        cleaned = []
        prev_empty = False

        for line in lines:
            line = line.strip()
            if not line:
                if not prev_empty:
                    cleaned.append("")
                    prev_empty=True
            else:
                cleaned.append(line)
                prev_empty=False

        return "\n".join(cleaned).strip()

    def count_tokens(self, text: str) -> int:
        return len(self.encoding.encode(text))

    def truncate_to_token_limit(self, text: str, max_tokens: int = None) -> str:
        if max_tokens is None:
            max_tokens = settings.MAX_TOKENS_PER_DOMAIN

        tokens = self.encoding.encode(text)
        if len(tokens) <= max_tokens:
            return text

        truncated_tokens = tokens[:max_tokens]
        truncated = self.encoding.decode(truncated_tokens)
        logger.warning(f"Truncated content from {len(tokens)} to {max_tokens} tokens")
        return truncated