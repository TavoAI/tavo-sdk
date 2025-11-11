using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Net.Http.Json;
using System.Threading.Tasks;

namespace TavoAI
{
    /// <summary>
    /// Client for registry endpoints
    /// </summary>
    public class RegistryClient
    {
        private readonly HttpClient httpClient;

        /// <summary>
        /// Create a new registry client
        /// </summary>
        /// <param name="httpClient">HTTP client instance</param>
        public RegistryClient(HttpClient httpClient)
        {
            this.httpClient = httpClient;
        }

        /// <summary>
        /// GET /marketplace
        /// </summary>
        
        public async Task<object> getmarketplace()
        {
                    var url = "/marketplace";
                    var content = null;
                    var response = await this.httpClient.GetAsync(url);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
        /// <summary>
        /// GET /categories
        /// </summary>
        
        public async Task<List<object>> getcategories()
        {
                    var url = "/categories";
                    var content = null;
                    var response = await this.httpClient.GetAsync(url);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
        /// <summary>
        /// POST /bundles
        /// </summary>
                /// <param name="bundle">bundle parameter</param>
        public async Task<object> postbundles(object bundle)
        {
                    var url = "/bundles";
                    var content = JsonContent.Create(bundle);
                    var response = await this.httpClient.PostAsync(url, content);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
        /// <summary>
        /// GET /bundles/{bundle_id}
        /// </summary>
                /// <param name="bundle_id">bundle_id parameter</param>
        public async Task<object> getbundles(string bundle_id)
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
        /// PUT /bundles/{bundle_id}
        /// </summary>
                /// <param name="bundle_id">bundle_id parameter</param>
        /// <param name="bundle_update">bundle_update parameter</param>
        public async Task<object> putbundles(string bundle_id, object bundle_update)
        {
                    var url = "/bundles/{bundle_id}";
                    var content = JsonContent.Create(new { bundle_id = bundle_id, bundle_update = bundle_update });
                    var response = await this.httpClient.PutAsync(url, content);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
        /// <summary>
        /// DELETE /bundles/{bundle_id}
        /// </summary>
                /// <param name="bundle_id">bundle_id parameter</param>
        public async Task<object> deletebundles(string bundle_id)
        {
                    var url = "/bundles/{bundle_id}";
                    var content = JsonContent.Create(bundle_id);
                    var response = await this.httpClient.DeleteAsync(url);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
        /// <summary>
        /// GET /bundles/{bundle_id}/download
        /// </summary>
                /// <param name="bundle_id">bundle_id parameter</param>
        public async Task<object> getbundlesdownload(string bundle_id)
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
        /// GET /my-bundles
        /// </summary>
        
        public async Task<List<object>> getmybundles()
        {
                    var url = "/my-bundles";
                    var content = null;
                    var response = await this.httpClient.GetAsync(url);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
        /// <summary>
        /// POST /execute/code-rule
        /// </summary>
        
        public async Task<object> postexecutecoderule()
        {
                    var url = "/execute/code-rule";
                    var content = null;
                    var response = await this.httpClient.PostAsync(url, content);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
        /// <summary>
        /// GET /executions/{execution_id}
        /// </summary>
                /// <param name="execution_id">execution_id parameter</param>
        public async Task<object> getexecutions(string execution_id)
        {
                    var queryParams = new Dictionary<string, object?> { "execution_id", execution_id };
                    var queryString = string.Join("&", queryParams.Where(p => p.Value != null).Select(p => $"{p.Key}={Uri.EscapeDataString(p.Value.ToString())}"));
                    var url = $"{formatted_path}" + (string.IsNullOrEmpty(queryString) ? "" : $"?{queryString}");
                    var content = null;
                    var response = await this.httpClient.GetAsync(url);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
        /// <summary>
        /// GET /my-executions
        /// </summary>
                /// <param name="page">page parameter</param>
        /// <param name="per_page">per_page parameter</param>
        public async Task<object> getmyexecutions(double? page = null, double? per_page = null)
        {
                    var queryParams = new Dictionary<string, object?> { "page", page, "per_page", per_page };
                    var queryString = string.Join("&", queryParams.Where(p => p.Value != null).Select(p => $"{p.Key}={Uri.EscapeDataString(p.Value.ToString())}"));
                    var url = $"{formatted_path}" + (string.IsNullOrEmpty(queryString) ? "" : $"?{queryString}");
                    var content = null;
                    var response = await this.httpClient.GetAsync(url);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
        /// <summary>
        /// POST /bundles/{bundle_id}/rate
        /// </summary>
                /// <param name="bundle_id">bundle_id parameter</param>
        /// <param name="rating">rating parameter</param>
        public async Task<object> postbundlesrate(string bundle_id, object rating)
        {
                    var url = "/bundles/{bundle_id}/rate";
                    var content = JsonContent.Create(new { bundle_id = bundle_id, rating = rating });
                    var response = await this.httpClient.PostAsync(url, content);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
        /// <summary>
        /// POST /bundles/{bundle_id}/review
        /// </summary>
                /// <param name="bundle_id">bundle_id parameter</param>
        /// <param name="review">review parameter</param>
        public async Task<object> postbundlesreview(string bundle_id, object review)
        {
                    var url = "/bundles/{bundle_id}/review";
                    var content = JsonContent.Create(new { bundle_id = bundle_id, review = review });
                    var response = await this.httpClient.PostAsync(url, content);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
        /// <summary>
        /// GET /bundles/{bundle_id}/reviews
        /// </summary>
                /// <param name="bundle_id">bundle_id parameter</param>
        /// <param name="page">page parameter</param>
        /// <param name="per_page">per_page parameter</param>
        public async Task<object> getbundlesreviews(string bundle_id, double? page = null, double? per_page = null)
        {
                    var queryParams = new Dictionary<string, object?> { "bundle_id", bundle_id, "page", page, "per_page", per_page };
                    var queryString = string.Join("&", queryParams.Where(p => p.Value != null).Select(p => $"{p.Key}={Uri.EscapeDataString(p.Value.ToString())}"));
                    var url = $"{formatted_path}" + (string.IsNullOrEmpty(queryString) ? "" : $"?{queryString}");
                    var content = null;
                    var response = await this.httpClient.GetAsync(url);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
        /// <summary>
        /// GET /bundles/{bundle_id}/versions
        /// </summary>
                /// <param name="bundle_id">bundle_id parameter</param>
        public async Task<object> getbundlesversions(string bundle_id)
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
        /// GET /bundles/{bundle_id}/changelog
        /// </summary>
                /// <param name="bundle_id">bundle_id parameter</param>
        public async Task<object> getbundleschangelog(string bundle_id)
        {
                    var queryParams = new Dictionary<string, object?> { "bundle_id", bundle_id };
                    var queryString = string.Join("&", queryParams.Where(p => p.Value != null).Select(p => $"{p.Key}={Uri.EscapeDataString(p.Value.ToString())}"));
                    var url = $"{formatted_path}" + (string.IsNullOrEmpty(queryString) ? "" : $"?{queryString}");
                    var content = null;
                    var response = await this.httpClient.GetAsync(url);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
    }
}
