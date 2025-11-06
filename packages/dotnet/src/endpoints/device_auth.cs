using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Net.Http.Json;
using System.Threading.Tasks;

namespace TavoAI
{
    /// <summary>
    /// Client for device_auth endpoints
    /// </summary>
    public class DeviceAuthClient
    {
        private readonly HttpClient httpClient;

        /// <summary>
        /// Create a new device_auth client
        /// </summary>
        /// <param name="httpClient">HTTP client instance</param>
        public DeviceAuthClient(HttpClient httpClient)
        {
            this.httpClient = httpClient;
        }


        /// <summary>
        /// POST /code
        /// </summary>
                /// <param name="client_id">client_id parameter</param>
        /// <param name="client_name">client_name parameter</param>
        public async Task<Task<dict>> postcode(string? client_id = null, string? client_name = null)
        {'                    var url = "/code";\n                    var content = JsonContent.Create(new { "client_id", client_id, "client_name", client_name });\n                    var response = await this.httpClient.PostAsync(url, content);\n                    response.EnsureSuccessStatusCode();\n                    return await response.Content.ReadFromJsonAsync<object>();'}

        /// <summary>
        /// POST /token
        /// </summary>
                /// <param name="device_code">device_code parameter</param>
        public async Task<Task<dict>> posttoken(string device_code)
        {'                    var url = "/token";\n                    var content = JsonContent.Create(device_code);\n                    var response = await this.httpClient.PostAsync(url, content);\n                    response.EnsureSuccessStatusCode();\n                    return await response.Content.ReadFromJsonAsync<object>();'}

        /// <summary>
        /// GET /info
        /// </summary>
                /// <param name="user_code">user_code parameter</param>
        public async Task<Task<dict>> getinfo(string user_code)
        {'                    var queryParams = new Dictionary<string, object?> { "user_code", user_code };\n                    var queryString = string.Join("&", queryParams.Where(p => p.Value != null).Select(p => $"{p.Key}={Uri.EscapeDataString(p.Value.ToString())}"));\n                    var url = "/info" + (string.IsNullOrEmpty(queryString) ? "" : $"?{queryString}");\n                    var content = null;\n                    var response = await this.httpClient.GetAsync(url);\n                    response.EnsureSuccessStatusCode();\n                    return await response.Content.ReadFromJsonAsync<object>();'}

        /// <summary>
        /// POST /approve
        /// </summary>
        
        public async Task<Task<dict>> postapprove()
        {'                    var url = "/approve";\n                    var content = null;\n                    var response = await this.httpClient.PostAsync(url, content);\n                    response.EnsureSuccessStatusCode();\n                    return await response.Content.ReadFromJsonAsync<object>();'}

        /// <summary>
        /// POST /code/cli
        /// </summary>
                /// <param name="client_name">client_name parameter</param>
        public async Task<Task<dict>> postcodecli(string? client_name = null)
        {'                    var url = "/code/cli";\n                    var content = JsonContent.Create(client_name);\n                    var response = await this.httpClient.PostAsync(url, content);\n                    response.EnsureSuccessStatusCode();\n                    return await response.Content.ReadFromJsonAsync<object>();'}

        /// <summary>
        /// GET /code/{device_code}/status
        /// </summary>
                /// <param name="device_code">device_code parameter</param>
        public async Task<Task<dict>> getcode{device_code}status(string device_code)
        {'                    var queryParams = new Dictionary<string, object?> { "device_code", device_code };\n                    var queryString = string.Join("&", queryParams.Where(p => p.Value != null).Select(p => $"{p.Key}={Uri.EscapeDataString(p.Value.ToString())}"));\n                    var url = "/code/{device_code}/status" + (string.IsNullOrEmpty(queryString) ? "" : $"?{queryString}");\n                    var content = null;\n                    var response = await this.httpClient.GetAsync(url);\n                    response.EnsureSuccessStatusCode();\n                    return await response.Content.ReadFromJsonAsync<object>();'}

        /// <summary>
        /// GET /usage/warnings
        /// </summary>
        
        public async Task<Task<dict>> getusagewarnings()
        {'                    var url = "/usage/warnings";\n                    var content = null;\n                    var response = await this.httpClient.GetAsync(url);\n                    response.EnsureSuccessStatusCode();\n                    return await response.Content.ReadFromJsonAsync<object>();'}

        /// <summary>
        /// GET /limits
        /// </summary>
        
        public async Task<Task<dict>> getlimits()
        {'                    var url = "/limits";\n                    var content = null;\n                    var response = await this.httpClient.GetAsync(url);\n                    response.EnsureSuccessStatusCode();\n                    return await response.Content.ReadFromJsonAsync<object>();'}
    }
}
