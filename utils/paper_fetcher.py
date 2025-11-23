"""
Utility module for fetching academic papers from various sources.
Supports multiple academic databases and repositories.
"""

import arxiv
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
import logging
import time
import json
from urllib.parse import quote

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PaperFetcher:
    """Fetches academic papers from various sources."""

    # Source configurations with priority and reliability scores
    SOURCE_CONFIG = {
        'openalex': {
            'name': 'OpenAlex',
            'priority': 1,
            'reliability': 0.95,
            'coverage': 'broad',
            'url': 'https://api.openalex.org/works'
        },
        'core': {
            'name': 'CORE',
            'priority': 2,
            'reliability': 0.90,
            'coverage': 'open_access',
            'url': 'https://api.core.ac.uk/v3/search/works'
        },
        'arxiv': {
            'name': 'arXiv',
            'priority': 3,
            'reliability': 0.98,
            'coverage': 'stem_preprints',
            'url': None  # Uses arxiv library
        },
        'zenodo': {
            'name': 'Zenodo',
            'priority': 4,
            'reliability': 0.85,
            'coverage': 'multidisciplinary',
            'url': 'https://zenodo.org/api/records'
        },
        'doaj': {
            'name': 'DOAJ',
            'priority': 5,
            'reliability': 0.88,
            'coverage': 'peer_reviewed',
            'url': 'https://doaj.org/api/search/articles'
        },
        'scienceopen': {
            'name': 'ScienceOpen',
            'priority': 6,
            'reliability': 0.70,
            'coverage': 'peer_reviewed',
            'url': 'https://www.scienceopen.com/search'
        },
        'jurn': {
            'name': 'JURN',
            'priority': 7,
            'reliability': 0.50,
            'coverage': 'humanities',
            'url': None  # No public API
        }
    }

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
    
    def _fetch_openalex(
        self,
        query: str,
        max_results: int,
        days_back: int = 30
    ) -> List[Dict]:
        """Fetch papers from OpenAlex API."""

        try:
            # OpenAlex API endpoint
            base_url = "https://api.openalex.org/works"
            cutoff_date = datetime.now() - timedelta(days=days_back)
            cutoff_str = cutoff_date.strftime('%Y-%m-%d')

            params = {
                'search': query,
                'filter': f'from_publication_date:{cutoff_str}',
                'per_page': min(max_results, 100),
                'sort': 'publication_date:desc',
                'mailto': 'research@example.com'  # Polite pool access
            }

            response = requests.get(base_url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()

            papers = []
            for work in data.get('results', [])[:max_results]:
                # Extract authors
                authors = []
                for authorship in work.get('authorships', []):
                    author = authorship.get('author', {})
                    if author.get('display_name'):
                        authors.append(author['display_name'])

                # Get publication date
                pub_date = work.get('publication_date', '')

                # Get abstract
                abstract = ''
                if work.get('abstract_inverted_index'):
                    # Reconstruct abstract from inverted index
                    inverted = work['abstract_inverted_index']
                    words = [''] * (max(max(positions) for positions in inverted.values()) + 1)
                    for word, positions in inverted.items():
                        for pos in positions:
                            words[pos] = word
                    abstract = ' '.join(words)

                # Get PDF URL
                pdf_url = None
                if work.get('open_access', {}).get('oa_url'):
                    pdf_url = work['open_access']['oa_url']
                elif work.get('primary_location', {}).get('pdf_url'):
                    pdf_url = work['primary_location']['pdf_url']

                paper = {
                    'title': work.get('title', 'No title'),
                    'authors': authors,
                    'abstract': abstract or 'No abstract available',
                    'published': pub_date,
                    'updated': pub_date,
                    'pdf_url': pdf_url,
                    'arxiv_url': work.get('id', ''),
                    'categories': [concept.get('display_name', '') for concept in work.get('concepts', [])[:3]],
                    'primary_category': work.get('primary_topic', {}).get('display_name', ''),
                    'source': 'openalex'
                }
                papers.append(paper)

            logger.info(f"Fetched {len(papers)} papers from OpenAlex for query: '{query}'")
            return papers

        except Exception as e:
            logger.error(f"Error fetching from OpenAlex: {str(e)}")
            return []

    def _fetch_core(
        self,
        query: str,
        max_results: int,
        days_back: int = 30
    ) -> List[Dict]:
        """Fetch papers from CORE API."""

        try:
            # CORE API v3 endpoint
            base_url = "https://api.core.ac.uk/v3/search/works"

            params = {
                'q': query,
                'limit': min(max_results, 100),
                'sort': 'publishedDate:desc'
            }

            response = requests.get(base_url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()

            papers = []
            cutoff_date = datetime.now() - timedelta(days=days_back)

            for work in data.get('results', [])[:max_results]:
                # Parse publication date
                pub_date_str = work.get('publishedDate', '')
                try:
                    if pub_date_str:
                        pub_date = datetime.strptime(pub_date_str.split('T')[0], '%Y-%m-%d')
                        if pub_date < cutoff_date:
                            continue
                        pub_date_formatted = pub_date.strftime('%Y-%m-%d')
                    else:
                        pub_date_formatted = ''
                except:
                    pub_date_formatted = pub_date_str

                # Extract authors
                authors = [author.get('name', '') for author in work.get('authors', [])]

                paper = {
                    'title': work.get('title', 'No title'),
                    'authors': authors,
                    'abstract': work.get('abstract', 'No abstract available'),
                    'published': pub_date_formatted,
                    'updated': pub_date_formatted,
                    'pdf_url': work.get('downloadUrl', ''),
                    'arxiv_url': work.get('doi', '') or work.get('id', ''),
                    'categories': work.get('subjects', [])[:3] if work.get('subjects') else [],
                    'primary_category': work.get('subjects', [''])[0] if work.get('subjects') else '',
                    'source': 'core'
                }
                papers.append(paper)

            logger.info(f"Fetched {len(papers)} papers from CORE for query: '{query}'")
            return papers

        except Exception as e:
            logger.error(f"Error fetching from CORE: {str(e)}")
            return []

    def _fetch_from_source(self, source: str, query: str, max_results: int, days_back: int = 30) -> List[Dict]:
        """
        Internal method to fetch from a specific source.

        Args:
            source: Source identifier
            query: Search query
            max_results: Maximum results to fetch
            days_back: Days to look back

        Returns:
            List of papers from the source
        """
        try:
            if source == 'arxiv':
                return self.fetch_from_arxiv(query, max_results, days_back)
            elif source == 'openalex':
                return self._fetch_openalex(query, max_results, days_back)
            elif source == 'core':
                return self._fetch_core(query, max_results, days_back)
            elif source == 'zenodo':
                return self._fetch_zenodo(query, max_results, days_back)
            elif source == 'doaj':
                return self._fetch_doaj(query, max_results, days_back)
            elif source == 'scienceopen':
                return self._fetch_scienceopen(query, max_results, days_back)
            elif source == 'jurn':
                return self._fetch_jurn(query, max_results, days_back)
            else:
                logger.warning(f"Unknown source: {source}")
                return []
        except Exception as e:
            logger.error(f"Error fetching from {source}: {str(e)}")
            return []

    def _select_best_source(self, sources: List[str], query: str) -> str:
        """
        Select the best source based on priority and availability.

        Args:
            sources: List of requested sources
            query: Search query (for future smart selection)

        Returns:
            Best source identifier
        """
        # Filter valid sources and sort by priority
        valid_sources = [s for s in sources if s in self.SOURCE_CONFIG]

        if not valid_sources:
            logger.warning(f"No valid sources in {sources}, defaulting to 'openalex'")
            return 'openalex'

        # Sort by priority (lower number = higher priority)
        sorted_sources = sorted(valid_sources, key=lambda s: self.SOURCE_CONFIG[s]['priority'])

        best_source = sorted_sources[0]
        logger.info(f"Selected best source: {best_source} from {sources}")
        return best_source

    def fetch_papers(
        self,
        query: str,
        sources: List[str] = None,
        max_results: Optional[int] = None,
        use_best_source: bool = False
    ) -> List[Dict]:
        """
        Fetch papers from multiple sources or automatically select the best one.

        Args:
            query: Search query string
            sources: List of sources to fetch from. If None, uses default sources.
                    Supported: 'arxiv', 'openalex', 'core', 'zenodo', 'doaj', 'scienceopen', 'jurn'
            max_results: Maximum number of results (total if use_best_source=True, per source otherwise)
            use_best_source: If True, automatically selects and uses only the best source from the list

        Returns:
            List of papers from all sources or best source
        """
        # Default sources if none provided
        if sources is None:
            sources = ['openalex', 'core', 'arxiv', 'zenodo', 'doaj']

        max_results = max_results or self.max_results

        # If use_best_source is True, select and use only the best source
        if use_best_source:
            best_source = self._select_best_source(sources, query)
            logger.info(f"Using best source: {best_source}")
            papers = self._fetch_from_source(best_source, query, max_results)
            logger.info(f"Fetched {len(papers)} papers from {best_source}")
            return papers

        # Otherwise, fetch from all requested sources
        all_papers = []
        for source in sources:
            if source in self.SOURCE_CONFIG:
                logger.info(f"Fetching from {source}...")
                papers = self._fetch_from_source(source, query, max_results)
                all_papers.extend(papers)
            else:
                logger.warning(f"Unknown source: {source}, skipping...")

        logger.info(f"Total papers fetched from {len(sources)} sources: {len(all_papers)}")
        return all_papers
    
    def _fetch_zenodo(
        self,
        query: str,
        max_results: int,
        days_back: int = 30
    ) -> List[Dict]:
        """Fetch papers from Zenodo API."""

        try:
            base_url = "https://zenodo.org/api/records"
            cutoff_date = datetime.now() - timedelta(days=days_back)

            params = {
                'q': query,
                'size': min(max_results, 100),
                'sort': 'mostrecent',
                'type': 'publication'
            }

            response = requests.get(base_url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()

            papers = []
            for record in data.get('hits', {}).get('hits', [])[:max_results]:
                metadata = record.get('metadata', {})

                # Parse publication date
                pub_date_str = metadata.get('publication_date', '')
                try:
                    if pub_date_str:
                        pub_date = datetime.strptime(pub_date_str, '%Y-%m-%d')
                        if pub_date < cutoff_date:
                            continue
                except:
                    pass

                # Extract authors
                authors = [creator.get('name', '') for creator in metadata.get('creators', [])]

                # Get PDF URL
                pdf_url = ''
                for file in record.get('files', []):
                    if file.get('type', '').lower() == 'pdf':
                        pdf_url = file.get('links', {}).get('self', '')
                        break

                paper = {
                    'title': metadata.get('title', 'No title'),
                    'authors': authors,
                    'abstract': metadata.get('description', 'No abstract available'),
                    'published': pub_date_str,
                    'updated': pub_date_str,
                    'pdf_url': pdf_url,
                    'arxiv_url': metadata.get('doi', '') or record.get('links', {}).get('self', ''),
                    'categories': metadata.get('keywords', [])[:3] if metadata.get('keywords') else [],
                    'primary_category': metadata.get('keywords', [''])[0] if metadata.get('keywords') else '',
                    'source': 'zenodo'
                }
                papers.append(paper)

            logger.info(f"Fetched {len(papers)} papers from Zenodo for query: '{query}'")
            return papers

        except Exception as e:
            logger.error(f"Error fetching from Zenodo: {str(e)}")
            return []

    def _fetch_scienceopen(
        self,
        query: str,
        max_results: int,
        days_back: int = 30
    ) -> List[Dict]:
        """Fetch papers from ScienceOpen API (limited functionality)."""
        try:
            # ScienceOpen requires authentication for full API access
            # This is a placeholder implementation
            logger.warning("ScienceOpen requires API authentication. Skipping...")
            return []
        except Exception as e:
            logger.error(f"Error fetching from ScienceOpen: {str(e)}")
            return []

    def _fetch_jurn(
        self,
        query: str,
        max_results: int,
        days_back: int = 30
    ) -> List[Dict]:
        """Fetch papers from JURN directory (no public API available)."""
        try:
            logger.warning("JURN does not provide a public API. Skipping...")
            return []
        except Exception as e:
            logger.error(f"Error fetching from JURN: {str(e)}")
            return []

    def _fetch_doaj(
        self,
        query: str,
        max_results: int,
        days_back: int = 30
    ) -> List[Dict]:
        """Fetch papers from DOAJ (Directory of Open Access Journals) API."""

        try:
            base_url = "https://doaj.org/api/search/articles"

            params = {
                'q': query,
                'pageSize': min(max_results, 100),
                'sort': 'created_date:desc'
            }

            response = requests.get(base_url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()

            papers = []
            cutoff_date = datetime.now() - timedelta(days=days_back)

            for article in data.get('results', [])[:max_results]:
                bibjson = article.get('bibjson', {})

                # Parse publication date
                pub_date_str = ''
                if bibjson.get('year'):
                    pub_date_str = f"{bibjson['year']}-01-01"
                    if bibjson.get('month'):
                        pub_date_str = f"{bibjson['year']}-{bibjson['month']:02d}-01"

                try:
                    if pub_date_str:
                        pub_date = datetime.strptime(pub_date_str.split('T')[0], '%Y-%m-%d')
                        if pub_date < cutoff_date:
                            continue
                except:
                    pass

                # Extract authors
                authors = [author.get('name', '') for author in bibjson.get('author', [])]

                # Get abstract
                abstract = bibjson.get('abstract', 'No abstract available')

                # Get PDF URL
                pdf_url = ''
                for link in bibjson.get('link', []):
                    if link.get('type') == 'fulltext':
                        pdf_url = link.get('url', '')
                        break

                paper = {
                    'title': bibjson.get('title', 'No title'),
                    'authors': authors,
                    'abstract': abstract,
                    'published': pub_date_str,
                    'updated': pub_date_str,
                    'pdf_url': pdf_url,
                    'arxiv_url': bibjson.get('identifier', [{}])[0].get('id', '') if bibjson.get('identifier') else '',
                    'categories': bibjson.get('subject', [])[:3] if bibjson.get('subject') else [],
                    'primary_category': bibjson.get('subject', [{}])[0].get('term', '') if bibjson.get('subject') else '',
                    'source': 'doaj'
                }
                papers.append(paper)

            logger.info(f"Fetched {len(papers)} papers from DOAJ for query: '{query}'")
            return papers

        except Exception as e:
            logger.error(f"Error fetching from DOAJ: {str(e)}")
            return []

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

