import asyncio
import json
import argparse
from pathlib import Path
from agent.lead_enrichment_agent import LeadEnrichmentAgent
from llm.structured_output import CompanyEnrichment
from config.settings import settings
from utils.logger import get_logger

logger = get_logger(__name__)


async def main():
    parser = argparse.ArgumentParser(description="Autonomous Lead Enrichment Agent")
    parser.add_argument("--domains", nargs="+", help="Domains to process")
    parser.add_argument("--output", default="output/output.json", help="Output file path")
    args = parser.parse_args()

    domains = args.domains if args.domains else settings.TARGET_DOMAINS

    agent = LeadEnrichmentAgent()

    try:
        initialized = await agent.initialize()
        if not initialized:
            logger.error("Failed to initialize agent")
            return

        logger.info(f"Starting enrichment for {len(domains)} domains: {domains}")
        results = await agent.run(domains)

        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        output_data = [r.model_dump() for r in results]
        with open(output_path, "w") as f:
            json.dump(output_data, f, indent=2)

        logger.info(f"Results saved to {output_path}")

        for r in results:
            logger.info(f"  {r.domain}: confidence={r.data_confidence_score:.2f}, overview={r.company_overview[:60]}...")

    finally:
        await agent.cleanup()


if __name__ == "__main__":
    asyncio.run(main())