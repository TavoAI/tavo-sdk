using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Net.Http.Json;
using System.Threading.Tasks;

namespace TavoAI
{
    /// <summary>
    /// Client for repository_connections endpoints
    /// </summary>
    public class RepositoryConnectionsClient
    {
        private readonly HttpClient httpClient;

        /// <summary>
        /// Create a new repository_connections client
        /// </summary>
        /// <param name="httpClient">HTTP client instance</param>
        public RepositoryConnectionsClient(HttpClient httpClient)
        {
            this.httpClient = httpClient;
        }


        /// <summary>
        /// POST /
        /// </summary>
                /// <param name="connection_in">connection_in parameter</param>
        public async Task<Task<RepositoryConnectionResponse>> postRoot(object connection_in)
        {'                    var url = "/";\n                    var content = JsonContent.Create(connection_in);\n                    var response = await this.httpClient.PostAsync(url, content);\n                    response.EnsureSuccessStatusCode();\n                    return await response.Content.ReadFromJsonAsync<object>();'}

        /// <summary>
        /// GET /
        /// </summary>
                /// <param name="provider_id">provider_id parameter</param>
        /// <param name="connection_type">connection_type parameter</param>
        /// <param name="is_active">is_active parameter</param>
        public async Task<Task<List[RepositoryConnectionResponse]>> getRoot(string? provider_id = null, string? connection_type = null, bool? is_active = null)
        {'                    var queryParams = new Dictionary<string, object?> { "provider_id", provider_id, "connection_type", connection_type, "is_active", is_active };\n                    var queryString = string.Join("&", queryParams.Where(p => p.Value != null).Select(p => $"{p.Key}={Uri.EscapeDataString(p.Value.ToString())}"));\n                    var url = "/" + (string.IsNullOrEmpty(queryString) ? "" : $"?{queryString}");\n                    var content = null;\n                    var response = await this.httpClient.GetAsync(url);\n                    response.EnsureSuccessStatusCode();\n                    return await response.Content.ReadFromJsonAsync<object>();'}

        /// <summary>
        /// GET /{connection_id}
        /// </summary>
                /// <param name="connection_id">connection_id parameter</param>
        public async Task<Task<RepositoryConnectionResponse>> get{connection_id}(string connection_id)
        {'                    var queryParams = new Dictionary<string, object?> { "connection_id", connection_id };\n                    var queryString = string.Join("&", queryParams.Where(p => p.Value != null).Select(p => $"{p.Key}={Uri.EscapeDataString(p.Value.ToString())}"));\n                    var url = "/{connection_id}" + (string.IsNullOrEmpty(queryString) ? "" : $"?{queryString}");\n                    var content = null;\n                    var response = await this.httpClient.GetAsync(url);\n                    response.EnsureSuccessStatusCode();\n                    return await response.Content.ReadFromJsonAsync<object>();'}

        /// <summary>
        /// PUT /{connection_id}
        /// </summary>
                /// <param name="connection_id">connection_id parameter</param>
        /// <param name="connection_update">connection_update parameter</param>
        public async Task<Task<RepositoryConnectionResponse>> put{connection_id}(string connection_id, object connection_update)
        {'                    var url = "/{connection_id}";\n                    var content = JsonContent.Create(new { "connection_id", connection_id, "connection_update", connection_update });\n                    var response = await this.httpClient.PutAsync(url, content);\n                    response.EnsureSuccessStatusCode();\n                    return await response.Content.ReadFromJsonAsync<object>();'}

        /// <summary>
        /// DELETE /{connection_id}
        /// </summary>
                /// <param name="connection_id">connection_id parameter</param>
        public async Task<Task<None>> delete{connection_id}(string connection_id)
        {'                    var url = "/{connection_id}";\n                    var content = JsonContent.Create(connection_id);\n                    var response = await this.httpClient.DeleteAsync(url);\n                    response.EnsureSuccessStatusCode();\n                    return await response.Content.ReadFromJsonAsync<object>();'}

        /// <summary>
        /// POST /{connection_id}/validate
        /// </summary>
                /// <param name="connection_id">connection_id parameter</param>
        public async Task<Task<ConnectionValidationResponse>> post{connection_id}validate(string connection_id)
        {'                    var url = "/{connection_id}/validate";\n                    var content = JsonContent.Create(connection_id);\n                    var response = await this.httpClient.PostAsync(url, content);\n                    response.EnsureSuccessStatusCode();\n                    return await response.Content.ReadFromJsonAsync<object>();'}

        /// <summary>
        /// POST /{connection_id}/refresh
        /// </summary>
                /// <param name="connection_id">connection_id parameter</param>
        public async Task<Task<RepositoryConnectionResponse>> post{connection_id}refresh(string connection_id)
        {'                    var url = "/{connection_id}/refresh";\n                    var content = JsonContent.Create(connection_id);\n                    var response = await this.httpClient.PostAsync(url, content);\n                    response.EnsureSuccessStatusCode();\n                    return await response.Content.ReadFromJsonAsync<object>();'}
    }
}
