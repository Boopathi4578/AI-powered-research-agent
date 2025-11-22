#!/usr/bin/env python3
"""
Test script to verify the installation and setup.
Run this to check if everything is configured correctly.
"""

import sys
import os

def test_imports():
    """Test if all required packages can be imported."""
    print("Testing imports...")
    try:
        import agno
        print("✓ Agno framework installed")
    except ImportError as e:
        print(f"✗ Agno not found: {e}")
        return False
    
    try:
        import arxiv
        print("✓ arXiv package installed")
    except ImportError as e:
        print(f"✗ arXiv not found: {e}")
        return False
    
    try:
        import openai
        print("✓ OpenAI package installed")
    except ImportError as e:
        print(f"✗ OpenAI not found: {e}")
        return False
    
    try:
        import anthropic
        print("✓ Anthropic package installed")
    except ImportError as e:
        print(f"✗ Anthropic not found: {e}")
        return False
    
    try:
        from dotenv import load_dotenv
        print("✓ python-dotenv installed")
    except ImportError as e:
        print(f"✗ python-dotenv not found: {e}")
        return False
    
    return True


def test_project_structure():
    """Test if project structure is correct."""
    print("\nTesting project structure...")
    
    required_dirs = ['src', 'models', 'utils', 'data']
    required_files = [
        'main.py',
        'requirements.txt',
        'README.md',
        'src/research_agent.py',
        'models/llm_config.py',
        'utils/paper_fetcher.py',
        'utils/report_generator.py'
    ]
    
    all_good = True
    
    for dir_name in required_dirs:
        if os.path.isdir(dir_name):
            print(f"✓ Directory '{dir_name}' exists")
        else:
            print(f"✗ Directory '{dir_name}' missing")
            all_good = False
    
    for file_name in required_files:
        if os.path.isfile(file_name):
            print(f"✓ File '{file_name}' exists")
        else:
            print(f"✗ File '{file_name}' missing")
            all_good = False
    
    return all_good


def test_env_config():
    """Test if environment is configured."""
    print("\nTesting environment configuration...")
    
    from dotenv import load_dotenv
    load_dotenv()
    
    openai_key = os.getenv('OPENAI_API_KEY')
    anthropic_key = os.getenv('ANTHROPIC_API_KEY')
    
    if openai_key and openai_key != 'your_openai_api_key_here':
        print("✓ OPENAI_API_KEY is configured")
        has_key = True
    else:
        print("⚠ OPENAI_API_KEY not configured")
        has_key = False
    
    if anthropic_key and anthropic_key != 'your_anthropic_api_key_here':
        print("✓ ANTHROPIC_API_KEY is configured")
        has_key = True
    else:
        print("⚠ ANTHROPIC_API_KEY not configured")
    
    if not has_key:
        print("\n⚠ Warning: No API keys configured!")
        print("  Please set at least one API key in your .env file")
        print("  Copy .env.example to .env and add your keys")
        return False
    
    return True


def test_arxiv_connection():
    """Test if we can connect to arXiv."""
    print("\nTesting arXiv connection...")
    
    try:
        import arxiv
        search = arxiv.Search(
            query="machine learning",
            max_results=1
        )
        result = next(search.results())
        print(f"✓ Successfully connected to arXiv")
        print(f"  Sample paper: {result.title[:50]}...")
        return True
    except Exception as e:
        print(f"✗ Failed to connect to arXiv: {e}")
        return False


def main():
    """Run all tests."""
    print("="*60)
    print("Research Agent - Setup Test")
    print("="*60)
    
    results = []
    
    results.append(("Imports", test_imports()))
    results.append(("Project Structure", test_project_structure()))
    results.append(("Environment Config", test_env_config()))
    results.append(("arXiv Connection", test_arxiv_connection()))
    
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    
    for test_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    all_passed = all(result[1] for result in results)
    
    print("="*60)
    if all_passed:
        print("✓ All tests passed! You're ready to go!")
        print("\nTry running:")
        print('  python main.py "machine learning" --max-papers 3')
    else:
        print("✗ Some tests failed. Please fix the issues above.")
        print("\nRefer to README.md or QUICKSTART.md for setup instructions.")
    print("="*60)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())

