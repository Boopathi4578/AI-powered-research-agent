# Project Summary: AI-Powered Research Agent

## Overview

This project implements an intelligent research agent that automates the process of finding, analyzing, and summarizing academic research papers. Built with the Agno multi-agent framework, it provides a production-ready solution for researchers, students, and professionals who need to quickly understand the state of research in any field.

## What It Does

1. **Accepts Research Queries**: Users provide natural language queries (e.g., "transformer models in NLP")
2. **Fetches Recent Papers**: Automatically retrieves relevant academic papers from arXiv
3. **AI-Powered Analysis**: Uses LLMs to analyze and summarize each paper
4. **Synthesizes Insights**: Identifies common themes and trends across multiple papers
5. **Generates Reports**: Creates professional markdown reports with structured insights

## Key Features

✅ **Multi-Agent Architecture**: Two specialized Agno agents (Summarizer & Synthesizer)  
✅ **Multiple LLM Providers**: Support for OpenAI GPT-4 and Anthropic Claude  
✅ **Automated Paper Fetching**: Integration with arXiv API  
✅ **Structured Reports**: Professional markdown + JSON output  
✅ **CLI Interface**: Easy-to-use command-line tool  
✅ **Extensible Design**: Modular architecture for easy customization  
✅ **Production Ready**: Error handling, logging, and validation  

## Project Structure

```
Onedata_assignment/
├── src/                          # Source code
│   ├── __init__.py
│   └── research_agent.py         # Main ResearchAgent class
├── models/                       # LLM configuration
│   ├── __init__.py
│   └── llm_config.py             # Model factory and setup
├── utils/                        # Utilities
│   ├── __init__.py
│   ├── paper_fetcher.py          # arXiv API integration
│   └── report_generator.py       # Report generation
├── data/                         # Data directory
│   ├── .gitkeep
│   └── sample_queries.txt        # Example queries
├── main.py                       # CLI entry point
├── test_setup.py                 # Setup verification script
├── requirements.txt              # Python dependencies
├── .env.example                  # Environment template
├── .gitignore                    # Git ignore rules
├── README.md                     # Main documentation
├── QUICKSTART.md                 # Quick start guide
├── ARCHITECTURE.md               # Architecture details
└── PROJECT_SUMMARY.md            # This file
```

## Technology Stack

- **Framework**: Agno 2.3+ (Multi-agent framework)
- **LLMs**: OpenAI GPT-4o-mini, Anthropic Claude-3.5-Sonnet
- **Data Source**: arXiv API (via arxiv Python package)
- **Templating**: Jinja2
- **Environment**: python-dotenv
- **CLI**: argparse
- **Language**: Python 3.8+

## How It Works

### Workflow

```
1. User Query
   ↓
2. Paper Fetcher → arXiv API → Recent papers
   ↓
3. Summarizer Agent → Analyzes each paper individually
   ↓
4. Synthesizer Agent → Identifies cross-paper themes
   ↓
5. Report Generator → Creates markdown + JSON
   ↓
6. Output saved to data/
```

### Multi-Agent System

The system uses two specialized Agno agents:

1. **Summarizer Agent**
   - Expert at analyzing individual research papers
   - Extracts key findings and contributions
   - Generates concise, technical summaries

2. **Synthesizer Agent**
   - Expert at cross-paper analysis
   - Identifies common themes and trends
   - Provides actionable insights and recommendations

## Usage Examples

```bash
# Basic usage
python main.py "transformer models in NLP"

# Use Anthropic Claude
python main.py "quantum computing" --provider anthropic

# Fetch more papers
python main.py "machine learning" --max-papers 10

# Custom output
python main.py "deep learning" --output my_report.md
```

## Setup Requirements

1. Python 3.8 or higher
2. Virtual environment (recommended)
3. API key from OpenAI or Anthropic
4. Internet connection for arXiv API

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure API key
cp .env.example .env
# Edit .env and add your API key

# 3. Run a query
python main.py "your research topic"
```

## Output Format

The agent generates two files:

1. **Markdown Report** (`research_report_YYYYMMDD_HHMMSS.md`)
   - Executive summary
   - Detailed paper summaries
   - Key themes and trends
   - Recommendations
   - Conclusion

2. **JSON Data** (`research_report_YYYYMMDD_HHMMSS.json`)
   - Raw structured data
   - All metadata
   - Timestamps

## Testing

Run the setup verification script:

```bash
python test_setup.py
```

This checks:
- ✓ All dependencies installed
- ✓ Project structure correct
- ✓ API keys configured
- ✓ arXiv connection working

## Documentation

- **README.md**: Comprehensive documentation with features, setup, and usage
- **QUICKSTART.md**: 5-minute quick start guide
- **ARCHITECTURE.md**: Detailed architecture and design patterns
- **PROJECT_SUMMARY.md**: This overview document

## Future Enhancements

Potential improvements:
- [ ] Parallel paper summarization for better performance
- [ ] Caching to avoid re-fetching papers
- [ ] Web interface (Streamlit/Gradio)
- [ ] Additional sources (PubMed, Google Scholar)
- [ ] PDF download and full-text analysis
- [ ] Citation graph analysis
- [ ] Database for historical queries

## Success Criteria Met

✅ Accepts research queries  
✅ Fetches recent academic papers via APIs  
✅ Summarizes papers using LLMs  
✅ Generates structured reports  
✅ Proper directory structure (/src, /models, /utils, /data)  
✅ README with setup instructions  
✅ Uses Agno agent framework  
✅ Production-ready code with error handling  
✅ Extensible and maintainable architecture  

## Video Walkthrough

[Placeholder for walkthrough video link - to be added to README.md]

## Contact & Support

For issues, questions, or contributions, please refer to the README.md file.

---

**Built with ❤️ using Agno Multi-Agent Framework**

