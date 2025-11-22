#!/usr/bin/env python3
"""
Main application entry point for the Research Agent.
Provides CLI interface for running research queries.
"""

import argparse
import sys
import os
from dotenv import load_dotenv

# Add src to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.research_agent import ResearchAgent

# Load environment variables
load_dotenv()


def main():
    """Main CLI interface."""
    parser = argparse.ArgumentParser(
        description="AI-Powered Research Agent - Fetch and summarize academic papers",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Search for papers on transformers in NLP
  python main.py "transformer models in natural language processing"
  
  # Use Anthropic Claude instead of OpenAI
  python main.py "quantum computing" --provider anthropic
  
  # Limit to 5 papers
  python main.py "machine learning" --max-papers 5
  
  # Custom output filename
  python main.py "deep learning" --output my_report.md
        """
    )
    
    parser.add_argument(
        'query',
        type=str,
        help='Research query to search for papers'
    )
    
    parser.add_argument(
        '--provider',
        type=str,
        choices=['openai', 'anthropic'],
        default='openai',
        help='LLM provider to use (default: openai)'
    )
    
    parser.add_argument(
        '--max-papers',
        type=int,
        default=5,
        help='Maximum number of papers to fetch (default: 5)'
    )
    
    parser.add_argument(
        '--output',
        type=str,
        default=None,
        help='Output filename for the report (default: auto-generated)'
    )
    
    parser.add_argument(
        '--sources',
        type=str,
        nargs='+',
        default=['arxiv'],
        help='Sources to search (default: arxiv)'
    )
    
    args = parser.parse_args()
    
    # Validate API keys
    if args.provider == 'openai' and not os.getenv('OPENAI_API_KEY'):
        print("Error: OPENAI_API_KEY not found in environment variables.")
        print("Please set it in your .env file or environment.")
        sys.exit(1)
    
    if args.provider == 'anthropic' and not os.getenv('ANTHROPIC_API_KEY'):
        print("Error: ANTHROPIC_API_KEY not found in environment variables.")
        print("Please set it in your .env file or environment.")
        sys.exit(1)
    
    # Create research agent
    print(f"\n{'='*60}")
    print(f"AI-Powered Research Agent")
    print(f"{'='*60}")
    print(f"Query: {args.query}")
    print(f"Provider: {args.provider}")
    print(f"Max Papers: {args.max_papers}")
    print(f"Sources: {', '.join(args.sources)}")
    print(f"{'='*60}\n")
    
    try:
        agent = ResearchAgent(
            model_provider=args.provider,
            max_papers=args.max_papers
        )
        
        # Generate report
        report_path = agent.generate_report(
            query=args.query,
            sources=args.sources,
            output_filename=args.output
        )
        
        if report_path:
            print(f"\n{'='*60}")
            print(f"✓ Report generated successfully!")
            print(f"{'='*60}")
            print(f"Report saved to: {report_path}")
            print(f"JSON data saved to: {report_path.replace('.md', '.json')}")
            print(f"{'='*60}\n")
        else:
            print("\n✗ No papers found for the query. Try a different search term.\n")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n✗ Error: {str(e)}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

