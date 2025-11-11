using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Net.Http.Json;
using System.Threading.Tasks;

namespace TavoAI
{
    /// <summary>
    /// Client for scan_rules endpoints
    /// </summary>
    public class ScanRulesClient
    {
        private readonly HttpClient httpClient;

        /// <summary>
        /// Create a new scan_rules client
        /// </summary>
        /// <param name="httpClient">HTTP client instance</param>
        public ScanRulesClient(HttpClient httpClient)
        {
            this.httpClient = httpClient;
        }

        /// <summary>
        /// POST /rules
        /// </summary>
                /// <param name="rule_in">rule_in parameter</param>
        public async Task<object> postrules(object rule_in)
        {
                    var url = "/rules";
                    var content = JsonContent.Create(rule_in);
                    var response = await this.httpClient.PostAsync(url, content);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
        /// <summary>
        /// GET /rules
        /// </summary>
                /// <param name="skip">skip parameter</param>
        /// <param name="limit">limit parameter</param>
        /// <param name="tool_filter">tool_filter parameter</param>
        /// <param name="category_filter">category_filter parameter</param>
        /// <param name="severity_filter">severity_filter parameter</param>
        /// <param name="language_filter">language_filter parameter</param>
        /// <param name="is_active">is_active parameter</param>
        /// <param name="organization_id">organization_id parameter</param>
        public async Task<List<object>> getrules(double? skip = null, double? limit = null, string? tool_filter = null, string? category_filter = null, string? severity_filter = null, string? language_filter = null, bool? is_active = null, string? organization_id = null)
        {
                    var queryParams = new Dictionary<string, object?> { "skip", skip, "limit", limit, "tool_filter", tool_filter, "category_filter", category_filter, "severity_filter", severity_filter, "language_filter", language_filter, "is_active", is_active, "organization_id", organization_id };
                    var queryString = string.Join("&", queryParams.Where(p => p.Value != null).Select(p => $"{p.Key}={Uri.EscapeDataString(p.Value.ToString())}"));
                    var url = $"{formatted_path}" + (string.IsNullOrEmpty(queryString) ? "" : $"?{queryString}");
                    var content = null;
                    var response = await this.httpClient.GetAsync(url);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
        /// <summary>
        /// GET /rules/{rule_id}
        /// </summary>
                /// <param name="rule_id">rule_id parameter</param>
        public async Task<object> getrules(string rule_id)
        {
                    var queryParams = new Dictionary<string, object?> { "rule_id", rule_id };
                    var queryString = string.Join("&", queryParams.Where(p => p.Value != null).Select(p => $"{p.Key}={Uri.EscapeDataString(p.Value.ToString())}"));
                    var url = $"{formatted_path}" + (string.IsNullOrEmpty(queryString) ? "" : $"?{queryString}");
                    var content = null;
                    var response = await this.httpClient.GetAsync(url);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
        /// <summary>
        /// POST /rules/upload
        /// </summary>
                /// <param name="file">file parameter</param>
        /// <param name="organization_id">organization_id parameter</param>
        public async Task<object> postrulesupload(object? file = null, string? organization_id = null)
        {
                    var url = "/rules/upload";
                    var content = JsonContent.Create(new { file = file, organization_id = organization_id });
                    var response = await this.httpClient.PostAsync(url, content);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
        /// <summary>
        /// PUT /rules/{rule_id}
        /// </summary>
                /// <param name="rule_id">rule_id parameter</param>
        /// <param name="rule_update">rule_update parameter</param>
        public async Task<object> putrules(string rule_id, object rule_update)
        {
                    var url = "/rules/{rule_id}";
                    var content = JsonContent.Create(new { rule_id = rule_id, rule_update = rule_update });
                    var response = await this.httpClient.PutAsync(url, content);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
        /// <summary>
        /// DELETE /rules/{rule_id}
        /// </summary>
                /// <param name="rule_id">rule_id parameter</param>
        public async Task<object> deleterules(string rule_id)
        {
                    var url = "/rules/{rule_id}";
                    var content = JsonContent.Create(rule_id);
                    var response = await this.httpClient.DeleteAsync(url);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
    }
}
