# Contributing to Research Agent

Thank you for your interest in contributing to the AI-Powered Research Agent! This document provides guidelines and information for contributors.

## Development Setup

1. **Fork and Clone**
   ```bash
   git clone <your-fork-url>
   cd Onedata_assignment
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment**
   ```bash
   cp .env.example .env
   # Add your API keys
   ```

5. **Verify Setup**
   ```bash
   python test_setup.py
   ```

## Project Structure

```
src/          → Core agent logic
models/       → LLM configuration
utils/        → Helper utilities
data/         → Sample data and outputs
```

## How to Contribute

### Adding New Paper Sources

To add support for a new academic paper source (e.g., PubMed, Google Scholar):

1. **Add method to `utils/paper_fetcher.py`**:
   ```python
   def fetch_from_pubmed(self, query: str, max_results: int = None) -> List[Dict]:
       """Fetch papers from PubMed."""
       # Implementation here
       pass
   ```

2. **Update `fetch_papers()` method** to include the new source

3. **Test thoroughly** with various queries

4. **Update documentation** in README.md

### Adding New LLM Providers

To add support for a new LLM provider:

1. **Update `models/llm_config.py`**:
   ```python
   @staticmethod
   def get_new_provider_model(model_name: str = "default-model"):
       """Get model from new provider."""
       # Implementation
       pass
   ```

2. **Update `get_default_model()` method**

3. **Add environment variable** to `.env.example`

4. **Update CLI** in `main.py` to accept new provider

5. **Update documentation**

### Customizing Report Format

To modify the report format:

1. **Edit template** in `utils/report_generator.py`
2. **Modify `MARKDOWN_TEMPLATE`** constant
3. **Test with sample data**
4. **Update `data/EXAMPLE_OUTPUT.md`**

### Adding New Agent Capabilities

To add new Agno agents:

1. **Create agent** in `src/research_agent.py`:
   ```python
   self.new_agent = Agent(
       name="New Agent",
       model=self.model,
       description="Agent description",
       instructions=[...],
   )
   ```

2. **Add method** to use the agent
3. **Integrate** into workflow
4. **Test thoroughly**

## Code Style

- Follow PEP 8 guidelines
- Use type hints where appropriate
- Add docstrings to all functions and classes
- Keep functions focused and modular
- Use meaningful variable names

## Testing

Before submitting:

1. **Run setup test**:
   ```bash
   python test_setup.py
   ```

2. **Test with sample queries**:
   ```bash
   python main.py "test query" --max-papers 2
   ```

3. **Test both providers** (if you have both API keys):
   ```bash
   python main.py "test" --provider openai
   python main.py "test" --provider anthropic
   ```

## Documentation

When adding features:

- Update README.md with new features
- Add examples to QUICKSTART.md if relevant
- Update ARCHITECTURE.md for structural changes
- Add sample queries to `data/sample_queries.txt`

## Pull Request Process

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** with clear, atomic commits

3. **Test thoroughly**

4. **Update documentation**

5. **Submit PR** with:
   - Clear description of changes
   - Why the change is needed
   - How to test it
   - Screenshots/examples if applicable

## Ideas for Contributions

### High Priority
- [ ] Parallel paper summarization
- [ ] Caching mechanism
- [ ] Additional paper sources (PubMed, etc.)
- [ ] Web interface (Streamlit/Gradio)

### Medium Priority
- [ ] PDF download and full-text analysis
- [ ] Citation graph analysis
- [ ] Database for historical queries
- [ ] Export to other formats (PDF, HTML)

### Nice to Have
- [ ] Multi-language support
- [ ] Custom agent instructions via config
- [ ] Batch processing multiple queries
- [ ] Email report delivery

## Questions?

- Open an issue for bugs or feature requests
- Check existing issues before creating new ones
- Be respectful and constructive

## License

By contributing, you agree that your contributions will be licensed under the same license as the project (MIT License).

---

Thank you for contributing! 🎉

