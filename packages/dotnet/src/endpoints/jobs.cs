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
        public async Task<Task<JobStatus>> getstatus{job_id}(string job_id)
        {'                    var queryParams = new Dictionary<string, object?> { "job_id", job_id };\n                    var queryString = string.Join("&", queryParams.Where(p => p.Value != null).Select(p => $"{p.Key}={Uri.EscapeDataString(p.Value.ToString())}"));\n                    var url = "/status/{job_id}" + (string.IsNullOrEmpty(queryString) ? "" : $"?{queryString}");\n                    var content = null;\n                    var response = await this.httpClient.GetAsync(url);\n                    response.EnsureSuccessStatusCode();\n                    return await response.Content.ReadFromJsonAsync<object>();'}

        /// <summary>
        /// GET /dashboard
        /// </summary>
                /// <param name="limit">limit parameter</param>
        /// <param name="authorization">authorization parameter</param>
        /// <param name="x_api_key">x_api_key parameter</param>
        public async Task<Task<JobSummary>> getdashboard(double? limit = null, string? authorization = null, string? x_api_key = null)
        {'                    var queryParams = new Dictionary<string, object?> { "limit", limit, "authorization", authorization, "x_api_key", x_api_key };\n                    var queryString = string.Join("&", queryParams.Where(p => p.Value != null).Select(p => $"{p.Key}={Uri.EscapeDataString(p.Value.ToString())}"));\n                    var url = "/dashboard" + (string.IsNullOrEmpty(queryString) ? "" : $"?{queryString}");\n                    var content = null;\n                    var response = await this.httpClient.GetAsync(url);\n                    response.EnsureSuccessStatusCode();\n                    return await response.Content.ReadFromJsonAsync<object>();'}
    }
}
