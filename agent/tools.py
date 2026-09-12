from typing import Optional, List
import json
import tiktoken
from scraper.browser_handler import BrowserHandler
from scraper.content_extractor import ContentExtractor
from llm.llm_client import OllamaClient
from llm.structured_output import CompanyEnrichment
from config.settings import settings
from utils.logger import get_logger

logger = get_logger(__name__)
encoding = tiktoken.get_encoding("cl100k_base")


def estimate_cost(input_tokens: int, output_tokens: int) -> float:
    return 0.0


async def scrape_domain(browser: BrowserHandler, domain: str) -> tuple[Optional[str], List[str]]:
    base_url = f"https://{domain}"

    html = await browser.fetch_page(base_url)
    if not html:
        logger.warning(f"Failed to fetch homepage for {domain}")
        return None, []

    subpages = await browser.discover_subpages(base_url, html)

    all_content = [html]
    for subpage in subpages:
        sub_html = await browser.fetch_page(subpage)
        if sub_html:
            all_content.append(sub_html)

    combined_html = "\n\n---PAGE BREAK---\n\n".join(all_content)
    return combined_html, subpages


async def extract_content(html: str) -> str:
    extractor = ContentExtractor()
    markdown = extractor.extract(html)
    markdown = extractor.truncate_to_token_limit(markdown)
    return markdown


async def enrich_with_llm(llm_client: OllamaClient, domain: str, content: str) -> Optional[CompanyEnrichment]:
    schema = CompanyEnrichment.model_json_schema()

    prompt = f"""Extract the following structured information from this company's website content:

1. Company Overview: 2-sentence summary of what they do
2. Target Audience: Who the product is built for (ICP)
3. Contact Points: Any generic emails (contact@, sales@, support@, etc.)
4. Key Leadership: Names, roles, LinkedIn URLs (if found)
5. Confidence: Rate 0.0-1.0 how complete/confident this extraction is

Domain: {domain}

Content:
{content}

Output ONLY valid JSON matching this schema:
{json.dumps(schema, indent=2)}"""

    input_tokens = len(encoding.encode(prompt))
    logger.info(f"Token count for {domain}: input={input_tokens}")

    result = await llm_client.generate(prompt, schema)
    if result:
        result.domain = domain
        output_tokens = len(encoding.encode(result.model_dump_json()))
        logger.info(f"Token count for {domain}: output={output_tokens}, estimated_cost=${estimate_cost(input_tokens, output_tokens):.6f}")
    return result


async def process_domain(browser: BrowserHandler, llm_client: OllamaClient, domain: str) -> CompanyEnrichment:
    logger.info(f"Processing domain: {domain}")

    html, subpages = await scrape_domain(browser, domain)

    if not html:
        return CompanyEnrichment(
            domain=domain,
            company_overview="Failed to fetch website",
            target_audience="Unknown",
            contact_points=[],
            key_leadership=[],
            data_confidence_score=0.0,
            errors=[f"Failed to fetch {domain}"]
        )

    content = await extract_content(html)
    logger.info(f"Extracted {len(content)} chars for {domain}")

    enrichment = await enrich_with_llm(llm_client, domain, content)

    if not enrichment:
        return CompanyEnrichment(
            domain=domain,
            company_overview="LLM extraction failed",
            target_audience="Unknown",
            contact_points=[],
            key_leadership=[],
            data_confidence_score=0.0,
            errors=["LLM extraction failed"]
        )

    logger.info(f"Successfully enriched {domain} with confidence {enrichment.data_confidence_score}")
    return enrichment