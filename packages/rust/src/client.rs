//! Tavo API Client

use reqwest::{Client, header::HeaderMap};
use std::sync::Arc;

#[derive(Clone)]
pub struct TavoClient {
    client: Arc<Client>,
    pub device_auth: DeviceAuthClient,
    pub scans: ScansClient,
    pub scan_management: ScanManagementClient,
    pub scan_tools: ScanToolsClient,
    pub scan_rules: ScanRulesClient,
    pub scan_schedules: ScanSchedulesClient,
    pub scan_bulk_operations: ScanBulkOperationsClient,
    pub scanner_integration: ScannerIntegrationClient,
    pub ai_analysis: AiAnalysisClient,
    pub ai_analysis_core: AiAnalysisCoreClient,
    pub ai_bulk_operations: AiBulkOperationsClient,
    pub ai_performance_quality: AiPerformanceQualityClient,
    pub ai_results_export: AiResultsExportClient,
    pub ai_risk_compliance: AiRiskComplianceClient,
    pub registry: RegistryClient,
    pub plugin_execution: PluginExecutionClient,
    pub plugin_marketplace: PluginMarketplaceClient,
    pub rules: RulesClient,
    pub code_submission: CodeSubmissionClient,
    pub repositories: RepositoriesClient,
    pub repository_connections: RepositoryConnectionsClient,
    pub repository_providers: RepositoryProvidersClient,
    pub repository_webhooks: RepositoryWebhooksClient,
    pub jobs: JobsClient,
    pub health: HealthClient,
    pub websockets: WebsocketsClient,
}

impl TavoClient {
    /// Create a new Tavo API client
    ///
    /// # Arguments
    /// * `api_key` - API key for authentication (preferred)
    /// * `device_token` - Device token for authentication
    /// * `base_url` - Base URL for the API
    pub async fn new(
        api_key: Option<String>,
        device_token: Option<String>,
        base_url: Option<String>,
    ) -> Result<Self, Box<dyn std::error::Error>> {
        let base_url = base_url.unwrap_or_else(|| "https://api.tavo.ai".to_string());

        let mut headers = HeaderMap::new();
        headers.insert("User-Agent", "tavo-sdk-rust/0.1.0".parse()?);

        // Set authentication headers
        if let Some(key) = api_key {
            headers.insert("X-API-Key", key.parse()?);
        } else if let Some(token) = device_token {
            headers.insert("Authorization", format!("Bearer {}", token).parse()?);
        }

        let client = Client::builder()
            .default_headers(headers)
            .build()?;

        let client = Arc::new(client);

        Ok(Self {
            client: client.clone(),
            device_auth: DeviceAuthClient::new(client.clone()),
            scans: ScansClient::new(client.clone()),
            scan_management: ScanManagementClient::new(client.clone()),
            scan_tools: ScanToolsClient::new(client.clone()),
            scan_rules: ScanRulesClient::new(client.clone()),
            scan_schedules: ScanSchedulesClient::new(client.clone()),
            scan_bulk_operations: ScanBulkOperationsClient::new(client.clone()),
            scanner_integration: ScannerIntegrationClient::new(client.clone()),
            ai_analysis: AiAnalysisClient::new(client.clone()),
            ai_analysis_core: AiAnalysisCoreClient::new(client.clone()),
            ai_bulk_operations: AiBulkOperationsClient::new(client.clone()),
            ai_performance_quality: AiPerformanceQualityClient::new(client.clone()),
            ai_results_export: AiResultsExportClient::new(client.clone()),
            ai_risk_compliance: AiRiskComplianceClient::new(client.clone()),
            registry: RegistryClient::new(client.clone()),
            plugin_execution: PluginExecutionClient::new(client.clone()),
            plugin_marketplace: PluginMarketplaceClient::new(client.clone()),
            rules: RulesClient::new(client.clone()),
            code_submission: CodeSubmissionClient::new(client.clone()),
            repositories: RepositoriesClient::new(client.clone()),
            repository_connections: RepositoryConnectionsClient::new(client.clone()),
            repository_providers: RepositoryProvidersClient::new(client.clone()),
            repository_webhooks: RepositoryWebhooksClient::new(client.clone()),
            jobs: JobsClient::new(client.clone()),
            health: HealthClient::new(client.clone()),
            websockets: WebsocketsClient::new(client.clone()),
        })
    }

    /// Update API key for authentication
    pub fn set_api_key(&mut self, api_key: String) {
        // This would update the client's default headers
        // Implementation depends on reqwest's header management
    }

    /// Update device token for authentication
    pub fn set_device_token(&mut self, device_token: String) {
        // This would update the client's default headers
        // Implementation depends on reqwest's header management
    }
}
