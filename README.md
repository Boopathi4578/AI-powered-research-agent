# AI-Powered Research Agent 🔬🤖

An intelligent research agent that automatically fetches recent academic papers from arXiv and other sources, summarizes them using Large Language Models (LLMs), and generates comprehensive, structured research reports.

Built with the **Agno** multi-agent framework for production-grade AI applications.

## 🎯 Features

- **Automated Paper Fetching**: Retrieves recent academic papers from arXiv API based on research queries
- **AI-Powered Summarization**: Uses LLMs (OpenAI GPT-4 or Anthropic Claude) to generate concise summaries
- **Multi-Agent Architecture**: Employs specialized Agno agents for summarization and synthesis
- **Structured Reports**: Generates professional markdown reports with:
  - Executive summary
  - Individual paper summaries with key findings
  - Cross-paper theme analysis
  - Recommendations for further reading
- **Flexible Configuration**: Support for multiple LLM providers and customizable parameters
- **JSON Export**: Saves raw data for further analysis

## 📁 Project Structure

```
/
├── src/                    # Source code
│   └── research_agent.py   # Main ResearchAgent class with Agno agents
├── models/                 # Model definitions and LLM setup
│   └── llm_config.py       # LLM provider configuration
├── utils/                  # Helper functions and pipelines
│   ├── paper_fetcher.py    # arXiv API integration
│   └── report_generator.py # Report generation utilities
├── data/                   # Sample data and generated reports
│   ├── sample_queries.txt  # Example research queries
│   └── .gitkeep
├── main.py                 # CLI entry point
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variables template
└── README.md               # This file
```

## 🚀 Setup Instructions

### Prerequisites

- Python 3.8 or higher
- API key from OpenAI or Anthropic (or both)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Onedata_assignment
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure API keys**
   ```bash
   cp .env.example .env
   # Edit .env and add your API keys
   ```

   Get your API keys:
   - OpenAI: https://platform.openai.com/api-keys
   - Anthropic: https://console.anthropic.com/

### Environment Variables

Create a `.env` file with the following:

```env
# Choose one or both providers
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

## 💻 Usage

### Basic Usage

```bash
python main.py "your research query here"
```

### Examples

```bash
# Search for papers on transformers in NLP (default: OpenAI, 5 papers)
python main.py "transformer models in natural language processing"

# Use Anthropic Claude instead
python main.py "quantum computing" --provider anthropic

# Fetch more papers
python main.py "machine learning" --max-papers 10

# Custom output filename
python main.py "deep learning" --output my_research_report.md
```

### Command-Line Options

```
positional arguments:
  query                 Research query to search for papers

optional arguments:
  -h, --help            Show help message
  --provider {openai,anthropic}
                        LLM provider to use (default: openai)
  --max-papers N        Maximum number of papers to fetch (default: 5)
  --output FILENAME     Output filename for the report
  --sources SOURCE [SOURCE ...]
                        Sources to search (default: arxiv)
```

## 🏗️ Architecture

### Multi-Agent System (Agno Framework)

The application uses **Agno**, a high-performance multi-agent framework, with two specialized agents:

1. **Paper Summarizer Agent**
   - Analyzes individual research papers
   - Extracts key findings and contributions
   - Generates concise, technical summaries

2. **Research Synthesizer Agent**
   - Synthesizes insights across multiple papers
   - Identifies common themes and trends
   - Provides recommendations and conclusions

### Workflow

```
User Query → Paper Fetcher → Summarizer Agent → Synthesizer Agent → Report Generator
                ↓                    ↓                   ↓                ↓
            arXiv API          Individual         Cross-paper      Markdown +
                              Summaries           Analysis          JSON
```

## 📊 Sample Output

The agent generates two files:

1. **Markdown Report** (`research_report_YYYYMMDD_HHMMSS.md`)
   - Executive summary
   - Detailed paper summaries with key findings
   - Cross-paper theme analysis
   - Recommendations
   - Conclusion

2. **JSON Data** (`research_report_YYYYMMDD_HHMMSS.json`)
   - Raw structured data
   - All paper metadata
   - Summaries and synthesis
   - Timestamp information

### Example Report Structure

```markdown
# Research Report: transformer models in natural language processing

**Generated on:** 2024-11-22 10:30:00
**Total Papers Analyzed:** 5

## Executive Summary
[AI-generated overview of the research landscape]

## Detailed Paper Summaries

### 1. Attention Is All You Need
**Authors:** Vaswani et al.
**Published:** 2017-06-12
**Summary:** [AI-generated summary]
**Key Findings:** [Bullet points]

[... more papers ...]

## Key Themes and Trends
[Cross-paper analysis]

## Recommendations for Further Reading
[Suggested directions]

## Conclusion
[Final insights]
```

## 🔧 Customization

### Adding New Paper Sources

Extend `utils/paper_fetcher.py` to add support for additional sources:

```python
def fetch_from_pubmed(self, query: str) -> List[Dict]:
    # Implement PubMed API integration
    pass
```

### Customizing LLM Behavior

Modify agent instructions in `src/research_agent.py`:

```python
self.summarizer_agent = Agent(
    name="Paper Summarizer",
    model=self.model,
    instructions=[
        "Your custom instructions here",
        # ...
    ],
)
```

### Changing Report Format

Edit the template in `utils/report_generator.py` to customize the output format.

## 🧪 Testing

Run with sample queries:

```bash
# Test with a well-known topic
python main.py "attention mechanism in neural networks" --max-papers 3

# Test with different provider
python main.py "graph neural networks" --provider anthropic --max-papers 3
```

Sample queries are available in `data/sample_queries.txt`.

## 🛠️ Technologies Used

- **[Agno](https://github.com/agno-agi/agno)** - Multi-agent framework for AI applications
- **[arXiv API](https://arxiv.org/help/api)** - Academic paper database
- **OpenAI GPT-4** / **Anthropic Claude** - Large Language Models
- **Python 3.8+** - Programming language
- **Jinja2** - Template engine for reports
- **BeautifulSoup4** - Web scraping (for future extensions)

## 📝 Key Components

### 1. Paper Fetcher (`utils/paper_fetcher.py`)
- Interfaces with arXiv API
- Filters papers by date and relevance
- Extensible for additional sources

### 2. LLM Configuration (`models/llm_config.py`)
- Manages API keys and model selection
- Supports OpenAI and Anthropic providers
- Configurable temperature and token limits

### 3. Research Agent (`src/research_agent.py`)
- Core orchestration logic
- Two specialized Agno agents:
  - Summarizer: Analyzes individual papers
  - Synthesizer: Identifies cross-paper insights
- Complete workflow management

### 4. Report Generator (`utils/report_generator.py`)
- Jinja2-based templating
- Markdown and JSON output
- Structured, professional formatting

## 🎥 Demo Video

[Link to walkthrough video will be added here]

## 🤝 Contributing

Contributions are welcome! Areas for improvement:

- [ ] Add support for more paper sources (PubMed, Google Scholar, etc.)
- [ ] Implement caching to avoid re-fetching papers
- [ ] Add web interface using Streamlit or Gradio
- [ ] Support for PDF download and full-text analysis
- [ ] Citation graph analysis
- [ ] Multi-language support

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- **Agno Framework** - For the powerful multi-agent system
- **arXiv** - For providing free access to academic papers
- **OpenAI & Anthropic** - For state-of-the-art language models

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

---

**Built with ❤️ using Agno Multi-Agent Framework**


