export interface Paper {
  id: string;
  title: string;
  authors: string[];
  abstract: string;
  published_date: string | null;
  pdf_link: string | null;
  arxiv_link: string | null;
  categories: string[];
  summary?: string;
}