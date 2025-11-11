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
        public async Task<object> postcode(string? client_id = null, string? client_name = null)
        {
                    var url = "/code";
                    var content = JsonContent.Create(new { client_id = client_id, client_name = client_name });
                    var response = await this.httpClient.PostAsync(url, content);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
        /// <summary>
        /// POST /token
        /// </summary>
                /// <param name="device_code">device_code parameter</param>
        public async Task<object> posttoken(string device_code)
        {
                    var url = "/token";
                    var content = JsonContent.Create(device_code);
                    var response = await this.httpClient.PostAsync(url, content);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
        /// <summary>
        /// GET /info
        /// </summary>
                /// <param name="user_code">user_code parameter</param>
        public async Task<object> getinfo(string user_code)
        {
                    var queryParams = new Dictionary<string, object?> { "user_code", user_code };
                    var queryString = string.Join("&", queryParams.Where(p => p.Value != null).Select(p => $"{p.Key}={Uri.EscapeDataString(p.Value.ToString())}"));
                    var url = $"{formatted_path}" + (string.IsNullOrEmpty(queryString) ? "" : $"?{queryString}");
                    var content = null;
                    var response = await this.httpClient.GetAsync(url);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
        /// <summary>
        /// POST /approve
        /// </summary>
        
        public async Task<object> postapprove()
        {
                    var url = "/approve";
                    var content = null;
                    var response = await this.httpClient.PostAsync(url, content);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
        /// <summary>
        /// POST /code/cli
        /// </summary>
                /// <param name="client_name">client_name parameter</param>
        public async Task<object> postcodecli(string? client_name = null)
        {
                    var url = "/code/cli";
                    var content = JsonContent.Create(client_name);
                    var response = await this.httpClient.PostAsync(url, content);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
        /// <summary>
        /// GET /code/{device_code}/status
        /// </summary>
                /// <param name="device_code">device_code parameter</param>
        public async Task<object> getcodestatus(string device_code)
        {
                    var queryParams = new Dictionary<string, object?> { "device_code", device_code };
                    var queryString = string.Join("&", queryParams.Where(p => p.Value != null).Select(p => $"{p.Key}={Uri.EscapeDataString(p.Value.ToString())}"));
                    var url = $"{formatted_path}" + (string.IsNullOrEmpty(queryString) ? "" : $"?{queryString}");
                    var content = null;
                    var response = await this.httpClient.GetAsync(url);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
        /// <summary>
        /// GET /usage/warnings
        /// </summary>
        
        public async Task<object> getusagewarnings()
        {
                    var url = "/usage/warnings";
                    var content = null;
                    var response = await this.httpClient.GetAsync(url);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
        /// <summary>
        /// GET /limits
        /// </summary>
        
        public async Task<object> getlimits()
        {
                    var url = "/limits";
                    var content = null;
                    var response = await this.httpClient.GetAsync(url);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
    }
}
