using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Net.Http.Json;
using System.Threading.Tasks;

namespace TavoAI
{
    /// <summary>
    /// Client for repositories endpoints
    /// </summary>
    public class RepositoriesClient
    {
        private readonly HttpClient httpClient;

        /// <summary>
        /// Create a new repositories client
        /// </summary>
        /// <param name="httpClient">HTTP client instance</param>
        public RepositoriesClient(HttpClient httpClient)
        {
            this.httpClient = httpClient;
        }


        /// <summary>
        /// POST /sync
        /// </summary>
                /// <param name="background_tasks">background_tasks parameter</param>
        public async Task<Task<List[RepositoryResponse]>> postsync(object background_tasks)
        {'                    var url = "/sync";\n                    var content = JsonContent.Create(background_tasks);\n                    var response = await this.httpClient.PostAsync(url, content);\n                    response.EnsureSuccessStatusCode();\n                    return await response.Content.ReadFromJsonAsync<object>();'}

        /// <summary>
        /// GET /
        /// </summary>
                /// <param name="connection_id">connection_id parameter</param>
        /// <param name="language">language parameter</param>
        /// <param name="scan_enabled">scan_enabled parameter</param>
        /// <param name="search">search parameter</param>
        /// <param name="page">page parameter</param>
        /// <param name="per_page">per_page parameter</param>
        public async Task<Task<RepositoryListResponse>> getRoot(string? connection_id = null, string? language = null, bool? scan_enabled = null, string? search = null, double? page = null, double? per_page = null)
        {'                    var queryParams = new Dictionary<string, object?> { "connection_id", connection_id, "language", language, "scan_enabled", scan_enabled, "search", search, "page", page, "per_page", per_page };\n                    var queryString = string.Join("&", queryParams.Where(p => p.Value != null).Select(p => $"{p.Key}={Uri.EscapeDataString(p.Value.ToString())}"));\n                    var url = "/" + (string.IsNullOrEmpty(queryString) ? "" : $"?{queryString}");\n                    var content = null;\n                    var response = await this.httpClient.GetAsync(url);\n                    response.EnsureSuccessStatusCode();\n                    return await response.Content.ReadFromJsonAsync<object>();'}

        /// <summary>
        /// GET /{repository_id}
        /// </summary>
                /// <param name="repository_id">repository_id parameter</param>
        public async Task<Task<RepositoryResponse>> get{repository_id}(string repository_id)
        {'                    var queryParams = new Dictionary<string, object?> { "repository_id", repository_id };\n                    var queryString = string.Join("&", queryParams.Where(p => p.Value != null).Select(p => $"{p.Key}={Uri.EscapeDataString(p.Value.ToString())}"));\n                    var url = "/{repository_id}" + (string.IsNullOrEmpty(queryString) ? "" : $"?{queryString}");\n                    var content = null;\n                    var response = await this.httpClient.GetAsync(url);\n                    response.EnsureSuccessStatusCode();\n                    return await response.Content.ReadFromJsonAsync<object>();'}

        /// <summary>
        /// PUT /{repository_id}
        /// </summary>
                /// <param name="repository_id">repository_id parameter</param>
        /// <param name="repository_update">repository_update parameter</param>
        public async Task<Task<RepositoryResponse>> put{repository_id}(string repository_id, object repository_update)
        {'                    var url = "/{repository_id}";\n                    var content = JsonContent.Create(new { "repository_id", repository_id, "repository_update", repository_update });\n                    var response = await this.httpClient.PutAsync(url, content);\n                    response.EnsureSuccessStatusCode();\n                    return await response.Content.ReadFromJsonAsync<object>();'}

        /// <summary>
        /// DELETE /{repository_id}
        /// </summary>
                /// <param name="repository_id">repository_id parameter</param>
        public async Task<Task<None>> delete{repository_id}(string repository_id)
        {'                    var url = "/{repository_id}";\n                    var content = JsonContent.Create(repository_id);\n                    var response = await this.httpClient.DeleteAsync(url);\n                    response.EnsureSuccessStatusCode();\n                    return await response.Content.ReadFromJsonAsync<object>();'}

        /// <summary>
        /// GET /{repository_id}/scans
        /// </summary>
                /// <param name="repository_id">repository_id parameter</param>
        /// <param name="limit">limit parameter</param>
        public async Task<Task<List[ScanInDB]>> get{repository_id}scans(string repository_id, double? limit = null)
        {'                    var queryParams = new Dictionary<string, object?> { "repository_id", repository_id, "limit", limit };\n                    var queryString = string.Join("&", queryParams.Where(p => p.Value != null).Select(p => $"{p.Key}={Uri.EscapeDataString(p.Value.ToString())}"));\n                    var url = "/{repository_id}/scans" + (string.IsNullOrEmpty(queryString) ? "" : $"?{queryString}");\n                    var content = null;\n                    var response = await this.httpClient.GetAsync(url);\n                    response.EnsureSuccessStatusCode();\n                    return await response.Content.ReadFromJsonAsync<object>();'}

        /// <summary>
        /// POST /{repository_id}/scan
        /// </summary>
                /// <param name="repository_id">repository_id parameter</param>
        /// <param name="background_tasks">background_tasks parameter</param>
        public async Task<Task<ScanInDB>> post{repository_id}scan(string repository_id, object background_tasks)
        {'                    var url = "/{repository_id}/scan";\n                    var content = JsonContent.Create(new { "repository_id", repository_id, "background_tasks", background_tasks });\n                    var response = await this.httpClient.PostAsync(url, content);\n                    response.EnsureSuccessStatusCode();\n                    return await response.Content.ReadFromJsonAsync<object>();'}

        /// <summary>
        /// GET /{repository_id}/branches
        /// </summary>
                /// <param name="repository_id">repository_id parameter</param>
        public async Task<Task<List[RepositoryBranchResponse]>> get{repository_id}branches(string repository_id)
        {'                    var queryParams = new Dictionary<string, object?> { "repository_id", repository_id };\n                    var queryString = string.Join("&", queryParams.Where(p => p.Value != null).Select(p => $"{p.Key}={Uri.EscapeDataString(p.Value.ToString())}"));\n                    var url = "/{repository_id}/branches" + (string.IsNullOrEmpty(queryString) ? "" : $"?{queryString}");\n                    var content = null;\n                    var response = await this.httpClient.GetAsync(url);\n                    response.EnsureSuccessStatusCode();\n                    return await response.Content.ReadFromJsonAsync<object>();'}

        /// <summary>
        /// POST /{repository_id}/pause
        /// </summary>
                /// <param name="repository_id">repository_id parameter</param>
        public async Task<Task<RepositoryResponse>> post{repository_id}pause(string repository_id)
        {'                    var url = "/{repository_id}/pause";\n                    var content = JsonContent.Create(repository_id);\n                    var response = await this.httpClient.PostAsync(url, content);\n                    response.EnsureSuccessStatusCode();\n                    return await response.Content.ReadFromJsonAsync<object>();'}

        /// <summary>
        /// POST /{repository_id}/resume
        /// </summary>
                /// <param name="repository_id">repository_id parameter</param>
        public async Task<Task<RepositoryResponse>> post{repository_id}resume(string repository_id)
        {'                    var url = "/{repository_id}/resume";\n                    var content = JsonContent.Create(repository_id);\n                    var response = await this.httpClient.PostAsync(url, content);\n                    response.EnsureSuccessStatusCode();\n                    return await response.Content.ReadFromJsonAsync<object>();'}

        /// <summary>
        /// GET /{repository_id}/analytics
        /// </summary>
                /// <param name="repository_id">repository_id parameter</param>
        /// <param name="timeframe">timeframe parameter</param>
        public async Task<Task<Dict[str, Any]>> get{repository_id}analytics(string repository_id, string? timeframe = null)
        {'                    var queryParams = new Dictionary<string, object?> { "repository_id", repository_id, "timeframe", timeframe };\n                    var queryString = string.Join("&", queryParams.Where(p => p.Value != null).Select(p => $"{p.Key}={Uri.EscapeDataString(p.Value.ToString())}"));\n                    var url = "/{repository_id}/analytics" + (string.IsNullOrEmpty(queryString) ? "" : $"?{queryString}");\n                    var content = null;\n                    var response = await this.httpClient.GetAsync(url);\n                    response.EnsureSuccessStatusCode();\n                    return await response.Content.ReadFromJsonAsync<object>();'}

        /// <summary>
        /// GET /{repository_id}/badge
        /// </summary>
                /// <param name="repository_id">repository_id parameter</param>
        /// <param name="style">style parameter</param>
        public async Task<Task<Dict[str, Any]>> get{repository_id}badge(string repository_id, string? style = null)
        {'                    var queryParams = new Dictionary<string, object?> { "repository_id", repository_id, "style", style };\n                    var queryString = string.Join("&", queryParams.Where(p => p.Value != null).Select(p => $"{p.Key}={Uri.EscapeDataString(p.Value.ToString())}"));\n                    var url = "/{repository_id}/badge" + (string.IsNullOrEmpty(queryString) ? "" : $"?{queryString}");\n                    var content = null;\n                    var response = await this.httpClient.GetAsync(url);\n                    response.EnsureSuccessStatusCode();\n                    return await response.Content.ReadFromJsonAsync<object>();'}

        /// <summary>
        /// GET /{repository_id}/activity
        /// </summary>
                /// <param name="repository_id">repository_id parameter</param>
        /// <param name="limit">limit parameter</param>
        public async Task<Task<List[Dict[str, Any]]>> get{repository_id}activity(string repository_id, double? limit = null)
        {'                    var queryParams = new Dictionary<string, object?> { "repository_id", repository_id, "limit", limit };\n                    var queryString = string.Join("&", queryParams.Where(p => p.Value != null).Select(p => $"{p.Key}={Uri.EscapeDataString(p.Value.ToString())}"));\n                    var url = "/{repository_id}/activity" + (string.IsNullOrEmpty(queryString) ? "" : $"?{queryString}");\n                    var content = null;\n                    var response = await this.httpClient.GetAsync(url);\n                    response.EnsureSuccessStatusCode();\n                    return await response.Content.ReadFromJsonAsync<object>();'}
    }
}
