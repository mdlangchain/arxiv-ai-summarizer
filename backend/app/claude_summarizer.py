"""
Claude API client for generating paper summaries.
"""
import anthropic
from typing import List, Dict, Optional
import logging
import os
import time
import gc
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class ClaudeSummarizer:
    """Client for generating paper summaries using Claude API."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY')
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables")

        # Initialize with longer timeout for Render hosting
        self.client = anthropic.Anthropic(
            api_key=self.api_key,
            timeout=60.0  # Increase timeout for network issues
        )
        self.model = "claude-3-sonnet-20240229"  # Use stable Claude 3 model

    def summarize_paper(self, title: str, abstract: str) -> str:
        """
        Generate a summary for a single research paper with retry logic.

        Args:
            title: Paper title
            abstract: Paper abstract

        Returns:
            Generated summary string
        """
        max_retries = 2
        retry_delay = 1

        for attempt in range(max_retries):
            try:
                prompt = self._build_summary_prompt(title, abstract)

                logger.info(f"Generating summary for paper: {title[:50]}... (attempt {attempt + 1})")

                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=500,
                    temperature=0.2,
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                )

                summary = response.content[0].text.strip()
                logger.info("Summary generated successfully")
                return summary

            except anthropic.APIConnectionError as e:
                logger.error(f"Claude API connection error (attempt {attempt + 1}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    retry_delay *= 2
                else:
                    # Fallback: generate basic summary from abstract
                    return self._generate_fallback_summary(title, abstract)
            except anthropic.APIError as e:
                logger.error(f"Claude API error (attempt {attempt + 1}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    retry_delay *= 2
                else:
                    # Fallback: generate basic summary from abstract
                    return self._generate_fallback_summary(title, abstract)
            except Exception as e:
                logger.error(f"Unexpected error generating summary (attempt {attempt + 1}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    retry_delay *= 2
                else:
                    # Fallback: generate basic summary from abstract
                    return self._generate_fallback_summary(title, abstract)

        # Final fallback
        return self._generate_fallback_summary(title, abstract)

    def summarize_papers(self, papers: List[Dict]) -> List[Dict]:
        """
        Generate summaries for multiple papers with memory optimization.

        Args:
            papers: List of paper dictionaries

        Returns:
            List of papers with added 'summary' field
        """
        # Strict limit for memory stability
        papers = papers[:8]  # Max 8 papers to prevent OOM
        summarized_papers = []

        logger.info(f"Starting to process {len(papers)} papers for summarization")

        for i, paper in enumerate(papers):
            logger.info(f"Processing paper {i+1}/{len(papers)}: {paper.get('title', 'Unknown')[:50]}...")

            try:
                summary = self.summarize_paper(
                    title=paper.get('title', ''),
                    abstract=paper.get('abstract', '')
                )

                # Create new dict to avoid memory buildup
                paper_with_summary = {
                    'id': paper.get('id', ''),
                    'title': paper.get('title', ''),
                    'authors': paper.get('authors', []),
                    'abstract': paper.get('abstract', ''),
                    'published_date': paper.get('published_date'),
                    'pdf_link': paper.get('pdf_link'),
                    'arxiv_link': paper.get('arxiv_link'),
                    'categories': paper.get('categories', []),
                    'summary': summary
                }
                summarized_papers.append(paper_with_summary)

                # Clear original paper from memory and force garbage collection
                del paper
                if i % 2 == 0:  # Run GC every 2 papers
                    gc.collect()

            except Exception as e:
                logger.error(f"Error summarizing paper {i+1}: {e}")
                # Add paper with error message
                paper_with_summary = {
                    'id': paper.get('id', ''),
                    'title': paper.get('title', ''),
                    'authors': paper.get('authors', []),
                    'abstract': paper.get('abstract', ''),
                    'published_date': paper.get('published_date'),
                    'pdf_link': paper.get('pdf_link'),
                    'arxiv_link': paper.get('arxiv_link'),
                    'categories': paper.get('categories', []),
                    'summary': "Summary generation failed."
                }
                summarized_papers.append(paper_with_summary)

        # Final garbage collection
        gc.collect()

        logger.info(f"Completed summarizing {len(summarized_papers)} papers")
        return summarized_papers

    def _build_summary_prompt(self, title: str, abstract: str) -> str:
        """Build the prompt for Claude to generate a paper summary."""
        return f"""Summarize this AI research paper in 3-4 sentences for a technical audience. Focus on the main contribution, methodology, and key findings. Be concise but informative.

Title: {title}

Abstract: {abstract}

Summary:"""

    def _generate_fallback_summary(self, title: str, abstract: str) -> str:
        """Generate a basic summary when Claude API is unavailable."""
        try:
            # Extract first few sentences from abstract
            sentences = abstract.split('. ')

            if len(sentences) >= 3:
                # Take first 3 sentences and clean them up
                summary_sentences = sentences[:3]
                summary = '. '.join(summary_sentences).strip()
                if not summary.endswith('.'):
                    summary += '.'
            else:
                # If abstract is short, use it but truncate if too long
                summary = abstract[:400] + ('...' if len(abstract) > 400 else '')

            # Add a note that this is a fallback
            summary += " [Summary generated from abstract - Claude AI unavailable]"

            logger.info("Generated fallback summary from abstract")
            return summary

        except Exception as e:
            logger.error(f"Error generating fallback summary: {e}")
            return f"Research paper: {title[:100]}... [Summary temporarily unavailable]"

    def test_connection(self) -> bool:
        """
        Test the connection to Claude API with retry logic.

        Returns:
            True if connection successful, False otherwise
        """
        max_retries = 3
        retry_delay = 2

        for attempt in range(max_retries):
            try:
                logger.info(f"Testing Claude API connection (attempt {attempt + 1}/{max_retries})")

                # Test with a very simple request
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=10,
                    messages=[
                        {
                            "role": "user",
                            "content": "Hi"
                        }
                    ]
                )

                result = response.content[0].text.strip()
                logger.info(f"Claude API connection test successful. Response: {result}")
                return True

            except anthropic.APIConnectionError as e:
                logger.error(f"Claude API connection error (attempt {attempt + 1}): {e}")
                # Connection errors are usually temporary, so we retry
            except anthropic.APIError as e:
                logger.error(f"Claude API error (attempt {attempt + 1}): {e}")
                if hasattr(e, 'status_code'):
                    logger.error(f"Status code: {e.status_code}")
                if hasattr(e, 'message'):
                    logger.error(f"Message: {e.message}")
            except anthropic.AuthenticationError as e:
                logger.error(f"Claude authentication error: {e}")
                return False  # Don't retry auth errors
            except Exception as e:
                logger.error(f"Claude API connection test failed (attempt {attempt + 1}): {type(e).__name__}: {e}")

            # Wait before retrying (except on last attempt)
            if attempt < max_retries - 1:
                logger.info(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
                retry_delay *= 2  # Exponential backoff

        logger.error(f"Claude API connection failed after {max_retries} attempts")
        return False


# Convenience function for easy import
def create_claude_summarizer() -> ClaudeSummarizer:
    """Create and return a ClaudeSummarizer instance."""
    return ClaudeSummarizer()