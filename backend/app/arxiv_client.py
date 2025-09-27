"""
arXiv API client for fetching research papers.
"""
import feedparser
import requests
from typing import List, Dict, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class ArxivClient:
    """Client for interacting with arXiv API."""

    def __init__(self, base_url: str = "http://export.arxiv.org/api/query"):
        self.base_url = base_url

    def fetch_papers(
        self,
        search_query: str = "cat:cs.AI",
        max_results: int = 10,
        sort_by: str = "submittedDate",
        sort_order: str = "descending"
    ) -> List[Dict]:
        """
        Fetch papers from arXiv API.

        Args:
            search_query: Search query (default: AI category)
            max_results: Number of papers to fetch
            sort_by: Sort by field (submittedDate, lastUpdatedDate, relevance)
            sort_order: Sort order (ascending, descending)

        Returns:
            List of paper dictionaries
        """
        try:
            params = {
                'search_query': search_query,
                'start': 0,
                'max_results': max_results,
                'sortBy': sort_by,
                'sortOrder': sort_order
            }

            logger.info(f"Fetching {max_results} papers from arXiv with query: {search_query}")
            response = requests.get(self.base_url, params=params, timeout=30)
            response.raise_for_status()

            # Parse the Atom XML response
            feed = feedparser.parse(response.content)

            papers = []
            for entry in feed.entries:
                paper = self._parse_entry(entry)
                papers.append(paper)

            logger.info(f"Successfully fetched {len(papers)} papers")
            return papers

        except requests.RequestException as e:
            logger.error(f"Error fetching papers from arXiv: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error parsing arXiv response: {e}")
            raise

    def _parse_entry(self, entry) -> Dict:
        """Parse a single arXiv entry into a structured dictionary."""
        try:
            # Extract ID from the entry id (format: http://arxiv.org/abs/XXXX.XXXXX)
            arxiv_id = entry.id.split('/abs/')[-1] if '/abs/' in entry.id else entry.id

            # Parse authors
            authors = []
            if hasattr(entry, 'authors'):
                authors = [author.name for author in entry.authors]
            elif hasattr(entry, 'author'):
                authors = [entry.author]

            # Parse published date
            published_date = None
            if hasattr(entry, 'published'):
                try:
                    published_date = datetime.strptime(entry.published, "%Y-%m-%dT%H:%M:%SZ").isoformat()
                except ValueError:
                    published_date = entry.published

            # Extract PDF link
            pdf_link = None
            if hasattr(entry, 'links'):
                for link in entry.links:
                    if link.get('type') == 'application/pdf':
                        pdf_link = link.href
                        break

            # If no PDF link found, construct it from arXiv ID
            if not pdf_link and arxiv_id:
                pdf_link = f"https://arxiv.org/pdf/{arxiv_id}.pdf"

            # Extract categories
            categories = []
            if hasattr(entry, 'tags'):
                categories = [tag.term for tag in entry.tags]

            return {
                'id': arxiv_id,
                'title': entry.title.strip() if hasattr(entry, 'title') else '',
                'authors': authors,
                'abstract': entry.summary.strip() if hasattr(entry, 'summary') else '',
                'published_date': published_date,
                'pdf_link': pdf_link,
                'arxiv_link': f"https://arxiv.org/abs/{arxiv_id}",
                'categories': categories
            }

        except Exception as e:
            logger.error(f"Error parsing arXiv entry: {e}")
            return {
                'id': 'unknown',
                'title': 'Error parsing paper',
                'authors': [],
                'abstract': '',
                'published_date': None,
                'pdf_link': None,
                'arxiv_link': None,
                'categories': []
            }

    def get_paper_by_id(self, arxiv_id: str) -> Optional[Dict]:
        """
        Fetch a specific paper by its arXiv ID.

        Args:
            arxiv_id: arXiv paper ID (e.g., "2301.00001")

        Returns:
            Paper dictionary or None if not found
        """
        try:
            search_query = f"id:{arxiv_id}"
            papers = self.fetch_papers(search_query=search_query, max_results=1)
            return papers[0] if papers else None
        except Exception as e:
            logger.error(f"Error fetching paper {arxiv_id}: {e}")
            return None


# Convenience function for easy import
def create_arxiv_client() -> ArxivClient:
    """Create and return an ArxivClient instance."""
    return ArxivClient()