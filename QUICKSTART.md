# Quick Start Guide

Get up and running with the Research Agent in 5 minutes!

## Step 1: Install Dependencies

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

## Step 2: Configure API Key

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your API key
# You need at least one of: OPENAI_API_KEY or ANTHROPIC_API_KEY
```

Get your API key:
- **OpenAI**: https://platform.openai.com/api-keys
- **Anthropic**: https://console.anthropic.com/

## Step 3: Run Your First Query

```bash
# Simple query (uses OpenAI by default)
python main.py "transformer models in NLP"

# Or with Anthropic Claude
python main.py "quantum computing" --provider anthropic
```

## Step 4: View Your Report

Reports are saved in the `data/` directory:
- `research_report_YYYYMMDD_HHMMSS.md` - Markdown report
- `research_report_YYYYMMDD_HHMMSS.json` - Raw JSON data

## Example Commands

```bash
# Fetch 10 papers on machine learning
python main.py "machine learning" --max-papers 10

# Use custom output filename
python main.py "deep learning" --output my_report.md

# Use Anthropic Claude
python main.py "neural networks" --provider anthropic
```

## Troubleshooting

### "OPENAI_API_KEY not found"
- Make sure you created a `.env` file (not `.env.example`)
- Check that your API key is correctly set in `.env`

### "No papers found"
- Try a more specific or different query
- Check your internet connection
- arXiv might be temporarily unavailable

### Import errors
- Make sure you activated the virtual environment
- Run `pip install -r requirements.txt` again

## Next Steps

- Check `data/sample_queries.txt` for more example queries
- Read the full `README.md` for advanced usage
- Customize the agent behavior in `src/research_agent.py`

Happy researching! 🔬🤖

