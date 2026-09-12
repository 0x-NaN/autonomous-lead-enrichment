# Autonomous Lead Enrichment Agent

An AI agent that scrapes company domains, enriches them with structured intelligence via LLM, and outputs clean, confident data.

## Features

- **Headless Browser Scraping**: Uses Playwright to fetch JavaScript-rendered content
- **Smart Content Extraction**: Converts HTML to clean Markdown, strips boilerplate
- **LLM-Powered Enrichment**: Uses Ollama (local) for structured data extraction
- **Graceful Error Handling**: Continues processing even if individual domains fail
- **Confidence Scoring**: Each extraction includes a 0.0-1.0 confidence score

## Extracted Fields

1. **Company Overview**: 2-sentence summary
2. **Target Audience**: ICP description
3. **Contact Points**: Generic emails (support@, sales@, etc.)
4. **Key Leadership**: Names, roles, LinkedIn URLs
5. **Data Confidence Score**: 0.0-1.0

## Quick Start

### Prerequisites

1. Python 3.10+
2. Ollama installed and running locally
3. Playwright browsers installed

### Installation

```bash
# Clone the repo
git clone <your-repo-url>
cd autonomous-lead-enrichment

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium

# Pull Ollama model (if not already pulled)
ollama pull qwen2.5:7b

# Copy environment file
cp .env.example .env
```

### Configuration

Edit `.env` to customize:
- `OLLAMA_HOST`: Ollama server URL (default: http://localhost:11434)
- `OLLAMA_MODEL`: Model to use (default: qwen2.5:7b)
- `TARGET_DOMAINS`: Comma-separated domains to process
- `MAX_SUBPAGES`: Max subpages to scrape per domain
- `MAX_TOKENS_PER_DOMAIN`: Token limit for LLM input

### Usage

```bash
# Run on default domains (postman.com, supabase.com, vapi.ai)
python main.py

# Run on custom domains
python main.py --domains example.com another.com

# Specify output file
python main.py --output output/custom.json
```

### Output

Results are saved to `output/output.json` as an array of enrichment objects:

```json
[
  {
    "domain": "postman.com",
    "company_overview": "Postman is a platform for building, testing, and collaborating on APIs...",
    "target_audience": "Software developers, API engineers, and teams building REST/GraphQL APIs",
    "contact_points": [
      {"email": "support@postman.com", "type": "support"},
      {"email": "sales@postman.com", "type": "sales"}
    ],
    "key_leadership": [
      {"name": "Abhinav Asthana", "role": "Founder & CEO", "linkedin_url": "https://linkedin.com/in/abhinav-asthana"}
    ],
    "data_confidence_score": 0.92,
    "errors": null
  }
]
```

## Project Structure

```
autonomous-lead-enrichment/
├── main.py                    # Entry point
├── config/
│   └── settings.py           # Configuration management
├── scraper/
│   ├── browser_handler.py    # Playwright browser management
│   ├── content_extractor.py  # HTML to Markdown conversion
│   └── error_handler.py      # Error handling utilities
├── llm/
│   ├── structured_output.py  # Pydantic schemas
│   └── llm_client.py         # Ollama client wrapper
├── agent/
│   ├── lead_enrichment_agent.py  # Main orchestration
│   └── tools.py              # Reusable tool functions
├── utils/
│   ├── logger.py             # Structured logging
│   ├── validators.py         # Email/LinkedIn validation
│   └── token_counter.py      # Token counting & cost estimation
├── tests/
│   └── (test files)
├── output/
│   └── output.json           # Sample output
├── requirements.txt
├── .env.example
└── .gitignore
```

## Architecture

```
INPUT (Domains)
    ↓
[Browser Handler - Playwright]
    ├─ Fetch homepage
    ├─ Discover subpages (/about, /team, /contact, etc.)
    └─ Handle JS rendering & errors
    ↓
[Content Extractor]
    ├─ Parse DOM, convert to Markdown
    ├─ Strip CSS, scripts, nav boilerplate
    └─ Token limit optimization
    ↓
[LLM Enrichment - Ollama]
    ├─ Feed cleaned content with structured prompt
    ├─ Pydantic schema for strict output
    └─ Extract all 5 fields + confidence
    ↓
OUTPUT (Structured JSON)
```

## Error Handling

- **Timeouts**: 30s default, configurable
- **404/Not Found**: Logged, confidence 0.0, continue
- **Rate Limits**: Logged, confidence 0.0, continue
- **Bot Blocks**: Logged, confidence 0.0, continue
- **LLM Failures**: Retry once, then skip domain
- **Never Crashes**: Always moves to next domain

## Testing

```bash
# Run tests (if implemented)
pytest tests/
```

## License

MIT