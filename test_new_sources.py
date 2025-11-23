#!/usr/bin/env python3
"""
Test script to demonstrate the new paper sources.
Tests OpenAlex, CORE, Zenodo, ScienceOpen, JURN, and DOAJ integrations.
"""

import sys
import os
from dotenv import load_dotenv

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.paper_fetcher import PaperFetcher

# Load environment variables
load_dotenv()


def test_source(source_name: str, query: str, max_results: int = 3):
    """Test a specific paper source."""
    print(f"\n{'='*70}")
    print(f"Testing {source_name.upper()}")
    print(f"{'='*70}")
    print(f"Query: {query}")
    print(f"Max Results: {max_results}\n")
    
    fetcher = PaperFetcher(max_results=max_results)
    
    try:
        papers = fetcher.fetch_papers(query, sources=[source_name], max_results=max_results)
        
        if papers:
            print(f"✅ Successfully fetched {len(papers)} papers from {source_name}")
            print("\nSample papers:")
            for i, paper in enumerate(papers[:2], 1):
                print(f"\n{i}. {paper['title']}")
                print(f"   Authors: {', '.join(paper['authors'][:3])}")
                print(f"   Published: {paper['published']}")
                print(f"   Source: {paper['source']}")
                if paper.get('pdf_url'):
                    print(f"   PDF: {paper['pdf_url'][:80]}...")
        else:
            print(f"⚠️  No papers found from {source_name}")
            
    except Exception as e:
        print(f"❌ Error testing {source_name}: {str(e)}")
        import traceback
        traceback.print_exc()


def test_all_sources():
    """Test all available sources."""
    query = "machine learning"
    
    print("\n" + "="*70)
    print("TESTING ALL NEW PAPER SOURCES")
    print("="*70)
    
    sources = [
        ('openalex', 'OpenAlex - Open scholarly metadata'),
        ('core', 'CORE - Aggregator of open access papers'),
        ('zenodo', 'Zenodo - Open research repository'),
        ('doaj', 'DOAJ - Directory of Open Access Journals'),
        ('scienceopen', 'ScienceOpen - Research network'),
        ('jurn', 'JURN - Arts & humanities journals'),
    ]
    
    for source_id, description in sources:
        print(f"\n{description}")
        test_source(source_id, query, max_results=3)
        print("\n" + "-"*70)


def test_multiple_sources():
    """Test fetching from multiple sources simultaneously."""
    print("\n" + "="*70)
    print("TESTING MULTIPLE SOURCES SIMULTANEOUSLY")
    print("="*70)
    
    query = "artificial intelligence"
    sources = ['arxiv', 'openalex', 'core', 'zenodo', 'doaj']
    
    print(f"\nQuery: {query}")
    print(f"Sources: {', '.join(sources)}")
    print(f"\nFetching papers...\n")
    
    fetcher = PaperFetcher(max_results=5)
    papers = fetcher.fetch_papers(query, sources=sources, max_results=5)
    
    print(f"\n✅ Total papers fetched: {len(papers)}")
    
    # Group by source
    by_source = {}
    for paper in papers:
        source = paper['source']
        if source not in by_source:
            by_source[source] = []
        by_source[source].append(paper)
    
    print("\nPapers by source:")
    for source, source_papers in by_source.items():
        print(f"  {source}: {len(source_papers)} papers")
    
    print("\nSample papers from each source:")
    for source, source_papers in by_source.items():
        if source_papers:
            paper = source_papers[0]
            print(f"\n[{source.upper()}] {paper['title'][:80]}...")
            print(f"  Authors: {', '.join(paper['authors'][:2])}")
            print(f"  Published: {paper['published']}")


def main():
    """Main test function."""
    print("\n" + "="*70)
    print("PAPER FETCHER - NEW SOURCES TEST SUITE")
    print("="*70)
    print("\nThis script tests the following new sources:")
    print("  1. OpenAlex - Open scholarly metadata")
    print("  2. CORE - Aggregator of open access papers")
    print("  3. Zenodo - Open research repository")
    print("  4. ScienceOpen - Research network")
    print("  5. JURN - Arts & humanities journals")
    print("  6. DOAJ - Directory of Open Access Journals")
    
    print("\nSelect test mode:")
    print("  1. Test all sources individually")
    print("  2. Test multiple sources simultaneously")
    print("  3. Test specific source")
    print("  4. Run all tests")
    
    choice = input("\nEnter choice (1-4) or press Enter for all tests: ").strip()
    
    if choice == '1':
        test_all_sources()
    elif choice == '2':
        test_multiple_sources()
    elif choice == '3':
        print("\nAvailable sources: openalex, core, zenodo, scienceopen, jurn, doaj")
        source = input("Enter source name: ").strip().lower()
        query = input("Enter search query: ").strip()
        test_source(source, query, max_results=5)
    else:
        # Run all tests
        test_all_sources()
        test_multiple_sources()
    
    print("\n" + "="*70)
    print("TEST COMPLETE")
    print("="*70)


if __name__ == "__main__":
    main()

