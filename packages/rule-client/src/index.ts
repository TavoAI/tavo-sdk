/**
 * TavoAI Rule Registry API Client
 *
 * Provides programmatic access to the TavoAI Rule Registry for:
 * - Browsing and searching security rules
 * - Installing rule bundles
 * - Managing custom rules and bundles
 * - Accessing the security rule marketplace
 */

export { RuleRegistryClient } from './client';
export type * from './types';

// Re-export commonly used types
export type {
  Rule,
  RuleBundle,
  RuleFormat,
  RuleCategory,
  RuleSeverity,
  RuleSource,
  InstallBundleRequest,
  MarketplaceSearchRequest,
} from './types';
