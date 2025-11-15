import axios, { AxiosInstance, AxiosResponse } from 'axios';
import { z } from 'zod';

import {
  Rule,
  RuleBundle,
  RuleVersion,
  ListRulesRequest,
  ListRulesResponse,
  ListBundlesRequest,
  ListBundlesResponse,
  CreateRuleRequest,
  UpdateRuleRequest,
  CreateBundleRequest,
  InstallBundleRequest,
  InstallBundleResponse,
  MarketplaceSearchRequest,
  MarketplaceSearchResponse,
  APIError,
} from './types';

// Validation schemas
const ListRulesRequestSchema = z.object({
  category: z.string().optional(),
  format: z.string().optional(),
  severity: z.string().optional(),
  authorId: z.string().optional(),
  tags: z.array(z.string()).optional(),
  search: z.string().optional(),
  page: z.number().min(1).optional(),
  limit: z.number().min(1).max(100).optional(),
});

export class RuleRegistryClient {
  private client: AxiosInstance;
  private baseURL: string;

  constructor(options: {
    apiKey?: string;
    baseURL?: string;
    timeout?: number;
  } = {}) {
    this.baseURL = options.baseURL || 'https://registry.tavoai.net/api/v1';

    this.client = axios.create({
      baseURL: this.baseURL,
      timeout: options.timeout || 30000,
      headers: {
        'Content-Type': 'application/json',
        ...(options.apiKey && { 'X-API-Key': options.apiKey }),
      },
    });

    // Add response interceptor for error handling
    this.client.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.data) {
          const apiError = error.response.data as APIError;
          const enhancedError = new Error(apiError.message);
          (enhancedError as any).code = apiError.code;
          (enhancedError as any).details = apiError.details;
          throw enhancedError;
        }
        throw error;
      }
    );
  }

  // Rules API
  async listRules(request: ListRulesRequest = {}): Promise<ListRulesResponse> {
    // Validate request
    ListRulesRequestSchema.parse(request);

    const params = new URLSearchParams();
    Object.entries(request).forEach(([key, value]) => {
      if (value !== undefined) {
        if (Array.isArray(value)) {
          value.forEach(v => params.append(key, v));
        } else {
          params.append(key, String(value));
        }
      }
    });

    const response = await this.client.get<ListRulesResponse>('/rules', { params });
    return response.data;
  }

  async getRule(id: string): Promise<Rule> {
    const response = await this.client.get<Rule>(`/rules/${id}`);
    return response.data;
  }

  async createRule(request: CreateRuleRequest): Promise<Rule> {
    const response = await this.client.post<Rule>('/rules', request);
    return response.data;
  }

  async updateRule(id: string, request: UpdateRuleRequest): Promise<Rule> {
    const response = await this.client.put<Rule>(`/rules/${id}`, request);
    return response.data;
  }

  async deleteRule(id: string): Promise<void> {
    await this.client.delete(`/rules/${id}`);
  }

  async getRuleVersions(id: string): Promise<RuleVersion[]> {
    const response = await this.client.get<RuleVersion[]>(`/rules/${id}/versions`);
    return response.data;
  }

  // Bundles API
  async listBundles(request: ListBundlesRequest = {}): Promise<ListBundlesResponse> {
    const params = new URLSearchParams();
    Object.entries(request).forEach(([key, value]) => {
      if (value !== undefined) {
        if (Array.isArray(value)) {
          value.forEach(v => params.append(key, v));
        } else {
          params.append(key, String(value));
        }
      }
    });

    const response = await this.client.get<ListBundlesResponse>('/bundles', { params });
    return response.data;
  }

  async getBundle(id: string): Promise<RuleBundle> {
    const response = await this.client.get<RuleBundle>(`/bundles/${id}`);
    return response.data;
  }

  async createBundle(request: CreateBundleRequest): Promise<RuleBundle> {
    const response = await this.client.post<RuleBundle>('/bundles', request);
    return response.data;
  }

  async updateBundle(id: string, request: Partial<CreateBundleRequest>): Promise<RuleBundle> {
    const response = await this.client.put<RuleBundle>(`/bundles/${id}`, request);
    return response.data;
  }

  async deleteBundle(id: string): Promise<void> {
    await this.client.delete(`/bundles/${id}`);
  }

  async installBundle(request: InstallBundleRequest): Promise<InstallBundleResponse> {
    const response = await this.client.post<InstallBundleResponse>('/bundles/install', request);
    return response.data;
  }

  async getBundleRules(id: string): Promise<Rule[]> {
    const response = await this.client.get<Rule[]>(`/bundles/${id}/rules`);
    return response.data;
  }

  // Marketplace API
  async searchMarketplace(request: MarketplaceSearchRequest = {}): Promise<MarketplaceSearchResponse> {
    const params = new URLSearchParams();
    Object.entries(request).forEach(([key, value]) => {
      if (value !== undefined) {
        if (Array.isArray(value)) {
          value.forEach(v => params.append(key, v));
        } else {
          params.append(key, String(value));
        }
      }
    });

    const response = await this.client.get<MarketplaceSearchResponse>('/marketplace/search', { params });
    return response.data;
  }

  async getMarketplaceItem(id: string): Promise<any> {
    const response = await this.client.get(`/marketplace/items/${id}`);
    return response.data;
  }

  async rateItem(itemId: string, rating: number, review?: string): Promise<void> {
    await this.client.post(`/marketplace/items/${itemId}/rate`, {
      rating,
      review,
    });
  }

  async getItemStats(itemId: string): Promise<any> {
    const response = await this.client.get(`/marketplace/items/${itemId}/stats`);
    return response.data;
  }

  // Utility methods
  async ping(): Promise<boolean> {
    try {
      await this.client.get('/health');
      return true;
    } catch {
      return false;
    }
  }

  setApiKey(apiKey: string): void {
    this.client.defaults.headers.common['X-API-Key'] = apiKey;
  }

  setBaseURL(baseURL: string): void {
    this.baseURL = baseURL;
    this.client.defaults.baseURL = baseURL;
  }
}
