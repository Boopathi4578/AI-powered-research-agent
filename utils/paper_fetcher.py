"""
Utility module for fetching academic papers from various sources.
Supports arXiv API and can be extended for other sources.
"""

import arxiv
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PaperFetcher:
    """Fetches academic papers from various sources."""
    
    def __init__(self, max_results: int = 10):
        """
        Initialize the PaperFetcher.
        
        Args:
            max_results: Maximum number of papers to fetch per query
        """
        self.max_results = max_results
    
    def fetch_from_arxiv(
        self, 
        query: str, 
        max_results: Optional[int] = None,
        days_back: int = 30
    ) -> List[Dict]:
        """
        Fetch papers from arXiv based on a search query.
        
        Args:
            query: Search query string
            max_results: Override default max_results
            days_back: Only fetch papers from the last N days
            
        Returns:
            List of paper dictionaries with metadata
        """
        max_results = max_results or self.max_results
        
        try:
            # Create arXiv search
            search = arxiv.Search(
                query=query,
                max_results=max_results,
                sort_by=arxiv.SortCriterion.SubmittedDate,
                sort_order=arxiv.SortOrder.Descending
            )
            
            papers = []
            cutoff_date = datetime.now() - timedelta(days=days_back)
            
            for result in search.results():
                # Filter by date
                if result.published.replace(tzinfo=None) < cutoff_date:
                    continue
                
                paper = {
                    'title': result.title,
                    'authors': [author.name for author in result.authors],
                    'abstract': result.summary,
                    'published': result.published.strftime('%Y-%m-%d'),
                    'updated': result.updated.strftime('%Y-%m-%d'),
                    'pdf_url': result.pdf_url,
                    'arxiv_url': result.entry_id,
                    'categories': result.categories,
                    'primary_category': result.primary_category,
                    'source': 'arxiv'
                }
                papers.append(paper)
            
            logger.info(f"Fetched {len(papers)} papers from arXiv for query: '{query}'")
            return papers
            
        except Exception as e:
            logger.error(f"Error fetching from arXiv: {str(e)}")
            return []
    
    def fetch_papers(
        self, 
        query: str, 
        sources: List[str] = ['arxiv'],
        max_results: Optional[int] = None
    ) -> List[Dict]:
        """
        Fetch papers from multiple sources.
        
        Args:
            query: Search query string
            sources: List of sources to fetch from (currently supports 'arxiv')
            max_results: Maximum number of results per source
            
        Returns:
            Combined list of papers from all sources
        """
        all_papers = []
        
        if 'arxiv' in sources:
            arxiv_papers = self.fetch_from_arxiv(query, max_results)
            all_papers.extend(arxiv_papers)
        
        # Can add more sources here in the future
        # if 'pubmed' in sources:
        #     pubmed_papers = self.fetch_from_pubmed(query, max_results)
        #     all_papers.extend(pubmed_papers)
        
        logger.info(f"Total papers fetched: {len(all_papers)}")
        return all_papers
    
    def get_paper_details(self, arxiv_id: str) -> Optional[Dict]:
        """
        Get detailed information about a specific arXiv paper.
        
        Args:
            arxiv_id: arXiv paper ID
            
        Returns:
            Paper details dictionary or None if not found
        """
        try:
            search = arxiv.Search(id_list=[arxiv_id])
            result = next(search.results())
            
            return {
                'title': result.title,
                'authors': [author.name for author in result.authors],
                'abstract': result.summary,
                'published': result.published.strftime('%Y-%m-%d'),
                'pdf_url': result.pdf_url,
                'arxiv_url': result.entry_id,
                'categories': result.categories,
            }
        except Exception as e:
            logger.error(f"Error fetching paper details: {str(e)}")
            return None

