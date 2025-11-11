using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Net.Http.Json;
using System.Threading.Tasks;

namespace TavoAI
{
    /// <summary>
    /// Client for scan_management endpoints
    /// </summary>
    public class ScanManagementClient
    {
        private readonly HttpClient httpClient;

        /// <summary>
        /// Create a new scan_management client
        /// </summary>
        /// <param name="httpClient">HTTP client instance</param>
        public ScanManagementClient(HttpClient httpClient)
        {
            this.httpClient = httpClient;
        }

        /// <summary>
        /// POST /
        /// </summary>
                /// <param name="scan_in">scan_in parameter</param>
        public async Task<object> postroot(object scan_in)
        {
                    var url = "/";
                    var content = JsonContent.Create(scan_in);
                    var response = await this.httpClient.PostAsync(url, content);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
        /// <summary>
        /// GET /
        /// </summary>
                /// <param name="skip">skip parameter</param>
        /// <param name="limit">limit parameter</param>
        /// <param name="status_filter">status_filter parameter</param>
        /// <param name="organization_id">organization_id parameter</param>
        public async Task<List<object>> getroot(double? skip = null, double? limit = null, string? status_filter = null, string? organization_id = null)
        {
                    var queryParams = new Dictionary<string, object?> { "skip", skip, "limit", limit, "status_filter", status_filter, "organization_id", organization_id };
                    var queryString = string.Join("&", queryParams.Where(p => p.Value != null).Select(p => $"{p.Key}={Uri.EscapeDataString(p.Value.ToString())}"));
                    var url = $"{formatted_path}" + (string.IsNullOrEmpty(queryString) ? "" : $"?{queryString}");
                    var content = null;
                    var response = await this.httpClient.GetAsync(url);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
        /// <summary>
        /// GET /{scan_id:uuid}
        /// </summary>
                /// <param name="scan_id">scan_id parameter</param>
        public async Task<Dictionary<string, object>> getroot(string scan_id)
        {
                    var queryParams = new Dictionary<string, object?> { "scan_id", scan_id };
                    var queryString = string.Join("&", queryParams.Where(p => p.Value != null).Select(p => $"{p.Key}={Uri.EscapeDataString(p.Value.ToString())}"));
                    var url = $"{formatted_path}" + (string.IsNullOrEmpty(queryString) ? "" : $"?{queryString}");
                    var content = null;
                    var response = await this.httpClient.GetAsync(url);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
        /// <summary>
        /// GET /{scan_id:uuid}/results
        /// </summary>
                /// <param name="scan_id">scan_id parameter</param>
        /// <param name="severity_filter">severity_filter parameter</param>
        /// <param name="rule_type_filter">rule_type_filter parameter</param>
        /// <param name="limit">limit parameter</param>
        public async Task<List<object>> getresults(string scan_id, string? severity_filter = null, string? rule_type_filter = null, double? limit = null)
        {
                    var queryParams = new Dictionary<string, object?> { "scan_id", scan_id, "severity_filter", severity_filter, "rule_type_filter", rule_type_filter, "limit", limit };
                    var queryString = string.Join("&", queryParams.Where(p => p.Value != null).Select(p => $"{p.Key}={Uri.EscapeDataString(p.Value.ToString())}"));
                    var url = $"{formatted_path}" + (string.IsNullOrEmpty(queryString) ? "" : $"?{queryString}");
                    var content = null;
                    var response = await this.httpClient.GetAsync(url);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
        /// <summary>
        /// POST /{scan_id:uuid}/cancel
        /// </summary>
                /// <param name="scan_id">scan_id parameter</param>
        public async Task<object> postcancel(string scan_id)
        {
                    var url = "/{scan_id:uuid}/cancel";
                    var content = JsonContent.Create(scan_id);
                    var response = await this.httpClient.PostAsync(url, content);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
    }
}
