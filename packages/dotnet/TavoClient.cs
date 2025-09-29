using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;
using Newtonsoft.Json;

namespace TavoAI
{
    /// <summary>
    /// Tavo AI SDK for .NET
    /// </summary>
    public class TavoClient
    {
        private readonly HttpClient _httpClient;
        private readonly TavoConfig _config;

        /// <summary>
        /// Initializes a new instance of the TavoClient
        /// </summary>
        /// <param name="apiKey">Your Tavo AI API key</param>
        /// <param name="baseUrl">Base URL for the API (optional)</param>
        public TavoClient(string apiKey, string baseUrl = null)
            : this(new TavoConfig { ApiKey = apiKey, BaseUrl = baseUrl ?? "https://api.tavoai.net" })
        {
        }

        /// <summary>
        /// Initializes a new instance of the TavoClient with configuration
        /// </summary>
        /// <param name="config">Client configuration</param>
        public TavoClient(TavoConfig config)
        {
            _config = config ?? throw new ArgumentNullException(nameof(config));
            _config.Validate();

            _httpClient = new HttpClient
            {
                BaseAddress = new Uri($"{_config.BaseUrl}/api/{_config.ApiVersion}")
            };

            // Set authentication headers
            if (!string.IsNullOrEmpty(_config.JwtToken))
            {
                _httpClient.DefaultRequestHeaders.Add("Authorization", $"Bearer {_config.JwtToken}");
            }
            else if (!string.IsNullOrEmpty(_config.SessionToken))
            {
                _httpClient.DefaultRequestHeaders.Add("X-Session-Token", _config.SessionToken);
            }
            else if (!string.IsNullOrEmpty(_config.ApiKey))
            {
                _httpClient.DefaultRequestHeaders.Add("X-API-Key", _config.ApiKey);
            }
        }

        /// <summary>
        /// Health check endpoint
        /// </summary>
        public async Task<Dictionary<string, object>> HealthCheckAsync()
        {
            using var client = new HttpClient();
            var response = await client.GetAsync($"{_config.BaseUrl}/");
            response.EnsureSuccessStatusCode();
            var content = await response.Content.ReadAsStringAsync();
            return JsonConvert.DeserializeObject<Dictionary<string, object>>(content);
        }

        /// <summary>
        /// User operations
        /// </summary>
        public UserOperations Users => new UserOperations(this);

        /// <summary>
        /// Report operations
        /// </summary>
        public ReportOperations Reports => new ReportOperations(this);

        /// <summary>
        /// Organization operations
        /// </summary>
        public OrganizationOperations Organizations => new OrganizationOperations(this);

        /// <summary>
        /// Job operations
        /// </summary>
        public JobOperations Jobs => new JobOperations(this);

        /// <summary>
        /// Scan operations
        /// </summary>
        public ScanOperations Scans => new ScanOperations(this);

        /// <summary>
        /// Webhook operations
        /// </summary>
        public WebhookOperations Webhooks => new WebhookOperations(this);

        /// <summary>
        /// AI analysis operations
        /// </summary>
        public AIAnalysisOperations AI => new AIAnalysisOperations(this);

        /// <summary>
        /// Billing operations
        /// </summary>
        public BillingOperations Billing => new BillingOperations(this);

        /// <summary>
        /// Authentication operations
        /// </summary>
        public AuthOperations Auth => new AuthOperations(this);

        /// <summary>
        /// Makes an HTTP request to the API
        /// </summary>
        internal async Task<T> MakeRequestAsync<T>(string method, string path, object data)
        {
            var request = new HttpRequestMessage
            {
                Method = new HttpMethod(method),
                RequestUri = new Uri(path, UriKind.Relative),
                Content = data != null ? new StringContent(
                    JsonConvert.SerializeObject(data),
                    Encoding.UTF8,
                    "application/json") : null
            };

            var response = await _httpClient.SendAsync(request);
            response.EnsureSuccessStatusCode();

            var content = await response.Content.ReadAsStringAsync();
            return JsonConvert.DeserializeObject<T>(content);
        }

        /// <summary>
        /// Makes an HTTP request to the API (untyped)
        /// </summary>
        internal async Task<Dictionary<string, object>> MakeRequestAsync(string method, string path, object data)
        {
            return await MakeRequestAsync<Dictionary<string, object>>(method, path, data);
        }
    }

    /// <summary>
    /// Result of a security scan
    /// </summary>
    public class ScanResult
    {
        public bool Success { get; set; }
        public List<Vulnerability> Vulnerabilities { get; set; } = new();
        public int TotalIssues { get; set; }
        public string ScanId { get; set; }
    }

    /// <summary>
    /// Security vulnerability
    /// </summary>
    public class Vulnerability
    {
        public string Id { get; set; }
        public string Title { get; set; }
        public string Description { get; set; }
        public string Severity { get; set; }
        public string Category { get; set; }
        public Location Location { get; set; }
    }

    /// <summary>
    /// Location of a vulnerability
    /// </summary>
    public class Location
    {
        public string File { get; set; }
        public int Line { get; set; }
        public int Column { get; set; }
    }

    /// <summary>
    /// Result of AI model analysis
    /// </summary>
    public class ModelAnalysisResult
    {
        public bool Safe { get; set; }
        public List<string> Risks { get; set; } = new();
        public Dictionary<string, object> Recommendations { get; set; } = new();
    }

    /// <summary>
    /// Client configuration
    /// </summary>
    public class TavoConfig
    {
        public string ApiKey { get; set; }
        public string JwtToken { get; set; }
        public string SessionToken { get; set; }
        public string BaseUrl { get; set; } = "https://api.tavoai.net";
        public string ApiVersion { get; set; } = "v1";
        public int Timeout { get; set; } = 30000;
        public int MaxRetries { get; set; } = 3;

        /// <summary>
        /// Validates the configuration
        /// </summary>
        public void Validate()
        {
            if (string.IsNullOrEmpty(ApiKey) && string.IsNullOrEmpty(JwtToken) && string.IsNullOrEmpty(SessionToken))
            {
                throw new ArgumentException("Either API key, JWT token, or session token must be provided");
            }
        }
    }

    /// <summary>
    /// User operations
    /// </summary>
    public class UserOperations
    {
        private readonly TavoClient _client;

        internal UserOperations(TavoClient client)
        {
            _client = client;
        }

        /// <summary>
        /// Get current user profile
        /// </summary>
        public async Task<Dictionary<string, object>> GetCurrentUserAsync()
        {
            return await _client.MakeRequestAsync("GET", "/users/me", null);
        }

        /// <summary>
        /// Update current user profile
        /// </summary>
        public async Task<Dictionary<string, object>> UpdateCurrentUserAsync(Dictionary<string, object> userData)
        {
            return await _client.MakeRequestAsync("PUT", "/users/me", userData);
        }

        /// <summary>
        /// List current user's API keys
        /// </summary>
        public async Task<Dictionary<string, object>> ListApiKeysAsync()
        {
            return await _client.MakeRequestAsync("GET", "/users/me/api-keys", null);
        }

        /// <summary>
        /// Create a new API key
        /// </summary>
        public async Task<Dictionary<string, object>> CreateApiKeyAsync(string name, Dictionary<string, object> additionalData = null)
        {
            var data = additionalData ?? new Dictionary<string, object>();
            data["name"] = name;
            return await _client.MakeRequestAsync("POST", "/users/me/api-keys", data);
        }

        /// <summary>
        /// Update an API key
        /// </summary>
        public async Task<Dictionary<string, object>> UpdateApiKeyAsync(string apiKeyId, Dictionary<string, object> updateData)
        {
            return await _client.MakeRequestAsync("PUT", $"/users/me/api-keys/{apiKeyId}", updateData);
        }

        /// <summary>
        /// Delete an API key
        /// </summary>
        public async Task DeleteApiKeyAsync(string apiKeyId)
        {
            await _client.MakeRequestAsync("DELETE", $"/users/me/api-keys/{apiKeyId}", null);
        }

        /// <summary>
        /// Rotate an API key
        /// </summary>
        public async Task<Dictionary<string, object>> RotateApiKeyAsync(string apiKeyId, Dictionary<string, object> additionalData = null)
        {
            return await _client.MakeRequestAsync("POST", $"/users/me/api-keys/{apiKeyId}/rotate", additionalData ?? new Dictionary<string, object>());
        }
    }

    /// <summary>
    /// Report operations
    /// </summary>
    public class ReportOperations
    {
        private readonly TavoClient _client;

        internal ReportOperations(TavoClient client)
        {
            _client = client;
        }

        /// <summary>
        /// Generate a report
        /// </summary>
        public async Task<Dictionary<string, object>> GenerateReportAsync(Dictionary<string, object> reportRequest)
        {
            return await _client.MakeRequestAsync("POST", "/reports/generate", reportRequest);
        }

        /// <summary>
        /// Get a report
        /// </summary>
        public async Task<Dictionary<string, object>> GetReportAsync(string reportId)
        {
            return await _client.MakeRequestAsync("GET", $"/reports/{reportId}", null);
        }

        /// <summary>
        /// List reports
        /// </summary>
        public async Task<Dictionary<string, object>> ListReportsAsync(Dictionary<string, object> parameters = null)
        {
            var query = "";
            if (parameters != null && parameters.Count > 0)
            {
                var queryParams = new List<string>();
                foreach (var param in parameters)
                {
                    queryParams.Add($"{param.Key}={param.Value}");
                }
                query = "?" + string.Join("&", queryParams);
            }
            return await _client.MakeRequestAsync("GET", $"/reports{query}", null);
        }

        /// <summary>
        /// Delete a report
        /// </summary>
        public async Task DeleteReportAsync(string reportId)
        {
            await _client.MakeRequestAsync("DELETE", $"/reports/{reportId}", null);
        }

        /// <summary>
        /// Get report summary statistics
        /// </summary>
        public async Task<Dictionary<string, object>> GetSummaryAsync()
        {
            return await _client.MakeRequestAsync("GET", "/reports/summary", null);
        }
    }

    /// <summary>
    /// Organization operations
    /// </summary>
    public class OrganizationOperations
    {
        private readonly TavoClient _client;

        internal OrganizationOperations(TavoClient client)
        {
            _client = client;
        }

        /// <summary>
        /// List organizations
        /// </summary>
        public async Task<Dictionary<string, object>> ListOrganizationsAsync()
        {
            return await _client.MakeRequestAsync("GET", "/organizations", null);
        }

        /// <summary>
        /// Create a new organization
        /// </summary>
        public async Task<Dictionary<string, object>> CreateOrganizationAsync(Dictionary<string, object> orgData)
        {
            return await _client.MakeRequestAsync("POST", "/organizations", orgData);
        }

        /// <summary>
        /// Get organization details
        /// </summary>
        public async Task<Dictionary<string, object>> GetOrganizationAsync(string orgId)
        {
            return await _client.MakeRequestAsync("GET", $"/organizations/{orgId}", null);
        }

        /// <summary>
        /// Update an organization
        /// </summary>
        public async Task<Dictionary<string, object>> UpdateOrganizationAsync(string orgId, Dictionary<string, object> orgData)
        {
            return await _client.MakeRequestAsync("PUT", $"/organizations/{orgId}", orgData);
        }

        /// <summary>
        /// Delete an organization
        /// </summary>
        public async Task DeleteOrganizationAsync(string orgId)
        {
            await _client.MakeRequestAsync("DELETE", $"/organizations/{orgId}", null);
        }
    }

    /// <summary>
    /// Job operations
    /// </summary>
    public class JobOperations
    {
        private readonly TavoClient _client;

        internal JobOperations(TavoClient client)
        {
            _client = client;
        }

        /// <summary>
        /// Get job status
        /// </summary>
        public async Task<Dictionary<string, object>> GetJobStatusAsync(string jobId)
        {
            return await _client.MakeRequestAsync("GET", $"/jobs/{jobId}", null);
        }

        /// <summary>
        /// List jobs
        /// </summary>
        public async Task<Dictionary<string, object>> ListJobsAsync(Dictionary<string, object> parameters = null)
        {
            var query = "";
            if (parameters != null && parameters.Count > 0)
            {
                var queryParams = new List<string>();
                foreach (var param in parameters)
                {
                    queryParams.Add($"{param.Key}={param.Value}");
                }
                query = "?" + string.Join("&", queryParams);
            }
            return await _client.MakeRequestAsync("GET", $"/jobs{query}", null);
        }

        /// <summary>
        /// Cancel a job
        /// </summary>
        public async Task<Dictionary<string, object>> CancelJobAsync(string jobId)
        {
            return await _client.MakeRequestAsync("POST", $"/jobs/{jobId}/cancel", null);
        }
    }

    /// <summary>
    /// Scan operations
    /// </summary>
    public class ScanOperations
    {
        private readonly TavoClient _client;

        internal ScanOperations(TavoClient client)
        {
            _client = client;
        }

        /// <summary>
        /// Create a new scan
        /// </summary>
        public async Task<Dictionary<string, object>> CreateScanAsync(Dictionary<string, object> scanRequest)
        {
            return await _client.MakeRequestAsync("POST", "/scans", scanRequest);
        }

        /// <summary>
        /// Get scan details
        /// </summary>
        public async Task<Dictionary<string, object>> GetScanAsync(string scanId)
        {
            return await _client.MakeRequestAsync("GET", $"/scans/{scanId}", null);
        }

        /// <summary>
        /// List scans
        /// </summary>
        public async Task<Dictionary<string, object>> ListScansAsync(Dictionary<string, object> parameters = null)
        {
            var query = "";
            if (parameters != null && parameters.Count > 0)
            {
                var queryParams = new List<string>();
                foreach (var param in parameters)
                {
                    queryParams.Add($"{param.Key}={param.Value}");
                }
                query = "?" + string.Join("&", queryParams);
            }
            return await _client.MakeRequestAsync("GET", $"/scans{query}", null);
        }

        /// <summary>
        /// Cancel a scan
        /// </summary>
        public async Task<Dictionary<string, object>> CancelScanAsync(string scanId)
        {
            return await _client.MakeRequestAsync("POST", $"/scans/{scanId}/cancel", null);
        }
    }

    /// <summary>
    /// Webhook operations
    /// </summary>
    public class WebhookOperations
    {
        private readonly TavoClient _client;

        internal WebhookOperations(TavoClient client)
        {
            _client = client;
        }

        /// <summary>
        /// Create a webhook
        /// </summary>
        public async Task<Dictionary<string, object>> CreateWebhookAsync(Dictionary<string, object> webhookData)
        {
            return await _client.MakeRequestAsync("POST", "/webhooks", webhookData);
        }

        /// <summary>
        /// List webhooks
        /// </summary>
        public async Task<Dictionary<string, object>> ListWebhooksAsync()
        {
            return await _client.MakeRequestAsync("GET", "/webhooks", null);
        }

        /// <summary>
        /// Get webhook details
        /// </summary>
        public async Task<Dictionary<string, object>> GetWebhookAsync(string webhookId)
        {
            return await _client.MakeRequestAsync("GET", $"/webhooks/{webhookId}", null);
        }

        /// <summary>
        /// Update a webhook
        /// </summary>
        public async Task<Dictionary<string, object>> UpdateWebhookAsync(string webhookId, Dictionary<string, object> webhookData)
        {
            return await _client.MakeRequestAsync("PUT", $"/webhooks/{webhookId}", webhookData);
        }

        /// <summary>
        /// Delete a webhook
        /// </summary>
        public async Task DeleteWebhookAsync(string webhookId)
        {
            await _client.MakeRequestAsync("DELETE", $"/webhooks/{webhookId}", null);
        }
    }

    /// <summary>
    /// AI analysis operations
    /// </summary>
    public class AIAnalysisOperations
    {
        private readonly TavoClient _client;

        internal AIAnalysisOperations(TavoClient client)
        {
            _client = client;
        }

        /// <summary>
        /// Analyze AI model
        /// </summary>
        public async Task<Dictionary<string, object>> AnalyzeModelAsync(Dictionary<string, object> modelConfig)
        {
            return await _client.MakeRequestAsync("POST", "/ai/analyze/model", modelConfig);
        }

        /// <summary>
        /// Analyze code with AI
        /// </summary>
        public async Task<Dictionary<string, object>> AnalyzeCodeAsync(Dictionary<string, object> codeAnalysisRequest)
        {
            return await _client.MakeRequestAsync("POST", "/ai/analyze/code", codeAnalysisRequest);
        }
    }

    /// <summary>
    /// Billing operations
    /// </summary>
    public class BillingOperations
    {
        private readonly TavoClient _client;

        internal BillingOperations(TavoClient client)
        {
            _client = client;
        }

        /// <summary>
        /// Get billing information
        /// </summary>
        public async Task<Dictionary<string, object>> GetBillingInfoAsync()
        {
            return await _client.MakeRequestAsync("GET", "/billing", null);
        }

        /// <summary>
        /// Get usage report
        /// </summary>
        public async Task<Dictionary<string, object>> GetUsageReportAsync(Dictionary<string, object> parameters = null)
        {
            var query = "";
            if (parameters != null && parameters.Count > 0)
            {
                var queryParams = new List<string>();
                foreach (var param in parameters)
                {
                    queryParams.Add($"{param.Key}={param.Value}");
                }
                query = "?" + string.Join("&", queryParams);
            }
            return await _client.MakeRequestAsync("GET", $"/billing/usage{query}", null);
        }
    }

    /// <summary>
    /// Authentication operations
    /// </summary>
    public class AuthOperations
    {
        private readonly TavoClient _client;

        internal AuthOperations(TavoClient client)
        {
            _client = client;
        }

        /// <summary>
        /// Login with credentials
        /// </summary>
        public async Task<Dictionary<string, object>> LoginAsync(string email, string password)
        {
            var credentials = new Dictionary<string, object>
            {
                ["email"] = email,
                ["password"] = password
            };
            return await _client.MakeRequestAsync("POST", "/auth/login", credentials);
        }

        /// <summary>
        /// Get current user info (when authenticated)
        /// </summary>
        public async Task<Dictionary<string, object>> GetCurrentUserAsync()
        {
            return await _client.MakeRequestAsync("GET", "/auth/me", null);
        }

        /// <summary>
        /// Logout
        /// </summary>
        public async Task<Dictionary<string, object>> LogoutAsync()
        {
            return await _client.MakeRequestAsync("POST", "/auth/logout", null);
        }
    }
}