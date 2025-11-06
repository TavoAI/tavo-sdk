/**
 * Tavo API Client
 */

import { AxiosInstance } from 'axios'
import { createHttpClient } from './utils'

import { Device_AuthClient } from './endpoints/device_auth'
import { ScansClient } from './endpoints/scans'
import { Scan_ManagementClient } from './endpoints/scan_management'
import { Scan_ToolsClient } from './endpoints/scan_tools'
import { Scan_RulesClient } from './endpoints/scan_rules'
import { Scan_SchedulesClient } from './endpoints/scan_schedules'
import { Scan_Bulk_OperationsClient } from './endpoints/scan_bulk_operations'
import { Scanner_IntegrationClient } from './endpoints/scanner_integration'
import { Ai_AnalysisClient } from './endpoints/ai_analysis'
import { Ai_Analysis_CoreClient } from './endpoints/ai_analysis_core'
import { Ai_Bulk_OperationsClient } from './endpoints/ai_bulk_operations'
import { Ai_Performance_QualityClient } from './endpoints/ai_performance_quality'
import { Ai_Results_ExportClient } from './endpoints/ai_results_export'
import { Ai_Risk_ComplianceClient } from './endpoints/ai_risk_compliance'
import { RegistryClient } from './endpoints/registry'
import { Plugin_ExecutionClient } from './endpoints/plugin_execution'
import { Plugin_MarketplaceClient } from './endpoints/plugin_marketplace'
import { RulesClient } from './endpoints/rules'
import { Code_SubmissionClient } from './endpoints/code_submission'
import { RepositoriesClient } from './endpoints/repositories'
import { Repository_ConnectionsClient } from './endpoints/repository_connections'
import { Repository_ProvidersClient } from './endpoints/repository_providers'
import { Repository_WebhooksClient } from './endpoints/repository_webhooks'
import { JobsClient } from './endpoints/jobs'
import { HealthClient } from './endpoints/health'
import { WebsocketsClient } from './endpoints/websockets'

export interface TavoClientConfig {
  /** API key for authentication (preferred for programmatic access) */
  apiKey?: string
  /** Device authentication token */
  deviceToken?: string
  /** Base URL for the API */
  baseURL?: string
  /** Request timeout in milliseconds */
  timeout?: number
}
