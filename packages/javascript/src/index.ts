/**
 * Tavo AI JavaScript/TypeScript SDK
 */

import axios from 'axios';

export const VERSION = '0.1.0';

export interface TavoConfig {
  apiKey: string;
  baseURL?: string;
  apiVersion?: string;
  timeout?: number;
  maxRetries?: number;
}

export interface ScanRequest {
  repositoryUrl: string;
  scanType?: 'security' | 'dependency' | 'full';
  branch?: string;
  commit?: string;
}

export interface ScanResult {
  id: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  repositoryUrl: string;
  scanType: string;
  createdAt: string;
  updatedAt: string;
  results?: ScanFindings;
}

export interface ScanFindings {
  vulnerabilities: Vulnerability[];
  dependencies: Dependency[];
  summary: ScanSummary;
}

export interface Vulnerability {
  id: string;
  severity: 'critical' | 'high' | 'medium' | 'low' | 'info';
  title: string;
  description: string;
  cwe?: string;
  cvss?: number;
  location: CodeLocation;
  remediation?: string;
}

export interface Dependency {
  name: string;
  version: string;
  ecosystem: string;
  vulnerabilities: string[];
}

export interface ScanSummary {
  totalVulnerabilities: number;
  criticalCount: number;
  highCount: number;
  mediumCount: number;
  lowCount: number;
  scannedFiles: number;
  scanDuration: number;
}

export interface CodeLocation {
  file: string;
  line?: number;
  column?: number;
  snippet?: string;
}

export class TavoClient {
  private readonly config: Required<TavoConfig>;
  private readonly axios: any;

  constructor(config: TavoConfig) {
    this.config = {
      apiKey: config.apiKey,
      baseURL: config.baseURL || 'https://api.tavo.ai',
      apiVersion: config.apiVersion || 'v1',
      timeout: config.timeout || 30000,
      maxRetries: config.maxRetries || 3,
    };

    // Initialize axios instance
    this.axios = this.createAxiosInstance();
  }

  private createAxiosInstance() {
    return axios.create({
      baseURL: `${this.config.baseURL}/api/${this.config.apiVersion}`,
      timeout: this.config.timeout,
      headers: {
        'Authorization': `Bearer ${this.config.apiKey}`,
        'Content-Type': 'application/json',
        'User-Agent': `tavo-js-sdk/${VERSION}`,
      },
    });
  }

  /**
   * Health check endpoint
   */
  async healthCheck(): Promise<{ status: string; timestamp: string }> {
    const response = await this.axios.get('/health');
    return response.data;
  }

  /**
   * Scan operations
   */
  get scans() {
    return {
      /**
       * Create a new security scan
       */
      create: async (request: ScanRequest): Promise<ScanResult> => {
        const response = await this.axios.post('/scans', request);
        return response.data;
      },

      /**
       * Get scan details
       */
      get: async (scanId: string): Promise<ScanResult> => {
        const response = await this.axios.get(`/scans/${scanId}`);
        return response.data;
      },

      /**
       * List scans
       */
      list: async (params?: {
        limit?: number;
        offset?: number;
        status?: string;
      }): Promise<{ scans: ScanResult[]; total: number }> => {
        const response = await this.axios.get('/scans', { params });
        return response.data;
      },

      /**
       * Cancel a scan
       */
      cancel: async (scanId: string): Promise<void> => {
        await this.axios.post(`/scans/${scanId}/cancel`);
      },
    };
  }

  /**
   * Report operations
   */
  get reports() {
    return {
      /**
       * Get report details
       */
      get: async (reportId: string): Promise<any> => {
        const response = await this.axios.get(`/reports/${reportId}`);
        return response.data;
      },

      /**
       * List reports
       */
      list: async (params?: {
        limit?: number;
        offset?: number;
        scanId?: string;
      }): Promise<any> => {
        const response = await this.axios.get('/reports', { params });
        return response.data;
      },
    };
  }
}

// Default export
export default TavoClient;