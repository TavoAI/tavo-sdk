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
        public async Task<object> postroot(object connection_in)
        {
                    var url = "/";
                    var content = JsonContent.Create(connection_in);
                    var response = await this.httpClient.PostAsync(url, content);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
        /// <summary>
        /// GET /
        /// </summary>
                /// <param name="provider_id">provider_id parameter</param>
        /// <param name="connection_type">connection_type parameter</param>
        /// <param name="is_active">is_active parameter</param>
        public async Task<List<object>> getroot(string? provider_id = null, string? connection_type = null, bool? is_active = null)
        {
                    var queryParams = new Dictionary<string, object?> { "provider_id", provider_id, "connection_type", connection_type, "is_active", is_active };
                    var queryString = string.Join("&", queryParams.Where(p => p.Value != null).Select(p => $"{p.Key}={Uri.EscapeDataString(p.Value.ToString())}"));
                    var url = $"{formatted_path}" + (string.IsNullOrEmpty(queryString) ? "" : $"?{queryString}");
                    var content = null;
                    var response = await this.httpClient.GetAsync(url);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
        /// <summary>
        /// GET /{connection_id}
        /// </summary>
                /// <param name="connection_id">connection_id parameter</param>
        public async Task<object> getroot(string connection_id)
        {
                    var queryParams = new Dictionary<string, object?> { "connection_id", connection_id };
                    var queryString = string.Join("&", queryParams.Where(p => p.Value != null).Select(p => $"{p.Key}={Uri.EscapeDataString(p.Value.ToString())}"));
                    var url = $"{formatted_path}" + (string.IsNullOrEmpty(queryString) ? "" : $"?{queryString}");
                    var content = null;
                    var response = await this.httpClient.GetAsync(url);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
        /// <summary>
        /// PUT /{connection_id}
        /// </summary>
                /// <param name="connection_id">connection_id parameter</param>
        /// <param name="connection_update">connection_update parameter</param>
        public async Task<object> putroot(string connection_id, object connection_update)
        {
                    var url = "/{connection_id}";
                    var content = JsonContent.Create(new { connection_id = connection_id, connection_update = connection_update });
                    var response = await this.httpClient.PutAsync(url, content);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
        /// <summary>
        /// DELETE /{connection_id}
        /// </summary>
                /// <param name="connection_id">connection_id parameter</param>
        public async Task<object> deleteroot(string connection_id)
        {
                    var url = "/{connection_id}";
                    var content = JsonContent.Create(connection_id);
                    var response = await this.httpClient.DeleteAsync(url);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
        /// <summary>
        /// POST /{connection_id}/validate
        /// </summary>
                /// <param name="connection_id">connection_id parameter</param>
        public async Task<object> postvalidate(string connection_id)
        {
                    var url = "/{connection_id}/validate";
                    var content = JsonContent.Create(connection_id);
                    var response = await this.httpClient.PostAsync(url, content);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
        /// <summary>
        /// POST /{connection_id}/refresh
        /// </summary>
                /// <param name="connection_id">connection_id parameter</param>
        public async Task<object> postrefresh(string connection_id)
        {
                    var url = "/{connection_id}/refresh";
                    var content = JsonContent.Create(connection_id);
                    var response = await this.httpClient.PostAsync(url, content);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
    }
}
