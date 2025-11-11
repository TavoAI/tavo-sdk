using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Net.Http.Json;
using System.Threading.Tasks;

namespace TavoAI
{
    /// <summary>
    /// Client for ai_bulk_operations endpoints
    /// </summary>
    public class AiBulkOperationsClient
    {
        private readonly HttpClient httpClient;

        /// <summary>
        /// Create a new ai_bulk_operations client
        /// </summary>
        /// <param name="httpClient">HTTP client instance</param>
        public AiBulkOperationsClient(HttpClient httpClient)
        {
            this.httpClient = httpClient;
        }

        /// <summary>
        /// DELETE /bulk/delete
        /// </summary>
                /// <param name="analysis_ids">analysis_ids parameter</param>
        public async Task<Dictionary<string, object>> deletebulkdelete(List<string>? analysis_ids = null)
        {
                    var url = "/bulk/delete";
                    var content = JsonContent.Create(analysis_ids);
                    var response = await this.httpClient.DeleteAsync(url);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
        /// <summary>
        /// PUT /bulk/update-status
        /// </summary>
                /// <param name="analysis_updates">analysis_updates parameter</param>
        public async Task<Dictionary<string, object>> putbulkupdatestatus(List<object>? analysis_updates = null)
        {
                    var url = "/bulk/update-status";
                    var content = JsonContent.Create(analysis_updates);
                    var response = await this.httpClient.PutAsync(url, content);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
        /// <summary>
        /// GET /bulk/export
        /// </summary>
                /// <param name="analysis_ids">analysis_ids parameter</param>
        /// <param name="export_format">export_format parameter</param>
        public async Task<object> getbulkexport(List<string>? analysis_ids = null, string? export_format = null)
        {
                    var queryParams = new Dictionary<string, object?> { "analysis_ids", analysis_ids, "export_format", export_format };
                    var queryString = string.Join("&", queryParams.Where(p => p.Value != null).Select(p => $"{p.Key}={Uri.EscapeDataString(p.Value.ToString())}"));
                    var url = $"{formatted_path}" + (string.IsNullOrEmpty(queryString) ? "" : $"?{queryString}");
                    var content = null;
                    var response = await this.httpClient.GetAsync(url);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
    }
}
