#!/usr/bin/env python3
"""
Simple demonstration of the new paper sources.
Shows how to use OpenAlex, CORE, Zenodo, and DOAJ.
"""

import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.paper_fetcher import PaperFetcher


def demo_auto_best_source():
    """Demonstrate automatic best source selection."""
    print("\n" + "="*70)
    print("DEMO 1: Automatic Best Source Selection")
    print("="*70)

    fetcher = PaperFetcher(max_results=5)

    # Provide a list of sources and let it pick the best one
    sources = ['openalex', 'core', 'arxiv', 'zenodo', 'doaj']
    print(f"\nAvailable sources: {', '.join(sources)}")
    print("Query: artificial intelligence")
    print("The fetcher will automatically select the best source...\n")

    papers = fetcher.fetch_papers(
        query="artificial intelligence",
        sources=sources,
        use_best_source=True  # Automatically picks the best source
    )

    print(f"\nFetched {len(papers)} papers:")
    for i, paper in enumerate(papers[:3], 1):
        print(f"\n{i}. {paper['title'][:80]}...")
        print(f"   Authors: {', '.join(paper['authors'][:3])}")
        print(f"   Published: {paper['published']}")
        print(f"   Source: {paper['source']}")


def demo_multiple_sources():
    """Demonstrate fetching from multiple sources."""
    print("\n" + "="*70)
    print("DEMO 2: Fetching from Multiple Sources")
    print("="*70)
    
    fetcher = PaperFetcher(max_results=2)
    
    # Fetch from multiple sources
    sources = ['arxiv', 'openalex', 'core', 'zenodo', 'doaj']
    print(f"\nSources: {', '.join(sources)}")
    print("Query: machine learning")
    print("Max results per source: 2\n")
    
    papers = fetcher.fetch_papers(
        query="machine learning",
        sources=sources,
        max_results=2
    )
    
    print(f"\nTotal papers fetched: {len(papers)}")
    
    # Count by source
    by_source = {}
    for paper in papers:
        source = paper['source']
        by_source[source] = by_source.get(source, 0) + 1
    
    print("\nBreakdown by source:")
    for source, count in by_source.items():
        print(f"  {source}: {count} papers")


def demo_default_sources():
    """Demonstrate using default sources."""
    print("\n" + "="*70)
    print("DEMO 3: Using Default Sources")
    print("="*70)

    fetcher = PaperFetcher(max_results=3)

    print("\nWhen no sources are specified, it uses default curated sources:")
    print("Default: openalex, core, arxiv, zenodo, doaj")
    print("Query: deep learning\n")

    # No sources specified - uses defaults
    papers = fetcher.fetch_papers(
        query="deep learning",
        use_best_source=True
    )

    print(f"\nFetched {len(papers)} papers using default sources:")
    if papers:
        print(f"Selected source: {papers[0]['source']}")
        for i, paper in enumerate(papers[:2], 1):
            print(f"\n{i}. {paper['title'][:80]}...")
            print(f"   Authors: {', '.join(paper['authors'][:2])}")


def demo_with_research_agent():
    """Demonstrate using new sources with ResearchAgent."""
    print("\n" + "="*70)
    print("DEMO 4: Using with Research Agent")
    print("="*70)

    print("\nExample code:")
    print("""
from src.research_agent import ResearchAgent

# Create agent
agent = ResearchAgent(max_papers=10)

# Option 1: Use default sources (recommended)
report_path = agent.generate_report(
    query="quantum computing",
    output_filename="quantum_report.md"
)

# Option 2: Specify custom sources
report_path = agent.generate_report(
    query="quantum computing",
    sources=['openalex', 'core', 'arxiv'],
    output_filename="quantum_report.md"
)

print(f"Report saved to: {report_path}")
    """)

    print("\nNote: This requires AWS Bedrock credentials to be configured.")
    print("See .env.example for required environment variables.")


def main():
    """Run all demonstrations."""
    print("\n" + "="*70)
    print("NEW PAPER SOURCES DEMONSTRATION")
    print("="*70)
    print("\nThis demo shows the simplified usage of multiple sources:")
    print("  • OpenAlex - Open scholarly metadata (Priority 1)")
    print("  • CORE - Open access papers aggregator (Priority 2)")
    print("  • arXiv - Preprint repository (Priority 3)")
    print("  • Zenodo - Open research repository (Priority 4)")
    print("  • DOAJ - Directory of Open Access Journals (Priority 5)")
    print("\nKey Features:")
    print("  ✓ Automatic best source selection")
    print("  ✓ Default curated source list")
    print("  ✓ Fetch from multiple sources or single source")

    try:
        demo_auto_best_source()
        demo_multiple_sources()
        demo_default_sources()
        demo_with_research_agent()

        print("\n" + "="*70)
        print("DEMONSTRATION COMPLETE")
        print("="*70)
        print("\nKey Takeaways:")
        print("  1. Use use_best_source=True for automatic source selection")
        print("  2. Default sources are used if none specified")
        print("  3. Fetch from multiple sources by setting use_best_source=False")
        print("\nFor more information, see NEW_SOURCES_GUIDE.md")
        print("To test all sources, run: python test_new_sources.py")

    except Exception as e:
        print(f"\n❌ Error during demonstration: {str(e)}")
        print("\nNote: Some sources may require internet connection.")
        print("Check NEW_SOURCES_GUIDE.md for troubleshooting tips.")


if __name__ == "__main__":
    main()

