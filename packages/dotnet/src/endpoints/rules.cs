using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Net.Http.Json;
using System.Threading.Tasks;

namespace TavoAI
{
    /// <summary>
    /// Client for rules endpoints
    /// </summary>
    public class RulesClient
    {
        private readonly HttpClient httpClient;

        /// <summary>
        /// Create a new rules client
        /// </summary>
        /// <param name="httpClient">HTTP client instance</param>
        public RulesClient(HttpClient httpClient)
        {
            this.httpClient = httpClient;
        }

        /// <summary>
        /// GET /bundles
        /// </summary>
                /// <param name="category">category parameter</param>
        /// <param name="official_only">official_only parameter</param>
        /// <param name="page">page parameter</param>
        /// <param name="per_page">per_page parameter</param>
        public async Task<object> getbundles(string? category = null, bool? official_only = null, double? page = null, double? per_page = null)
        {
                    var queryParams = new Dictionary<string, object?> { "category", category, "official_only", official_only, "page", page, "per_page", per_page };
                    var queryString = string.Join("&", queryParams.Where(p => p.Value != null).Select(p => $"{p.Key}={Uri.EscapeDataString(p.Value.ToString())}"));
                    var url = $"{formatted_path}" + (string.IsNullOrEmpty(queryString) ? "" : $"?{queryString}");
                    var content = null;
                    var response = await this.httpClient.GetAsync(url);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
        /// <summary>
        /// POST /bundles/{bundle_id}/install
        /// </summary>
                /// <param name="bundle_id">bundle_id parameter</param>
        /// <param name="installation">installation parameter</param>
        public async Task<object> postbundlesinstall(string bundle_id, object installation)
        {
                    var url = "/bundles/{bundle_id}/install";
                    var content = JsonContent.Create(new { bundle_id = bundle_id, installation = installation });
                    var response = await this.httpClient.PostAsync(url, content);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
        /// <summary>
        /// GET /bundles/{bundle_id}/rules
        /// </summary>
                /// <param name="bundle_id">bundle_id parameter</param>
        public async Task<List<object>> getbundlesrules(string bundle_id)
        {
                    var queryParams = new Dictionary<string, object?> { "bundle_id", bundle_id };
                    var queryString = string.Join("&", queryParams.Where(p => p.Value != null).Select(p => $"{p.Key}={Uri.EscapeDataString(p.Value.ToString())}"));
                    var url = $"{formatted_path}" + (string.IsNullOrEmpty(queryString) ? "" : $"?{queryString}");
                    var content = null;
                    var response = await this.httpClient.GetAsync(url);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
        /// <summary>
        /// POST /validate
        /// </summary>
        
        public async Task<object> postvalidate()
        {
                    var url = "/validate";
                    var content = null;
                    var response = await this.httpClient.PostAsync(url, content);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
        /// <summary>
        /// GET /updates
        /// </summary>
        
        public async Task<List<object>> getupdates()
        {
                    var url = "/updates";
                    var content = null;
                    var response = await this.httpClient.GetAsync(url);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
        /// <summary>
        /// DELETE /bundles/{bundle_id}/install
        /// </summary>
                /// <param name="bundle_id">bundle_id parameter</param>
        public async Task<object> deletebundlesinstall(string bundle_id)
        {
                    var url = "/bundles/{bundle_id}/install";
                    var content = JsonContent.Create(bundle_id);
                    var response = await this.httpClient.DeleteAsync(url);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
        /// <summary>
        /// GET /organizations/{organization_id}/bundles
        /// </summary>
                /// <param name="organization_id">organization_id parameter</param>
        public async Task<List<object>> getorganizationsbundles(string organization_id)
        {
                    var queryParams = new Dictionary<string, object?> { "organization_id", organization_id };
                    var queryString = string.Join("&", queryParams.Where(p => p.Value != null).Select(p => $"{p.Key}={Uri.EscapeDataString(p.Value.ToString())}"));
                    var url = $"{formatted_path}" + (string.IsNullOrEmpty(queryString) ? "" : $"?{queryString}");
                    var content = null;
                    var response = await this.httpClient.GetAsync(url);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
        /// <summary>
        /// POST /organizations/{organization_id}/bundles/{bundle_id}/install
        /// </summary>
                /// <param name="organization_id">organization_id parameter</param>
        /// <param name="bundle_id">bundle_id parameter</param>
        public async Task<object> postorganizationsbundlesinstall(string organization_id, string bundle_id)
        {
                    var url = "/organizations/{organization_id}/bundles/{bundle_id}/install";
                    var content = JsonContent.Create(new { organization_id = organization_id, bundle_id = bundle_id });
                    var response = await this.httpClient.PostAsync(url, content);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
        /// <summary>
        /// DELETE /organizations/{organization_id}/bundles/{bundle_id}
        /// </summary>
                /// <param name="organization_id">organization_id parameter</param>
        /// <param name="bundle_id">bundle_id parameter</param>
        public async Task<object> deleteorganizationsbundles(string organization_id, string bundle_id)
        {
                    var url = "/organizations/{organization_id}/bundles/{bundle_id}";
                    var content = JsonContent.Create(new { organization_id = organization_id, bundle_id = bundle_id });
                    var response = await this.httpClient.DeleteAsync(url);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
        /// <summary>
        /// GET /organizations/{organization_id}/rules
        /// </summary>
                /// <param name="organization_id">organization_id parameter</param>
        /// <param name="category">category parameter</param>
        /// <param name="severity">severity parameter</param>
        public async Task<List<object>> getorganizationsrules(string organization_id, string? category = null, string? severity = null)
        {
                    var queryParams = new Dictionary<string, object?> { "organization_id", organization_id, "category", category, "severity", severity };
                    var queryString = string.Join("&", queryParams.Where(p => p.Value != null).Select(p => $"{p.Key}={Uri.EscapeDataString(p.Value.ToString())}"));
                    var url = $"{formatted_path}" + (string.IsNullOrEmpty(queryString) ? "" : $"?{queryString}");
                    var content = null;
                    var response = await this.httpClient.GetAsync(url);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
        /// <summary>
        /// GET /organizations/{organization_id}/rules/stats
        /// </summary>
                /// <param name="organization_id">organization_id parameter</param>
        public async Task<object> getorganizationsrulesstats(string organization_id)
        {
                    var queryParams = new Dictionary<string, object?> { "organization_id", organization_id };
                    var queryString = string.Join("&", queryParams.Where(p => p.Value != null).Select(p => $"{p.Key}={Uri.EscapeDataString(p.Value.ToString())}"));
                    var url = $"{formatted_path}" + (string.IsNullOrEmpty(queryString) ? "" : $"?{queryString}");
                    var content = null;
                    var response = await this.httpClient.GetAsync(url);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
    }
}
