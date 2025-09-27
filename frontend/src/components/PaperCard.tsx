import React from 'react';
import { Paper } from '../types/Paper';
import './PaperCard.css';

interface PaperCardProps {
  paper: Paper;
}

const PaperCard: React.FC<PaperCardProps> = ({ paper }) => {
  const formatDate = (dateString: string | null): string => {
    if (!dateString) return 'Date not available';

    try {
      const date = new Date(dateString);
      return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      });
    } catch {
      return dateString;
    }
  };

  const formatAuthors = (authors: string[]): string => {
    if (authors.length === 0) return 'Authors not available';
    if (authors.length === 1) return authors[0];
    if (authors.length <= 3) return authors.join(', ');
    return `${authors.slice(0, 3).join(', ')} et al.`;
  };

  return (
    <div className="paper-card">
      <div className="paper-header">
        <h3 className="paper-title">
          <a
            href={paper.arxiv_link || '#'}
            target="_blank"
            rel="noopener noreferrer"
            className="title-link"
          >
            {paper.title}
          </a>
        </h3>
        <div className="paper-meta">
          <span className="paper-authors">{formatAuthors(paper.authors)}</span>
          <span className="paper-date">{formatDate(paper.published_date)}</span>
        </div>
      </div>

      {paper.summary && (
        <div className="paper-summary">
          <h4>AI Summary</h4>
          <p>{paper.summary}</p>
        </div>
      )}

      <div className="paper-actions">
        {paper.pdf_link && (
          <a
            href={paper.pdf_link}
            target="_blank"
            rel="noopener noreferrer"
            className="action-button pdf-button"
          >
            📄 Read PDF
          </a>
        )}
        {paper.arxiv_link && (
          <a
            href={paper.arxiv_link}
            target="_blank"
            rel="noopener noreferrer"
            className="action-button arxiv-button"
          >
            🔗 View on arXiv
          </a>
        )}
      </div>

      {paper.categories.length > 0 && (
        <div className="paper-categories">
          {paper.categories.slice(0, 3).map((category, index) => (
            <span key={index} className="category-tag">
              {category}
            </span>
          ))}
        </div>
      )}
    </div>
  );
};

export default PaperCard;