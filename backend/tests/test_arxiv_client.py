"""
Tests for arXiv API client.
"""
import unittest
from unittest.mock import patch, Mock
import sys
import os

# Add app directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

from arxiv_client import ArxivClient


class TestArxivClient(unittest.TestCase):
    """Test cases for ArxivClient."""

    def setUp(self):
        """Set up test fixtures."""
        self.client = ArxivClient()

    def test_client_initialization(self):
        """Test that client initializes correctly."""
        self.assertEqual(self.client.base_url, "http://export.arxiv.org/api/query")

    @patch('arxiv_client.requests.get')
    @patch('arxiv_client.feedparser.parse')
    def test_fetch_papers_success(self, mock_parse, mock_get):
        """Test successful paper fetching."""
        # Mock response
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.content = b"<feed>test</feed>"
        mock_get.return_value = mock_response

        # Mock parsed feed
        mock_entry = Mock()
        mock_entry.id = "http://arxiv.org/abs/2301.00001v1"
        mock_entry.title = "Test Paper"
        mock_entry.summary = "Test abstract"
        mock_entry.authors = [Mock(name="Author One"), Mock(name="Author Two")]
        mock_entry.published = "2023-01-01T00:00:00Z"
        mock_entry.links = [{"type": "application/pdf", "href": "https://arxiv.org/pdf/2301.00001.pdf"}]
        mock_entry.tags = [Mock(term="cs.AI"), Mock(term="cs.LG")]

        mock_feed = Mock()
        mock_feed.entries = [mock_entry]
        mock_parse.return_value = mock_feed

        # Call method
        papers = self.client.fetch_papers(max_results=1)

        # Assertions
        self.assertEqual(len(papers), 1)
        paper = papers[0]
        self.assertEqual(paper['id'], '2301.00001v1')
        self.assertEqual(paper['title'], 'Test Paper')
        self.assertEqual(paper['abstract'], 'Test abstract')
        self.assertEqual(len(paper['authors']), 2)
        self.assertEqual(paper['authors'][0], 'Author One')

    @patch('arxiv_client.requests.get')
    def test_fetch_papers_api_error(self, mock_get):
        """Test handling of API errors."""
        mock_get.side_effect = Exception("API Error")

        with self.assertRaises(Exception):
            self.client.fetch_papers()

    def test_parse_entry_basic(self):
        """Test parsing of basic entry data."""
        mock_entry = Mock()
        mock_entry.id = "http://arxiv.org/abs/2301.00001v1"
        mock_entry.title = "Test Paper"
        mock_entry.summary = "Test abstract"
        mock_entry.authors = [Mock(name="Author One")]
        mock_entry.published = "2023-01-01T00:00:00Z"
        mock_entry.links = []
        mock_entry.tags = []

        paper = self.client._parse_entry(mock_entry)

        self.assertEqual(paper['id'], '2301.00001v1')
        self.assertEqual(paper['title'], 'Test Paper')
        self.assertEqual(paper['abstract'], 'Test abstract')
        self.assertEqual(len(paper['authors']), 1)


if __name__ == '__main__':
    unittest.main()