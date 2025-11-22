# Deployment Guide

This guide covers different ways to deploy and use the Research Agent.

## Local Development

### Standard Setup

```bash
# 1. Clone repository
git clone <repository-url>
cd Onedata_assignment

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env and add API keys

# 5. Verify setup
python test_setup.py

# 6. Run
python main.py "your query here"
```

## Using as a Python Package

You can import and use the ResearchAgent in your own Python scripts:

```python
from src.research_agent import ResearchAgent

# Initialize agent
agent = ResearchAgent(
    model_provider="openai",  # or "anthropic"
    max_papers=5
)

# Generate report
report_path = agent.generate_report(
    query="machine learning",
    sources=['arxiv'],
    output_filename="my_report.md"
)

print(f"Report saved to: {report_path}")
```

## Docker Deployment (Future)

Create a `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["python", "main.py"]
```

Build and run:

```bash
docker build -t research-agent .
docker run -e OPENAI_API_KEY=your_key research-agent "your query"
```

## Web Service Deployment

### Using AgentOS (Agno's Runtime)

The Agno framework includes AgentOS, a production-ready FastAPI runtime:

```python
# Create serve.py
from agno.agentos import AgentOS
from src.research_agent import ResearchAgent

agent = ResearchAgent()
app = AgentOS(agent)

if __name__ == "__main__":
    app.run()
```

Run:
```bash
python serve.py
```

Access at: `http://localhost:8000`

### Using Streamlit

Create `app.py`:

```python
import streamlit as st
from src.research_agent import ResearchAgent

st.title("🔬 AI Research Agent")

query = st.text_input("Enter your research query:")
max_papers = st.slider("Max papers", 1, 20, 5)
provider = st.selectbox("LLM Provider", ["openai", "anthropic"])

if st.button("Generate Report"):
    with st.spinner("Fetching and analyzing papers..."):
        agent = ResearchAgent(provider, max_papers)
        report_path = agent.generate_report(query)
        
        with open(report_path, 'r') as f:
            st.markdown(f.read())
```

Run:
```bash
streamlit run app.py
```

## Cloud Deployment

### AWS Lambda

1. Package dependencies:
   ```bash
   pip install -r requirements.txt -t package/
   ```

2. Create Lambda function with the code

3. Set environment variables (API keys)

4. Configure API Gateway for HTTP access

### Google Cloud Run

1. Create `Dockerfile`

2. Build and push:
   ```bash
   gcloud builds submit --tag gcr.io/PROJECT_ID/research-agent
   ```

3. Deploy:
   ```bash
   gcloud run deploy --image gcr.io/PROJECT_ID/research-agent
   ```

### Heroku

1. Create `Procfile`:
   ```
   web: python main.py
   ```

2. Deploy:
   ```bash
   heroku create
   git push heroku main
   ```

## Environment Variables

Required environment variables:

```bash
# At least one is required
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

# Optional
LOG_LEVEL=INFO
```

## Security Considerations

1. **Never commit `.env` file** - Use `.env.example` as template
2. **Use secrets management** in production (AWS Secrets Manager, etc.)
3. **Rotate API keys** regularly
4. **Implement rate limiting** for web deployments
5. **Validate user inputs** to prevent injection attacks

## Monitoring

### Logging

The application uses Python's logging module:

```python
import logging
logging.basicConfig(level=logging.INFO)
```

Logs include:
- Query processing steps
- Paper fetching progress
- Summarization status
- Errors and warnings

### Metrics to Track

- Number of queries processed
- Average processing time
- API call counts
- Error rates
- Paper sources used

## Scaling Considerations

### Performance Optimization

1. **Parallel Processing**: Summarize papers concurrently
2. **Caching**: Store fetched papers and summaries
3. **Batch Processing**: Process multiple queries together
4. **Connection Pooling**: Reuse HTTP connections

### Cost Optimization

1. **Use cheaper models** for initial summarization
2. **Implement caching** to reduce API calls
3. **Set rate limits** to control costs
4. **Monitor usage** with provider dashboards

## Troubleshooting

### Common Issues

**"Module not found" errors**
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt`

**"API key not found"**
- Check `.env` file exists
- Verify API key is correctly set
- Ensure no extra spaces in `.env`

**"No papers found"**
- Try different query terms
- Check internet connection
- Verify arXiv API is accessible

**Slow performance**
- Reduce `--max-papers` count
- Use faster LLM models
- Check network latency

## Backup and Recovery

### Backup Generated Reports

```bash
# Backup data directory
tar -czf reports_backup_$(date +%Y%m%d).tar.gz data/
```

### Version Control

- Commit code changes regularly
- Tag releases: `git tag -a v1.0.0 -m "Release 1.0.0"`
- Keep `.env` out of version control

## Updates and Maintenance

### Updating Dependencies

```bash
# Update all packages
pip install --upgrade -r requirements.txt

# Update specific package
pip install --upgrade agno

# Freeze new versions
pip freeze > requirements.txt
```

### Monitoring for Updates

- Watch Agno framework releases
- Monitor LLM provider API changes
- Check arXiv API status

---

For more information, see:
- README.md - General documentation
- QUICKSTART.md - Quick start guide
- ARCHITECTURE.md - System architecture

