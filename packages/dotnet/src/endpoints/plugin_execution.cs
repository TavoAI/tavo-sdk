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
        public async Task<Task<PluginExecutionResponse>> postexecute(object background_tasks)
        {'                    var url = "/execute";\n                    var content = JsonContent.Create(background_tasks);\n                    var response = await this.httpClient.PostAsync(url, content);\n                    response.EnsureSuccessStatusCode();\n                    return await response.Content.ReadFromJsonAsync<object>();'}

        /// <summary>
        /// GET /executions/{execution_id}
        /// </summary>
                /// <param name="execution_id">execution_id parameter</param>
        public async Task<Task<PluginExecutionResponse>> getexecutions{execution_id}(string execution_id)
        {'                    var queryParams = new Dictionary<string, object?> { "execution_id", execution_id };\n                    var queryString = string.Join("&", queryParams.Where(p => p.Value != null).Select(p => $"{p.Key}={Uri.EscapeDataString(p.Value.ToString())}"));\n                    var url = "/executions/{execution_id}" + (string.IsNullOrEmpty(queryString) ? "" : $"?{queryString}");\n                    var content = null;\n                    var response = await this.httpClient.GetAsync(url);\n                    response.EnsureSuccessStatusCode();\n                    return await response.Content.ReadFromJsonAsync<object>();'}

        /// <summary>
        /// GET /executions
        /// </summary>
                /// <param name="plugin_id">plugin_id parameter</param>
        /// <param name="limit">limit parameter</param>
        public async Task<Task<List[PluginExecutionResponse]>> getexecutions(string? plugin_id = null, double? limit = null)
        {'                    var queryParams = new Dictionary<string, object?> { "plugin_id", plugin_id, "limit", limit };\n                    var queryString = string.Join("&", queryParams.Where(p => p.Value != null).Select(p => $"{p.Key}={Uri.EscapeDataString(p.Value.ToString())}"));\n                    var url = "/executions" + (string.IsNullOrEmpty(queryString) ? "" : $"?{queryString}");\n                    var content = null;\n                    var response = await this.httpClient.GetAsync(url);\n                    response.EnsureSuccessStatusCode();\n                    return await response.Content.ReadFromJsonAsync<object>();'}
    }
}
