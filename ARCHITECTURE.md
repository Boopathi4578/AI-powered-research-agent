# Architecture Overview

## System Architecture

The Research Agent is built using a multi-agent architecture powered by the Agno framework. The system follows a modular design with clear separation of concerns.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         User Interface                       │
│                    (CLI - main.py)                          │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    Research Agent                            │
│              (src/research_agent.py)                        │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Orchestration Layer                                  │  │
│  │  - Workflow Management                                │  │
│  │  - Agent Coordination                                 │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌─────────────────┐         ┌─────────────────┐          │
│  │ Summarizer      │         │ Synthesizer     │          │
│  │ Agent (Agno)    │         │ Agent (Agno)    │          │
│  │                 │         │                 │          │
│  │ - Analyzes      │         │ - Cross-paper   │          │
│  │   individual    │         │   analysis      │          │
│  │   papers        │         │ - Theme         │          │
│  │ - Extracts      │         │   extraction    │          │
│  │   key findings  │         │ - Synthesis     │          │
│  └─────────────────┘         └─────────────────┘          │
└────────┬──────────────────────────────┬──────────────────┘
         │                              │
         ▼                              ▼
┌─────────────────┐            ┌─────────────────┐
│  LLM Config     │            │  Paper Fetcher  │
│  (models/)      │            │  (utils/)       │
│                 │            │                 │
│ - OpenAI GPT-4  │            │ - arXiv API     │
│ - Claude 3.5    │            │ - Date filter   │
│ - Model factory │            │ - Metadata      │
└────────┬────────┘            └────────┬────────┘
         │                              │
         ▼                              ▼
┌─────────────────┐            ┌─────────────────┐
│  OpenAI API     │            │  arXiv API      │
│  Anthropic API  │            │  (External)     │
└─────────────────┘            └─────────────────┘
                                        │
                                        ▼
                              ┌─────────────────┐
                              │ Report Generator│
                              │  (utils/)       │
                              │                 │
                              │ - Markdown      │
                              │ - JSON export   │
                              │ - Templates     │
                              └────────┬────────┘
                                       │
                                       ▼
                              ┌─────────────────┐
                              │  Output Files   │
                              │  (data/)        │
                              │                 │
                              │ - .md reports   │
                              │ - .json data    │
                              └─────────────────┘
```

## Component Details

### 1. CLI Interface (`main.py`)
- **Purpose**: User-facing command-line interface
- **Responsibilities**:
  - Parse command-line arguments
  - Validate API keys
  - Initialize ResearchAgent
  - Display progress and results
- **Key Features**:
  - Argument parsing with argparse
  - Environment variable validation
  - User-friendly error messages

### 2. Research Agent (`src/research_agent.py`)
- **Purpose**: Core orchestration and agent management
- **Responsibilities**:
  - Manage workflow: fetch → summarize → synthesize → report
  - Coordinate two specialized Agno agents
  - Handle errors and logging
- **Key Components**:
  - **Summarizer Agent**: Analyzes individual papers
  - **Synthesizer Agent**: Identifies cross-paper insights
- **Workflow**:
  1. Fetch papers using PaperFetcher
  2. Summarize each paper with Summarizer Agent
  3. Synthesize insights with Synthesizer Agent
  4. Generate report with ReportGenerator

### 3. LLM Configuration (`models/llm_config.py`)
- **Purpose**: Manage LLM provider configuration
- **Responsibilities**:
  - Factory methods for model creation
  - API key management
  - Model parameter configuration
- **Supported Providers**:
  - OpenAI (GPT-4o-mini default)
  - Anthropic (Claude-3.5-Sonnet default)

### 4. Paper Fetcher (`utils/paper_fetcher.py`)
- **Purpose**: Fetch academic papers from external sources
- **Responsibilities**:
  - Query arXiv API
  - Filter by date and relevance
  - Extract metadata
- **Features**:
  - Date-based filtering (default: last 30 days)
  - Configurable result limits
  - Extensible for additional sources

### 5. Report Generator (`utils/report_generator.py`)
- **Purpose**: Generate structured reports
- **Responsibilities**:
  - Template-based markdown generation
  - JSON data export
  - File management
- **Features**:
  - Jinja2 templating
  - Professional formatting
  - Dual output (markdown + JSON)

## Data Flow

```
User Query
    ↓
[CLI validates input]
    ↓
[ResearchAgent.generate_report()]
    ↓
[PaperFetcher.fetch_papers()]
    ↓
[arXiv API returns papers]
    ↓
[For each paper: Summarizer Agent analyzes]
    ↓
[Synthesizer Agent cross-analyzes all papers]
    ↓
[ReportGenerator creates markdown + JSON]
    ↓
[Files saved to data/]
    ↓
[Success message to user]
```

## Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Framework | Agno 2.3+ | Multi-agent orchestration |
| LLMs | OpenAI GPT-4, Claude 3.5 | Text analysis & generation |
| Data Source | arXiv API | Academic paper retrieval |
| Templating | Jinja2 | Report generation |
| CLI | argparse | Command-line interface |
| Config | python-dotenv | Environment management |

## Design Patterns

1. **Factory Pattern**: LLMConfig provides factory methods for model creation
2. **Template Method**: ReportGenerator uses Jinja2 templates
3. **Strategy Pattern**: Pluggable LLM providers (OpenAI/Anthropic)
4. **Agent Pattern**: Specialized agents for different tasks

## Extensibility Points

1. **New Paper Sources**: Add methods to PaperFetcher
2. **New LLM Providers**: Extend LLMConfig
3. **Custom Report Formats**: Modify ReportGenerator templates
4. **Additional Agents**: Create new Agno agents in ResearchAgent
5. **Web Interface**: Add Flask/FastAPI layer on top

## Security Considerations

- API keys stored in `.env` file (not committed to git)
- Environment variable validation before execution
- Error handling to prevent API key leakage in logs
- Rate limiting handled by underlying APIs

## Performance Considerations

- Sequential paper summarization (can be parallelized)
- LLM API calls are the bottleneck
- Caching not implemented (future enhancement)
- Network I/O for arXiv API

## Future Enhancements

1. **Parallel Processing**: Summarize papers concurrently
2. **Caching**: Store fetched papers and summaries
3. **Web UI**: Streamlit or Gradio interface
4. **Database**: Store historical queries and results
5. **PDF Analysis**: Full-text extraction and analysis
6. **Citation Graphs**: Analyze paper relationships
7. **Multi-source**: PubMed, Google Scholar, etc.

