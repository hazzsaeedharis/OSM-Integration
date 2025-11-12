/**
 * API Service - Connects to FastAPI backend
 */

import axios from 'axios';

// API Configuration
const API_BASE_URL = 'http://localhost:8000/api/v1';

// Types
export interface Business {
  id: string;
  name: string;
  postal_code: string;
  city: string;
  lat: number | null;
  lon: number | null;
  categories: string[];
  branch_ids: string[];
}

export interface BusinessResponse {
  businesses: Business[];
  total: number;
  limit: number;
  offset: number;
}

export interface Statistics {
  total_businesses: number;
  geocoded_businesses: number;
  unique_postal_codes: number;
  unique_cities: number;
}

// API Client
class ApiService {
  private baseURL: string;

  constructor(baseURL: string = API_BASE_URL) {
    this.baseURL = baseURL;
  }

  /**
   * Get businesses with filters
   */
  async getBusinesses(params: {
    search?: string;
    category?: string;
    city?: string;
    limit?: number;
    offset?: number;
  } = {}): Promise<BusinessResponse> {
    try {
      const response = await axios.get<BusinessResponse>(`${this.baseURL}/businesses`, {
        params,
        timeout: 10000,
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching businesses:', error);
      throw error;
    }
  }

  /**
   * Get single business by ID
   */
  async getBusiness(id: string): Promise<Business> {
    try {
      const response = await axios.get<Business>(`${this.baseURL}/businesses/${id}`, {
        timeout: 5000,
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching business:', error);
      throw error;
    }
  }

  /**
   * Get all categories
   */
  async getCategories(): Promise<string[]> {
    try {
      const response = await axios.get<string[]>(`${this.baseURL}/categories`, {
        timeout: 5000,
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching categories:', error);
      throw error;
    }
  }

  /**
   * Get all cities
   */
  async getCities(): Promise<string[]> {
    try {
      const response = await axios.get<string[]>(`${this.baseURL}/cities`, {
        timeout: 5000,
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching cities:', error);
      throw error;
    }
  }

  /**
   * Get statistics
   */
  async getStatistics(): Promise<Statistics> {
    try {
      const response = await axios.get<Statistics>(`${this.baseURL}/statistics`, {
        timeout: 5000,
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching statistics:', error);
      throw error;
    }
  }

  /**
   * Health check
   */
  async healthCheck(): Promise<{ status: string }> {
    try {
      const response = await axios.get(`${this.baseURL.replace('/api/v1', '')}/health`, {
        timeout: 3000,
      });
      return response.data;
    } catch (error) {
      console.error('Health check failed:', error);
      throw error;
    }
  }
}

export default new ApiService();

