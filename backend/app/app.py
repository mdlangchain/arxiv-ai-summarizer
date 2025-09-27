"""
Flask backend for arXiv AI Research Paper Summarizer.
"""
from flask import Flask, jsonify, request
from flask_cors import CORS
import logging
import os
from dotenv import load_dotenv

from arxiv_client import create_arxiv_client
from claude_summarizer import create_claude_summarizer

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)

# Enable CORS for all domains on all routes
CORS(app)

# Configure Flask
app.config['DEBUG'] = os.getenv('FLASK_DEBUG', 'false').lower() == 'true'

# Production configuration
if os.getenv('FLASK_ENV') == 'production':
    app.config['DEBUG'] = False
    # Disable detailed error messages in production
    app.config['PROPAGATE_EXCEPTIONS'] = False

# Initialize clients
try:
    arxiv_client = create_arxiv_client()
    claude_summarizer = create_claude_summarizer()
    logger.info("Successfully initialized arXiv and Claude clients")
except Exception as e:
    logger.error(f"Failed to initialize clients: {e}")
    arxiv_client = None
    claude_summarizer = None


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'service': 'arXiv AI Paper Summarizer',
        'arxiv_client': arxiv_client is not None,
        'claude_client': claude_summarizer is not None
    })


@app.route('/api/papers', methods=['GET'])
def get_papers():
    """
    Get latest papers with summaries.
    Query parameters:
    - limit: Number of papers (default: 10, max: 50)
    - category: arXiv category (default: cs.AI)
    """
    try:
        # Validate clients
        if not arxiv_client or not claude_summarizer:
            return jsonify({'error': 'Service unavailable - clients not initialized'}), 503

        # Get query parameters - strict limits for free tier memory
        limit = min(int(request.args.get('limit', 5)), 8)  # Max 8 papers for stability
        category = request.args.get('category', 'cs.AI')

        logger.info(f"Processing request for {limit} papers")

        # Build search query
        search_query = f'cat:{category}' if category else 'cat:cs.AI'

        logger.info(f"Fetching {limit} papers from category: {category}")

        # Fetch papers from arXiv
        papers = arxiv_client.fetch_papers(
            search_query=search_query,
            max_results=limit
        )

        if not papers:
            return jsonify({
                'papers': [],
                'count': 0,
                'message': 'No papers found'
            })

        # Generate summaries
        papers_with_summaries = claude_summarizer.summarize_papers(papers)

        return jsonify({
            'papers': papers_with_summaries,
            'count': len(papers_with_summaries),
            'category': category
        })

    except ValueError as e:
        logger.error(f"Validation error: {e}")
        return jsonify({'error': 'Invalid parameters'}), 400
    except Exception as e:
        logger.error(f"Error fetching papers: {e}")
        return jsonify({'error': 'Internal server error'}), 500


@app.route('/api/paper/<paper_id>', methods=['GET'])
def get_paper(paper_id):
    """
    Get a specific paper by ID with summary.
    """
    try:
        # Validate clients
        if not arxiv_client or not claude_summarizer:
            return jsonify({'error': 'Service unavailable - clients not initialized'}), 503

        logger.info(f"Fetching paper: {paper_id}")

        # Fetch paper from arXiv
        paper = arxiv_client.get_paper_by_id(paper_id)

        if not paper:
            return jsonify({'error': 'Paper not found'}), 404

        # Generate summary
        summary = claude_summarizer.summarize_paper(
            title=paper.get('title', ''),
            abstract=paper.get('abstract', '')
        )

        paper['summary'] = summary

        return jsonify({
            'paper': paper
        })

    except Exception as e:
        logger.error(f"Error fetching paper {paper_id}: {e}")
        return jsonify({'error': 'Internal server error'}), 500


@app.route('/api/refresh', methods=['POST'])
def refresh_papers():
    """
    Manually trigger refresh of papers cache (placeholder for future caching).
    """
    try:
        # For now, just return a success message
        # In the future, this could clear caches or trigger background jobs
        logger.info("Refresh requested")

        return jsonify({
            'message': 'Refresh completed',
            'timestamp': '2024-01-01T00:00:00Z'  # Placeholder
        })

    except Exception as e:
        logger.error(f"Error during refresh: {e}")
        return jsonify({'error': 'Internal server error'}), 500


@app.route('/api/test', methods=['GET'])
def test_apis():
    """
    Test both arXiv and Claude API connections.
    """
    try:
        results = {
            'arxiv': False,
            'claude': False
        }

        # Test arXiv
        if arxiv_client:
            try:
                test_papers = arxiv_client.fetch_papers(max_results=1)
                results['arxiv'] = len(test_papers) > 0
            except Exception as e:
                logger.error(f"arXiv test failed: {e}")

        # Test Claude
        if claude_summarizer:
            try:
                results['claude'] = claude_summarizer.test_connection()
            except Exception as e:
                logger.error(f"Claude test failed: {e}")

        return jsonify({
            'status': 'tests_completed',
            'results': results,
            'all_working': all(results.values())
        })

    except Exception as e:
        logger.error(f"Error testing APIs: {e}")
        return jsonify({'error': 'Internal server error'}), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    # Check if API key is set
    if not os.getenv('ANTHROPIC_API_KEY'):
        logger.warning("ANTHROPIC_API_KEY not found in environment variables")
        logger.warning("Please set your Claude API key in the .env file")

    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'false').lower() == 'true'

    logger.info(f"Starting Flask server on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)