using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Net.Http.Json;
using System.Threading.Tasks;

namespace TavoAI
{
    /// <summary>
    /// Client for repository_webhooks endpoints
    /// </summary>
    public class RepositoryWebhooksClient
    {
        private readonly HttpClient httpClient;

        /// <summary>
        /// Create a new repository_webhooks client
        /// </summary>
        /// <param name="httpClient">HTTP client instance</param>
        public RepositoryWebhooksClient(HttpClient httpClient)
        {
            this.httpClient = httpClient;
        }

        /// <summary>
        /// POST /github
        /// </summary>
                /// <param name="x_hub_signature_256">x_hub_signature_256 parameter</param>
        /// <param name="x_github_event">x_github_event parameter</param>
        /// <param name="x_github_delivery">x_github_delivery parameter</param>
        public async Task<Dictionary<string, object>> postgithub(string? x_hub_signature_256 = null, string? x_github_event = null, string? x_github_delivery = null)
        {
                    var url = "/github";
                    var content = JsonContent.Create(new { x_hub_signature_256 = x_hub_signature_256, x_github_event = x_github_event, x_github_delivery = x_github_delivery });
                    var response = await this.httpClient.PostAsync(url, content);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
        /// <summary>
        /// POST /{repository_id}/setup
        /// </summary>
                /// <param name="repository_id">repository_id parameter</param>
        public async Task<object> postsetup(string repository_id)
        {
                    var url = "/{repository_id}/setup";
                    var content = JsonContent.Create(repository_id);
                    var response = await this.httpClient.PostAsync(url, content);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
        /// <summary>
        /// GET /{repository_id}/status
        /// </summary>
                /// <param name="repository_id">repository_id parameter</param>
        public async Task<object> getstatus(string repository_id)
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
        /// DELETE /{repository_id}/webhook
        /// </summary>
                /// <param name="repository_id">repository_id parameter</param>
        public async Task<Dictionary<string, object>> deletewebhook(string repository_id)
        {
                    var url = "/{repository_id}/webhook";
                    var content = JsonContent.Create(repository_id);
                    var response = await this.httpClient.DeleteAsync(url);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
    }
}
