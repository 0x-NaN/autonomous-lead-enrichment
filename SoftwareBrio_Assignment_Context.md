# SoftwareBrio AI Engineer Intern Assignment — Complete Context

---

## 📋 PROJECT OVERVIEW

**Role:** AI Engineer Intern (Paid, Remote, Winter 2026)
**Company:** SoftwareBrio (Bangalore/Gurugram)
**Deadline:** 48-72 hours from assignment receipt
**Work Model:** 40% Manual Operations + 60% AI Agent Engineering

**Core Task:** Build an autonomous agent that scrapes company domains, enriches them with structured intelligence via LLM, and outputs clean, confident data.

---

## 🎯 DELIVERABLES CHECKLIST

- [ ] GitHub Repository (clean, modular Python code)
- [ ] requirements.txt or pyproject.toml
- [ ] README.md with setup instructions
- [ ] Sample output.json (from 3 test domains: postman.com, supabase.com, vapi.ai)
- [ ] 2-3 min Loom video walkthrough
- [ ] Explicit answer to operations question ("Are you 100% comfortable with 40% manual ops?")
- [ ] Submit to: support@softwarebrio.com with subject: [AI Intern Submission] - [Your Full Name]

---

## 📂 RECOMMENDED FILE STRUCTURE

```
autonomous-lead-enrichment/
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
├── main.py                          # Entry point
├── config/
│   └── settings.py                  # Config, API keys, model params
├── scraper/
│   ├── __init__.py
│   ├── browser_handler.py           # Playwright/Selenium headless browser
│   ├── content_extractor.py         # DOM parsing, markdown conversion, token cleanup
│   └── error_handler.py             # Graceful timeout/404/bot-block handling
├── llm/
│   ├── __init__.py
│   ├── structured_output.py         # Pydantic schemas for strict output
│   └── llm_client.py                # Ollama/OpenAI/Groq wrapper
├── agent/
│   ├── __init__.py
│   ├── lead_enrichment_agent.py     # Main orchestration logic
│   └── tools.py                     # Reusable tool definitions (search, scrape, extract)
├── utils/
│   ├── __init__.py
│   ├── token_counter.py             # Token tracking & cost estimation
│   ├── logger.py                    # Structured logging
│   └── validators.py                # Data validation & confidence scoring
├── tests/
│   ├── test_scraper.py
│   ├── test_llm.py
│   └── test_agent.py
└── output/
    └── output.json                  # Sample run output
```

---

## 🏗️ SYSTEM ARCHITECTURE

```
INPUT (Company Domains)
  ↓
[Browser Handler - Playwright/Selenium]
  ├─ Fetch homepage
  ├─ Discover subpages (/about, /team, /contact, /pricing, etc.)
  ├─ Handle JavaScript-rendered content
  └─ Graceful error handling (404, timeouts, bot-blocks)
  ↓
[Content Extractor]
  ├─ Parse DOM, convert to clean Markdown
  ├─ Strip CSS, SVGs, scripts, navigation boilerplate
  ├─ Estimate token count
  └─ Optimize for LLM input (no raw HTML dumps)
  ↓
[LLM Extraction Pipeline]
  ├─ Feed cleaned content to LLM (Ollama local or API)
  ├─ Use Pydantic/JSON Schema for strict structured output
  └─ Extract:
     • Company Overview (2-sentence summary)
     • Target Audience / ICP
     • Contact Points (emails)
     • Key Leadership / Team Members + LinkedIn URLs
     • Data Confidence Score (0.0 - 1.0)
  ↓
[Resilience & Fallback]
  ├─ Graceful degradation (missing fields OK)
  ├─ Retry logic for transient failures
  └─ Log errors, continue to next domain
  ↓
OUTPUT (Structured JSON/CSV)
```

---

## 🔄 FULL WORKFLOW / DATA FLOW

### Step 1: Initialize Agent
1. Load environment variables (.env): LLM API key, model name, domains list
2. Create browser session (Playwright headless)
3. Initialize LLM client (local Ollama or API)
4. Set up structured output schema (Pydantic)

### Step 2: For Each Domain
1. **Browsing Phase:**
   - Fetch `https://domain.com` with headless browser
   - Wait for JavaScript to render (configurable timeout, e.g., 5-10 seconds)
   - Discover subpages by scanning `<a>` tags for common patterns (/about, /team, /company, /contact, /pricing)
   - Fetch content from top 3-5 most relevant subpages

2. **Content Extraction Phase:**
   - Parse HTML → clean Markdown (use `html2text` or similar)
   - Remove CSS, JavaScript, SVG, nav boilerplate
   - Extract plain text and structural content
   - Estimate tokens (safety threshold: cap at 2000-3000 tokens max per domain)

3. **LLM Enrichment Phase:**
   - Feed cleaned content to LLM with prompt:
     ```
     Extract the following structured information from this company's website:
     1. Company Overview: 2-sentence summary of what they do
     2. Target Audience: Who the product is built for
     3. Contact Points: Any generic emails (contact@, sales@, support@, etc.)
     4. Key Leadership: Names, roles, LinkedIn URLs (if found)
     5. Confidence: Rate 0.0-1.0 how complete/confident this extraction is
     
     Content: [cleaned markdown content]
     ```
   - Use strict schema (Pydantic) to enforce output format

4. **Error Handling:**
   - If fetch fails (404, timeout, rate limit): log error, assign confidence 0.0, continue
   - If LLM fails: retry once, then skip domain
   - Never crash — always move to next domain

### Step 3: Aggregate & Output
1. Collect all extracted data into list of dicts
2. Write to output.json (or CSV if preferred)
3. Log token usage & estimated API cost
4. Generate summary report

---

## 📊 EVALUATION RUBRIC (30% → 10% breakdown)

| Criterion | Weight | What We're Looking For |
|-----------|--------|------------------------|
| **Agent & Scraping Architecture** | 30% | • Efficient DOM handling<br>• Headless browser integration (Playwright/Selenium)<br>• Pagination/link discovery without crashes<br>• Proper session management & cleanup |
| **LLM & Structured Output Quality** | 25% | • Reliable Pydantic/JSON schemas<br>• Robust prompt design<br>• Token filtering (no raw HTML dumps)<br>• Accurate extraction of all 5 fields |
| **Error Handling & Resilience** | 20% | • Graceful timeout handling<br>• Anti-bot/rate-limit recovery<br>• Missing field handling (defaults, confidence 0.0)<br>• No crashes on edge cases |
| **Code Quality & Documentation** | 15% | • Clean, modular functions<br>• Separation of concerns<br>• Type hints throughout<br>• Clear README with setup steps |
| **Loom Walkthrough** | 10% | • Clear explanation of architecture<br>• Demo of running script end-to-end<br>• Output inspection<br>• 2-3 minutes max |

**Total: 100%**

---

## 🛠️ TECH STACK RECOMMENDATIONS

### Headless Browser
- **Playwright** (preferred): faster, async-friendly, cross-platform
- Alternative: Selenium (more stable, slightly slower)

### Content Processing
- `html2text`: Convert HTML → clean Markdown
- `BeautifulSoup4`: DOM parsing
- `httpx` or `requests`: HTTP client

### LLM
- **Local (Recommended):** Ollama with Qwen2.5-7B (you already have this running)
  - Zero API costs
  - Works offline
  - Fast inference on RTX 4060
- **API (Alternative):** Groq, Together AI, Anthropic, or OpenAI

### Structured Output
- **Pydantic v2:** Define schemas, auto-validate
- Alternative: `instructor` library (wrapper for LLM JSON mode)

### Other
- `python-dotenv`: Load .env variables
- `loguru`: Structured logging
- `tiktoken`: Token counting for cost estimation
- `pytest`: Unit tests (optional but helpful)

---

## 💾 PYDANTIC SCHEMA EXAMPLE

```python
from pydantic import BaseModel, Field
from typing import Optional

class ContactPoints(BaseModel):
    email: str
    type: str  # e.g., "support", "sales", "contact"

class TeamMember(BaseModel):
    name: str
    role: str
    linkedin_url: Optional[str] = None

class CompanyEnrichment(BaseModel):
    domain: str
    company_overview: str = Field(..., description="2-sentence summary")
    target_audience: str = Field(..., description="ICP description")
    contact_points: list[ContactPoints] = Field(default_factory=list)
    key_leadership: list[TeamMember] = Field(default_factory=list)
    data_confidence_score: float = Field(..., ge=0.0, le=1.0)
    errors: Optional[list[str]] = None
```

---

## 📝 SAMPLE OUTPUT.JSON STRUCTURE

```json
[
  {
    "domain": "postman.com",
    "company_overview": "Postman is a platform for building, testing, and collaborating on APIs. It provides tools for API development lifecycle management.",
    "target_audience": "Software developers, API engineers, and teams building and testing REST/GraphQL APIs",
    "contact_points": [
      {
        "email": "support@postman.com",
        "type": "support"
      },
      {
        "email": "sales@postman.com",
        "type": "sales"
      }
    ],
    "key_leadership": [
      {
        "name": "Abhinav Asthana",
        "role": "Founder & CEO",
        "linkedin_url": "https://linkedin.com/in/abhinav-asthana"
      }
    ],
    "data_confidence_score": 0.92,
    "errors": null
  },
  {
    "domain": "supabase.com",
    "company_overview": "Supabase is an open-source Firebase alternative. It provides a Postgres database, realtime subscriptions, and authentication APIs.",
    "target_audience": "Full-stack developers and startups building real-time applications with Postgres backends",
    "contact_points": [
      {
        "email": "support@supabase.com",
        "type": "support"
      }
    ],
    "key_leadership": [
      {
        "name": "Paul Copplestone",
        "role": "Founder & CEO",
        "linkedin_url": "https://linkedin.com/in/paulcopplestone"
      }
    ],
    "data_confidence_score": 0.88,
    "errors": null
  },
  {
    "domain": "vapi.ai",
    "company_overview": "Vapi is a platform for building, deploying, and scaling voice AI agents. It simplifies voice AI development.",
    "target_audience": "Developers and businesses building conversational AI and voice agent applications",
    "contact_points": [
      {
        "email": "hello@vapi.ai",
        "type": "general"
      }
    ],
    "key_leadership": [
      {
        "name": "Amir Adel",
        "role": "Founder & CEO",
        "linkedin_url": "https://linkedin.com/in/amir-adel"
      }
    ],
    "data_confidence_score": 0.85,
    "errors": null
  }
]
```

---

## ⏱️ TIMELINE BREAKDOWN (48-72 hours)

**Hour 0-4: Setup & Architecture**
- Set up repo structure
- Install dependencies (Playwright, Pydantic, LLM client)
- Create .env.example, config
- Write browser handler skeleton

**Hour 4-12: Scraper Implementation**
- Implement headless browser (Playwright)
- Implement content extractor (HTML → clean Markdown)
- Test on 1 domain (postman.com)
- Add error handling

**Hour 12-20: LLM Integration**
- Define Pydantic schemas
- Write LLM client (Ollama wrapper)
- Test structured output on sample content
- Iterate on prompt robustness

**Hour 20-28: Agent Orchestration**
- Tie everything together in main agent loop
- Test on all 3 domains
- Refine error handling
- Add token counting & logging

**Hour 28-36: Testing & Polish**
- Test edge cases (missing fields, timeouts, bot blocks)
- Clean up code, add type hints
- Write README.md
- Generate sample output.json

**Hour 36-42: Loom Recording & Final Submission**
- Record 2-3 min walkthrough (code → execution → output)
- Write explicit operations question answer
- Final email prep & submission

**Buffer: 6-30 hours** for iteration, debugging, unforeseen issues

---

## ✅ MANDATORY SUBMISSION REQUIREMENTS

1. **GitHub Repo:**
   - Public or private (your choice)
   - requirements.txt with all dependencies
   - README.md explaining setup and usage
   - Clean, modular code with type hints

2. **Sample Output File:**
   - output.json from running on postman.com, supabase.com, vapi.ai
   - Show all 5 extracted fields
   - Include confidence scores

3. **Loom Video:**
   - Show code structure (2-3 files walkthrough)
   - Run the script in terminal
   - Display final output.json
   - Total: 2-3 minutes max

4. **Operations Question Answer:**
   - Explicit "Yes" or "No" to: "Are you 100% comfortable with 40% manual ops?"
   - Non-answer or "No" = automatic disqualification

5. **Email Details:**
   - To: support@softwarebrio.com
   - Subject: [AI Intern Submission] - [Your Full Name]
   - Include: LinkedIn profile link

---

## 🚀 KEY DECISIONS TO MAKE NOW

1. **LLM Choice:** Ollama (local, free) or API (Groq/OpenAI, cost)?
   - Recommendation: **Ollama** (you have qwen2.5:7b running)

2. **Headless Browser:** Playwright (faster, async) or Selenium (stable)?
   - Recommendation: **Playwright** (better for async scraping)

3. **Content Extraction:** html2text (simple) or custom DOM parsing (precise)?
   - Recommendation: **html2text + BeautifulSoup** combo

4. **Structured Output:** Pydantic (strict schema) or raw JSON (flexible)?
   - Recommendation: **Pydantic** (matches rubric, auto-validates)

5. **Error Strategy:** Fail-fast (crash on error) or fail-graceful (log & continue)?
   - Recommendation: **Fail-graceful** (explicitly required by rubric)

---

## 📌 ANTI-PATTERNS TO AVOID

❌ Feeding raw HTML into LLM (inefficient, wastes tokens)
❌ No timeout handling (script crashes on slow/blocked domains)
❌ Not stripping boilerplate (nav, CSS, scripts inflate token count)
❌ Rigid schema (fails when a field is missing; use Optional/defaults)
❌ No logging (impossible to debug issues in real time)
❌ Single-threaded scraping (slow; consider async with asyncio + Playwright)

---

## 🎬 LOOM SCRIPT OUTLINE (2-3 minutes)

1. **Intro (20 sec):**
   - "Building an autonomous lead enrichment agent for SoftwareBrio"
   - Show file structure

2. **Architecture (30 sec):**
   - Walk through main.py flow
   - Show browser_handler.py, content_extractor.py, structured_output.py

3. **Execution (40 sec):**
   - Run: `python main.py`
   - Show the script processing the 3 domains in real-time
   - Show logs (domain being scraped, subpages discovered, LLM extraction)

4. **Output (30 sec):**
   - Display output.json
   - Highlight one full record (all 5 fields + confidence score)
   - Show confidence scores are reasonable (0.85-0.92 range)

5. **Wrap (10 sec):**
   - "This agent runs autonomously, handles errors gracefully, and outputs structured data ready for downstream CRM integration"

---

## 🏁 FINAL CHECKLIST

**Before submitting, verify:**

- [ ] All 3 test domains scraped successfully
- [ ] output.json has valid JSON, 5 fields per domain
- [ ] Confidence scores are 0.0-1.0 range
- [ ] No domain crashes the script
- [ ] README.md has clear setup instructions (.env variables)
- [ ] requirements.txt lists all dependencies
- [ ] Code is typed (type hints on all functions)
- [ ] Loom video is 2-3 minutes, shows working system
- [ ] GitHub repo is clean, no secrets in code
- [ ] Operations question answered explicitly ("Yes")
- [ ] Email subject: [AI Intern Submission] - [Your Full Name]
- [ ] Email includes LinkedIn profile URL

---

## 📚 REFERENCE DOCS

- Pydantic v2 Docs: https://docs.pydantic.dev/latest/
- Playwright Python: https://playwright.dev/python/
- Ollama API: https://github.com/ollama/ollama/blob/main/docs/api.md
- html2text: https://github.com/Alir3z4/html2text
- Loguru: https://loguru.readthedocs.io/

---

**You're ready to start. Good luck!**
