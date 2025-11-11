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
        public async Task<List<object>> postsync(object background_tasks)
        {
                    var url = "/sync";
                    var content = JsonContent.Create(background_tasks);
                    var response = await this.httpClient.PostAsync(url, content);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
        /// <summary>
        /// GET /
        /// </summary>
                /// <param name="connection_id">connection_id parameter</param>
        /// <param name="language">language parameter</param>
        /// <param name="scan_enabled">scan_enabled parameter</param>
        /// <param name="search">search parameter</param>
        /// <param name="page">page parameter</param>
        /// <param name="per_page">per_page parameter</param>
        public async Task<object> getroot(string? connection_id = null, string? language = null, bool? scan_enabled = null, string? search = null, double? page = null, double? per_page = null)
        {
                    var queryParams = new Dictionary<string, object?> { "connection_id", connection_id, "language", language, "scan_enabled", scan_enabled, "search", search, "page", page, "per_page", per_page };
                    var queryString = string.Join("&", queryParams.Where(p => p.Value != null).Select(p => $"{p.Key}={Uri.EscapeDataString(p.Value.ToString())}"));
                    var url = $"{formatted_path}" + (string.IsNullOrEmpty(queryString) ? "" : $"?{queryString}");
                    var content = null;
                    var response = await this.httpClient.GetAsync(url);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
        /// <summary>
        /// GET /{repository_id}
        /// </summary>
                /// <param name="repository_id">repository_id parameter</param>
        public async Task<object> getroot(string repository_id)
        {
                    var queryParams = new Dictionary<string, object?> { "repository_id", repository_id };
                    var queryString = string.Join("&", queryParams.Where(p => p.Value != null).Select(p => $"{p.Key}={Uri.EscapeDataString(p.Value.ToString())}"));
                    var url = $"{formatted_path}" + (string.IsNullOrEmpty(queryString) ? "" : $"?{queryString}");
                    var content = null;
                    var response = await this.httpClient.GetAsync(url);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
        /// <summary>
        /// PUT /{repository_id}
        /// </summary>
                /// <param name="repository_id">repository_id parameter</param>
        /// <param name="repository_update">repository_update parameter</param>
        public async Task<object> putroot(string repository_id, object repository_update)
        {
                    var url = "/{repository_id}";
                    var content = JsonContent.Create(new { repository_id = repository_id, repository_update = repository_update });
                    var response = await this.httpClient.PutAsync(url, content);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
        /// <summary>
        /// DELETE /{repository_id}
        /// </summary>
                /// <param name="repository_id">repository_id parameter</param>
        public async Task<object> deleteroot(string repository_id)
        {
                    var url = "/{repository_id}";
                    var content = JsonContent.Create(repository_id);
                    var response = await this.httpClient.DeleteAsync(url);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
        /// <summary>
        /// GET /{repository_id}/scans
        /// </summary>
                /// <param name="repository_id">repository_id parameter</param>
        /// <param name="limit">limit parameter</param>
        public async Task<List<object>> getscans(string repository_id, double? limit = null)
        {
                    var queryParams = new Dictionary<string, object?> { "repository_id", repository_id, "limit", limit };
                    var queryString = string.Join("&", queryParams.Where(p => p.Value != null).Select(p => $"{p.Key}={Uri.EscapeDataString(p.Value.ToString())}"));
                    var url = $"{formatted_path}" + (string.IsNullOrEmpty(queryString) ? "" : $"?{queryString}");
                    var content = null;
                    var response = await this.httpClient.GetAsync(url);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
        /// <summary>
        /// POST /{repository_id}/scan
        /// </summary>
                /// <param name="repository_id">repository_id parameter</param>
        /// <param name="background_tasks">background_tasks parameter</param>
        public async Task<object> postscan(string repository_id, object background_tasks)
        {
                    var url = "/{repository_id}/scan";
                    var content = JsonContent.Create(new { repository_id = repository_id, background_tasks = background_tasks });
                    var response = await this.httpClient.PostAsync(url, content);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
        /// <summary>
        /// GET /{repository_id}/branches
        /// </summary>
                /// <param name="repository_id">repository_id parameter</param>
        public async Task<List<object>> getbranches(string repository_id)
        {
                    var queryParams = new Dictionary<string, object?> { "repository_id", repository_id };
                    var queryString = string.Join("&", queryParams.Where(p => p.Value != null).Select(p => $"{p.Key}={Uri.EscapeDataString(p.Value.ToString())}"));
                    var url = $"{formatted_path}" + (string.IsNullOrEmpty(queryString) ? "" : $"?{queryString}");
                    var content = null;
                    var response = await this.httpClient.GetAsync(url);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
        /// <summary>
        /// POST /{repository_id}/pause
        /// </summary>
                /// <param name="repository_id">repository_id parameter</param>
        public async Task<object> postpause(string repository_id)
        {
                    var url = "/{repository_id}/pause";
                    var content = JsonContent.Create(repository_id);
                    var response = await this.httpClient.PostAsync(url, content);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
        /// <summary>
        /// POST /{repository_id}/resume
        /// </summary>
                /// <param name="repository_id">repository_id parameter</param>
        public async Task<object> postresume(string repository_id)
        {
                    var url = "/{repository_id}/resume";
                    var content = JsonContent.Create(repository_id);
                    var response = await this.httpClient.PostAsync(url, content);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
        /// <summary>
        /// GET /{repository_id}/analytics
        /// </summary>
                /// <param name="repository_id">repository_id parameter</param>
        /// <param name="timeframe">timeframe parameter</param>
        public async Task<Dictionary<string, object>> getanalytics(string repository_id, string? timeframe = null)
        {
                    var queryParams = new Dictionary<string, object?> { "repository_id", repository_id, "timeframe", timeframe };
                    var queryString = string.Join("&", queryParams.Where(p => p.Value != null).Select(p => $"{p.Key}={Uri.EscapeDataString(p.Value.ToString())}"));
                    var url = $"{formatted_path}" + (string.IsNullOrEmpty(queryString) ? "" : $"?{queryString}");
                    var content = null;
                    var response = await this.httpClient.GetAsync(url);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
        /// <summary>
        /// GET /{repository_id}/badge
        /// </summary>
                /// <param name="repository_id">repository_id parameter</param>
        /// <param name="style">style parameter</param>
        public async Task<Dictionary<string, object>> getbadge(string repository_id, string? style = null)
        {
                    var queryParams = new Dictionary<string, object?> { "repository_id", repository_id, "style", style };
                    var queryString = string.Join("&", queryParams.Where(p => p.Value != null).Select(p => $"{p.Key}={Uri.EscapeDataString(p.Value.ToString())}"));
                    var url = $"{formatted_path}" + (string.IsNullOrEmpty(queryString) ? "" : $"?{queryString}");
                    var content = null;
                    var response = await this.httpClient.GetAsync(url);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
        /// <summary>
        /// GET /{repository_id}/activity
        /// </summary>
                /// <param name="repository_id">repository_id parameter</param>
        /// <param name="limit">limit parameter</param>
        public async Task<List<Dictionary<string, object>>> getactivity(string repository_id, double? limit = null)
        {
                    var queryParams = new Dictionary<string, object?> { "repository_id", repository_id, "limit", limit };
                    var queryString = string.Join("&", queryParams.Where(p => p.Value != null).Select(p => $"{p.Key}={Uri.EscapeDataString(p.Value.ToString())}"));
                    var url = $"{formatted_path}" + (string.IsNullOrEmpty(queryString) ? "" : $"?{queryString}");
                    var content = null;
                    var response = await this.httpClient.GetAsync(url);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
    }
}
