/**
 * Tavo AI JavaScript/TypeScript SDK
 */

import axios from 'axios';

export const VERSION = '0.1.0';

export interface TavoConfig {
  apiKey?: string;
  jwtToken?: string;
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

export interface ReportRequest {
  scanId: string;
  reportType?: 'scan_summary' | 'compliance' | 'sarif' | 'custom';
  format?: 'json' | 'sarif' | 'pdf' | 'csv' | 'html';
  title?: string;
  description?: string;
  complianceFramework?: string;
}

export interface ReportResult {
  id: string;
  reportId: string;
  title: string;
  reportType: string;
  format: string;
  status: 'generating' | 'completed' | 'failed';
  scanId: string;
  userId: string;
  createdAt: string;
  updatedAt: string;
  completedAt?: string;
  content?: any;
  filePath?: string;
  fileSize?: number;
  complianceFramework?: string;
  totalFindings?: number;
  criticalCount?: number;
  highCount?: number;
  mediumCount?: number;
  lowCount?: number;
  infoCount?: number;
}

export interface ReportSummary {
  totalReports: number;
  reportsByType: Record<string, number>;
  reportsByStatus: Record<string, number>;
  recentReports: number;
}

export class TavoClient {
  private readonly config: Required<TavoConfig>;
  private readonly axios: any;

  constructor(config: TavoConfig) {
    // Validate authentication
    if (!config.apiKey && !config.jwtToken) {
      throw new Error('Either API key or JWT token must be provided');
    }

    this.config = {
      apiKey: config.apiKey || '',
      jwtToken: config.jwtToken || '',
      baseURL: config.baseURL || 'https://api.tavo.ai',
      apiVersion: config.apiVersion || 'v1',
      timeout: config.timeout || 30000,
      maxRetries: config.maxRetries || 3,
    };

    // Initialize axios instance
    this.axios = this.createAxiosInstance();
  }

  private createAxiosInstance() {
    const headers: any = {
      'Content-Type': 'application/json',
      'User-Agent': `tavo-js-sdk/${VERSION}`,
    };

    // Set authentication header - API keys use X-API-Key, JWT tokens use Authorization
    if (this.config.jwtToken) {
      headers['Authorization'] = `Bearer ${this.config.jwtToken}`;
    } else if (this.config.apiKey) {
      headers['X-API-Key'] = this.config.apiKey;
    }

    return axios.create({
      baseURL: `${this.config.baseURL}/api/${this.config.apiVersion}`,
      timeout: this.config.timeout,
      headers,
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
       * Get scan results
       */
      results: async (scanId: string, params?: any): Promise<any> => {
        const response = await this.axios.get(`/scans/${scanId}/results`, { params });
        return response.data;
      },

      /**
       * Cancel a running scan
       */
      cancel: async (scanId: string): Promise<{ message: string }> => {
        const response = await this.axios.post(`/scans/${scanId}/cancel`);
        return response.data;
      },

      /**
       * Scan rules operations
       */
      rules: {
        /**
         * Create scan rule
         */
        create: async (ruleData: any): Promise<any> => {
          const response = await this.axios.post('/scans/rules', ruleData);
          return response.data;
        },

        /**
         * List scan rules
         */
        list: async (): Promise<any> => {
          const response = await this.axios.get('/scans/rules');
          return response.data;
        },

        /**
         * Get scan rule
         */
        get: async (ruleId: string): Promise<any> => {
          const response = await this.axios.get(`/scans/rules/${ruleId}`);
          return response.data;
        },

        /**
         * Update scan rule
         */
        update: async (ruleId: string, ruleData: any): Promise<any> => {
          const response = await this.axios.put(`/scans/rules/${ruleId}`, ruleData);
          return response.data;
        },

        /**
         * Delete scan rule
         */
        delete: async (ruleId: string): Promise<void> => {
          await this.axios.delete(`/scans/rules/${ruleId}`);
        },

        /**
         * Upload scan rules file
         */
        upload: async (file: File): Promise<any> => {
          const formData = new FormData();
          formData.append('file', file);
          const response = await this.axios.post('/scans/rules/upload', formData, {
            headers: {
              'Content-Type': 'multipart/form-data',
            },
          });
          return response.data;
        },
      },
    };
  }

  /**
   * Report operations
   */
  get reports() {
    return {
      /**
       * Create a new report
       */
      create: async (reportData: ReportRequest): Promise<ReportResult> => {
        const response = await this.axios.post('/reports', reportData);
        return response.data;
      },

      /**
       * Get report by ID
       */
      get: async (reportId: string): Promise<ReportResult> => {
        const response = await this.axios.get(`/reports/${reportId}`);
        return response.data;
      },

      /**
       * List reports
       */
      list: async (params?: {
        limit?: number;
        offset?: number;
        scan_id?: string;
        format?: string;
      }): Promise<{ reports: ReportResult[]; total: number }> => {
        const response = await this.axios.get('/reports', { params });
        return response.data;
      },

      /**
       * Update report
       */
      update: async (reportId: string, reportData: Partial<ReportRequest>): Promise<ReportResult> => {
        const response = await this.axios.put(`/reports/${reportId}`, reportData);
        return response.data;
      },

      /**
       * Delete report
       */
      delete: async (reportId: string): Promise<void> => {
        await this.axios.delete(`/reports/${reportId}`);
      },

      /**
       * Download report in specified format
       */
      download: async (reportId: string): Promise<Blob> => {
        const response = await this.axios.get(`/reports/${reportId}/download`, {
          responseType: 'blob',
        });
        return response.data;
      },

      /**
       * Generate PDF report
       */
      generatePdf: async (scanId: string): Promise<ReportResult> => {
        const response = await this.axios.post('/reports/generate', {
          scan_id: scanId,
          format: 'pdf',
        });
        return response.data;
      },

      /**
       * Generate CSV report
       */
      generateCsv: async (scanId: string): Promise<ReportResult> => {
        const response = await this.axios.post('/reports/generate', {
          scan_id: scanId,
          format: 'csv',
        });
        return response.data;
      },

      /**
       * Generate JSON report
       */
      generateJson: async (scanId: string): Promise<ReportResult> => {
        const response = await this.axios.post('/reports/generate', {
          scan_id: scanId,
          format: 'json',
        });
        return response.data;
      },

      /**
       * Generate SARIF report
       */
      generateSarif: async (scanId: string): Promise<ReportResult> => {
        const response = await this.axios.post('/reports/generate', {
          scan_id: scanId,
          format: 'sarif',
        });
        return response.data;
      },

      /**
       * Generate HTML report
       */
      generateHtml: async (scanId: string): Promise<ReportResult> => {
        const response = await this.axios.post('/reports/generate', {
          scan_id: scanId,
          format: 'html',
        });
        return response.data;
      },
    };
  }

  /**
   * Authentication operations
   */
  get auth() {
    return {
      /**
       * Login with username/password
       */
      login: async (username: string, password: string): Promise<any> => {
        const response = await this.axios.post('/auth/login', {
          username,
          password,
        });
        return response.data;
      },

      /**
       * Register a new user
       */
      register: async (userData: any): Promise<any> => {
        const response = await this.axios.post('/auth/register', userData);
        return response.data;
      },

      /**
       * Refresh JWT token
       */
      refreshToken: async (refreshToken: string): Promise<any> => {
        const response = await this.axios.post('/auth/refresh', {
          refresh_token: refreshToken,
        });
        return response.data;
      },

      /**
       * Get current user info
       */
      me: async (): Promise<any> => {
        const response = await this.axios.get('/auth/me');
        return response.data;
      },
    };
  }

  /**
   * User management operations
   */
  get users() {
    return {
      /**
       * Create user (admin only)
       */
      create: async (userData: any): Promise<any> => {
        const response = await this.axios.post('/users', userData);
        return response.data;
      },

      /**
       * List users (admin only)
       */
      list: async (): Promise<any> => {
        const response = await this.axios.get('/users');
        return response.data;
      },

      /**
       * Get user details
       */
      get: async (userId: string): Promise<any> => {
        const response = await this.axios.get(`/users/${userId}`);
        return response.data;
      },

      /**
       * Update user
       */
      update: async (userId: string, userData: any): Promise<any> => {
        const response = await this.axios.put(`/users/${userId}`, userData);
        return response.data;
      },

      /**
       * Get current user profile
       */
      getMe: async (): Promise<any> => {
        const response = await this.axios.get('/users/me');
        return response.data;
      },

      /**
       * Update current user profile
       */
      updateMe: async (userData: any): Promise<any> => {
        const response = await this.axios.put('/users/me', userData);
        return response.data;
      },

      /**
       * API key operations
       */
      apiKeys: (() => ({
        /**
         * List my API keys
         */
        list: async (): Promise<any> => {
          const response = await this.axios.get('/users/me/api-keys');
          return response.data;
        },

        /**
         * Create new API key
         */
        create: async (name: string, options?: any): Promise<any> => {
          const response = await this.axios.post('/users/me/api-keys', {
            name,
            ...options,
          });
          return response.data;
        },
      }))(),
    };
  }

  /**
   * Job operations
   */
  get jobs() {
    return {
      /**
       * Get job status
       */
      status: async (jobId: string): Promise<any> => {
        const response = await this.axios.get(`/jobs/status/${jobId}`);
        return response.data;
      },

      /**
       * Get job dashboard
       */
      dashboard: async (): Promise<any> => {
        const response = await this.axios.get('/jobs/dashboard');
        return response.data;
      },
    };
  }

  /**
   * Webhook operations
   */
  get webhooks() {
    return {
      /**
       * List webhook events
       */
      listEvents: async (): Promise<any> => {
        const response = await this.axios.get('/webhooks/events');
        return response.data;
      },

      /**
       * Get webhook event
       */
      getEvent: async (eventId: string): Promise<any> => {
        const response = await this.axios.get(`/webhooks/events/${eventId}`);
        return response.data;
      },
    };
  }

  /**
   * AI analysis operations
   */
  get ai() {
    return {
      /**
       * Analyze code for fixes
       */
      analyzeCode: async (scanId: string, options?: any): Promise<any> => {
        const response = await this.axios.post(`/ai/analyze/${scanId}`, options || {});
        return response.data;
      },

      /**
       * Classify vulnerabilities
       */
      classifyVulnerabilities: async (scanId: string, options?: any): Promise<any> => {
        const response = await this.axios.post(`/ai/classify/${scanId}`, options || {});
        return response.data;
      },

      /**
       * Calculate risk score
       */
      calculateRiskScore: async (scanId: string, options?: any): Promise<any> => {
        const response = await this.axios.post(`/ai/risk-score/${scanId}`, options || {});
        return response.data;
      },

      /**
       * Generate compliance report
       */
      generateComplianceReport: async (scanId: string, options?: any): Promise<any> => {
        const response = await this.axios.post(`/ai/compliance/${scanId}`, options || {});
        return response.data;
      },

      /**
       * Perform predictive analysis
       */
      predictiveAnalysis: async (scanId: string, options?: any): Promise<any> => {
        const response = await this.axios.post(`/ai/predictive/${scanId}`, options || {});
        return response.data;
      },
    };
  }

  /**
   * Billing operations
   */
  get billing() {
    return {
      /**
       * Get usage report
       */
      getUsage: async (): Promise<any> => {
        const response = await this.axios.get('/billing/usage');
        return response.data;
      },

      /**
       * Get usage summary
       */
      getUsageSummary: async (): Promise<any> => {
        const response = await this.axios.get('/billing/usage/summary');
        return response.data;
      },

      /**
       * Get subscription info
       */
      getSubscription: async (): Promise<any> => {
        const response = await this.axios.get('/billing/subscription');
        return response.data;
      },

      /**
       * Get feature access
       */
      getFeatures: async (): Promise<any> => {
        const response = await this.axios.get('/billing/features');
        return response.data;
      },

      /**
       * Get billing information
       */
      getBillingInfo: async (): Promise<any> => {
        const response = await this.axios.get('/billing/billing');
        return response.data;
      },

      /**
       * Upgrade subscription
       */
      upgradeSubscription: async (newTier: string): Promise<any> => {
        const response = await this.axios.post('/billing/upgrade', null, {
          params: { new_tier: newTier }
        });
        return response.data;
      },
    };
  }

  /**
   * Organization operations
   */
  get organizations() {
    return {
      /**
       * Create organization
       */
      create: async (orgData: any): Promise<any> => {
        const response = await this.axios.post('/organizations', orgData);
        return response.data;
      },

      /**
       * List organizations
       */
      list: async (): Promise<any> => {
        const response = await this.axios.get('/organizations');
        return response.data;
      },

      /**
       * Get organization details
       */
      get: async (orgId: string): Promise<any> => {
        const response = await this.axios.get(`/organizations/${orgId}`);
        return response.data;
      },

      /**
       * Update organization
       */
      update: async (orgId: string, orgData: any): Promise<any> => {
        const response = await this.axios.put(`/organizations/${orgId}`, orgData);
        return response.data;
      },

      /**
       * List organization members
       */
      listMembers: async (orgId: string): Promise<any> => {
        const response = await this.axios.get(`/organizations/${orgId}/members`);
        return response.data;
      },

      /**
       * Create organization invite
       */
      createInvite: async (orgId: string, inviteData: any): Promise<any> => {
        const response = await this.axios.post(`/organizations/${orgId}/invites`, inviteData);
        return response.data;
      },

      /**
       * List organization invites
       */
      listInvites: async (orgId: string): Promise<any> => {
        const response = await this.axios.get(`/organizations/${orgId}/invites`);
        return response.data;
      },

      /**
       * Accept organization invite
       */
      acceptInvite: async (token: string): Promise<any> => {
        const response = await this.axios.post(`/organizations/invites/${token}/accept`);
        return response.data;
      },

      /**
       * Reject organization invite
       */
      rejectInvite: async (token: string): Promise<any> => {
        const response = await this.axios.post(`/organizations/invites/${token}/reject`);
        return response.data;
      },
    };
  }
}

// Default export
export default TavoClient;