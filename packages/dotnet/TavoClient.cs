using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Net.Http;
using System.Net.WebSockets;
using System.Text;
using System.Text.Json;
using System.Threading;
using System.Threading.Tasks;
using Microsoft.Extensions.Logging;
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

            // Make config accessible to nested classes
            Config = _config;
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
        /// Device operations (CLI tools and scanners)
        /// </summary>
        public DeviceOperations Device => new DeviceOperations(this);

        /// <summary>
        /// Scanner operations (rule/plugin discovery, heartbeats)
        /// </summary>
        public ScannerOperations Scanner => new ScannerOperations(this);

        /// <summary>
        /// Code submission operations (file/repo/code analysis)
        /// </summary>
        public CodeSubmissionOperations CodeSubmission => new CodeSubmissionOperations(this);

        /// <summary>
        /// WebSocket operations for real-time communication
        /// </summary>
        public WebSocketOperations WebSocket => new WebSocketOperations(this);

        /// <summary>
        /// Rule management operations
        /// </summary>
        public RuleManagementOperations RuleManagement => new RuleManagementOperations(this);

        /// <summary>
        /// Local scanner operations
        /// </summary>
        public LocalScannerOperations LocalScanner => new LocalScannerOperations();

        /// <summary>
        /// Plugin marketplace operations
        /// </summary>
        public PluginOperations Plugins => new PluginOperations(this);

        /// <summary>
        /// Public access to client configuration for nested operations
        /// </summary>
        public TavoConfig Config { get; private set; }

        /// <summary>
        /// Job operations (deprecated - use DeviceOperations, ScannerOperations, and CodeSubmissionOperations)
        /// </summary>
        [Obsolete("JobOperations.dashboard() is deprecated. Use DeviceOperations, ScannerOperations, and CodeSubmissionOperations for tooling-focused endpoints.")]
        public JobOperations Jobs => new JobOperations(this);

        /// <summary>
        /// Webhook operations (deprecated - use GitHub App webhook management)
        /// </summary>
        [Obsolete("WebhookOperations are deprecated. Use GitHub App webhook management for repository integrations.")]
        public WebhookOperations Webhooks => new WebhookOperations(this);

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

        /// <summary>
        /// Makes an HTTP request to the API with cancellation support
        /// </summary>
        internal async Task<T> MakeRequestAsync<T>(string method, string path, object data, CancellationToken cancellationToken)
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

            var response = await _httpClient.SendAsync(request, cancellationToken);
            response.EnsureSuccessStatusCode();

            var content = await response.Content.ReadAsStringAsync(cancellationToken);
            return JsonConvert.DeserializeObject<T>(content);
        }

        /// <summary>
        /// Makes an HTTP request to the API with cancellation support (untyped)
        /// </summary>
        internal async Task<Dictionary<string, object>> MakeRequestAsync(string method, string path, object data, CancellationToken cancellationToken)
        {
            return await MakeRequestAsync<Dictionary<string, object>>(method, path, data, cancellationToken);
        }

        /// <summary>
        /// Downloads a file from the API
        /// </summary>
        internal async Task<byte[]> DownloadFileAsync(string path, CancellationToken cancellationToken = default)
        {
            var request = new HttpRequestMessage
            {
                Method = HttpMethod.Get,
                RequestUri = new Uri(path, UriKind.Relative)
            };

            var response = await _httpClient.SendAsync(request, cancellationToken);
            response.EnsureSuccessStatusCode();

            return await response.Content.ReadAsByteArrayAsync(cancellationToken);
        }
    }

    /// <summary>
    /// Client configuration
    /// </summary>
    public class TavoConfig
    {
        public string? ApiKey { get; set; }
        public string? JwtToken { get; set; }
        public string? SessionToken { get; set; }
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
    /// Device operations for CLI tools and scanners
    /// </summary>
    public class DeviceOperations
    {
        private readonly TavoClient _client;

        internal DeviceOperations(TavoClient client)
        {
            _client = client;
        }

        /// <summary>
        /// Create device code for authentication
        /// </summary>
        public async Task<Dictionary<string, object>> CreateDeviceCodeAsync(string? clientId = null, string? clientName = null, CancellationToken cancellationToken = default)
        {
            var data = new Dictionary<string, object>();
            if (!string.IsNullOrEmpty(clientId)) data["client_id"] = clientId;
            if (!string.IsNullOrEmpty(clientName)) data["client_name"] = clientName;
            return await _client.MakeRequestAsync("POST", "/device/code", data, cancellationToken);
        }

        /// <summary>
        /// Create CLI-optimized device code for authentication
        /// </summary>
        public async Task<Dictionary<string, object>> CreateDeviceCodeForCliAsync(string? clientId = null, string? clientName = null, CancellationToken cancellationToken = default)
        {
            var data = new Dictionary<string, object>();
            data["client_name"] = clientName ?? "Tavo CLI";
            if (!string.IsNullOrEmpty(clientId)) data["client_id"] = clientId;
            return await _client.MakeRequestAsync("POST", "/device/code/cli", data, cancellationToken);
        }

        /// <summary>
        /// Poll for device token
        /// </summary>
        public async Task<Dictionary<string, object>> PollDeviceTokenAsync(string deviceCode, CancellationToken cancellationToken = default)
        {
            var data = new Dictionary<string, object> { ["device_code"] = deviceCode };
            return await _client.MakeRequestAsync("POST", "/device/token", data, cancellationToken);
        }

        /// <summary>
        /// Get device code status (lightweight polling for CLI)
        /// </summary>
        public async Task<Dictionary<string, object>> GetDeviceCodeStatusAsync(string deviceCode, CancellationToken cancellationToken = default)
        {
            return await _client.MakeRequestAsync("GET", $"/device/code/{deviceCode}/status", null, cancellationToken);
        }

        /// <summary>
        /// Get usage warnings and limits for CLI tools
        /// </summary>
        public async Task<Dictionary<string, object>> GetUsageWarningsAsync(CancellationToken cancellationToken = default)
        {
            return await _client.MakeRequestAsync("GET", "/device/usage/warnings", null, cancellationToken);
        }

        /// <summary>
        /// Get current limits and quotas for CLI tools
        /// </summary>
        public async Task<Dictionary<string, object>> GetLimitsAsync(CancellationToken cancellationToken = default)
        {
            return await _client.MakeRequestAsync("GET", "/device/limits", null, cancellationToken);
        }
    }

    /// <summary>
    /// Scanner operations for CLI tools and scanners
    /// </summary>
    public class ScannerOperations
    {
        private readonly TavoClient _client;

        internal ScannerOperations(TavoClient client)
        {
            _client = client;
        }

        /// <summary>
        /// Discover rules optimized for scanner types
        /// </summary>
        public async Task<List<Dictionary<string, object>>> DiscoverRulesAsync(string? scannerType = null, string? language = null, string? category = null, CancellationToken cancellationToken = default)
        {
            var queryParams = new List<string>();
            if (!string.IsNullOrEmpty(scannerType)) queryParams.Add($"scanner_type={Uri.EscapeDataString(scannerType)}");
            if (!string.IsNullOrEmpty(language)) queryParams.Add($"language={Uri.EscapeDataString(language)}");
            if (!string.IsNullOrEmpty(category)) queryParams.Add($"category={Uri.EscapeDataString(category)}");

            var query = queryParams.Count > 0 ? "?" + string.Join("&", queryParams) : "";
            return await _client.MakeRequestAsync<List<Dictionary<string, object>>>($"GET", $"/scanner/rules{query}", null, cancellationToken);
        }

        /// <summary>
        /// Get rules for a specific bundle
        /// </summary>
        public async Task<List<Dictionary<string, object>>> GetBundleRulesAsync(string bundleId, CancellationToken cancellationToken = default)
        {
            return await _client.MakeRequestAsync<List<Dictionary<string, object>>>("GET", $"/scanner/bundles/{bundleId}/rules", null, cancellationToken);
        }

        /// <summary>
        /// Track bundle usage for analytics
        /// </summary>
        public async Task<Dictionary<string, object>> TrackBundleUsageAsync(string bundleId, Dictionary<string, object>? usageData = null, CancellationToken cancellationToken = default)
        {
            return await _client.MakeRequestAsync("POST", $"/scanner/bundles/{bundleId}/usage", usageData ?? new Dictionary<string, object>(), cancellationToken);
        }

        /// <summary>
        /// Discover plugins for scanners
        /// </summary>
        public async Task<List<Dictionary<string, object>>> DiscoverPluginsAsync(string? scannerType = null, string? language = null, string? category = null, CancellationToken cancellationToken = default)
        {
            var queryParams = new List<string>();
            if (!string.IsNullOrEmpty(scannerType)) queryParams.Add($"scanner_type={Uri.EscapeDataString(scannerType)}");
            if (!string.IsNullOrEmpty(language)) queryParams.Add($"language={Uri.EscapeDataString(language)}");
            if (!string.IsNullOrEmpty(category)) queryParams.Add($"category={Uri.EscapeDataString(category)}");

            var query = queryParams.Count > 0 ? "?" + string.Join("&", queryParams) : "";
            return await _client.MakeRequestAsync<List<Dictionary<string, object>>>($"GET", $"/scanner/plugins{query}", null, cancellationToken);
        }

        /// <summary>
        /// Get configuration for a specific plugin
        /// </summary>
        public async Task<Dictionary<string, object>> GetPluginConfigAsync(string pluginId, CancellationToken cancellationToken = default)
        {
            return await _client.MakeRequestAsync("GET", $"/scanner/plugins/{pluginId}/config", null, cancellationToken);
        }

        /// <summary>
        /// Get recommendations for rules and plugins
        /// </summary>
        public async Task<Dictionary<string, object>> GetRecommendationsAsync(string? language = null, string? scannerType = null, List<string>? currentRules = null, List<string>? currentPlugins = null, CancellationToken cancellationToken = default)
        {
            var data = new Dictionary<string, object>();
            if (!string.IsNullOrEmpty(language)) data["language"] = language;
            if (!string.IsNullOrEmpty(scannerType)) data["scanner_type"] = scannerType;
            if (currentRules != null) data["current_rules"] = currentRules;
            if (currentPlugins != null) data["current_plugins"] = currentPlugins;

            return await _client.MakeRequestAsync("POST", "/scanner/recommendations", data, cancellationToken);
        }

        /// <summary>
        /// Send scanner heartbeat for tracking and analytics
        /// </summary>
        public async Task<Dictionary<string, object>> SendHeartbeatAsync(HeartbeatData heartbeatData, CancellationToken cancellationToken = default)
        {
            var data = new Dictionary<string, object>
            {
                ["scanner_version"] = heartbeatData.ScannerVersion,
                ["scanner_type"] = heartbeatData.ScannerType,
                ["active_rules"] = heartbeatData.ActiveRules,
                ["active_plugins"] = heartbeatData.ActivePlugins,
                ["system_info"] = heartbeatData.SystemInfo,
                ["scan_count"] = heartbeatData.ScanCount
            };

            return await _client.MakeRequestAsync("POST", "/scanner/heartbeat", data, cancellationToken);
        }

        /// <summary>
        /// Heartbeat data structure
        /// </summary>
        public class HeartbeatData
        {
            public string? ScannerVersion { get; set; }
            public string? ScannerType { get; set; }
            public List<string> ActiveRules { get; set; } = new();
            public List<string> ActivePlugins { get; set; } = new();
            public Dictionary<string, object> SystemInfo { get; set; } = new();
            public long? ScanCount { get; set; }
        }
    }

    /// <summary>
    /// Code submission operations for CLI tools and scanners
    /// </summary>
    public class CodeSubmissionOperations
    {
        private readonly TavoClient _client;

        internal CodeSubmissionOperations(TavoClient client)
        {
            _client = client;
        }

        /// <summary>
        /// Submit code files directly for scanning
        /// </summary>
        public async Task<Dictionary<string, object>> SubmitCodeAsync(List<FileInfo> files, string? repositoryName = null, string? branch = null, string? commitSha = null, Dictionary<string, object>? scanConfig = null, CancellationToken cancellationToken = default)
        {
            var data = new Dictionary<string, object>();
            data["files"] = files.Select(f => new Dictionary<string, object>
            {
                ["filename"] = f.Filename,
                ["content"] = f.Content,
                ["language"] = f.Language
            }).ToList();

            if (!string.IsNullOrEmpty(repositoryName)) data["repository_name"] = repositoryName;
            if (!string.IsNullOrEmpty(branch)) data["branch"] = branch;
            if (!string.IsNullOrEmpty(commitSha)) data["commit_sha"] = commitSha;
            if (scanConfig != null) data["scan_config"] = scanConfig;

            return await _client.MakeRequestAsync("POST", "/code/submit", data, cancellationToken);
        }

        /// <summary>
        /// Submit repository for scanning
        /// </summary>
        public async Task<Dictionary<string, object>> SubmitRepositoryAsync(string repositoryUrl, RepositorySnapshot snapshot, string? branch = null, string? commitSha = null, Dictionary<string, object>? scanConfig = null, CancellationToken cancellationToken = default)
        {
            var data = new Dictionary<string, object>
            {
                ["repository_url"] = repositoryUrl,
                ["snapshot_data"] = new Dictionary<string, object>
                {
                    ["url"] = snapshot.Url,
                    ["branch"] = snapshot.Branch,
                    ["commit_sha"] = snapshot.CommitSha,
                    ["files"] = snapshot.Files.Select(f => new Dictionary<string, object>
                    {
                        ["filename"] = f.Filename,
                        ["content"] = f.Content,
                        ["language"] = f.Language
                    }).ToList()
                }
            };

            if (!string.IsNullOrEmpty(branch)) data["branch"] = branch;
            if (!string.IsNullOrEmpty(commitSha)) data["commit_sha"] = commitSha;
            if (scanConfig != null) data["scan_config"] = scanConfig;

            return await _client.MakeRequestAsync("POST", "/code/submit/repository", data, cancellationToken);
        }

        /// <summary>
        /// Submit code for targeted analysis
        /// </summary>
        public async Task<Dictionary<string, object>> SubmitAnalysisAsync(string codeContent, AnalysisContext analysisContext, CancellationToken cancellationToken = default)
        {
            var data = new Dictionary<string, object>
            {
                ["code_content"] = codeContent,
                ["language"] = analysisContext.Language,
                ["analysis_type"] = analysisContext.AnalysisType,
                ["rules"] = analysisContext.Rules,
                ["plugins"] = analysisContext.Plugins,
                ["context"] = analysisContext.Context
            };

            return await _client.MakeRequestAsync("POST", "/code/analyze", data, cancellationToken);
        }

        /// <summary>
        /// Get scan status (CLI-optimized)
        /// </summary>
        public async Task<Dictionary<string, object>> GetScanStatusAsync(string scanId, CancellationToken cancellationToken = default)
        {
            return await _client.MakeRequestAsync("GET", $"/code/scans/{scanId}/status", null, cancellationToken);
        }

        /// <summary>
        /// Get scan results summary (CLI-optimized)
        /// </summary>
        public async Task<Dictionary<string, object>> GetScanResultsAsync(string scanId, CancellationToken cancellationToken = default)
        {
            return await _client.MakeRequestAsync("GET", $"/code/scans/{scanId}/results/summary", null, cancellationToken);
        }

        /// <summary>
        /// File information for code submission
        /// </summary>
        public class FileInfo
        {
            public string? Filename { get; set; }
            public string? Content { get; set; }
            public string? Language { get; set; }
        }

        /// <summary>
        /// Repository snapshot data
        /// </summary>
        public class RepositorySnapshot
        {
            public string? Url { get; set; }
            public string? Branch { get; set; }
            public string? CommitSha { get; set; }
            public List<FileInfo> Files { get; set; } = new();
        }

        /// <summary>
        /// Analysis context
        /// </summary>
        public class AnalysisContext
        {
            public string? Language { get; set; }
            public string? AnalysisType { get; set; }
            public List<string> Rules { get; set; } = new();
            public List<string> Plugins { get; set; } = new();
            public Dictionary<string, object> Context { get; set; } = new();
        }
    }

    /// <summary>
    /// WebSocket operations for real-time communication
    /// </summary>
    public class WebSocketOperations
    {
        private readonly TavoClient _client;

        internal WebSocketOperations(TavoClient client)
        {
            _client = client;
        }

        /// <summary>
        /// WebSocket configuration
        /// </summary>
        public class WebSocketConfig
        {
            public TimeSpan ReconnectInterval { get; set; } = TimeSpan.FromSeconds(5);
            public int MaxReconnectAttempts { get; set; } = 10;
            public TimeSpan PingInterval { get; set; } = TimeSpan.FromSeconds(30);
            public TimeSpan ReadTimeout { get; set; } = TimeSpan.FromSeconds(60);
            public TimeSpan WriteTimeout { get; set; } = TimeSpan.FromSeconds(10);
        }

        /// <summary>
        /// WebSocket connection for real-time communication
        /// </summary>
        public class WebSocketConnection : IDisposable
        {
            private readonly ClientWebSocket _webSocket;
            private readonly WebSocketConfig _config;
            private readonly TavoClient _client;
            private readonly string _uri;
            private readonly Action<string> _messageHandler;
            private readonly Action<Exception> _errorHandler;
            private readonly Action _connectHandler;
            private readonly Action _disconnectHandler;
            private readonly CancellationTokenSource _cts;
            private Task _receiveTask;
            private Task _pingTask;
            private bool _isConnected;

            public WebSocketConnection(
                string uri,
                WebSocketConfig config,
                TavoClient client,
                Action<string>? messageHandler,
                Action<Exception>? errorHandler,
                Action? connectHandler,
                Action? disconnectHandler)
            {
                _webSocket = new ClientWebSocket();
                _config = config;
                _client = client;
                _uri = uri;
                _messageHandler = messageHandler;
                _errorHandler = errorHandler;
                _connectHandler = connectHandler;
                _disconnectHandler = disconnectHandler;
                _cts = new CancellationTokenSource();
                _isConnected = false;

                // Add authentication headers
                if (!string.IsNullOrEmpty(_client.Config.ApiKey))
                {
                    _webSocket.Options.SetRequestHeader("X-API-Key", _client.Config.ApiKey);
                }
                if (!string.IsNullOrEmpty(_client.Config.JwtToken))
                {
                    _webSocket.Options.SetRequestHeader("Authorization", $"Bearer {_client.Config.JwtToken}");
                }
                if (!string.IsNullOrEmpty(_client.Config.SessionToken))
                {
                    _webSocket.Options.SetRequestHeader("X-Session-Token", _client.Config.SessionToken);
                }
            }

            /// <summary>
            /// Connect to the WebSocket
            /// </summary>
            public async Task ConnectAsync()
            {
                try
                {
                    await _webSocket.ConnectAsync(new Uri(_uri), _cts.Token);
                    _isConnected = true;

                    // Start receive and ping tasks
                    _receiveTask = ReceiveMessagesAsync();
                    _pingTask = PingAsync();

                    _connectHandler?.Invoke();
                }
                catch (Exception ex)
                {
                    _errorHandler?.Invoke(ex);
                    throw;
                }
            }

            /// <summary>
            /// Disconnect from the WebSocket
            /// </summary>
            public async Task DisconnectAsync()
            {
                _cts.Cancel();

                if (_webSocket.State == WebSocketState.Open)
                {
                    await _webSocket.CloseAsync(WebSocketCloseStatus.NormalClosure, "Client disconnecting", CancellationToken.None);
                }

                _isConnected = false;
                _disconnectHandler?.Invoke();
            }

            /// <summary>
            /// Send a message
            /// </summary>
            public async Task SendMessageAsync(string messageType, object data)
            {
                if (!_isConnected) throw new InvalidOperationException("Not connected");

                var message = new Dictionary<string, object>
                {
                    ["type"] = messageType,
                    ["data"] = data,
                    ["timestamp"] = DateTimeOffset.UtcNow.ToUnixTimeSeconds()
                };

                var json = JsonConvert.SerializeObject(message);
                var buffer = Encoding.UTF8.GetBytes(json);

                await _webSocket.SendAsync(new ArraySegment<byte>(buffer), WebSocketMessageType.Text, true, _cts.Token);
            }

            /// <summary>
            /// Check if connected
            /// </summary>
            public bool IsConnected => _isConnected;

            private async Task ReceiveMessagesAsync()
            {
                var buffer = new byte[8192];

                try
                {
                    while (!_cts.Token.IsCancellationRequested && _isConnected)
                    {
                        var result = await _webSocket.ReceiveAsync(new ArraySegment<byte>(buffer), _cts.Token);

                        if (result.MessageType == WebSocketMessageType.Text)
                        {
                            var message = Encoding.UTF8.GetString(buffer, 0, result.Count);
                            _messageHandler?.Invoke(message);
                        }
                        else if (result.MessageType == WebSocketMessageType.Close)
                        {
                            break;
                        }
                    }
                }
                catch (Exception ex)
                {
                    _errorHandler?.Invoke(ex);
                }
            }

            private async Task PingAsync()
            {
                try
                {
                    while (!_cts.Token.IsCancellationRequested && _isConnected)
                    {
                        await Task.Delay(_config.PingInterval, _cts.Token);
                        await _webSocket.SendAsync(new ArraySegment<byte>(new byte[0]), WebSocketMessageType.Binary, true, _cts.Token);
                    }
                }
                catch (OperationCanceledException)
                {
                    // Expected when cancelled
                }
                catch (Exception ex)
                {
                    _errorHandler?.Invoke(ex);
                }
            }

            public void Dispose()
            {
                _cts?.Dispose();
                _webSocket?.Dispose();
            }
        }

        /// <summary>
        /// Connect to real-time scan progress updates
        /// </summary>
        public async Task<WebSocketConnection> ConnectToScanProgressAsync(string scanId, WebSocketConfig? config = null, Action<string>? messageHandler = null, Action<Exception>? errorHandler = null, Action? connectHandler = null, Action? disconnectHandler = null)
        {
            config ??= new WebSocketConfig();
            var wsUrl = _client.Config.BaseUrl.Replace("http", "ws") + $"/api/v1/code/scans/{scanId}/progress";

            var connection = new WebSocketConnection(wsUrl, config, _client, messageHandler, errorHandler, connectHandler, disconnectHandler);
            await connection.ConnectAsync();
            return connection;
        }

        /// <summary>
        /// Connect to general real-time updates
        /// </summary>
        public async Task<WebSocketConnection> ConnectToGeneralUpdatesAsync(WebSocketConfig? config = null, Action<string>? messageHandler = null, Action<Exception>? errorHandler = null, Action? connectHandler = null, Action? disconnectHandler = null)
        {
            config ??= new WebSocketConfig();
            var wsUrl = _client.Config.BaseUrl.Replace("http", "ws") + "/api/v1/updates";

            var connection = new WebSocketConnection(wsUrl, config, _client, messageHandler, errorHandler, connectHandler, disconnectHandler);
            await connection.ConnectAsync();
            return connection;
        }
    }

    /// <summary>
    /// Job operations (deprecated)
    /// </summary>
    [Obsolete("JobOperations.dashboard() is deprecated. Use DeviceOperations, ScannerOperations, and CodeSubmissionOperations for tooling-focused endpoints.")]
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
        public async Task<Dictionary<string, object>> ListJobsAsync(Dictionary<string, object>? parameters = null)
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
    /// Webhook operations (deprecated)
    /// </summary>
    [Obsolete("WebhookOperations are deprecated. Use GitHub App webhook management for repository integrations.")]
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
    /// Rule management operations for rule bundles
    /// </summary>
    public class RuleManagementOperations
    {
        private readonly TavoClient _client;

        internal RuleManagementOperations(TavoClient client)
        {
            _client = client;
        }

        /// <summary>
        /// List available rule bundles
        /// </summary>
        public async Task<Dictionary<string, object>> ListBundlesAsync(string? category = null, bool officialOnly = false, int page = 1, int perPage = 50, CancellationToken cancellationToken = default)
        {
            var queryParams = new List<string>
            {
                $"page={page}",
                $"per_page={perPage}"
            };

            if (!string.IsNullOrEmpty(category))
                queryParams.Add($"category={Uri.EscapeDataString(category)}");
            if (officialOnly)
                queryParams.Add("official_only=true");

            var query = "?" + string.Join("&", queryParams);
            return await _client.MakeRequestAsync("GET", $"/rules/bundles{query}", null, cancellationToken);
        }

        /// <summary>
        /// Get rules from a specific bundle
        /// </summary>
        public async Task<Dictionary<string, object>> GetBundleRulesAsync(string bundleId, CancellationToken cancellationToken = default)
        {
            return await _client.MakeRequestAsync("GET", $"/rules/bundles/{bundleId}/rules", null, cancellationToken);
        }

        /// <summary>
        /// Install a rule bundle
        /// </summary>
        public async Task<Dictionary<string, object>> InstallBundleAsync(string bundleId, string? organizationId = null, CancellationToken cancellationToken = default)
        {
            var data = new Dictionary<string, object>();
            if (!string.IsNullOrEmpty(organizationId))
                data["organization_id"] = organizationId;

            return await _client.MakeRequestAsync("POST", $"/rules/bundles/{bundleId}/install", data, cancellationToken);
        }

        /// <summary>
        /// Uninstall a rule bundle
        /// </summary>
        public async Task<Dictionary<string, object>> UninstallBundleAsync(string bundleId, CancellationToken cancellationToken = default)
        {
            return await _client.MakeRequestAsync("DELETE", $"/rules/bundles/{bundleId}/install", null, cancellationToken);
        }

        /// <summary>
        /// Validate rule syntax
        /// </summary>
        public async Task<Dictionary<string, object>> ValidateRulesAsync(List<Dictionary<string, object>> rules, CancellationToken cancellationToken = default)
        {
            var data = new Dictionary<string, object> { ["rules"] = rules };
            return await _client.MakeRequestAsync("POST", "/rules/validate", data, cancellationToken);
        }

        /// <summary>
        /// Check for updates to installed rule bundles
        /// </summary>
        public async Task<Dictionary<string, object>> CheckBundleUpdatesAsync(List<string>? bundleIds = null, CancellationToken cancellationToken = default)
        {
            var queryParams = new List<string>();
            if (bundleIds != null && bundleIds.Count > 0)
            {
                queryParams.Add($"bundle_ids={Uri.EscapeDataString(string.Join(",", bundleIds))}");
            }

            var query = queryParams.Count > 0 ? "?" + string.Join("&", queryParams) : "";
            return await _client.MakeRequestAsync("GET", $"/rules/updates{query}", null, cancellationToken);
        }
    }

    /// <summary>
    /// Local scanner operations using scanner binaries
    /// </summary>
    public class LocalScannerOperations
    {
        private string? _scannerPath;

        internal LocalScannerOperations()
        {
            _scannerPath = FindScannerBinary();
        }

        /// <summary>
        /// Find the scanner binary in the SDK or system PATH
        /// </summary>
        private static string? FindScannerBinary()
        {
            // First, try to find it relative to the SDK installation
            var sdkDir = AppDomain.CurrentDomain.BaseDirectory;
            var scannerPath = Path.Combine(sdkDir, "..", "..", "..", "..", "scanner", "dist", "tavo-scanner");

            if (File.Exists(scannerPath))
                return scannerPath;

            // Try to find it in the workspace
            var currentDir = Directory.GetCurrentDirectory();
            var workspaceRoot = currentDir;
            while (workspaceRoot != null && !Directory.Exists(Path.Combine(workspaceRoot, ".git")))
            {
                workspaceRoot = Directory.GetParent(workspaceRoot)?.FullName;
            }

            if (workspaceRoot != null)
            {
                scannerPath = Path.Combine(workspaceRoot, "tavo-sdk", "packages", "scanner", "dist", "tavo-scanner");
                if (File.Exists(scannerPath))
                    return scannerPath;
            }

            // Fall back to system PATH
            return "tavo-scanner";
        }

        /// <summary>
        /// Scan a codebase using the local scanner binary
        /// </summary>
        public async Task<Dictionary<string, object>> ScanCodebaseAsync(string path, string bundle = "llm-security", string outputFormat = "json", CancellationToken cancellationToken = default)
        {
            if (_scannerPath == null)
            {
                throw new InvalidOperationException("Scanner binary not found. Please install the Tavo scanner.");
            }

            if (!File.Exists(path) && !Directory.Exists(path))
            {
                throw new ArgumentException($"Path not found: {path}");
            }

            var cmd = $"{_scannerPath} \"{path}\" --bundle {bundle} --format {outputFormat}";

            var result = await RunCommandAsync(cmd, cancellationToken: cancellationToken);

            if (result.ExitCode != 0 && result.ExitCode != 1)
            {
                var errorMsg = result.Error.Trim();
                if (string.IsNullOrEmpty(errorMsg))
                    errorMsg = "Unknown scanner error";
                throw new InvalidOperationException($"Scanner failed: {errorMsg}");
            }

            if (outputFormat == "json")
            {
                try
                {
                    return JsonConvert.DeserializeObject<Dictionary<string, object>>(result.Output) ?? new Dictionary<string, object>();
                }
                catch (Newtonsoft.Json.JsonException ex)
                {
                    throw new InvalidOperationException($"Failed to parse scanner output: {ex.Message}", ex);
                }
            }

            return new Dictionary<string, object>
            {
                ["output"] = result.Output,
                ["exit_code"] = result.ExitCode,
                ["passed"] = result.ExitCode == 0
            };
        }

        /// <summary>
        /// Scan a single file
        /// </summary>
        public async Task<Dictionary<string, object>> ScanFileAsync(string filePath, string bundle = "llm-security", CancellationToken cancellationToken = default)
        {
            return await ScanCodebaseAsync(filePath, bundle, cancellationToken: cancellationToken);
        }

        /// <summary>
        /// Scan a directory
        /// </summary>
        public async Task<Dictionary<string, object>> ScanDirectoryAsync(string dirPath, string bundle = "llm-security", CancellationToken cancellationToken = default)
        {
            return await ScanCodebaseAsync(dirPath, bundle, cancellationToken: cancellationToken);
        }

        private static async Task<CommandResult> RunCommandAsync(string command, CancellationToken cancellationToken = default)
        {
            var isWindows = Environment.OSVersion.Platform == PlatformID.Win32NT;
            var startInfo = new ProcessStartInfo
            {
                FileName = isWindows ? "cmd.exe" : "/bin/bash",
                Arguments = isWindows ? $"/c {command}" : $"-c \"{command}\"",
                RedirectStandardOutput = true,
                RedirectStandardError = true,
                UseShellExecute = false,
                CreateNoWindow = true
            };

            using var process = Process.Start(startInfo);
            if (process == null)
                throw new InvalidOperationException("Failed to start process");

            var outputTask = process.StandardOutput.ReadToEndAsync(cancellationToken);
            var errorTask = process.StandardError.ReadToEndAsync(cancellationToken);

            await process.WaitForExitAsync(cancellationToken);

            var output = await outputTask;
            var error = await errorTask;

            return new CommandResult
            {
                ExitCode = process.ExitCode,
                Output = output,
                Error = error
            };
        }

        private class CommandResult
        {
            public int ExitCode { get; set; }
            public string Output { get; set; } = "";
            public string Error { get; set; } = "";
        }
    }

    /// <summary>
    /// Plugin marketplace operations
    /// </summary>
    public class PluginOperations
    {
        private readonly TavoClient _client;

        internal PluginOperations(TavoClient client)
        {
            _client = client;
        }

        /// <summary>
        /// Browse plugin marketplace
        /// </summary>
        public async Task<Dictionary<string, object>> BrowseMarketplaceAsync(string? pluginType = null, string? category = null, string? pricingTier = null, string? search = null, int page = 1, int perPage = 20, CancellationToken cancellationToken = default)
        {
            var queryParams = new List<string>
            {
                $"page={page}",
                $"per_page={perPage}"
            };

            if (!string.IsNullOrEmpty(pluginType))
                queryParams.Add($"plugin_type={Uri.EscapeDataString(pluginType)}");
            if (!string.IsNullOrEmpty(category))
                queryParams.Add($"category={Uri.EscapeDataString(category)}");
            if (!string.IsNullOrEmpty(pricingTier))
                queryParams.Add($"pricing_tier={Uri.EscapeDataString(pricingTier)}");
            if (!string.IsNullOrEmpty(search))
                queryParams.Add($"search={Uri.EscapeDataString(search)}");

            var query = "?" + string.Join("&", queryParams);
            return await _client.MakeRequestAsync("GET", $"/plugins/marketplace{query}", null, cancellationToken);
        }

        /// <summary>
        /// Get plugin details
        /// </summary>
        public async Task<Dictionary<string, object>> GetPluginAsync(string pluginId, CancellationToken cancellationToken = default)
        {
            return await _client.MakeRequestAsync("GET", $"/plugins/{pluginId}", null, cancellationToken);
        }

        /// <summary>
        /// Install a plugin
        /// </summary>
        public async Task<Dictionary<string, object>> InstallPluginAsync(string pluginId, CancellationToken cancellationToken = default)
        {
            return await _client.MakeRequestAsync("POST", $"/plugins/{pluginId}/install", null, cancellationToken);
        }

        /// <summary>
        /// Download plugin package
        /// </summary>
        public async Task<byte[]> DownloadPluginAsync(string pluginId, CancellationToken cancellationToken = default)
        {
            return await _client.DownloadFileAsync($"/plugins/{pluginId}/download", cancellationToken);
        }

        /// <summary>
        /// List installed plugins
        /// </summary>
        public async Task<Dictionary<string, object>> ListInstalledAsync(CancellationToken cancellationToken = default)
        {
            return await _client.MakeRequestAsync("GET", "/plugins/installed", null, cancellationToken);
        }

        /// <summary>
        /// Execute a plugin (cloud execution)
        /// </summary>
        public async Task<Dictionary<string, object>> ExecutePluginAsync(string pluginId, Dictionary<string, object> executionData, CancellationToken cancellationToken = default)
        {
            return await _client.MakeRequestAsync("POST", $"/plugins/{pluginId}/execute", executionData, cancellationToken);
        }

        /// <summary>
        /// Create/publish a new plugin
        /// </summary>
        public async Task<Dictionary<string, object>> CreatePluginAsync(Dictionary<string, object> pluginData, CancellationToken cancellationToken = default)
        {
            return await _client.MakeRequestAsync("POST", "/plugins", pluginData, cancellationToken);
        }

        /// <summary>
        /// Update plugin metadata
        /// </summary>
        public async Task<Dictionary<string, object>> UpdatePluginAsync(string pluginId, Dictionary<string, object> pluginData, CancellationToken cancellationToken = default)
        {
            return await _client.MakeRequestAsync("PUT", $"/plugins/{pluginId}", pluginData, cancellationToken);
        }

        /// <summary>
        /// Delete a plugin
        /// </summary>
        public async Task DeletePluginAsync(string pluginId, CancellationToken cancellationToken = default)
        {
            await _client.MakeRequestAsync("DELETE", $"/plugins/{pluginId}", null, cancellationToken);
        }
    }
}
