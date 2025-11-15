/**
 * Rule Registry API Types
 * Auto-generated from Rule Registry OpenAPI spec
 */

export interface Rule {
  id: string;
  name: string;
  description?: string;
  format: RuleFormat;
  category: RuleCategory;
  severity: RuleSeverity;
  content: string;
  version: string;
  authorId: string;
  bundleId?: string;
  tags: string[];
  metadata: Record<string, any>;
  createdAt: string;
  updatedAt: string;
}

export interface RuleBundle {
  id: string;
  name: string;
  description?: string;
  rules: string[]; // Rule IDs
  version: string;
  authorId: string;
  tags: string[];
  metadata: Record<string, any>;
  createdAt: string;
  updatedAt: string;
}

export interface RuleVersion {
  id: string;
  ruleId: string;
  version: string;
  content: string;
  changelog?: string;
  createdAt: string;
}

export interface RuleSource {
  type: 'git' | 'gcs';
  url?: string; // Git URL
  bucket?: string; // GCS bucket
  path: string;
  access: 'public' | 'private';
  auth?: GitAuth | GCSAuth;
}

export interface GitAuth {
  type: 'oauth' | 'pat';
  token: string;
}

export interface GCSAuth {
  type: 'service_account';
  credentials: string; // JSON credentials
}

export type RuleFormat =
  | 'semgrep'
  | 'opa'
  | 'sigma'
  | 'yara'
  | 'clamav'
  | 'suricata'
  | 'falco'
  | 'zap';

export type RuleCategory =
  | 'sast'
  | 'dast'
  | 'network'
  | 'proxy'
  | 'compliance'
  | 'malware'
  | 'intrusion'
  | 'runtime';

export type RuleSeverity = 'info' | 'low' | 'medium' | 'high' | 'critical';

// API Request/Response types
export interface ListRulesRequest {
  category?: RuleCategory;
  format?: RuleFormat;
  severity?: RuleSeverity;
  authorId?: string;
  tags?: string[];
  search?: string;
  page?: number;
  limit?: number;
}

export interface ListRulesResponse {
  items: Rule[];
  total: number;
  page: number;
  limit: number;
  hasMore: boolean;
}

export interface ListBundlesRequest {
  tags?: string[];
  search?: string;
  page?: number;
  limit?: number;
}

export interface ListBundlesResponse {
  items: RuleBundle[];
  total: number;
  page: number;
  limit: number;
  hasMore: boolean;
}

export interface CreateRuleRequest {
  name: string;
  description?: string;
  format: RuleFormat;
  category: RuleCategory;
  severity: RuleSeverity;
  content: string;
  tags?: string[];
  metadata?: Record<string, any>;
}

export interface UpdateRuleRequest {
  name?: string;
  description?: string;
  content?: string;
  tags?: string[];
  metadata?: Record<string, any>;
}

export interface CreateBundleRequest {
  name: string;
  description?: string;
  ruleIds: string[];
  tags?: string[];
  metadata?: Record<string, any>;
}

export interface InstallBundleRequest {
  bundleId: string;
  source?: RuleSource;
  version?: string;
}

export interface InstallBundleResponse {
  bundle: RuleBundle;
  rules: Rule[];
  installedAt: string;
}

// Marketplace types
export interface MarketplaceItem {
  id: string;
  name: string;
  description?: string;
  type: 'rule' | 'bundle';
  author: string;
  version: string;
  downloads: number;
  rating: number;
  tags: string[];
  createdAt: string;
  updatedAt: string;
}

export interface MarketplaceSearchRequest {
  query?: string;
  type?: 'rule' | 'bundle';
  category?: RuleCategory;
  format?: RuleFormat;
  tags?: string[];
  sortBy?: 'downloads' | 'rating' | 'updated' | 'created';
  sortOrder?: 'asc' | 'desc';
  page?: number;
  limit?: number;
}

export interface MarketplaceSearchResponse {
  items: MarketplaceItem[];
  total: number;
  page: number;
  limit: number;
  hasMore: boolean;
}

// Error types
export interface APIError {
  code: string;
  message: string;
  details?: Record<string, any>;
}
