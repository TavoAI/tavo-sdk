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
        public async Task<Task<Dict[str, Any]>> postgithub(string? x_hub_signature_256 = null, string? x_github_event = null, string? x_github_delivery = null)
        {'                    var url = "/github";\n                    var content = JsonContent.Create(new { "x_hub_signature_256", x_hub_signature_256, "x_github_event", x_github_event, "x_github_delivery", x_github_delivery });\n                    var response = await this.httpClient.PostAsync(url, content);\n                    response.EnsureSuccessStatusCode();\n                    return await response.Content.ReadFromJsonAsync<object>();'}

        /// <summary>
        /// POST /{repository_id}/setup
        /// </summary>
                /// <param name="repository_id">repository_id parameter</param>
        public async Task<Task<WebhookSetupResponse>> post{repository_id}setup(string repository_id)
        {'                    var url = "/{repository_id}/setup";\n                    var content = JsonContent.Create(repository_id);\n                    var response = await this.httpClient.PostAsync(url, content);\n                    response.EnsureSuccessStatusCode();\n                    return await response.Content.ReadFromJsonAsync<object>();'}

        /// <summary>
        /// GET /{repository_id}/status
        /// </summary>
                /// <param name="repository_id">repository_id parameter</param>
        public async Task<Task<WebhookStatusResponse>> get{repository_id}status(string repository_id)
        {'                    var queryParams = new Dictionary<string, object?> { "repository_id", repository_id };\n                    var queryString = string.Join("&", queryParams.Where(p => p.Value != null).Select(p => $"{p.Key}={Uri.EscapeDataString(p.Value.ToString())}"));\n                    var url = "/{repository_id}/status" + (string.IsNullOrEmpty(queryString) ? "" : $"?{queryString}");\n                    var content = null;\n                    var response = await this.httpClient.GetAsync(url);\n                    response.EnsureSuccessStatusCode();\n                    return await response.Content.ReadFromJsonAsync<object>();'}

        /// <summary>
        /// DELETE /{repository_id}/webhook
        /// </summary>
                /// <param name="repository_id">repository_id parameter</param>
        public async Task<Task<Dict[str, str]>> delete{repository_id}webhook(string repository_id)
        {'                    var url = "/{repository_id}/webhook";\n                    var content = JsonContent.Create(repository_id);\n                    var response = await this.httpClient.DeleteAsync(url);\n                    response.EnsureSuccessStatusCode();\n                    return await response.Content.ReadFromJsonAsync<object>();'}
    }
}
