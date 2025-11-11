using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Net.Http.Json;
using System.Threading.Tasks;

namespace TavoAI
{
    /// <summary>
    /// Client for jobs endpoints
    /// </summary>
    public class JobsClient
    {
        private readonly HttpClient httpClient;

        /// <summary>
        /// Create a new jobs client
        /// </summary>
        /// <param name="httpClient">HTTP client instance</param>
        public JobsClient(HttpClient httpClient)
        {
            this.httpClient = httpClient;
        }

        /// <summary>
        /// GET /status/{job_id}
        /// </summary>
                /// <param name="job_id">job_id parameter</param>
        public async Task<object> getstatus(string job_id)
        {
                    var queryParams = new Dictionary<string, object?> { "job_id", job_id };
                    var queryString = string.Join("&", queryParams.Where(p => p.Value != null).Select(p => $"{p.Key}={Uri.EscapeDataString(p.Value.ToString())}"));
                    var url = $"{formatted_path}" + (string.IsNullOrEmpty(queryString) ? "" : $"?{queryString}");
                    var content = null;
                    var response = await this.httpClient.GetAsync(url);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
        /// <summary>
        /// GET /dashboard
        /// </summary>
                /// <param name="limit">limit parameter</param>
        /// <param name="authorization">authorization parameter</param>
        /// <param name="x_api_key">x_api_key parameter</param>
        public async Task<object> getdashboard(double? limit = null, string? authorization = null, string? x_api_key = null)
        {
                    var queryParams = new Dictionary<string, object?> { "limit", limit, "authorization", authorization, "x_api_key", x_api_key };
                    var queryString = string.Join("&", queryParams.Where(p => p.Value != null).Select(p => $"{p.Key}={Uri.EscapeDataString(p.Value.ToString())}"));
                    var url = $"{formatted_path}" + (string.IsNullOrEmpty(queryString) ? "" : $"?{queryString}");
                    var content = null;
                    var response = await this.httpClient.GetAsync(url);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
    }
}
