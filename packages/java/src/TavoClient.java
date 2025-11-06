package net.tavoai.sdk;

import okhttp3.OkHttpClient;
import okhttp3.Request;
import java.util.concurrent.CompletableFuture;

/**
 * Main client for interacting with Tavo AI API
 */
public class TavoClient {
    private final OkHttpClient httpClient;
    private final String baseUrl;

    // Authentication
    private String apiKey;
    private String deviceToken;

    private final DeviceAuthClient deviceAuth;
    private final ScansClient scans;
    private final ScanManagementClient scanManagement;
    private final ScanToolsClient scanTools;
    private final ScanRulesClient scanRules;
    private final ScanSchedulesClient scanSchedules;
    private final ScanBulkOperationsClient scanBulkOperations;
    private final ScannerIntegrationClient scannerIntegration;
    private final AiAnalysisClient aiAnalysis;
    private final AiAnalysisCoreClient aiAnalysisCore;
    private final AiBulkOperationsClient aiBulkOperations;
    private final AiPerformanceQualityClient aiPerformanceQuality;
    private final AiResultsExportClient aiResultsExport;
    private final AiRiskComplianceClient aiRiskCompliance;
    private final RegistryClient registry;
    private final PluginExecutionClient pluginExecution;
    private final PluginMarketplaceClient pluginMarketplace;
    private final RulesClient rules;
    private final CodeSubmissionClient codeSubmission;
    private final RepositoriesClient repositories;
    private final RepositoryConnectionsClient repositoryConnections;
    private final RepositoryProvidersClient repositoryProviders;
    private final RepositoryWebhooksClient repositoryWebhooks;
    private final JobsClient jobs;
    private final HealthClient health;
    private final WebsocketsClient websockets;

    /**
     * Create a new Tavo API client
     * @param apiKey API key for authentication (preferred)
     * @param deviceToken Device token for authentication
     * @param baseUrl Base URL for the API
     */
    public TavoClient(String apiKey, String deviceToken, String baseUrl) {
        this.apiKey = apiKey;
        this.deviceToken = deviceToken;
        this.baseUrl = baseUrl != null ? baseUrl : "https://api.tavo.ai";

        this.httpClient = new OkHttpClient.Builder()
            .addInterceptor(chain -> {
                Request.Builder requestBuilder = chain.request().newBuilder()
                    .addHeader("User-Agent", "tavo-sdk-java/0.1.0");

                // Set authentication headers
                if (apiKey != null && !apiKey.isEmpty()) {
                    requestBuilder.addHeader("X-API-Key", apiKey);
                } else if (deviceToken != null && !deviceToken.isEmpty()) {
                    requestBuilder.addHeader("Authorization", "Bearer " + deviceToken);
                }

                return chain.proceed(requestBuilder.build());
            })
            .build();

        this.deviceAuth = new DeviceAuthClient(httpClient);
        this.scans = new ScansClient(httpClient);
        this.scanManagement = new ScanManagementClient(httpClient);
        this.scanTools = new ScanToolsClient(httpClient);
        this.scanRules = new ScanRulesClient(httpClient);
        this.scanSchedules = new ScanSchedulesClient(httpClient);
        this.scanBulkOperations = new ScanBulkOperationsClient(httpClient);
        this.scannerIntegration = new ScannerIntegrationClient(httpClient);
        this.aiAnalysis = new AiAnalysisClient(httpClient);
        this.aiAnalysisCore = new AiAnalysisCoreClient(httpClient);
        this.aiBulkOperations = new AiBulkOperationsClient(httpClient);
        this.aiPerformanceQuality = new AiPerformanceQualityClient(httpClient);
        this.aiResultsExport = new AiResultsExportClient(httpClient);
        this.aiRiskCompliance = new AiRiskComplianceClient(httpClient);
        this.registry = new RegistryClient(httpClient);
        this.pluginExecution = new PluginExecutionClient(httpClient);
        this.pluginMarketplace = new PluginMarketplaceClient(httpClient);
        this.rules = new RulesClient(httpClient);
        this.codeSubmission = new CodeSubmissionClient(httpClient);
        this.repositories = new RepositoriesClient(httpClient);
        this.repositoryConnections = new RepositoryConnectionsClient(httpClient);
        this.repositoryProviders = new RepositoryProvidersClient(httpClient);
        this.repositoryWebhooks = new RepositoryWebhooksClient(httpClient);
        this.jobs = new JobsClient(httpClient);
        this.health = new HealthClient(httpClient);
        this.websockets = new WebsocketsClient(httpClient);
    }

    /**
     * Update API key for authentication
     * @param apiKey New API key
     */
    public void setApiKey(String apiKey) {
        this.apiKey = apiKey;
        this.deviceToken = null;
    }

    /**
     * Update device token for authentication
     * @param deviceToken New device token
     */
    public void setDeviceToken(String deviceToken) {
        this.deviceToken = deviceToken;
        this.apiKey = null;
    }

    // Getters for endpoint clients
    public DeviceAuthClient getDeviceAuth() { return deviceAuth; }
    public ScansClient getScans() { return scans; }
    public ScanManagementClient getScanManagement() { return scanManagement; }
    public ScanToolsClient getScanTools() { return scanTools; }
    public ScanRulesClient getScanRules() { return scanRules; }
    public ScanSchedulesClient getScanSchedules() { return scanSchedules; }
    public ScanBulkOperationsClient getScanBulkOperations() { return scanBulkOperations; }
    public ScannerIntegrationClient getScannerIntegration() { return scannerIntegration; }
    public AiAnalysisClient getAiAnalysis() { return aiAnalysis; }
    public AiAnalysisCoreClient getAiAnalysisCore() { return aiAnalysisCore; }
    public AiBulkOperationsClient getAiBulkOperations() { return aiBulkOperations; }
    public AiPerformanceQualityClient getAiPerformanceQuality() { return aiPerformanceQuality; }
    public AiResultsExportClient getAiResultsExport() { return aiResultsExport; }
    public AiRiskComplianceClient getAiRiskCompliance() { return aiRiskCompliance; }
    public RegistryClient getRegistry() { return registry; }
    public PluginExecutionClient getPluginExecution() { return pluginExecution; }
    public PluginMarketplaceClient getPluginMarketplace() { return pluginMarketplace; }
    public RulesClient getRules() { return rules; }
    public CodeSubmissionClient getCodeSubmission() { return codeSubmission; }
    public RepositoriesClient getRepositories() { return repositories; }
    public RepositoryConnectionsClient getRepositoryConnections() { return repositoryConnections; }
    public RepositoryProvidersClient getRepositoryProviders() { return repositoryProviders; }
    public RepositoryWebhooksClient getRepositoryWebhooks() { return repositoryWebhooks; }
    public JobsClient getJobs() { return jobs; }
    public HealthClient getHealth() { return health; }
    public WebsocketsClient getWebsockets() { return websockets; }
}
