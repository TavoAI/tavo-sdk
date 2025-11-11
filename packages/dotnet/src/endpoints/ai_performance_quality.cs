using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Net.Http.Json;
using System.Threading.Tasks;

namespace TavoAI
{
    /// <summary>
    /// Client for ai_performance_quality endpoints
    /// </summary>
    public class AiPerformanceQualityClient
    {
        private readonly HttpClient httpClient;

        /// <summary>
        /// Create a new ai_performance_quality client
        /// </summary>
        /// <param name="httpClient">HTTP client instance</param>
        public AiPerformanceQualityClient(HttpClient httpClient)
        {
            this.httpClient = httpClient;
        }

        /// <summary>
        /// GET /performance-metrics
        /// </summary>
                /// <param name="start_date">start_date parameter</param>
        /// <param name="end_date">end_date parameter</param>
        /// <param name="analysis_type">analysis_type parameter</param>
        public async Task<Dictionary<string, object>> getperformancemetrics(string? start_date = null, string? end_date = null, string? analysis_type = null)
        {
                    var queryParams = new Dictionary<string, object?> { "start_date", start_date, "end_date", end_date, "analysis_type", analysis_type };
                    var queryString = string.Join("&", queryParams.Where(p => p.Value != null).Select(p => $"{p.Key}={Uri.EscapeDataString(p.Value.ToString())}"));
                    var url = $"{formatted_path}" + (string.IsNullOrEmpty(queryString) ? "" : $"?{queryString}");
                    var content = null;
                    var response = await this.httpClient.GetAsync(url);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
        /// <summary>
        /// GET /quality-review/{scan_id}
        /// </summary>
                /// <param name="scan_id">scan_id parameter</param>
        public async Task<Dictionary<string, object>> getqualityreview(string scan_id)
        {
                    var queryParams = new Dictionary<string, object?> { "scan_id", scan_id };
                    var queryString = string.Join("&", queryParams.Where(p => p.Value != null).Select(p => $"{p.Key}={Uri.EscapeDataString(p.Value.ToString())}"));
                    var url = $"{formatted_path}" + (string.IsNullOrEmpty(queryString) ? "" : $"?{queryString}");
                    var content = null;
                    var response = await this.httpClient.GetAsync(url);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
    }
}
