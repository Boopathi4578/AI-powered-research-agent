# AI-Powered Research Agent

This repository contains a small research automation tool that fetches academic papers from multiple sources, summarizes them with an LLM (AWS Bedrock), and generates a structured Markdown research report.

**Key points:**
- **Purpose:** Automate literature discovery and produce concise, synthesized research reports.
- **LLM backend:** AWS Bedrock (configurable via environment variables).
- **Outputs:** Markdown reports and JSON data written to the `data/` folder.

**Features**
- Fetch papers from multiple sources: `openalex`, `core`, `arxiv`, `zenodo`, `doaj`, and placeholders for others.
- Automatic best-source selection or multi-source fetching.
- Per-paper summarization and multi-paper synthesis using Agno agents and Bedrock.
- Report rendering via Jinja2 templates.

**Repository Structure**
- `main.py`: : Programmatic and interactive entrypoint. Use it for interactive queries or call `run()` from other code.
- `demo_new_sources.py`: : Small demo to exercise the new paper sources and show example usage.
- `test_new_sources.py`: : Script to test individual or multiple paper sources.
- `src/research_agent.py`: : Core orchestration class `ResearchAgent` (fetch -> summarize -> synthesize -> report).
- `utils/paper_fetcher.py`: : Paper fetching implementation for supported sources (arXiv, OpenAlex, CORE, Zenodo, DOAJ).
- `utils/report_generator.py`: : Report generation (Markdown template + save helpers).
- `models/llm_config.py`: : Thin Bedrock wrapper and helper factory for LLM configuration.
- `requirements.txt`: : Python dependencies used by the project.
- `data/`: : Output folder where generated `*.md` and `*.json` files are saved.

**Requirements**
- Python 3.10+ (recommended)
- Install dependencies from `requirements.txt`:

```bash
python -m pip install -r requirements.txt
```

**Environment variables**
The project expects certain environment variables (you can create a `.env` file and use `python-dotenv`):

- `BEDROCK_MODEL_ID`: AWS Bedrock model identifier (required for LLM calls).
- `AWS_REGION` or `AWS_DEFAULT_REGION`: AWS region for Bedrock (recommended).
- `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`: AWS credentials (or use IAM role/other AWS auth chain).
- `MAX_PAPERS`: Optional, default number of papers to fetch.
- `OUTPUT`: Optional, filename prefix for generated reports.
- `SOURCES`: Optional space-separated list of default sources (e.g., `openalex arxiv`).

Example `.env` entries:

```bash
BEDROCK_MODEL_ID="arn:aws:bedrock:us-east-1:...:inference-profile/your-model:0"
AWS_REGION="us-east-1"
AWS_ACCESS_KEY_ID="AKIA..."
AWS_SECRET_ACCESS_KEY="..."
MAX_PAPERS=5
```

**Quick start**

- Interactive mode (recommended for exploration):

```bash
export BEDROCK_MODEL_ID="<your-bedrock-model-id>"
export AWS_REGION="us-east-1"
python main.py
```

- Programmatic call (example from Python):

```python
from main import run
report_path = run(
    query="quantum computing",
    max_papers=5,
    output="quantum_report.md",
    sources=['openalex','arxiv']
)
print(report_path)
```

- Demo and tests:

```bash
python demo_new_sources.py   # runs several demo scenarios for paper fetching
python test_new_sources.py   # runs source-specific tests and multi-source tests
```

**Data & Outputs**
- Generated Markdown reports are saved to `data/` (e.g. `data/research_report_YYYYMMDD_HHMMSS.md`).
- Raw JSON data for each run is saved alongside the report (same name with `.json`).

**Notes & Caveats**
- AWS Bedrock is required for LLM summarization; without `BEDROCK_MODEL_ID` the agent will raise an error.
- Paper source APIs may require network access and may enforce rate limits or API keys for some providers.
- The `paper_fetcher` module uses third-party APIs and scraping where necessary — expect variation in returned metadata.
- The Bedrock wrapper in `models/llm_config.py` is intentionally minimal and may need adaptation for streaming/structured APIs or advanced model inputs.

**Contributing & Next steps**
- Add unit tests for `src/research_agent.py` and `utils/report_generator.py`.
- Add CI to run linting and tests.
- Improve Bedrock integration for typed responses or streaming.

