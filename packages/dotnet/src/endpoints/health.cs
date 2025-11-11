using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Net.Http.Json;
using System.Threading.Tasks;

namespace TavoAI
{
    /// <summary>
    /// Client for health endpoints
    /// </summary>
    public class HealthClient
    {
        private readonly HttpClient httpClient;

        /// <summary>
        /// Create a new health client
        /// </summary>
        /// <param name="httpClient">HTTP client instance</param>
        public HealthClient(HttpClient httpClient)
        {
            this.httpClient = httpClient;
        }

        /// <summary>
        /// GET /health
        /// </summary>
        
        public async Task<Dictionary<string, object>> gethealth()
        {
                    var url = "/health";
                    var content = null;
                    var response = await this.httpClient.GetAsync(url);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
        /// <summary>
        /// GET /health/ready
        /// </summary>
        
        public async Task<Dictionary<string, object>> gethealthready()
        {
                    var url = "/health/ready";
                    var content = null;
                    var response = await this.httpClient.GetAsync(url);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
        /// <summary>
        /// GET /health/live
        /// </summary>
        
        public async Task<Dictionary<string, object>> gethealthlive()
        {
                    var url = "/health/live";
                    var content = null;
                    var response = await this.httpClient.GetAsync(url);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
    }
}
