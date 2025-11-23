#!/usr/bin/env python3
"""Main application entry point for the Research Agent.

This application runs as an interactive loop, continuously accepting research queries
from the user until they choose to exit.

This application uses AWS Bedrock for LLM inference.

Environment variables:
  - BEDROCK_MODEL_ID: AWS Bedrock model identifier (required)
  - MAX_PAPERS: int (default: 5)
  - OUTPUT: optional output filename prefix
  - SOURCES: space-separated list of sources (default: 'arxiv')
  - AWS_REGION: AWS region (default: us-east-1)

Example:
  export BEDROCK_MODEL_ID="arn:aws:bedrock:us-east-1:123456789012:inference-profile/us.anthropic.claude-3-5-haiku-20241022-v1:0"
  python main.py

  Then enter your research queries interactively.
"""

import sys
import os
from dotenv import load_dotenv
from datetime import datetime

# Add src to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.research_agent import ResearchAgent

# Load environment variables
load_dotenv()


def run(
    query: str,
    max_papers: int = 5,
    output: str = None,
    sources: list = None,
):
    """Programmatic entrypoint to run a research query.

    Returns the path to the generated report or None.
    """
    if sources is None:
        sources = ["arxiv"]

    # Validate AWS Bedrock configuration
    bedrock_model_id = os.getenv("BEDROCK_MODEL_ID")
    if not bedrock_model_id:
        raise RuntimeError("BEDROCK_MODEL_ID not set. Please set the AWS Bedrock model ID in environment variables.")

    # Create research agent
    print(f"\n{'='*60}")
    print("AI-Powered Research Agent (AWS Bedrock)")
    print(f"{'='*60}")
    print(f"Query: {query}")
    print(f"Model: {bedrock_model_id}")
    print(f"Max Papers: {max_papers}")
    print(f"Sources: {', '.join(sources)}")
    print(f"{'='*60}\n")

    agent = ResearchAgent(max_papers=max_papers)

    report_path = agent.generate_report(
        query=query,
        sources=sources,
        output_filename=output,
    )

    return report_path


def main():
    """Interactive loop for continuous research queries."""
    # Validate AWS Bedrock configuration at startup
    bedrock_model_id = os.getenv("BEDROCK_MODEL_ID")
    if not bedrock_model_id:
        print("Error: BEDROCK_MODEL_ID not set. Please configure AWS Bedrock credentials.")
        print("Example:")
        print('  export BEDROCK_MODEL_ID="arn:aws:bedrock:us-east-1:123456789012:inference-profile/us.anthropic.claude-3-5-haiku-20241022-v1:0"')
        print('  export AWS_REGION="us-east-1"')
        print('  export AWS_ACCESS_KEY_ID="your-access-key"')
        print('  export AWS_SECRET_ACCESS_KEY="your-secret-key"')
        sys.exit(1)

    # Get configuration from environment
    max_papers = int(os.getenv("MAX_PAPERS", "5"))
    output_prefix = os.getenv("OUTPUT", "research_report")
    sources_env = os.getenv("SOURCES")
    sources = sources_env.split() if sources_env else ["arxiv"]

    # Print welcome banner
    print(f"\n{'='*70}")
    print("AI-Powered Research Agent (AWS Bedrock) - Interactive Mode")
    print(f"{'='*70}")
    print(f"Model: {bedrock_model_id}")
    print(f"Max Papers: {max_papers}")
    print(f"Sources: {', '.join(sources)}")
    print(f"{'='*70}")
    print("\nEnter your research queries below.")
    print("Type 'exit', 'quit', or press Ctrl+C to stop.\n")

    # Main interactive loop
    query_count = 0
    while True:
        try:
            # Get user input
            query = input("\n🔍 Enter research query: ").strip()

            # Check for exit commands
            if query.lower() in ['exit', 'quit', 'q']:
                print("\n👋 Thank you for using the Research Agent. Goodbye!")
                break

            # Skip empty queries
            if not query:
                print("⚠️ Please enter a valid query.")
                continue

            query_count += 1

            # Generate unique output filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"{output_prefix}_{timestamp}.md"

            try:
                print(f"\n{'─'*70}")
                print(f"Processing query #{query_count}: {query}")
                print(f"{'─'*70}\n")

                report_path = run(
                    query=query,
                    max_papers=max_papers,
                    output=output_filename,
                    sources=sources,
                )

                if report_path:
                    print(f"\n✅ Report saved to: {report_path}")
                    print(f"📊 JSON data saved to: {report_path.replace('.md', '.json')}")
                else:
                    print("\n⚠️ No report generated.")

            except Exception as e:
                print(f"\n❌ Error processing query: {e}")
                import traceback
                traceback.print_exc()
                print("\nYou can try another query or type 'exit' to quit.")

        except KeyboardInterrupt:
            print("\n\n👋 Interrupted by user. Goodbye!")
            break
        except EOFError:
            print("\n\n👋 End of input. Goodbye!")
            break

    print(f"\nTotal queries processed: {query_count}")
    sys.exit(0)


if __name__ == "__main__":
    main()

