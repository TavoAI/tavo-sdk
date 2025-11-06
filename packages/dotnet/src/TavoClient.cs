using System;
using System.Net.Http;

namespace TavoAI
{
    /// <summary>
    /// Main client for interacting with Tavo AI API
    /// </summary>
    public class TavoClient
    {
        private readonly HttpClient httpClient;

        /// <summary>
        /// API Key for authentication
        /// </summary>
        public string? ApiKey { get; set; }

        /// <summary>
        /// Device token for authentication
        /// </summary>
        public string? DeviceToken { get; set; }

        public DeviceAuthClient DeviceAuth { get; private set; }
        public ScansClient Scans { get; private set; }
        public ScanManagementClient ScanManagement { get; private set; }
        public ScanToolsClient ScanTools { get; private set; }
        public ScanRulesClient ScanRules { get; private set; }
        public ScanSchedulesClient ScanSchedules { get; private set; }
        public ScanBulkOperationsClient ScanBulkOperations { get; private set; }
        public ScannerIntegrationClient ScannerIntegration { get; private set; }
        public AiAnalysisClient AiAnalysis { get; private set; }
        public AiAnalysisCoreClient AiAnalysisCore { get; private set; }
        public AiBulkOperationsClient AiBulkOperations { get; private set; }
        public AiPerformanceQualityClient AiPerformanceQuality { get; private set; }
        public AiResultsExportClient AiResultsExport { get; private set; }
        public AiRiskComplianceClient AiRiskCompliance { get; private set; }
        public RegistryClient Registry { get; private set; }
        public PluginExecutionClient PluginExecution { get; private set; }
        public PluginMarketplaceClient PluginMarketplace { get; private set; }
        public RulesClient Rules { get; private set; }
        public CodeSubmissionClient CodeSubmission { get; private set; }
        public RepositoriesClient Repositories { get; private set; }
        public RepositoryConnectionsClient RepositoryConnections { get; private set; }
        public RepositoryProvidersClient RepositoryProviders { get; private set; }
        public RepositoryWebhooksClient RepositoryWebhooks { get; private set; }
        public JobsClient Jobs { get; private set; }
        public HealthClient Health { get; private set; }
        public WebsocketsClient Websockets { get; private set; }

        /// <summary>
        /// Create a new Tavo API client
        /// </summary>
        /// <param name="apiKey">API key for authentication (preferred)</param>
        /// <param name="deviceToken">Device token for authentication</param>
        /// <param name="baseUrl">Base URL for the API</param>
        public TavoClient(string? apiKey = null, string? deviceToken = null, string baseUrl = "https://api.tavo.ai")
        {
            this.ApiKey = apiKey;
            this.DeviceToken = deviceToken;

            this.httpClient = new HttpClient { BaseAddress = new Uri(baseUrl) };
            this.httpClient.DefaultRequestHeaders.Add("User-Agent", "tavo-sdk-dotnet/0.1.0");

            // Set authentication headers
            if (!string.IsNullOrEmpty(apiKey))
            {
                this.httpClient.DefaultRequestHeaders.Add("X-API-Key", apiKey);
            }
            else if (!string.IsNullOrEmpty(deviceToken))
            {
                this.httpClient.DefaultRequestHeaders.Add("Authorization", $"Bearer {deviceToken}");
            }

            this.DeviceAuth = new DeviceAuthClient(httpClient);
            this.Scans = new ScansClient(httpClient);
            this.ScanManagement = new ScanManagementClient(httpClient);
            this.ScanTools = new ScanToolsClient(httpClient);
            this.ScanRules = new ScanRulesClient(httpClient);
            this.ScanSchedules = new ScanSchedulesClient(httpClient);
            this.ScanBulkOperations = new ScanBulkOperationsClient(httpClient);
            this.ScannerIntegration = new ScannerIntegrationClient(httpClient);
            this.AiAnalysis = new AiAnalysisClient(httpClient);
            this.AiAnalysisCore = new AiAnalysisCoreClient(httpClient);
            this.AiBulkOperations = new AiBulkOperationsClient(httpClient);
            this.AiPerformanceQuality = new AiPerformanceQualityClient(httpClient);
            this.AiResultsExport = new AiResultsExportClient(httpClient);
            this.AiRiskCompliance = new AiRiskComplianceClient(httpClient);
            this.Registry = new RegistryClient(httpClient);
            this.PluginExecution = new PluginExecutionClient(httpClient);
            this.PluginMarketplace = new PluginMarketplaceClient(httpClient);
            this.Rules = new RulesClient(httpClient);
            this.CodeSubmission = new CodeSubmissionClient(httpClient);
            this.Repositories = new RepositoriesClient(httpClient);
            this.RepositoryConnections = new RepositoryConnectionsClient(httpClient);
            this.RepositoryProviders = new RepositoryProvidersClient(httpClient);
            this.RepositoryWebhooks = new RepositoryWebhooksClient(httpClient);
            this.Jobs = new JobsClient(httpClient);
            this.Health = new HealthClient(httpClient);
            this.Websockets = new WebsocketsClient(httpClient);
        }

        /// <summary>
        /// Update API key for authentication
        /// </summary>
        /// <param name="apiKey">New API key</param>
        public void SetApiKey(string apiKey)
        {
            this.ApiKey = apiKey;
            this.DeviceToken = null;

            // Remove old auth headers
            this.httpClient.DefaultRequestHeaders.Remove("Authorization");
            if (this.httpClient.DefaultRequestHeaders.Contains("X-API-Key"))
            {
                this.httpClient.DefaultRequestHeaders.Remove("X-API-Key");
            }

            this.httpClient.DefaultRequestHeaders.Add("X-API-Key", apiKey);
        }

        /// <summary>
        /// Update device token for authentication
        /// </summary>
        /// <param name="deviceToken">New device token</param>
        public void SetDeviceToken(string deviceToken)
        {
            this.DeviceToken = deviceToken;
            this.ApiKey = null;

            // Remove old auth headers
            if (this.httpClient.DefaultRequestHeaders.Contains("X-API-Key"))
            {
                this.httpClient.DefaultRequestHeaders.Remove("X-API-Key");
            }
            this.httpClient.DefaultRequestHeaders.Remove("Authorization");

            this.httpClient.DefaultRequestHeaders.Add("Authorization", $"Bearer {deviceToken}");
        }
    }
}
