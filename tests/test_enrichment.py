import pytest
from llm.structured_output import CompanyEnrichment, ContactPoints, TeamMember
from scraper.content_extractor import ContentExtractor
from pydantic import ValidationError

class TestStructuredOutput:
    def test_valid_company_enrichment(self):
        data={
            "domain": "test.com",
            "company_overview": "Test company overview.",
            "target_audience": "Test audience.",
            "contact_points": [{"email": "contact@test.com", "type": "general"}],
            "key_leadership": [{"name": "John Doe", "role": "CEO", "linkedin_url": "https://linkedin.com/in/johndoe"}],
            "data_confidence_score": 0.95
        }
        result=CompanyEnrichment(**data)
        assert result.domain=="test.com"
        assert result.data_confidence_score==0.95
        assert len(result.contact_points)==1

    def test_invalid_confidence_score(self):
        data={
            "domain": "test.com",
            "company_overview": "Test overview.",
            "target_audience": "Test audience.",
            "contact_points": [],
            "key_leadership": [],
            "data_confidence_score": 1.5
        }
        with pytest.raises(ValidationError):
            CompanyEnrichment(**data)

class TestContentExtractor:
    def test_html_stripping(self):
        extractor=ContentExtractor()
        raw_html="<html><body><script>alert('xss');</script><nav>Menu</nav><main>Hello World</main></body></html>"
        result=extractor.extract(raw_html)
        assert "alert" not in result
        assert "Menu" not in result
        assert "Hello World" in result

    def test_token_truncation(self):
        extractor=ContentExtractor()
        long_text="word " * 5000
        truncated=extractor.truncate_to_token_limit(long_text, max_tokens=100)
        assert extractor.count_tokens(truncated) <= 100

class TestErrorResilience:
    @pytest.mark.asyncio
    async def test_agent_handles_missing_domain_gracefully(self):
        from agent.lead_enrichment_agent import LeadEnrichmentAgent
        agent=LeadEnrichmentAgent()
        await agent.initialize()
        results=await agent.run(["this-domain-does-not-exist-12345.com"])
        assert len(results)==1
        assert results[0].domain=="this-domain-does-not-exist-12345.com"
        assert results[0].data_confidence_score==0.0
        assert results[0].errors is not None
        await agent.cleanup()