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
        public async Task<Task<ListResponse[RuleBundleSchema]>> getrulesdiscover(string? category = null, string? language = null, string? scanner_type = null, double? limit = null)
        {'                    var queryParams = new Dictionary<string, object?> { "category", category, "language", language, "scanner_type", scanner_type, "limit", limit };\n                    var queryString = string.Join("&", queryParams.Where(p => p.Value != null).Select(p => $"{p.Key}={Uri.EscapeDataString(p.Value.ToString())}"));\n                    var url = "/rules/discover" + (string.IsNullOrEmpty(queryString) ? "" : $"?{queryString}");\n                    var content = null;\n                    var response = await this.httpClient.GetAsync(url);\n                    response.EnsureSuccessStatusCode();\n                    return await response.Content.ReadFromJsonAsync<object>();'}

        /// <summary>
        /// GET /rules/bundle/{bundle_id}/rules
        /// </summary>
                /// <param name="bundle_id">bundle_id parameter</param>
        /// <param name="severity">severity parameter</param>
        /// <param name="language">language parameter</param>
        /// <param name="limit">limit parameter</param>
        public async Task<Task<ListResponse[RuleSchema]>> getrulesbundle{bundle_id}rules(string bundle_id, string? severity = null, string? language = null, double? limit = null)
        {'                    var queryParams = new Dictionary<string, object?> { "bundle_id", bundle_id, "severity", severity, "language", language, "limit", limit };\n                    var queryString = string.Join("&", queryParams.Where(p => p.Value != null).Select(p => $"{p.Key}={Uri.EscapeDataString(p.Value.ToString())}"));\n                    var url = "/rules/bundle/{bundle_id}/rules" + (string.IsNullOrEmpty(queryString) ? "" : $"?{queryString}");\n                    var content = null;\n                    var response = await this.httpClient.GetAsync(url);\n                    response.EnsureSuccessStatusCode();\n                    return await response.Content.ReadFromJsonAsync<object>();'}

        /// <summary>
        /// POST /rules/bundle/{bundle_id}/use
        /// </summary>
                /// <param name="bundle_id">bundle_id parameter</param>
        /// <param name="scan_id">scan_id parameter</param>
        public async Task<Task<object>> postrulesbundle{bundle_id}use(string bundle_id, string? scan_id = null)
        {'                    var url = "/rules/bundle/{bundle_id}/use";\n                    var content = JsonContent.Create(new { "bundle_id", bundle_id, "scan_id", scan_id });\n                    var response = await this.httpClient.PostAsync(url, content);\n                    response.EnsureSuccessStatusCode();\n                    return await response.Content.ReadFromJsonAsync<object>();'}

        /// <summary>
        /// GET /plugins/discover
        /// </summary>
                /// <param name="plugin_type">plugin_type parameter</param>
        /// <param name="language">language parameter</param>
        /// <param name="scanner_integration">scanner_integration parameter</param>
        /// <param name="limit">limit parameter</param>
        public async Task<Task<ListResponse[PluginResponse]>> getpluginsdiscover(string? plugin_type = null, string? language = null, bool? scanner_integration = null, double? limit = null)
        {'                    var queryParams = new Dictionary<string, object?> { "plugin_type", plugin_type, "language", language, "scanner_integration", scanner_integration, "limit", limit };\n                    var queryString = string.Join("&", queryParams.Where(p => p.Value != null).Select(p => $"{p.Key}={Uri.EscapeDataString(p.Value.ToString())}"));\n                    var url = "/plugins/discover" + (string.IsNullOrEmpty(queryString) ? "" : $"?{queryString}");\n                    var content = null;\n                    var response = await this.httpClient.GetAsync(url);\n                    response.EnsureSuccessStatusCode();\n                    return await response.Content.ReadFromJsonAsync<object>();'}

        /// <summary>
        /// GET /plugins/{plugin_id}/config
        /// </summary>
                /// <param name="plugin_id">plugin_id parameter</param>
        public async Task<Task<object>> getplugins{plugin_id}config(string plugin_id)
        {'                    var queryParams = new Dictionary<string, object?> { "plugin_id", plugin_id };\n                    var queryString = string.Join("&", queryParams.Where(p => p.Value != null).Select(p => $"{p.Key}={Uri.EscapeDataString(p.Value.ToString())}"));\n                    var url = "/plugins/{plugin_id}/config" + (string.IsNullOrEmpty(queryString) ? "" : $"?{queryString}");\n                    var content = null;\n                    var response = await this.httpClient.GetAsync(url);\n                    response.EnsureSuccessStatusCode();\n                    return await response.Content.ReadFromJsonAsync<object>();'}

        /// <summary>
        /// POST /scanner/heartbeat
        /// </summary>
                /// <param name="scanner_version">scanner_version parameter</param>
        /// <param name="scanner_type">scanner_type parameter</param>
        /// <param name="active_rules">active_rules parameter</param>
        /// <param name="active_plugins">active_plugins parameter</param>
        public async Task<Task<object>> postscannerheartbeat(string scanner_version, string? scanner_type = null, List<string>? active_rules = null, List<string>? active_plugins = null)
        {'                    var url = "/scanner/heartbeat";\n                    var content = JsonContent.Create(new { "scanner_version", scanner_version, "scanner_type", scanner_type, "active_rules", active_rules, "active_plugins", active_plugins });\n                    var response = await this.httpClient.PostAsync(url, content);\n                    response.EnsureSuccessStatusCode();\n                    return await response.Content.ReadFromJsonAsync<object>();'}

        /// <summary>
        /// GET /scanner/recommendations
        /// </summary>
                /// <param name="scanner_type">scanner_type parameter</param>
        /// <param name="current_rules">current_rules parameter</param>
        /// <param name="current_plugins">current_plugins parameter</param>
        public async Task<Task<object>> getscannerrecommendations(string? scanner_type = null, List<string>? current_rules = null, List<string>? current_plugins = null)
        {'                    var queryParams = new Dictionary<string, object?> { "scanner_type", scanner_type, "current_rules", current_rules, "current_plugins", current_plugins };\n                    var queryString = string.Join("&", queryParams.Where(p => p.Value != null).Select(p => $"{p.Key}={Uri.EscapeDataString(p.Value.ToString())}"));\n                    var url = "/scanner/recommendations" + (string.IsNullOrEmpty(queryString) ? "" : $"?{queryString}");\n                    var content = null;\n                    var response = await this.httpClient.GetAsync(url);\n                    response.EnsureSuccessStatusCode();\n                    return await response.Content.ReadFromJsonAsync<object>();'}
    }
}
