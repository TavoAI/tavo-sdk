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
        public async Task<List<object>> getroot(bool? enabled_only = null)
        {
                    var queryParams = new Dictionary<string, object?> { "enabled_only", enabled_only };
                    var queryString = string.Join("&", queryParams.Where(p => p.Value != null).Select(p => $"{p.Key}={Uri.EscapeDataString(p.Value.ToString())}"));
                    var url = $"{formatted_path}" + (string.IsNullOrEmpty(queryString) ? "" : $"?{queryString}");
                    var content = null;
                    var response = await this.httpClient.GetAsync(url);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
        /// <summary>
        /// GET /{provider_id}
        /// </summary>
                /// <param name="provider_id">provider_id parameter</param>
        public async Task<object> getroot(string provider_id)
        {
                    var queryParams = new Dictionary<string, object?> { "provider_id", provider_id };
                    var queryString = string.Join("&", queryParams.Where(p => p.Value != null).Select(p => $"{p.Key}={Uri.EscapeDataString(p.Value.ToString())}"));
                    var url = $"{formatted_path}" + (string.IsNullOrEmpty(queryString) ? "" : $"?{queryString}");
                    var content = null;
                    var response = await this.httpClient.GetAsync(url);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
    }
}
