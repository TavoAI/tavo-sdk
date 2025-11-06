using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Net.Http.Json;
using System.Threading.Tasks;

namespace TavoAI
{
    /// <summary>
    /// Client for ai_analysis endpoints
    /// </summary>
    public class AiAnalysisClient
    {
        private readonly HttpClient httpClient;

        /// <summary>
        /// Create a new ai_analysis client
        /// </summary>
        /// <param name="httpClient">HTTP client instance</param>
        public AiAnalysisClient(HttpClient httpClient)
        {
            this.httpClient = httpClient;
        }


        /// <summary>
        /// POST /analyze/{scan_id}
        /// </summary>
                /// <param name="scan_id">scan_id parameter</param>
        /// <param name="background_tasks">background_tasks parameter</param>
        public async Task<Task<CodeFixResponse>> postanalyze{scan_id}(string scan_id, object background_tasks)
        {'                    var url = "/analyze/{scan_id}";\n                    var content = JsonContent.Create(new { "scan_id", scan_id, "background_tasks", background_tasks });\n                    var response = await this.httpClient.PostAsync(url, content);\n                    response.EnsureSuccessStatusCode();\n                    return await response.Content.ReadFromJsonAsync<object>();'}

        /// <summary>
        /// POST /classify/{scan_id}
        /// </summary>
                /// <param name="scan_id">scan_id parameter</param>
        /// <param name="background_tasks">background_tasks parameter</param>
        public async Task<Task<VulnerabilityClassificationResponse>> postclassify{scan_id}(string scan_id, object background_tasks)
        {'                    var url = "/classify/{scan_id}";\n                    var content = JsonContent.Create(new { "scan_id", scan_id, "background_tasks", background_tasks });\n                    var response = await this.httpClient.PostAsync(url, content);\n                    response.EnsureSuccessStatusCode();\n                    return await response.Content.ReadFromJsonAsync<object>();'}

        /// <summary>
        /// POST /risk-score/{scan_id}
        /// </summary>
                /// <param name="scan_id">scan_id parameter</param>
        public async Task<Task<RiskScoreResponse>> postriskscore{scan_id}(string scan_id)
        {'                    var url = "/risk-score/{scan_id}";\n                    var content = JsonContent.Create(scan_id);\n                    var response = await this.httpClient.PostAsync(url, content);\n                    response.EnsureSuccessStatusCode();\n                    return await response.Content.ReadFromJsonAsync<object>();'}

        /// <summary>
        /// POST /compliance/{scan_id}
        /// </summary>
                /// <param name="scan_id">scan_id parameter</param>
        /// <param name="framework">framework parameter</param>
        public async Task<Task<ComplianceReportResponse>> postcompliance{scan_id}(double scan_id, string? framework = null)
        {'                    var url = "/compliance/{scan_id}";\n                    var content = JsonContent.Create(new { "scan_id", scan_id, "framework", framework });\n                    var response = await this.httpClient.PostAsync(url, content);\n                    response.EnsureSuccessStatusCode();\n                    return await response.Content.ReadFromJsonAsync<object>();'}

        /// <summary>
        /// POST /predictive/{scan_id}
        /// </summary>
                /// <param name="scan_id">scan_id parameter</param>
        public async Task<Task<PredictiveAnalysisResponse>> postpredictive{scan_id}(string scan_id)
        {'                    var url = "/predictive/{scan_id}";\n                    var content = JsonContent.Create(scan_id);\n                    var response = await this.httpClient.PostAsync(url, content);\n                    response.EnsureSuccessStatusCode();\n                    return await response.Content.ReadFromJsonAsync<object>();'}

        /// <summary>
        /// GET /fix-suggestions
        /// </summary>
                /// <param name="search">search parameter</param>
        /// <param name="status">status parameter</param>
        /// <param name="severity">severity parameter</param>
        /// <param name="analysis_type">analysis_type parameter</param>
        /// <param name="limit">limit parameter</param>
        /// <param name="offset">offset parameter</param>
        public async Task<Task<Dict[str, Any]>> getfixsuggestions(string? search = null, string? status = null, string? severity = null, string? analysis_type = null, double? limit = null, double? offset = null)
        {'                    var queryParams = new Dictionary<string, object?> { "search", search, "status", status, "severity", severity, "analysis_type", analysis_type, "limit", limit, "offset", offset };\n                    var queryString = string.Join("&", queryParams.Where(p => p.Value != null).Select(p => $"{p.Key}={Uri.EscapeDataString(p.Value.ToString())}"));\n                    var url = "/fix-suggestions" + (string.IsNullOrEmpty(queryString) ? "" : $"?{queryString}");\n                    var content = null;\n                    var response = await this.httpClient.GetAsync(url);\n                    response.EnsureSuccessStatusCode();\n                    return await response.Content.ReadFromJsonAsync<object>();'}

        /// <summary>
        /// GET /predictive
        /// </summary>
                /// <param name="time_horizon">time_horizon parameter</param>
        /// <param name="severity">severity parameter</param>
        /// <param name="prediction_type">prediction_type parameter</param>
        /// <param name="analysis_type">analysis_type parameter</param>
        public async Task<Task<Dict[str, Any]>> getpredictive(string? time_horizon = null, string? severity = null, string? prediction_type = null, string? analysis_type = null)
        {'                    var queryParams = new Dictionary<string, object?> { "time_horizon", time_horizon, "severity", severity, "prediction_type", prediction_type, "analysis_type", analysis_type };\n                    var queryString = string.Join("&", queryParams.Where(p => p.Value != null).Select(p => $"{p.Key}={Uri.EscapeDataString(p.Value.ToString())}"));\n                    var url = "/predictive" + (string.IsNullOrEmpty(queryString) ? "" : $"?{queryString}");\n                    var content = null;\n                    var response = await this.httpClient.GetAsync(url);\n                    response.EnsureSuccessStatusCode();\n                    return await response.Content.ReadFromJsonAsync<object>();'}

        /// <summary>
        /// GET /compliance
        /// </summary>
                /// <param name="framework">framework parameter</param>
        /// <param name="status">status parameter</param>
        /// <param name="risk_level">risk_level parameter</param>
        /// <param name="category">category parameter</param>
        public async Task<Task<Dict[str, Any]>> getcompliance(string? framework = null, string? status = null, string? risk_level = null, string? category = null)
        {'                    var queryParams = new Dictionary<string, object?> { "framework", framework, "status", status, "risk_level", risk_level, "category", category };\n                    var queryString = string.Join("&", queryParams.Where(p => p.Value != null).Select(p => $"{p.Key}={Uri.EscapeDataString(p.Value.ToString())}"));\n                    var url = "/compliance" + (string.IsNullOrEmpty(queryString) ? "" : $"?{queryString}");\n                    var content = null;\n                    var response = await this.httpClient.GetAsync(url);\n                    response.EnsureSuccessStatusCode();\n                    return await response.Content.ReadFromJsonAsync<object>();'}
    }
}
