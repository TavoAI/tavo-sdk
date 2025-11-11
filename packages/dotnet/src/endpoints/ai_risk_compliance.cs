using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Net.Http.Json;
using System.Threading.Tasks;

namespace TavoAI
{
    /// <summary>
    /// Client for ai_risk_compliance endpoints
    /// </summary>
    public class AiRiskComplianceClient
    {
        private readonly HttpClient httpClient;

        /// <summary>
        /// Create a new ai_risk_compliance client
        /// </summary>
        /// <param name="httpClient">HTTP client instance</param>
        public AiRiskComplianceClient(HttpClient httpClient)
        {
            this.httpClient = httpClient;
        }

        /// <summary>
        /// GET /risk-scores
        /// </summary>
                /// <param name="skip">skip parameter</param>
        /// <param name="limit">limit parameter</param>
        /// <param name="scan_id">scan_id parameter</param>
        /// <param name="min_score">min_score parameter</param>
        /// <param name="max_score">max_score parameter</param>
        public async Task<Dictionary<string, object>> getriskscores(double? skip = null, double? limit = null, string? scan_id = null, double? min_score = null, double? max_score = null)
        {
                    var queryParams = new Dictionary<string, object?> { "skip", skip, "limit", limit, "scan_id", scan_id, "min_score", min_score, "max_score", max_score };
                    var queryString = string.Join("&", queryParams.Where(p => p.Value != null).Select(p => $"{p.Key}={Uri.EscapeDataString(p.Value.ToString())}"));
                    var url = $"{formatted_path}" + (string.IsNullOrEmpty(queryString) ? "" : $"?{queryString}");
                    var content = null;
                    var response = await this.httpClient.GetAsync(url);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
        /// <summary>
        /// GET /compliance-reports
        /// </summary>
                /// <param name="skip">skip parameter</param>
        /// <param name="limit">limit parameter</param>
        /// <param name="scan_id">scan_id parameter</param>
        /// <param name="framework">framework parameter</param>
        /// <param name="status">status parameter</param>
        public async Task<Dictionary<string, object>> getcompliancereports(double? skip = null, double? limit = null, string? scan_id = null, string? framework = null, string? status = null)
        {
                    var queryParams = new Dictionary<string, object?> { "skip", skip, "limit", limit, "scan_id", scan_id, "framework", framework, "status", status };
                    var queryString = string.Join("&", queryParams.Where(p => p.Value != null).Select(p => $"{p.Key}={Uri.EscapeDataString(p.Value.ToString())}"));
                    var url = $"{formatted_path}" + (string.IsNullOrEmpty(queryString) ? "" : $"?{queryString}");
                    var content = null;
                    var response = await this.httpClient.GetAsync(url);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
        /// <summary>
        /// GET /predictive-analyses
        /// </summary>
                /// <param name="skip">skip parameter</param>
        /// <param name="limit">limit parameter</param>
        /// <param name="scan_id">scan_id parameter</param>
        /// <param name="prediction_type">prediction_type parameter</param>
        /// <param name="confidence_threshold">confidence_threshold parameter</param>
        public async Task<Dictionary<string, object>> getpredictiveanalyses(double? skip = null, double? limit = null, string? scan_id = null, string? prediction_type = null, double? confidence_threshold = null)
        {
                    var queryParams = new Dictionary<string, object?> { "skip", skip, "limit", limit, "scan_id", scan_id, "prediction_type", prediction_type, "confidence_threshold", confidence_threshold };
                    var queryString = string.Join("&", queryParams.Where(p => p.Value != null).Select(p => $"{p.Key}={Uri.EscapeDataString(p.Value.ToString())}"));
                    var url = $"{formatted_path}" + (string.IsNullOrEmpty(queryString) ? "" : $"?{queryString}");
                    var content = null;
                    var response = await this.httpClient.GetAsync(url);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
    }
}
