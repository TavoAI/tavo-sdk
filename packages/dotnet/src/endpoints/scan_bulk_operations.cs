using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Net.Http.Json;
using System.Threading.Tasks;

namespace TavoAI
{
    /// <summary>
    /// Client for scan_bulk_operations endpoints
    /// </summary>
    public class ScanBulkOperationsClient
    {
        private readonly HttpClient httpClient;

        /// <summary>
        /// Create a new scan_bulk_operations client
        /// </summary>
        /// <param name="httpClient">HTTP client instance</param>
        public ScanBulkOperationsClient(HttpClient httpClient)
        {
            this.httpClient = httpClient;
        }

        /// <summary>
        /// POST /bulk/initiate
        /// </summary>
                /// <param name="scan_requests">scan_requests parameter</param>
        public async Task<Dictionary<string, object>> postbulkinitiate(List<object> scan_requests)
        {
                    var url = "/bulk/initiate";
                    var content = JsonContent.Create(scan_requests);
                    var response = await this.httpClient.PostAsync(url, content);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
        /// <summary>
        /// POST /bulk/cancel
        /// </summary>
                /// <param name="scan_ids">scan_ids parameter</param>
        public async Task<Dictionary<string, object>> postbulkcancel(List<string> scan_ids)
        {
                    var url = "/bulk/cancel";
                    var content = JsonContent.Create(scan_ids);
                    var response = await this.httpClient.PostAsync(url, content);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
        /// <summary>
        /// DELETE /bulk/delete
        /// </summary>
                /// <param name="scan_ids">scan_ids parameter</param>
        public async Task<Dictionary<string, object>> deletebulkdelete(List<string> scan_ids)
        {
                    var url = "/bulk/delete";
                    var content = JsonContent.Create(scan_ids);
                    var response = await this.httpClient.DeleteAsync(url);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
        /// <summary>
        /// GET /bulk/status
        /// </summary>
                /// <param name="scan_ids">scan_ids parameter</param>
        /// <param name="organization_id">organization_id parameter</param>
        /// <param name="status_filter">status_filter parameter</param>
        /// <param name="limit">limit parameter</param>
        public async Task<Dictionary<string, object>> getbulkstatus(List<string>? scan_ids = null, string? organization_id = null, string? status_filter = null, double? limit = null)
        {
                    var queryParams = new Dictionary<string, object?> { "scan_ids", scan_ids, "organization_id", organization_id, "status_filter", status_filter, "limit", limit };
                    var queryString = string.Join("&", queryParams.Where(p => p.Value != null).Select(p => $"{p.Key}={Uri.EscapeDataString(p.Value.ToString())}"));
                    var url = $"{formatted_path}" + (string.IsNullOrEmpty(queryString) ? "" : $"?{queryString}");
                    var content = null;
                    var response = await this.httpClient.GetAsync(url);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
    }
}
