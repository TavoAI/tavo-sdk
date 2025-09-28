/**
 * Tavo AI JavaScript/TypeScript SDK
 */

import axios from 'axios';
import { RuleManager, SecurityScanner } from './rules';

// Rule management exports
export * from './rules';

export const VERSION = '0.1.0';

export interface TavoConfig {
  apiKey?: string;
  jwtToken?: string;
  sessionToken?: string;
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

export interface ScanUpdateMessage {
  scan_id: string;
  update_type: 'started' | 'progress' | 'result' | 'completed' | 'error';
  message: string;
  data?: any;
  timestamp?: string;
}

export interface NotificationMessage {
  type: 'info' | 'warning' | 'error' | 'success';
  title: string;
  message: string;
  data?: any;
  timestamp?: string;
}

export interface GeneralMessage {
  type: string;
  message: string;
  data?: any;
  timestamp?: string;
}

export interface WebSocketConfig {
  reconnectInterval?: number;
  maxReconnectAttempts?: number;
  heartbeatInterval?: number;
}

export interface WebSocketConnection {
  websocket: WebSocket;
  clientId: string;
  reconnectAttempts: number;
  isConnected: boolean;
  heartbeatTimer?: NodeJS.Timeout;
  reconnectTimer?: NodeJS.Timeout;
}

export class TavoClient {
  private readonly config: Required<TavoConfig>;
  private readonly axios: any;
  private readonly ruleManager: RuleManager;
  private readonly scanner: SecurityScanner;
  private readonly websocketConnections: Map<string, WebSocketConnection> = new Map();
  private readonly wsConfig: Required<WebSocketConfig>;

  constructor(config: TavoConfig, wsConfig?: WebSocketConfig) {
    // Validate authentication
    if (!config.apiKey && !config.jwtToken && !config.sessionToken) {
      throw new Error('Either API key, JWT token, or session token must be provided');
    }

    this.config = {
      apiKey: config.apiKey || '',
      jwtToken: config.jwtToken || '',
      sessionToken: config.sessionToken || '',
      baseURL: config.baseURL || 'https://api.tavoai.net',
      apiVersion: config.apiVersion || 'v1',
      timeout: config.timeout || 30000,
      maxRetries: config.maxRetries || 3,
    };

    this.wsConfig = {
      reconnectInterval: wsConfig?.reconnectInterval || 5000,
      maxReconnectAttempts: wsConfig?.maxReconnectAttempts || 5,
      heartbeatInterval: wsConfig?.heartbeatInterval || 30000,
    };

    // Initialize axios instance
    this.axios = this.createAxiosInstance();

    // Initialize rule management
    this.ruleManager = new RuleManager();
    this.scanner = new SecurityScanner(this.ruleManager);
  }

  private createAxiosInstance() {
    const headers: any = {
      'Content-Type': 'application/json',
      'User-Agent': `tavo-js-sdk/${VERSION}`,
    };

    // Set authentication header - API keys use X-API-Key, JWT tokens use Authorization, session tokens use X-Session-Token
    if (this.config.jwtToken) {
      headers['Authorization'] = `Bearer ${this.config.jwtToken}`;
    } else if (this.config.sessionToken) {
      headers['X-Session-Token'] = this.config.sessionToken;
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

      /**
       * Get report summary statistics
       */
      getSummary: async (): Promise<ReportSummary> => {
        const response = await this.axios.get('/reports/summary');
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

        /**
         * Update API key
         */
        update: async (apiKeyId: string, name: string, options?: any): Promise<any> => {
          const response = await this.axios.put(`/users/me/api-keys/${apiKeyId}`, {
            name,
            ...options,
          });
          return response.data;
        },

        /**
         * Delete API key
         */
        delete: async (apiKeyId: string): Promise<void> => {
          await this.axios.delete(`/users/me/api-keys/${apiKeyId}`);
        },

        /**
         * Rotate API key
         */
        rotate: async (apiKeyId: string, options?: any): Promise<any> => {
          const response = await this.axios.post(`/users/me/api-keys/${apiKeyId}/rotate`, options || {});
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

  /**
   * Rule management methods
   */
  get rules() {
    return {
      /**
       * Download a rule bundle
       */
      downloadBundle: async (bundleName: string) => {
        return await this.ruleManager.downloadBundle(bundleName);
      },

      /**
       * Scan codebase with local rules
       */
      scanCodebase: async (path: string, bundleName: string = 'llm-security', useBinary?: boolean) => {
        return await this.scanner.scanCodebase(path, bundleName, useBinary);
      },

      /**
       * Scan codebase using scanner binary (if available)
       */
      scanWithBinary: async (path: string, bundleName: string = 'llm-security') => {
        return await this.scanner.scanCodebase(path, bundleName, true);
      },

      /**
       * List available rule bundles
       */
      listBundles: () => {
        return this.ruleManager.listBundles();
      },
    };
  }

  /**
   * Rule management API operations
   */
  get ruleManagement() {
    return {
      /**
       * List available rule bundles from API
       */
      listBundles: async (options?: {
        category?: string;
        officialOnly?: boolean;
        page?: number;
        perPage?: number;
      }): Promise<any> => {
        const params: any = {};
        if (options?.category) params.category = options.category;
        if (options?.officialOnly) params.official_only = options.officialOnly;
        if (options?.page) params.page = options.page;
        if (options?.perPage) params.per_page = options.perPage;

        const response = await this.axios.get('/rules/bundles', { params });
        return response.data;
      },

      /**
       * Get rules from a specific bundle
       */
      getBundleRules: async (bundleId: string): Promise<any> => {
        const response = await this.axios.get(`/rules/bundles/${bundleId}/rules`);
        return response.data;
      },

      /**
       * Install a rule bundle
       */
      installBundle: async (bundleId: string, organizationId?: string): Promise<any> => {
        const data: any = {};
        if (organizationId) data.organization_id = organizationId;

        const response = await this.axios.post(`/rules/bundles/${bundleId}/install`, data);
        return response.data;
      },

      /**
       * Uninstall a rule bundle
       */
      uninstallBundle: async (bundleId: string): Promise<any> => {
        const response = await this.axios.delete(`/rules/bundles/${bundleId}/install`);
        return response.data;
      },

      /**
       * Validate rule syntax
       */
      validateRules: async (rules: any[]): Promise<any> => {
        const response = await this.axios.post('/rules/validate', { rules });
        return response.data;
      },

      /**
       * Check for bundle updates
       */
      checkUpdates: async (bundleIds?: string[]): Promise<any> => {
        const params: any = {};
        if (bundleIds) params.bundle_ids = bundleIds.join(',');

        const response = await this.axios.get('/rules/updates', { params });
        return response.data;
      },
    };
  }

  /**
   * Device authentication operations
   */
  get deviceAuth() {
    return {
      /**
       * Create device code for authentication
       */
      createDeviceCode: async (options?: {
        clientId?: string;
        clientName?: string;
      }): Promise<any> => {
        const data: any = {};
        if (options?.clientId) data.client_id = options.clientId;
        if (options?.clientName) data.client_name = options.clientName || 'Tavo SDK';

        const response = await this.axios.post('/device/code', data);
        return response.data;
      },

      /**
       * Poll for device token
       */
      pollDeviceToken: async (deviceCode: string): Promise<any> => {
        const response = await this.axios.post('/device/token', {
          device_code: deviceCode,
        });
        return response.data;
      },
    };
  }

  /**
   * Session authentication operations
   */
  get sessionAuth() {
    return {
      /**
       * Create session token
       */
      createSessionToken: async (description?: string): Promise<any> => {
        const response = await this.axios.post('/auth/session/create', {
          description: description || 'SDK Session',
        });
        return response.data;
      },

      /**
       * List session tokens
       */
      listSessionTokens: async (): Promise<any> => {
        const response = await this.axios.get('/auth/session/list');
        return response.data;
      },

      /**
       * Delete session token
       */
      deleteSessionToken: async (tokenId: string): Promise<any> => {
        const response = await this.axios.delete(`/auth/session/${tokenId}`);
        return response.data;
      },

      /**
       * Delete all session tokens
       */
      deleteAllSessionTokens: async (): Promise<any> => {
        const response = await this.axios.delete('/auth/session/');
        return response.data;
      },

      /**
       * Validate session token
       */
      validateSessionToken: async (token: string): Promise<any> => {
        const response = await this.axios.post('/auth/session/validate', {
          token,
        });
        return response.data;
      },

      /**
       * Authenticate with session token
       */
      authenticateWithSessionToken: async (token: string): Promise<any> => {
        const response = await this.axios.post('/auth/session/authenticate', {
          token,
        });
        return response.data;
      },
    };
  }

  /**
   * WebSocket operations
   */
  get websocket() {
    return {
      /**
       * Connect to scan progress updates WebSocket
       */
      connectToScan: (
        scanId: string,
        onMessage: (message: ScanUpdateMessage) => void,
        onError?: (error: Event) => void,
        onClose?: (event: Event) => void
      ): Promise<string> => {
        return this.connectWebSocket(
          `ws/scan/${scanId}`,
          'scan',
          scanId,
          onMessage,
          onError,
          onClose
        );
      },

      /**
       * Connect to notifications WebSocket
       */
      connectToNotifications: (
        onMessage: (message: NotificationMessage) => void,
        onError?: (error: Event) => void,
        onClose?: (event: Event) => void
      ): Promise<string> => {
        return this.connectWebSocket(
          'ws/notifications',
          'notifications',
          'notifications',
          onMessage,
          onError,
          onClose
        );
      },

      /**
       * Connect to general broadcasts WebSocket
       */
      connectToGeneral: (
        onMessage: (message: GeneralMessage) => void,
        onError?: (error: Event) => void,
        onClose?: (event: Event) => void
      ): Promise<string> => {
        return this.connectWebSocket(
          'ws/general',
          'general',
          'general',
          onMessage,
          onError,
          onClose
        );
      },

      /**
       * Disconnect from a WebSocket connection
       */
      disconnect: (connectionId: string): void => {
        const connection = this.websocketConnections.get(connectionId);
        if (connection) {
          this.cleanupConnection(connection);
          this.websocketConnections.delete(connectionId);
        }
      },

      /**
       * Disconnect from all WebSocket connections
       */
      disconnectAll: (): void => {
        for (const connection of this.websocketConnections.values()) {
          this.cleanupConnection(connection);
        }
        this.websocketConnections.clear();
      },

      /**
       * Send a message to a WebSocket connection
       */
      sendMessage: (connectionId: string, message: any): boolean => {
        const connection = this.websocketConnections.get(connectionId);
        if (connection?.isConnected) {
          try {
            connection.websocket.send(JSON.stringify(message));
            return true;
          } catch (error) {
            console.error('Failed to send WebSocket message:', error);
            return false;
          }
        }
        return false;
      },
    };
  }

  /**
   * Internal WebSocket connection method
   */
  private async connectWebSocket<T>(
    endpoint: string,
    type: string,
    connectionKey: string,
    onMessage: (message: T) => void,
    onError?: (error: Event) => void,
    onClose?: (event: Event) => void
  ): Promise<string> {
    const connectionId = `${type}_${connectionKey}_${Date.now()}`;

    // Build WebSocket URL with authentication
    const wsUrl = new URL(this.config.baseURL);
    wsUrl.protocol = wsUrl.protocol === 'https:' ? 'wss:' : 'ws:';
    wsUrl.pathname = `/${endpoint}`;

    // Add authentication token as query parameter
    const authToken = this.config.jwtToken || this.config.sessionToken || this.config.apiKey;
    if (authToken) {
      wsUrl.searchParams.set('token', authToken);
    }

    // Generate client ID
    const clientId = `client_${Date.now()}_${Math.random().toString(36).substring(2, 11)}`;
    wsUrl.searchParams.set('client_id', clientId);

    const websocket = new WebSocket(wsUrl.toString());

    const connection: WebSocketConnection = {
      websocket,
      clientId,
      reconnectAttempts: 0,
      isConnected: false,
    };

    websocket.onopen = () => {
      connection.isConnected = true;
      connection.reconnectAttempts = 0;

      // Start heartbeat
      this.startHeartbeat(connection);

      console.log(`WebSocket connected to ${endpoint}`);
    };

    websocket.onmessage = (event) => {
      try {
        const message = JSON.parse(event.data);
        onMessage(message);
      } catch (error) {
        console.error('Failed to parse WebSocket message:', error);
      }
    };

    websocket.onerror = (error) => {
      console.error(`WebSocket error for ${endpoint}:`, error);
      if (onError) {
        onError(error);
      }
    };

    websocket.onclose = (event) => {
      connection.isConnected = false;
      this.stopHeartbeat(connection);

      console.log(`WebSocket closed for ${endpoint}:`, event.code, event.reason);

      if (onClose) {
        onClose(event);
      }

      // Attempt reconnection if not a normal closure
      if (event.code !== 1000 && connection.reconnectAttempts < this.wsConfig.maxReconnectAttempts) {
        this.scheduleReconnect(connection, endpoint, type, connectionKey, onMessage, onError, onClose);
      }
    };

    this.websocketConnections.set(connectionId, connection);
    return connectionId;
  }

  /**
   * Start heartbeat for a WebSocket connection
   */
  private startHeartbeat(connection: WebSocketConnection): void {
    connection.heartbeatTimer = setInterval(() => {
      if (connection.isConnected) {
        try {
          connection.websocket.send(JSON.stringify({ type: 'ping' }));
        } catch (error) {
          console.error('Heartbeat failed:', error);
          this.cleanupConnection(connection);
        }
      }
    }, this.wsConfig.heartbeatInterval);
  }

  /**
   * Stop heartbeat for a WebSocket connection
   */
  private stopHeartbeat(connection: WebSocketConnection): void {
    if (connection.heartbeatTimer) {
      clearInterval(connection.heartbeatTimer);
      connection.heartbeatTimer = undefined;
    }
  }

  /**
   * Schedule reconnection for a WebSocket connection
   */
  private scheduleReconnect<T>(
    connection: WebSocketConnection,
    endpoint: string,
    type: string,
    connectionKey: string,
    onMessage: (message: T) => void,
    onError?: (error: Event) => void,
    onClose?: (event: Event) => void
  ): void {
    connection.reconnectAttempts++;

    connection.reconnectTimer = setTimeout(async () => {
      console.log(`Attempting to reconnect WebSocket (${connection.reconnectAttempts}/${this.wsConfig.maxReconnectAttempts})`);

      try {
        await this.connectWebSocket(
          endpoint,
          type,
          connectionKey,
          onMessage,
          onError,
          onClose
        );
      } catch (error) {
        console.error('Reconnection failed:', error);
      }
    }, this.wsConfig.reconnectInterval * connection.reconnectAttempts);
  }

  /**
   * Clean up a WebSocket connection
   */
  private cleanupConnection(connection: WebSocketConnection): void {
    this.stopHeartbeat(connection);

    if (connection.reconnectTimer) {
      clearTimeout(connection.reconnectTimer);
      connection.reconnectTimer = undefined;
    }

    if (connection.websocket.readyState === WebSocket.OPEN) {
      connection.websocket.close(1000, 'Client disconnecting');
    }

    connection.isConnected = false;
  }
}

// Default export
export default TavoClient;