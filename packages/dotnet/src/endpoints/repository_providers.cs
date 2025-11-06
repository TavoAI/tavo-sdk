using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Net.Http.Json;
using System.Threading.Tasks;

namespace TavoAI
{
    /// <summary>
    /// Client for repository_providers endpoints
    /// </summary>
    public class RepositoryProvidersClient
    {
        private readonly HttpClient httpClient;

        /// <summary>
        /// Create a new repository_providers client
        /// </summary>
        /// <param name="httpClient">HTTP client instance</param>
        public RepositoryProvidersClient(HttpClient httpClient)
        {
            this.httpClient = httpClient;
        }


        /// <summary>
        /// GET /
        /// </summary>
                /// <param name="enabled_only">enabled_only parameter</param>
        public async Task<Task<List[RepositoryProviderResponse]>> getRoot(bool? enabled_only = null)
        {'                    var queryParams = new Dictionary<string, object?> { "enabled_only", enabled_only };\n                    var queryString = string.Join("&", queryParams.Where(p => p.Value != null).Select(p => $"{p.Key}={Uri.EscapeDataString(p.Value.ToString())}"));\n                    var url = "/" + (string.IsNullOrEmpty(queryString) ? "" : $"?{queryString}");\n                    var content = null;\n                    var response = await this.httpClient.GetAsync(url);\n                    response.EnsureSuccessStatusCode();\n                    return await response.Content.ReadFromJsonAsync<object>();'}

        /// <summary>
        /// GET /{provider_id}
        /// </summary>
                /// <param name="provider_id">provider_id parameter</param>
        public async Task<Task<RepositoryProviderResponse>> get{provider_id}(string provider_id)
        {'                    var queryParams = new Dictionary<string, object?> { "provider_id", provider_id };\n                    var queryString = string.Join("&", queryParams.Where(p => p.Value != null).Select(p => $"{p.Key}={Uri.EscapeDataString(p.Value.ToString())}"));\n                    var url = "/{provider_id}" + (string.IsNullOrEmpty(queryString) ? "" : $"?{queryString}");\n                    var content = null;\n                    var response = await this.httpClient.GetAsync(url);\n                    response.EnsureSuccessStatusCode();\n                    return await response.Content.ReadFromJsonAsync<object>();'}
    }
}
