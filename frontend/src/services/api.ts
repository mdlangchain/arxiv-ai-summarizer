import axios from 'axios';
import { Paper } from '../types/Paper';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
});

export interface PapersResponse {
  papers: Paper[];
  count: number;
  category: string;
}

export interface PaperResponse {
  paper: Paper;
}

export class ApiService {
  static async getPapers(limit: number = 10, category: string = 'cs.AI'): Promise<PapersResponse> {
    try {
      const response = await api.get('/api/papers', {
        params: { limit, category }
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching papers:', error);
      throw error;
    }
  }

  static async getPaper(paperId: string): Promise<PaperResponse> {
    try {
      const response = await api.get(`/api/paper/${paperId}`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching paper ${paperId}:`, error);
      throw error;
    }
  }

  static async healthCheck(): Promise<any> {
    try {
      const response = await api.get('/health');
      return response.data;
    } catch (error) {
      console.error('Health check failed:', error);
      throw error;
    }
  }

  static async testApis(): Promise<any> {
    try {
      const response = await api.get('/api/test');
      return response.data;
    } catch (error) {
      console.error('API test failed:', error);
      throw error;
    }
  }
}