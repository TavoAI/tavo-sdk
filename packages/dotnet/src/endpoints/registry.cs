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
        
        public async Task<Task<PaginatedResponse[ArtifactBundleList]>> getmarketplace()
        {'                    var url = "/marketplace";\n                    var content = null;\n                    var response = await this.httpClient.GetAsync(url);\n                    response.EnsureSuccessStatusCode();\n                    return await response.Content.ReadFromJsonAsync<object>();'}

        /// <summary>
        /// GET /categories
        /// </summary>
        
        public async Task<Task<List[CategoryResponse]>> getcategories()
        {'                    var url = "/categories";\n                    var content = null;\n                    var response = await this.httpClient.GetAsync(url);\n                    response.EnsureSuccessStatusCode();\n                    return await response.Content.ReadFromJsonAsync<object>();'}

        /// <summary>
        /// POST /bundles
        /// </summary>
                /// <param name="bundle">bundle parameter</param>
        public async Task<Task<ArtifactBundleDetail>> postbundles(object bundle)
        {'                    var url = "/bundles";\n                    var content = JsonContent.Create(bundle);\n                    var response = await this.httpClient.PostAsync(url, content);\n                    response.EnsureSuccessStatusCode();\n                    return await response.Content.ReadFromJsonAsync<object>();'}

        /// <summary>
        /// GET /bundles/{bundle_id}
        /// </summary>
                /// <param name="bundle_id">bundle_id parameter</param>
        public async Task<Task<ArtifactBundleDetail>> getbundles{bundle_id}(string bundle_id)
        {'                    var queryParams = new Dictionary<string, object?> { "bundle_id", bundle_id };\n                    var queryString = string.Join("&", queryParams.Where(p => p.Value != null).Select(p => $"{p.Key}={Uri.EscapeDataString(p.Value.ToString())}"));\n                    var url = "/bundles/{bundle_id}" + (string.IsNullOrEmpty(queryString) ? "" : $"?{queryString}");\n                    var content = null;\n                    var response = await this.httpClient.GetAsync(url);\n                    response.EnsureSuccessStatusCode();\n                    return await response.Content.ReadFromJsonAsync<object>();'}

        /// <summary>
        /// PUT /bundles/{bundle_id}
        /// </summary>
                /// <param name="bundle_id">bundle_id parameter</param>
        /// <param name="bundle_update">bundle_update parameter</param>
        public async Task<Task<ArtifactBundleDetail>> putbundles{bundle_id}(string bundle_id, object bundle_update)
        {'                    var url = "/bundles/{bundle_id}";\n                    var content = JsonContent.Create(new { "bundle_id", bundle_id, "bundle_update", bundle_update });\n                    var response = await this.httpClient.PutAsync(url, content);\n                    response.EnsureSuccessStatusCode();\n                    return await response.Content.ReadFromJsonAsync<object>();'}

        /// <summary>
        /// DELETE /bundles/{bundle_id}
        /// </summary>
                /// <param name="bundle_id">bundle_id parameter</param>
        public async Task<Task<object>> deletebundles{bundle_id}(string bundle_id)
        {'                    var url = "/bundles/{bundle_id}";\n                    var content = JsonContent.Create(bundle_id);\n                    var response = await this.httpClient.DeleteAsync(url);\n                    response.EnsureSuccessStatusCode();\n                    return await response.Content.ReadFromJsonAsync<object>();'}

        /// <summary>
        /// GET /bundles/{bundle_id}/download
        /// </summary>
                /// <param name="bundle_id">bundle_id parameter</param>
        public async Task<Task<object>> getbundles{bundle_id}download(string bundle_id)
        {'                    var queryParams = new Dictionary<string, object?> { "bundle_id", bundle_id };\n                    var queryString = string.Join("&", queryParams.Where(p => p.Value != null).Select(p => $"{p.Key}={Uri.EscapeDataString(p.Value.ToString())}"));\n                    var url = "/bundles/{bundle_id}/download" + (string.IsNullOrEmpty(queryString) ? "" : $"?{queryString}");\n                    var content = null;\n                    var response = await this.httpClient.GetAsync(url);\n                    response.EnsureSuccessStatusCode();\n                    return await response.Content.ReadFromJsonAsync<object>();'}

        /// <summary>
        /// POST /bundles/{bundle_id}/install
        /// </summary>
                /// <param name="bundle_id">bundle_id parameter</param>
        /// <param name="installation">installation parameter</param>
        public async Task<Task<BundleInstallationResponse>> postbundles{bundle_id}install(string bundle_id, object installation)
        {'                    var url = "/bundles/{bundle_id}/install";\n                    var content = JsonContent.Create(new { "bundle_id", bundle_id, "installation", installation });\n                    var response = await this.httpClient.PostAsync(url, content);\n                    response.EnsureSuccessStatusCode();\n                    return await response.Content.ReadFromJsonAsync<object>();'}

        /// <summary>
        /// GET /my-bundles
        /// </summary>
        
        public async Task<Task<List[BundleInstallationResponse]>> getmybundles()
        {'                    var url = "/my-bundles";\n                    var content = null;\n                    var response = await this.httpClient.GetAsync(url);\n                    response.EnsureSuccessStatusCode();\n                    return await response.Content.ReadFromJsonAsync<object>();'}

        /// <summary>
        /// POST /execute/code-rule
        /// </summary>
        
        public async Task<Task<ArtifactExecutionResponse>> postexecutecoderule()
        {'                    var url = "/execute/code-rule";\n                    var content = null;\n                    var response = await this.httpClient.PostAsync(url, content);\n                    response.EnsureSuccessStatusCode();\n                    return await response.Content.ReadFromJsonAsync<object>();'}

        /// <summary>
        /// GET /executions/{execution_id}
        /// </summary>
                /// <param name="execution_id">execution_id parameter</param>
        public async Task<Task<ArtifactExecutionResponse>> getexecutions{execution_id}(string execution_id)
        {'                    var queryParams = new Dictionary<string, object?> { "execution_id", execution_id };\n                    var queryString = string.Join("&", queryParams.Where(p => p.Value != null).Select(p => $"{p.Key}={Uri.EscapeDataString(p.Value.ToString())}"));\n                    var url = "/executions/{execution_id}" + (string.IsNullOrEmpty(queryString) ? "" : $"?{queryString}");\n                    var content = null;\n                    var response = await this.httpClient.GetAsync(url);\n                    response.EnsureSuccessStatusCode();\n                    return await response.Content.ReadFromJsonAsync<object>();'}

        /// <summary>
        /// GET /my-executions
        /// </summary>
                /// <param name="page">page parameter</param>
        /// <param name="per_page">per_page parameter</param>
        public async Task<Task<PaginatedResponse[ArtifactExecutionResponse]>> getmyexecutions(double? page = null, double? per_page = null)
        {'                    var queryParams = new Dictionary<string, object?> { "page", page, "per_page", per_page };\n                    var queryString = string.Join("&", queryParams.Where(p => p.Value != null).Select(p => $"{p.Key}={Uri.EscapeDataString(p.Value.ToString())}"));\n                    var url = "/my-executions" + (string.IsNullOrEmpty(queryString) ? "" : $"?{queryString}");\n                    var content = null;\n                    var response = await this.httpClient.GetAsync(url);\n                    response.EnsureSuccessStatusCode();\n                    return await response.Content.ReadFromJsonAsync<object>();'}

        /// <summary>
        /// POST /bundles/{bundle_id}/rate
        /// </summary>
                /// <param name="bundle_id">bundle_id parameter</param>
        /// <param name="rating">rating parameter</param>
        public async Task<Task<BundleRatingResponse>> postbundles{bundle_id}rate(string bundle_id, object rating)
        {'                    var url = "/bundles/{bundle_id}/rate";\n                    var content = JsonContent.Create(new { "bundle_id", bundle_id, "rating", rating });\n                    var response = await this.httpClient.PostAsync(url, content);\n                    response.EnsureSuccessStatusCode();\n                    return await response.Content.ReadFromJsonAsync<object>();'}

        /// <summary>
        /// POST /bundles/{bundle_id}/review
        /// </summary>
                /// <param name="bundle_id">bundle_id parameter</param>
        /// <param name="review">review parameter</param>
        public async Task<Task<BundleReviewResponse>> postbundles{bundle_id}review(string bundle_id, object review)
        {'                    var url = "/bundles/{bundle_id}/review";\n                    var content = JsonContent.Create(new { "bundle_id", bundle_id, "review", review });\n                    var response = await this.httpClient.PostAsync(url, content);\n                    response.EnsureSuccessStatusCode();\n                    return await response.Content.ReadFromJsonAsync<object>();'}

        /// <summary>
        /// GET /bundles/{bundle_id}/reviews
        /// </summary>
                /// <param name="bundle_id">bundle_id parameter</param>
        /// <param name="page">page parameter</param>
        /// <param name="per_page">per_page parameter</param>
        public async Task<Task<PaginatedResponse[BundleReviewResponse]>> getbundles{bundle_id}reviews(string bundle_id, double? page = null, double? per_page = null)
        {'                    var queryParams = new Dictionary<string, object?> { "bundle_id", bundle_id, "page", page, "per_page", per_page };\n                    var queryString = string.Join("&", queryParams.Where(p => p.Value != null).Select(p => $"{p.Key}={Uri.EscapeDataString(p.Value.ToString())}"));\n                    var url = "/bundles/{bundle_id}/reviews" + (string.IsNullOrEmpty(queryString) ? "" : $"?{queryString}");\n                    var content = null;\n                    var response = await this.httpClient.GetAsync(url);\n                    response.EnsureSuccessStatusCode();\n                    return await response.Content.ReadFromJsonAsync<object>();'}

        /// <summary>
        /// GET /bundles/{bundle_id}/versions
        /// </summary>
                /// <param name="bundle_id">bundle_id parameter</param>
        public async Task<Task<object>> getbundles{bundle_id}versions(string bundle_id)
        {'                    var queryParams = new Dictionary<string, object?> { "bundle_id", bundle_id };\n                    var queryString = string.Join("&", queryParams.Where(p => p.Value != null).Select(p => $"{p.Key}={Uri.EscapeDataString(p.Value.ToString())}"));\n                    var url = "/bundles/{bundle_id}/versions" + (string.IsNullOrEmpty(queryString) ? "" : $"?{queryString}");\n                    var content = null;\n                    var response = await this.httpClient.GetAsync(url);\n                    response.EnsureSuccessStatusCode();\n                    return await response.Content.ReadFromJsonAsync<object>();'}

        /// <summary>
        /// GET /bundles/{bundle_id}/changelog
        /// </summary>
                /// <param name="bundle_id">bundle_id parameter</param>
        public async Task<Task<object>> getbundles{bundle_id}changelog(string bundle_id)
        {'                    var queryParams = new Dictionary<string, object?> { "bundle_id", bundle_id };\n                    var queryString = string.Join("&", queryParams.Where(p => p.Value != null).Select(p => $"{p.Key}={Uri.EscapeDataString(p.Value.ToString())}"));\n                    var url = "/bundles/{bundle_id}/changelog" + (string.IsNullOrEmpty(queryString) ? "" : $"?{queryString}");\n                    var content = null;\n                    var response = await this.httpClient.GetAsync(url);\n                    response.EnsureSuccessStatusCode();\n                    return await response.Content.ReadFromJsonAsync<object>();'}
    }
}
