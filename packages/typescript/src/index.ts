/**
 * Tavo AI TypeScript SDK
 *
 * Official TypeScript SDK for the Tavo AI platform providing access to:
 * - REST API client with all endpoints
 * - Tavo scanner execution and configuration
 */

export { TavoScanner, ScannerConfig, ScanOptions, ScanResult } from './scanner';

// Export API client types
export * from './types';

// Export endpoint clients
export * from './endpoints/device-auth';
export * from './endpoints/scan-tools';
export * from './endpoints/scan-management';
export * from './endpoints/scan-rules';
export * from './endpoints/scan-schedules';
export * from './endpoints/scan-bulk-operations';
export * from './endpoints/scanner-integration';
export * from './endpoints/ai-analysis';
export * from './endpoints/ai-analysis-core';
export * from './endpoints/ai-bulk-operations';
export * from './endpoints/ai-performance-quality';
export * from './endpoints/ai-results-export';
export * from './endpoints/ai-risk-compliance';
export * from './endpoints/registry';
export * from './endpoints/plugin-execution';
export * from './endpoints/plugin-marketplace';
export * from './endpoints/rules';
export * from './endpoints/code-submission';
export * from './endpoints/repositories';
export * from './endpoints/repository-connections';
export * from './endpoints/repository-providers';
export * from './endpoints/repository-webhooks';
export * from './endpoints/jobs';
export * from './endpoints/health';

export const VERSION = '0.1.0';