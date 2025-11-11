using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Net.Http.Json;
using System.Threading.Tasks;

namespace TavoAI
{
    /// <summary>
    /// Client for plugin_execution endpoints
    /// </summary>
    public class PluginExecutionClient
    {
        private readonly HttpClient httpClient;

        /// <summary>
        /// Create a new plugin_execution client
        /// </summary>
        /// <param name="httpClient">HTTP client instance</param>
        public PluginExecutionClient(HttpClient httpClient)
        {
            this.httpClient = httpClient;
        }

        /// <summary>
        /// POST /execute
        /// </summary>
                /// <param name="background_tasks">background_tasks parameter</param>
        public async Task<object> postexecute(object background_tasks)
        {
                    var url = "/execute";
                    var content = JsonContent.Create(background_tasks);
                    var response = await this.httpClient.PostAsync(url, content);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
        /// <summary>
        /// GET /executions/{execution_id}
        /// </summary>
                /// <param name="execution_id">execution_id parameter</param>
        public async Task<object> getexecutions(string execution_id)
        {
                    var queryParams = new Dictionary<string, object?> { "execution_id", execution_id };
                    var queryString = string.Join("&", queryParams.Where(p => p.Value != null).Select(p => $"{p.Key}={Uri.EscapeDataString(p.Value.ToString())}"));
                    var url = $"{formatted_path}" + (string.IsNullOrEmpty(queryString) ? "" : $"?{queryString}");
                    var content = null;
                    var response = await this.httpClient.GetAsync(url);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
        /// <summary>
        /// GET /executions
        /// </summary>
                /// <param name="plugin_id">plugin_id parameter</param>
        /// <param name="limit">limit parameter</param>
        public async Task<List<object>> getexecutions(string? plugin_id = null, double? limit = null)
        {
                    var queryParams = new Dictionary<string, object?> { "plugin_id", plugin_id, "limit", limit };
                    var queryString = string.Join("&", queryParams.Where(p => p.Value != null).Select(p => $"{p.Key}={Uri.EscapeDataString(p.Value.ToString())}"));
                    var url = $"{formatted_path}" + (string.IsNullOrEmpty(queryString) ? "" : $"?{queryString}");
                    var content = null;
                    var response = await this.httpClient.GetAsync(url);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
    }
}
