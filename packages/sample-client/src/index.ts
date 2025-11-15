/**
 * TavoAI Sample Submission Client
 *
 * Handles code sample submission for analysis and result polling.
 * Supports both synchronous and asynchronous analysis workflows.
 */

import axios, { AxiosInstance } from 'axios';

export interface SampleSubmission {
  id: string;
  code: string;
  language: string;
  scanType: 'SAST' | 'DAST' | 'IAST' | 'SCA';
  rules?: string[];
  metadata?: Record<string, any>;
  status: 'pending' | 'processing' | 'completed' | 'failed';
  createdAt: string;
  updatedAt: string;
}

export interface AnalysisResult {
  id: string;
  submissionId: string;
  findings: SecurityFinding[];
  summary: {
    totalFindings: number;
    criticalCount: number;
    highCount: number;
    mediumCount: number;
    lowCount: number;
    infoCount: number;
  };
  metadata: Record<string, any>;
  completedAt: string;
}

export interface SecurityFinding {
  id: string;
  ruleId: string;
  title: string;
  description: string;
  severity: 'info' | 'low' | 'medium' | 'high' | 'critical';
  confidence: number;
  location: {
    file?: string;
    line?: number;
    column?: number;
    codeSnippet?: string;
  };
  recommendations: string[];
  metadata: Record<string, any>;
}

export interface SubmitSampleRequest {
  code: string;
  language: string;
  scanType: 'SAST' | 'DAST' | 'IAST' | 'SCA';
  rules?: string[];
  metadata?: Record<string, any>;
  waitForResults?: boolean; // If true, wait for completion
  timeout?: number; // Timeout in seconds for waiting
}

export interface SubmitSampleResponse {
  submission: SampleSubmission;
  results?: AnalysisResult; // Only present if waitForResults=true
}

export class SampleClient {
  private client: AxiosInstance;

  constructor(options: {
    apiKey?: string;
    baseURL?: string;
    timeout?: number;
  } = {}) {
    this.client = axios.create({
      baseURL: options.baseURL || 'https://api.tavoai.net/v1',
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
        if (error.response?.data?.message) {
          const enhancedError = new Error(error.response.data.message);
          (enhancedError as any).code = error.response.data.code;
          (enhancedError as any).details = error.response.data.details;
          throw enhancedError;
        }
        throw error;
      }
    );
  }

  async submit(request: SubmitSampleRequest): Promise<SubmitSampleResponse> {
    const payload = {
      code: request.code,
      language: request.language,
      scanType: request.scanType,
      rules: request.rules,
      metadata: request.metadata,
    };

    const response = await this.client.post<SubmitSampleResponse>('/samples', payload);

    // If waiting for results, poll until completion
    if (request.waitForResults) {
      const submission = response.data.submission;
      const results = await this.waitForResults(submission.id, request.timeout || 300);
      return {
        submission,
        results,
      };
    }

    return response.data;
  }

  async getSubmission(submissionId: string): Promise<SampleSubmission> {
    const response = await this.client.get<SampleSubmission>(`/samples/${submissionId}`);
    return response.data;
  }

  async getResults(submissionId: string): Promise<AnalysisResult | null> {
    try {
      const response = await this.client.get<AnalysisResult>(`/samples/${submissionId}/results`);
      return response.data;
    } catch (error: any) {
      // Return null if analysis is not complete yet
      if (error.response?.status === 404 || error.response?.status === 202) {
        return null;
      }
      throw error;
    }
  }

  async waitForResults(submissionId: string, timeoutSeconds: number = 300): Promise<AnalysisResult> {
    const startTime = Date.now();
    const timeoutMs = timeoutSeconds * 1000;

    while (Date.now() - startTime < timeoutMs) {
      const results = await this.getResults(submissionId);
      if (results) {
        return results;
      }

      // Wait 2 seconds before checking again
      await new Promise(resolve => setTimeout(resolve, 2000));
    }

    throw new Error(`Timeout waiting for analysis results (${timeoutSeconds}s)`);
  }

  async listSubmissions(options: {
    status?: string;
    scanType?: string;
    limit?: number;
    offset?: number;
  } = {}): Promise<{
    submissions: SampleSubmission[];
    total: number;
    limit: number;
    offset: number;
  }> {
    const params = new URLSearchParams();
    Object.entries(options).forEach(([key, value]) => {
      if (value !== undefined) {
        params.append(key, String(value));
      }
    });

    const response = await this.client.get('/samples', { params });
    return response.data;
  }

  async deleteSubmission(submissionId: string): Promise<void> {
    await this.client.delete(`/samples/${submissionId}`);
  }

  // Bulk operations
  async submitBatch(requests: SubmitSampleRequest[]): Promise<SubmitSampleResponse[]> {
    const promises = requests.map(request => this.submit(request));
    return Promise.all(promises);
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
    this.client.defaults.baseURL = baseURL;
  }

  // Helper method to analyze code directly (convenience wrapper)
  async analyzeCode(
    code: string,
    language: string,
    options: {
      scanType?: 'SAST' | 'DAST' | 'IAST' | 'SCA';
      rules?: string[];
      waitForResults?: boolean;
      timeout?: number;
    } = {}
  ): Promise<AnalysisResult> {
    const submission = await this.submit({
      code,
      language,
      scanType: options.scanType || 'SAST',
      rules: options.rules,
      waitForResults: options.waitForResults ?? true,
      timeout: options.timeout,
    });

    if (submission.results) {
      return submission.results;
    }

    // This should not happen if waitForResults is true
    throw new Error('Analysis results not available');
  }
}
