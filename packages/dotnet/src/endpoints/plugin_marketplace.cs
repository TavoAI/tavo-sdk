using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Net.Http.Json;
using System.Threading.Tasks;

namespace TavoAI
{
    /// <summary>
    /// Client for plugin_marketplace endpoints
    /// </summary>
    public class PluginMarketplaceClient
    {
        private readonly HttpClient httpClient;

        /// <summary>
        /// Create a new plugin_marketplace client
        /// </summary>
        /// <param name="httpClient">HTTP client instance</param>
        public PluginMarketplaceClient(HttpClient httpClient)
        {
            this.httpClient = httpClient;
        }

        /// <summary>
        /// GET /marketplace
        /// </summary>
                /// <param name="plugin_type">plugin_type parameter</param>
        /// <param name="category">category parameter</param>
        /// <param name="pricing_tier">pricing_tier parameter</param>
        /// <param name="search">search parameter</param>
        /// <param name="is_official">is_official parameter</param>
        /// <param name="is_vetted">is_vetted parameter</param>
        /// <param name="min_rating">min_rating parameter</param>
        /// <param name="page">page parameter</param>
        /// <param name="per_page">per_page parameter</param>
        /// <param name="sort_by">sort_by parameter</param>
        /// <param name="sort_order">sort_order parameter</param>
        public async Task<object> getmarketplace(string? plugin_type = null, string? category = null, string? pricing_tier = null, string? search = null, bool? is_official = null, bool? is_vetted = null, double? min_rating = null, double? page = null, double? per_page = null, string? sort_by = null, string? sort_order = null)
        {
                    var queryParams = new Dictionary<string, object?> { "plugin_type", plugin_type, "category", category, "pricing_tier", pricing_tier, "search", search, "is_official", is_official, "is_vetted", is_vetted, "min_rating", min_rating, "page", page, "per_page", per_page, "sort_by", sort_by, "sort_order", sort_order };
                    var queryString = string.Join("&", queryParams.Where(p => p.Value != null).Select(p => $"{p.Key}={Uri.EscapeDataString(p.Value.ToString())}"));
                    var url = $"{formatted_path}" + (string.IsNullOrEmpty(queryString) ? "" : $"?{queryString}");
                    var content = null;
                    var response = await this.httpClient.GetAsync(url);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
        /// <summary>
        /// GET /{plugin_id}
        /// </summary>
                /// <param name="plugin_id">plugin_id parameter</param>
        public async Task<object> getroot(string plugin_id)
        {
                    var queryParams = new Dictionary<string, object?> { "plugin_id", plugin_id };
                    var queryString = string.Join("&", queryParams.Where(p => p.Value != null).Select(p => $"{p.Key}={Uri.EscapeDataString(p.Value.ToString())}"));
                    var url = $"{formatted_path}" + (string.IsNullOrEmpty(queryString) ? "" : $"?{queryString}");
                    var content = null;
                    var response = await this.httpClient.GetAsync(url);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
        /// <summary>
        /// POST /{plugin_id}/install
        /// </summary>
                /// <param name="plugin_id">plugin_id parameter</param>
        /// <param name="organization_id">organization_id parameter</param>
        public async Task<object> postinstall(string plugin_id, string? organization_id = null)
        {
                    var url = "/{plugin_id}/install";
                    var content = JsonContent.Create(new { plugin_id = plugin_id, organization_id = organization_id });
                    var response = await this.httpClient.PostAsync(url, content);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
        /// <summary>
        /// GET /{plugin_id}/download
        /// </summary>
                /// <param name="plugin_id">plugin_id parameter</param>
        /// <param name="version">version parameter</param>
        public async Task<object> getdownload(string plugin_id, string? version = null)
        {
                    var queryParams = new Dictionary<string, object?> { "plugin_id", plugin_id, "version", version };
                    var queryString = string.Join("&", queryParams.Where(p => p.Value != null).Select(p => $"{p.Key}={Uri.EscapeDataString(p.Value.ToString())}"));
                    var url = $"{formatted_path}" + (string.IsNullOrEmpty(queryString) ? "" : $"?{queryString}");
                    var content = null;
                    var response = await this.httpClient.GetAsync(url);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
        /// <summary>
        /// GET /installed
        /// </summary>
        
        public async Task<List<object>> getinstalled()
        {
                    var url = "/installed";
                    var content = null;
                    var response = await this.httpClient.GetAsync(url);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
        /// <summary>
        /// PUT /{plugin_id}
        /// </summary>
                /// <param name="plugin_id">plugin_id parameter</param>
        /// <param name="plugin_data">plugin_data parameter</param>
        public async Task<object> putroot(string plugin_id, object plugin_data)
        {
                    var url = "/{plugin_id}";
                    var content = JsonContent.Create(new { plugin_id = plugin_id, plugin_data = plugin_data });
                    var response = await this.httpClient.PutAsync(url, content);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
        /// <summary>
        /// DELETE /{plugin_id}
        /// </summary>
                /// <param name="plugin_id">plugin_id parameter</param>
        public async Task<object> deleteroot(string plugin_id)
        {
                    var url = "/{plugin_id}";
                    var content = JsonContent.Create(plugin_id);
                    var response = await this.httpClient.DeleteAsync(url);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
        /// <summary>
        /// POST /{plugin_id}/publish
        /// </summary>
                /// <param name="plugin_id">plugin_id parameter</param>
        public async Task<object> postpublish(string plugin_id)
        {
                    var url = "/{plugin_id}/publish";
                    var content = JsonContent.Create(plugin_id);
                    var response = await this.httpClient.PostAsync(url, content);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
        /// <summary>
        /// POST /{plugin_id}/versions
        /// </summary>
                /// <param name="plugin_id">plugin_id parameter</param>
        /// <param name="version_data">version_data parameter</param>
        public async Task<object> postversions(string plugin_id, object version_data)
        {
                    var url = "/{plugin_id}/versions";
                    var content = JsonContent.Create(new { plugin_id = plugin_id, version_data = version_data });
                    var response = await this.httpClient.PostAsync(url, content);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
        /// <summary>
        /// GET /{plugin_id}/versions
        /// </summary>
                /// <param name="plugin_id">plugin_id parameter</param>
        public async Task<List<object>> getversions(string plugin_id)
        {
                    var queryParams = new Dictionary<string, object?> { "plugin_id", plugin_id };
                    var queryString = string.Join("&", queryParams.Where(p => p.Value != null).Select(p => $"{p.Key}={Uri.EscapeDataString(p.Value.ToString())}"));
                    var url = $"{formatted_path}" + (string.IsNullOrEmpty(queryString) ? "" : $"?{queryString}");
                    var content = null;
                    var response = await this.httpClient.GetAsync(url);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
        /// <summary>
        /// GET /{plugin_id}/reviews
        /// </summary>
                /// <param name="plugin_id">plugin_id parameter</param>
        /// <param name="page">page parameter</param>
        /// <param name="limit">limit parameter</param>
        /// <param name="min_rating">min_rating parameter</param>
        /// <param name="sort_by">sort_by parameter</param>
        /// <param name="sort_order">sort_order parameter</param>
        public async Task<List<object>> getreviews(string plugin_id, double? page = null, double? limit = null, double? min_rating = null, string? sort_by = null, string? sort_order = null)
        {
                    var queryParams = new Dictionary<string, object?> { "plugin_id", plugin_id, "page", page, "limit", limit, "min_rating", min_rating, "sort_by", sort_by, "sort_order", sort_order };
                    var queryString = string.Join("&", queryParams.Where(p => p.Value != null).Select(p => $"{p.Key}={Uri.EscapeDataString(p.Value.ToString())}"));
                    var url = $"{formatted_path}" + (string.IsNullOrEmpty(queryString) ? "" : $"?{queryString}");
                    var content = null;
                    var response = await this.httpClient.GetAsync(url);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
        /// <summary>
        /// POST /{plugin_id}/reviews
        /// </summary>
                /// <param name="plugin_id">plugin_id parameter</param>
        /// <param name="review_data">review_data parameter</param>
        public async Task<object> postreviews(string plugin_id, object review_data)
        {
                    var url = "/{plugin_id}/reviews";
                    var content = JsonContent.Create(new { plugin_id = plugin_id, review_data = review_data });
                    var response = await this.httpClient.PostAsync(url, content);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
        /// <summary>
        /// GET /{plugin_id}/reviews/{review_id}
        /// </summary>
                /// <param name="plugin_id">plugin_id parameter</param>
        /// <param name="review_id">review_id parameter</param>
        public async Task<object> getreviews(string plugin_id, string review_id)
        {
                    var queryParams = new Dictionary<string, object?> { "plugin_id", plugin_id, "review_id", review_id };
                    var queryString = string.Join("&", queryParams.Where(p => p.Value != null).Select(p => $"{p.Key}={Uri.EscapeDataString(p.Value.ToString())}"));
                    var url = $"{formatted_path}" + (string.IsNullOrEmpty(queryString) ? "" : $"?{queryString}");
                    var content = null;
                    var response = await this.httpClient.GetAsync(url);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
        /// <summary>
        /// PUT /{plugin_id}/reviews/{review_id}
        /// </summary>
                /// <param name="plugin_id">plugin_id parameter</param>
        /// <param name="review_id">review_id parameter</param>
        /// <param name="review_update">review_update parameter</param>
        public async Task<object> putreviews(string plugin_id, string review_id, object review_update)
        {
                    var url = "/{plugin_id}/reviews/{review_id}";
                    var content = JsonContent.Create(new { plugin_id = plugin_id, review_id = review_id, review_update = review_update });
                    var response = await this.httpClient.PutAsync(url, content);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
        /// <summary>
        /// DELETE /{plugin_id}/reviews/{review_id}
        /// </summary>
                /// <param name="plugin_id">plugin_id parameter</param>
        /// <param name="review_id">review_id parameter</param>
        public async Task<object> deletereviews(string plugin_id, string review_id)
        {
                    var url = "/{plugin_id}/reviews/{review_id}";
                    var content = JsonContent.Create(new { plugin_id = plugin_id, review_id = review_id });
                    var response = await this.httpClient.DeleteAsync(url);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
        /// <summary>
        /// POST /{plugin_id}/reviews/{review_id}/helpful
        /// </summary>
                /// <param name="plugin_id">plugin_id parameter</param>
        /// <param name="review_id">review_id parameter</param>
        public async Task<object> postreviewshelpful(string plugin_id, string review_id)
        {
                    var url = "/{plugin_id}/reviews/{review_id}/helpful";
                    var content = JsonContent.Create(new { plugin_id = plugin_id, review_id = review_id });
                    var response = await this.httpClient.PostAsync(url, content);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
    }
}
