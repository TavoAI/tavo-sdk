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
        
        public async Task<Task<Dict[str, Any]>> gethealth()
        {'                    var url = "/health";\n                    var content = null;\n                    var response = await this.httpClient.GetAsync(url);\n                    response.EnsureSuccessStatusCode();\n                    return await response.Content.ReadFromJsonAsync<object>();'}

        /// <summary>
        /// GET /health/ready
        /// </summary>
        
        public async Task<Task<Dict[str, Any]>> gethealthready()
        {'                    var url = "/health/ready";\n                    var content = null;\n                    var response = await this.httpClient.GetAsync(url);\n                    response.EnsureSuccessStatusCode();\n                    return await response.Content.ReadFromJsonAsync<object>();'}

        /// <summary>
        /// GET /health/live
        /// </summary>
        
        public async Task<Task<Dict[str, Any]>> gethealthlive()
        {'                    var url = "/health/live";\n                    var content = null;\n                    var response = await this.httpClient.GetAsync(url);\n                    response.EnsureSuccessStatusCode();\n                    return await response.Content.ReadFromJsonAsync<object>();'}
    }
}
