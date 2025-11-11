using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Net.Http.Json;
using System.Threading.Tasks;

namespace TavoAI
{
    /// <summary>
    /// Client for ai_analysis_core endpoints
    /// </summary>
    public class AiAnalysisCoreClient
    {
        private readonly HttpClient httpClient;

        /// <summary>
        /// Create a new ai_analysis_core client
        /// </summary>
        /// <param name="httpClient">HTTP client instance</param>
        public AiAnalysisCoreClient(HttpClient httpClient)
        {
            this.httpClient = httpClient;
        }

        /// <summary>
        /// GET /analyses
        /// </summary>
                /// <param name="skip">skip parameter</param>
        /// <param name="limit">limit parameter</param>
        /// <param name="scan_id">scan_id parameter</param>
        /// <param name="analysis_type">analysis_type parameter</param>
        /// <param name="status">status parameter</param>
        /// <param name="start_date">start_date parameter</param>
        /// <param name="end_date">end_date parameter</param>
        public async Task<Dictionary<string, object>> getanalyses(double? skip = null, double? limit = null, string? scan_id = null, string? analysis_type = null, string? status = null, string? start_date = null, string? end_date = null)
        {
                    var queryParams = new Dictionary<string, object?> { "skip", skip, "limit", limit, "scan_id", scan_id, "analysis_type", analysis_type, "status", status, "start_date", start_date, "end_date", end_date };
                    var queryString = string.Join("&", queryParams.Where(p => p.Value != null).Select(p => $"{p.Key}={Uri.EscapeDataString(p.Value.ToString())}"));
                    var url = $"{formatted_path}" + (string.IsNullOrEmpty(queryString) ? "" : $"?{queryString}");
                    var content = null;
                    var response = await this.httpClient.GetAsync(url);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
        /// <summary>
        /// GET /analyses/{analysis_id}
        /// </summary>
                /// <param name="analysis_id">analysis_id parameter</param>
        public async Task<Dictionary<string, object>> getanalyses(string analysis_id)
        {
                    var queryParams = new Dictionary<string, object?> { "analysis_id", analysis_id };
                    var queryString = string.Join("&", queryParams.Where(p => p.Value != null).Select(p => $"{p.Key}={Uri.EscapeDataString(p.Value.ToString())}"));
                    var url = $"{formatted_path}" + (string.IsNullOrEmpty(queryString) ? "" : $"?{queryString}");
                    var content = null;
                    var response = await this.httpClient.GetAsync(url);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
    }
}
