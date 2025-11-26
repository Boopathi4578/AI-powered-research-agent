# 🔬 AI-Powered Research Agent

An intelligent research automation tool that fetches academic papers from multiple sources, summarizes them using AWS Bedrock LLM, and generates comprehensive Markdown research reports with synthesized insights.

## 📋 Overview

This project automates literature discovery and research synthesis, enabling users to:
- Query multiple academic paper sources simultaneously
- Automatically fetch and aggregate results from diverse databases
- Leverage AI-powered summarization for quick insights
- Generate professional research reports in Markdown and JSON formats
- Access results via web interface or CLI

**Perfect for:** Literature reviews, market research, competitive analysis, and academic research support.

## ✨ Key Features

- **Multi-Source Paper Fetching:** OpenAlex, arXiv, CORE, Zenodo, DOAJ, and more
- **Intelligent Source Selection:** Automatic best-source selection or parallel multi-source queries
- **AI-Powered Summarization:** Per-paper summaries and cross-paper synthesis using AWS Bedrock
- **Web UI Dashboard:** Interactive Streamlit interface with real-time progress tracking
- **CLI & Programmatic Access:** Multiple usage modes for different workflows
- **Professional Reports:** Auto-generated Markdown and JSON output with timestamps
- **Template-Based Rendering:** Jinja2 templates for consistent report formatting

## 📁 Repository Structure

```
.
├── main.py                          # Interactive CLI entry point
├── streamlit_app.py                 # Web UI dashboard
├── requirements.txt                 # Python dependencies
├── run_streamlit.sh                 # Linux/Mac launch script
├── run_streamlit.bat                # Windows launch script
├── src/
│   ├── __init__.py
│   └── research_agent.py            # Core orchestration engine
├── utils/
│   ├── __init__.py
│   ├── paper_fetcher.py             # Multi-source paper fetching
│   └── report_generator.py          # Report generation & templates
├── models/
│   ├── __init__.py
│   └── llm_config.py                # AWS Bedrock LLM wrapper
├── data/                            # Generated reports (auto-created)
└── README.md                        # This file
```

## 🔧 Prerequisites

- **Python:** 3.11 or higher
- **AWS Account:** With Bedrock access and appropriate credentials
- **Internet:** For fetching papers from academic APIs

## ⚡ Quick Start Guide

### 1️⃣ Installation

Clone and set up the project:

```bash
# Clone repository
cd Onedata_AI_assignment

# Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate        # Linux/Mac
# or
venv\Scripts\activate            # Windows

# Install dependencies
pip install -r requirements.txt
```

### 2️⃣ Configure AWS Credentials

Create a `.env` file in the project root:

```bash
# AWS Bedrock Configuration (REQUIRED)
BEDROCK_MODEL_ID="arn:aws:bedrock:us-east-1:...:inference-profile/us.anthropic.claude-3-5-haiku-20241022-v1:0"
AWS_REGION="us-east-1"
AWS_ACCESS_KEY_ID="AKIA..."
AWS_SECRET_ACCESS_KEY="..."

# Research Agent Configuration (OPTIONAL)
MAX_PAPERS=5
OUTPUT="research_report"
SOURCES="arxiv openalex"
```

**Notes on AWS Credentials:**
- You can use environment variables, `.env` file, or AWS credential profiles
- Ensure your AWS IAM user has Bedrock access permissions
- Get your `BEDROCK_MODEL_ID` from AWS Bedrock console

### 3️⃣ Run the Application

#### Option A: Web UI (Recommended) 🌐

```bash
# Method 1: Direct Streamlit command
streamlit run streamlit_app.py

# Method 2: Using convenience script
./run_streamlit.sh              # Linux/Mac
run_streamlit.bat               # Windows
```

Then open your browser to `http://localhost:8501`

**Web UI Features:**
- Interactive query interface
- Real-time progress tracking
- Multi-source selection checkboxes
- Live execution logs
- Markdown and JSON report downloads
- In-browser report preview

#### Option B: Interactive CLI 💻

```bash
python main.py
```

This launches an interactive loop where you can:
1. Enter research queries
2. Specify number of papers to fetch
3. Choose paper sources
4. View generated reports

Example session:
```
Welcome to the Research Agent!
Enter your research query: quantum computing applications
Number of papers to fetch (default: 5): 10
Choose sources (comma-separated, default: arxiv): arxiv,openalex
```

#### Option C: Programmatic Usage 🐍

```python
from main import run

# Generate a research report programmatically
report_path = run(
    query="machine learning in healthcare",
    max_papers=10,
    output="ml_healthcare_report",
    sources=['arxiv', 'openalex', 'core']
)

print(f"Report saved to: {report_path}")
```

#### Option D: Info 🧪

## 📊 Supported Paper Sources

| Source | Coverage | Speed | Notes |
|--------|----------|-------|-------|
| **arXiv** | Computer Science, Physics, Math | ⚡⚡⚡ | Excellent for preprints |
| **OpenAlex** | Multidisciplinary | ⚡⚡ | Comprehensive database |
| **CORE** | Multidisciplinary | ⚡⚡ | Academic papers & preprints |
| **Zenodo** | Open science | ⚡⚡ | Various research outputs |
| **DOAJ** | Open access journals | ⚡ | Quality-checked journals |

## 📝 Generated Outputs

Reports are automatically saved to the `data/` directory with the following structure:

```
data/
├── research_report_20251126_114034.md       # Formatted report
├── research_report_20251126_114034.json     # Raw data & metadata
└── ...
```

**Report Contents:**
- Research query and parameters
- Summary of fetched papers
- Per-paper AI summaries
- Cross-paper synthesis and insights
- Source attribution and links
- Execution metadata

## 🔐 Environment Variables Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `BEDROCK_MODEL_ID` | ✅ Yes | - | AWS Bedrock model ARN |
| `AWS_REGION` | ❌ No | us-east-1 | AWS region for Bedrock |
| `AWS_ACCESS_KEY_ID` | ✅ Yes | - | AWS access key |
| `AWS_SECRET_ACCESS_KEY` | ✅ Yes | - | AWS secret key |
| `MAX_PAPERS` | ❌ No | 5 | Default papers to fetch |
| `OUTPUT` | ❌ No | research_report | Output filename prefix |
| `SOURCES` | ❌ No | arxiv | Space-separated sources |

## 🛠️ Project Architecture

### Core Components

**`src/research_agent.py`** - Main orchestration engine
- Coordinates the entire research workflow
- Manages paper fetching, summarization, and synthesis
- Handles error management and retries

**`utils/paper_fetcher.py`** - Multi-source paper aggregator
- Implements APIs for all supported sources
- Handles rate limiting and retries
- Normalizes metadata across sources

**`utils/report_generator.py`** - Report generation
- Jinja2 template-based rendering
- Markdown and JSON export
- File management and persistence

**`models/llm_config.py`** - AWS Bedrock integration
- LLM configuration and initialization
- Prompt management
- Response parsing

## ❓ Troubleshooting

| Issue | Solution |
|-------|----------|
| `AWS credentials not found` | Set `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` in `.env` |
| `BEDROCK_MODEL_ID not set` | Add your model ARN to `.env` or environment |
| `Connection timeout` | Check internet connection and API rate limits |
| `Streamlit port already in use` | Run `streamlit run streamlit_app.py --server.port 8502` |
| `Module not found errors` | Ensure `pip install -r requirements.txt` completed successfully |

## 📚 Additional Documentation

- See [STREAMLIT_README.md](STREAMLIT_README.md) for detailed Streamlit interface documentation

## 🚀 Performance Tips

- **First run:** May take longer due to API calls and LLM processing
- **Rate limits:** Some sources enforce rate limits; use `MAX_PAPERS` judiciously
- **Network:** Multi-source queries benefit from good bandwidth
- **Bedrock costs:** Monitor AWS usage; each query invokes the LLM

## ⚠️ Important Notes

- **AWS Bedrock Required:** LLM summarization requires active Bedrock service
- **API Access:** Some paper sources may require API keys or have rate limits
- **Network-Dependent:** All operations require internet connectivity
- **Data Freshness:** Report timestamps indicate when data was fetched

## 📦 Dependencies

Core dependencies (see `requirements.txt` for versions):
- `agno` - Agent framework
- `boto3` / `botocore` - AWS Bedrock client
- `arxiv` - arXiv paper fetching
- `requests` - HTTP client
- `beautifulsoup4` - HTML parsing
- `jinja2` - Template rendering
- `streamlit` - Web UI framework
- `pydantic` - Data validation
- `python-dotenv` - Environment configuration

## 🤝 Contributing & Future Improvements

- [ ] Add comprehensive unit tests
- [ ] Implement CI/CD pipeline
- [ ] Support for more paper sources (PubMed, SSRN, etc.)
- [ ] Caching layer for repeated queries
- [ ] Advanced filtering and ranking options
- [ ] Export to additional formats (PDF, DOCX)
- [ ] Streaming responses for large reports

## 📄 License

This project is provided as-is for research and educational purposes.

## ✉️ Support

For issues or questions:
1. Check the troubleshooting section above
2. Review generated logs in the `data/` directory
3. Verify AWS credentials and Bedrock access

