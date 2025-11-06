using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Net.Http.Json;
using System.Threading.Tasks;

namespace TavoAI
{
    /// <summary>
    /// Client for scan_tools endpoints
    /// </summary>
    public class ScanToolsClient
    {
        private readonly HttpClient httpClient;

        /// <summary>
        /// Create a new scan_tools client
        /// </summary>
        /// <param name="httpClient">HTTP client instance</param>
        public ScanToolsClient(HttpClient httpClient)
        {
            this.httpClient = httpClient;
        }


        /// <summary>
        /// GET /tools
        /// </summary>
                /// <param name="active_only">active_only parameter</param>
        public async Task<Task<List[ScanToolInfo]>> gettools(bool? active_only = null)
        {'                    var queryParams = new Dictionary<string, object?> { "active_only", active_only };\n                    var queryString = string.Join("&", queryParams.Where(p => p.Value != null).Select(p => $"{p.Key}={Uri.EscapeDataString(p.Value.ToString())}"));\n                    var url = "/tools" + (string.IsNullOrEmpty(queryString) ? "" : $"?{queryString}");\n                    var content = null;\n                    var response = await this.httpClient.GetAsync(url);\n                    response.EnsureSuccessStatusCode();\n                    return await response.Content.ReadFromJsonAsync<object>();'}

        /// <summary>
        /// GET /tools/{tool_name}
        /// </summary>
                /// <param name="tool_name">tool_name parameter</param>
        public async Task<Task<ScanToolInfo>> gettools{tool_name}(string tool_name)
        {'                    var queryParams = new Dictionary<string, object?> { "tool_name", tool_name };\n                    var queryString = string.Join("&", queryParams.Where(p => p.Value != null).Select(p => $"{p.Key}={Uri.EscapeDataString(p.Value.ToString())}"));\n                    var url = "/tools/{tool_name}" + (string.IsNullOrEmpty(queryString) ? "" : $"?{queryString}");\n                    var content = null;\n                    var response = await this.httpClient.GetAsync(url);\n                    response.EnsureSuccessStatusCode();\n                    return await response.Content.ReadFromJsonAsync<object>();'}

        /// <summary>
        /// GET /templates
        /// </summary>
                /// <param name="tool">tool parameter</param>
        /// <param name="category">category parameter</param>
        /// <param name="language">language parameter</param>
        /// <param name="active_only">active_only parameter</param>
        public async Task<Task<List[ScanTemplateInfo]>> gettemplates(string? tool = null, string? category = null, string? language = null, bool? active_only = null)
        {'                    var queryParams = new Dictionary<string, object?> { "tool", tool, "category", category, "language", language, "active_only", active_only };\n                    var queryString = string.Join("&", queryParams.Where(p => p.Value != null).Select(p => $"{p.Key}={Uri.EscapeDataString(p.Value.ToString())}"));\n                    var url = "/templates" + (string.IsNullOrEmpty(queryString) ? "" : $"?{queryString}");\n                    var content = null;\n                    var response = await this.httpClient.GetAsync(url);\n                    response.EnsureSuccessStatusCode();\n                    return await response.Content.ReadFromJsonAsync<object>();'}

        /// <summary>
        /// GET /templates/{template_id}
        /// </summary>
                /// <param name="template_id">template_id parameter</param>
        public async Task<Task<ScanTemplateInfo>> gettemplates{template_id}(string template_id)
        {'                    var queryParams = new Dictionary<string, object?> { "template_id", template_id };\n                    var queryString = string.Join("&", queryParams.Where(p => p.Value != null).Select(p => $"{p.Key}={Uri.EscapeDataString(p.Value.ToString())}"));\n                    var url = "/templates/{template_id}" + (string.IsNullOrEmpty(queryString) ? "" : $"?{queryString}");\n                    var content = null;\n                    var response = await this.httpClient.GetAsync(url);\n                    response.EnsureSuccessStatusCode();\n                    return await response.Content.ReadFromJsonAsync<object>();'}

        /// <summary>
        /// POST /validate-configuration
        /// </summary>
        
        public async Task<Task<ScanConfigurationValidationResponse>> postvalidateconfiguration()
        {'                    var url = "/validate-configuration";\n                    var content = null;\n                    var response = await this.httpClient.PostAsync(url, content);\n                    response.EnsureSuccessStatusCode();\n                    return await response.Content.ReadFromJsonAsync<object>();'}

        /// <summary>
        /// GET /repositories/{repository_id}/settings
        /// </summary>
                /// <param name="repository_id">repository_id parameter</param>
        public async Task<Task<RepositoryScanSettings>> getrepositories{repository_id}settings(string repository_id)
        {'                    var queryParams = new Dictionary<string, object?> { "repository_id", repository_id };\n                    var queryString = string.Join("&", queryParams.Where(p => p.Value != null).Select(p => $"{p.Key}={Uri.EscapeDataString(p.Value.ToString())}"));\n                    var url = "/repositories/{repository_id}/settings" + (string.IsNullOrEmpty(queryString) ? "" : $"?{queryString}");\n                    var content = null;\n                    var response = await this.httpClient.GetAsync(url);\n                    response.EnsureSuccessStatusCode();\n                    return await response.Content.ReadFromJsonAsync<object>();'}

        /// <summary>
        /// PUT /repositories/{repository_id}/settings
        /// </summary>
                /// <param name="repository_id">repository_id parameter</param>
        /// <param name="settings">settings parameter</param>
        public async Task<Task<RepositoryScanSettings>> putrepositories{repository_id}settings(string repository_id, object settings)
        {'                    var url = "/repositories/{repository_id}/settings";\n                    var content = JsonContent.Create(new { "repository_id", repository_id, "settings", settings });\n                    var response = await this.httpClient.PutAsync(url, content);\n                    response.EnsureSuccessStatusCode();\n                    return await response.Content.ReadFromJsonAsync<object>();'}

        /// <summary>
        /// POST /validate-access
        /// </summary>
        
        public async Task<Task<RepositoryAccessValidationResponse>> postvalidateaccess()
        {'                    var url = "/validate-access";\n                    var content = null;\n                    var response = await this.httpClient.PostAsync(url, content);\n                    response.EnsureSuccessStatusCode();\n                    return await response.Content.ReadFromJsonAsync<object>();'}
    }
}
