using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Net.Http.Json;
using System.Threading.Tasks;

namespace TavoAI
{
    /// <summary>
    /// Client for scanner_integration endpoints
    /// </summary>
    public class ScannerIntegrationClient
    {
        private readonly HttpClient httpClient;

        /// <summary>
        /// Create a new scanner_integration client
        /// </summary>
        /// <param name="httpClient">HTTP client instance</param>
        public ScannerIntegrationClient(HttpClient httpClient)
        {
            this.httpClient = httpClient;
        }

        /// <summary>
        /// GET /rules/discover
        /// </summary>
                /// <param name="category">category parameter</param>
        /// <param name="language">language parameter</param>
        /// <param name="scanner_type">scanner_type parameter</param>
        /// <param name="limit">limit parameter</param>
        public async Task<object> getrulesdiscover(string? category = null, string? language = null, string? scanner_type = null, double? limit = null)
        {
                    var queryParams = new Dictionary<string, object?> { "category", category, "language", language, "scanner_type", scanner_type, "limit", limit };
                    var queryString = string.Join("&", queryParams.Where(p => p.Value != null).Select(p => $"{p.Key}={Uri.EscapeDataString(p.Value.ToString())}"));
                    var url = $"{formatted_path}" + (string.IsNullOrEmpty(queryString) ? "" : $"?{queryString}");
                    var content = null;
                    var response = await this.httpClient.GetAsync(url);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
        /// <summary>
        /// GET /rules/bundle/{bundle_id}/rules
        /// </summary>
                /// <param name="bundle_id">bundle_id parameter</param>
        /// <param name="severity">severity parameter</param>
        /// <param name="language">language parameter</param>
        /// <param name="limit">limit parameter</param>
        public async Task<object> getrulesbundlerules(string bundle_id, string? severity = null, string? language = null, double? limit = null)
        {
                    var queryParams = new Dictionary<string, object?> { "bundle_id", bundle_id, "severity", severity, "language", language, "limit", limit };
                    var queryString = string.Join("&", queryParams.Where(p => p.Value != null).Select(p => $"{p.Key}={Uri.EscapeDataString(p.Value.ToString())}"));
                    var url = $"{formatted_path}" + (string.IsNullOrEmpty(queryString) ? "" : $"?{queryString}");
                    var content = null;
                    var response = await this.httpClient.GetAsync(url);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
        /// <summary>
        /// POST /rules/bundle/{bundle_id}/use
        /// </summary>
                /// <param name="bundle_id">bundle_id parameter</param>
        /// <param name="scan_id">scan_id parameter</param>
        public async Task<object> postrulesbundleuse(string bundle_id, string? scan_id = null)
        {
                    var url = "/rules/bundle/{bundle_id}/use";
                    var content = JsonContent.Create(new { bundle_id = bundle_id, scan_id = scan_id });
                    var response = await this.httpClient.PostAsync(url, content);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
        /// <summary>
        /// GET /plugins/discover
        /// </summary>
                /// <param name="plugin_type">plugin_type parameter</param>
        /// <param name="language">language parameter</param>
        /// <param name="scanner_integration">scanner_integration parameter</param>
        /// <param name="limit">limit parameter</param>
        public async Task<object> getpluginsdiscover(string? plugin_type = null, string? language = null, bool? scanner_integration = null, double? limit = null)
        {
                    var queryParams = new Dictionary<string, object?> { "plugin_type", plugin_type, "language", language, "scanner_integration", scanner_integration, "limit", limit };
                    var queryString = string.Join("&", queryParams.Where(p => p.Value != null).Select(p => $"{p.Key}={Uri.EscapeDataString(p.Value.ToString())}"));
                    var url = $"{formatted_path}" + (string.IsNullOrEmpty(queryString) ? "" : $"?{queryString}");
                    var content = null;
                    var response = await this.httpClient.GetAsync(url);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
        /// <summary>
        /// GET /plugins/{plugin_id}/config
        /// </summary>
                /// <param name="plugin_id">plugin_id parameter</param>
        public async Task<object> getpluginsconfig(string plugin_id)
        {
                    var queryParams = new Dictionary<string, object?> { "plugin_id", plugin_id };
                    var queryString = string.Join("&", queryParams.Where(p => p.Value != null).Select(p => $"{p.Key}={Uri.EscapeDataString(p.Value.ToString())}"));
                    var url = $"{formatted_path}" + (string.IsNullOrEmpty(queryString) ? "" : $"?{queryString}");
                    var content = null;
                    var response = await this.httpClient.GetAsync(url);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
        /// <summary>
        /// POST /scanner/heartbeat
        /// </summary>
                /// <param name="scanner_version">scanner_version parameter</param>
        /// <param name="scanner_type">scanner_type parameter</param>
        /// <param name="active_rules">active_rules parameter</param>
        /// <param name="active_plugins">active_plugins parameter</param>
        public async Task<object> postscannerheartbeat(string scanner_version, string? scanner_type = null, List<string>? active_rules = null, List<string>? active_plugins = null)
        {
                    var url = "/scanner/heartbeat";
                    var content = JsonContent.Create(new { scanner_version = scanner_version, scanner_type = scanner_type, active_rules = active_rules, active_plugins = active_plugins });
                    var response = await this.httpClient.PostAsync(url, content);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
        /// <summary>
        /// GET /scanner/recommendations
        /// </summary>
                /// <param name="scanner_type">scanner_type parameter</param>
        /// <param name="current_rules">current_rules parameter</param>
        /// <param name="current_plugins">current_plugins parameter</param>
        public async Task<object> getscannerrecommendations(string? scanner_type = null, List<string>? current_rules = null, List<string>? current_plugins = null)
        {
                    var queryParams = new Dictionary<string, object?> { "scanner_type", scanner_type, "current_rules", current_rules, "current_plugins", current_plugins };
                    var queryString = string.Join("&", queryParams.Where(p => p.Value != null).Select(p => $"{p.Key}={Uri.EscapeDataString(p.Value.ToString())}"));
                    var url = $"{formatted_path}" + (string.IsNullOrEmpty(queryString) ? "" : $"?{queryString}");
                    var content = null;
                    var response = await this.httpClient.GetAsync(url);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
    }
}
