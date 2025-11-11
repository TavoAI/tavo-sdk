using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Net.Http.Json;
using System.Threading.Tasks;

namespace TavoAI
{
    /// <summary>
    /// Client for ai_results_export endpoints
    /// </summary>
    public class AiResultsExportClient
    {
        private readonly HttpClient httpClient;

        /// <summary>
        /// Create a new ai_results_export client
        /// </summary>
        /// <param name="httpClient">HTTP client instance</param>
        public AiResultsExportClient(HttpClient httpClient)
        {
            this.httpClient = httpClient;
        }

        /// <summary>
        /// GET /results
        /// </summary>
                /// <param name="skip">skip parameter</param>
        /// <param name="limit">limit parameter</param>
        /// <param name="scan_id">scan_id parameter</param>
        /// <param name="analysis_type">analysis_type parameter</param>
        /// <param name="severity">severity parameter</param>
        /// <param name="start_date">start_date parameter</param>
        /// <param name="end_date">end_date parameter</param>
        public async Task<Dictionary<string, object>> getresults(double? skip = null, double? limit = null, string? scan_id = null, string? analysis_type = null, string? severity = null, string? start_date = null, string? end_date = null)
        {
                    var queryParams = new Dictionary<string, object?> { "skip", skip, "limit", limit, "scan_id", scan_id, "analysis_type", analysis_type, "severity", severity, "start_date", start_date, "end_date", end_date };
                    var queryString = string.Join("&", queryParams.Where(p => p.Value != null).Select(p => $"{p.Key}={Uri.EscapeDataString(p.Value.ToString())}"));
                    var url = $"{formatted_path}" + (string.IsNullOrEmpty(queryString) ? "" : $"?{queryString}");
                    var content = null;
                    var response = await this.httpClient.GetAsync(url);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
        /// <summary>
        /// GET /results/export
        /// </summary>
                /// <param name="format">format parameter</param>
        /// <param name="scan_id">scan_id parameter</param>
        /// <param name="analysis_type">analysis_type parameter</param>
        /// <param name="start_date">start_date parameter</param>
        /// <param name="end_date">end_date parameter</param>
        public async Task<object> getresultsexport(string? format = null, string? scan_id = null, string? analysis_type = null, string? start_date = null, string? end_date = null)
        {
                    var queryParams = new Dictionary<string, object?> { "format", format, "scan_id", scan_id, "analysis_type", analysis_type, "start_date", start_date, "end_date", end_date };
                    var queryString = string.Join("&", queryParams.Where(p => p.Value != null).Select(p => $"{p.Key}={Uri.EscapeDataString(p.Value.ToString())}"));
                    var url = $"{formatted_path}" + (string.IsNullOrEmpty(queryString) ? "" : $"?{queryString}");
                    var content = null;
                    var response = await this.httpClient.GetAsync(url);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
    }
}
