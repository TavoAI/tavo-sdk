using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Net.Http.Json;
using System.Threading.Tasks;

namespace TavoAI
{
    /// <summary>
    /// Client for code_submission endpoints
    /// </summary>
    public class CodeSubmissionClient
    {
        private readonly HttpClient httpClient;

        /// <summary>
        /// Create a new code_submission client
        /// </summary>
        /// <param name="httpClient">HTTP client instance</param>
        public CodeSubmissionClient(HttpClient httpClient)
        {
            this.httpClient = httpClient;
        }

        /// <summary>
        /// POST /submit/code
        /// </summary>
                /// <param name="files">files parameter</param>
        /// <param name="scan_config">scan_config parameter</param>
        /// <param name="repository_name">repository_name parameter</param>
        /// <param name="branch">branch parameter</param>
        /// <param name="commit_sha">commit_sha parameter</param>
        public async Task<object> postsubmitcode(List<object>? files = null, object? scan_config = null, string? repository_name = null, string? branch = null, string? commit_sha = null)
        {
                    var url = "/submit/code";
                    var content = JsonContent.Create(new { files = files, scan_config = scan_config, repository_name = repository_name, branch = branch, commit_sha = commit_sha });
                    var response = await this.httpClient.PostAsync(url, content);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
        /// <summary>
        /// POST /submit/repository
        /// </summary>
                /// <param name="repository_url">repository_url parameter</param>
        /// <param name="snapshot_data">snapshot_data parameter</param>
        /// <param name="scan_config">scan_config parameter</param>
        /// <param name="branch">branch parameter</param>
        /// <param name="commit_sha">commit_sha parameter</param>
        public async Task<object> postsubmitrepository(string? repository_url = null, object? snapshot_data = null, object? scan_config = null, string? branch = null, string? commit_sha = null)
        {
                    var url = "/submit/repository";
                    var content = JsonContent.Create(new { repository_url = repository_url, snapshot_data = snapshot_data, scan_config = scan_config, branch = branch, commit_sha = commit_sha });
                    var response = await this.httpClient.PostAsync(url, content);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
        /// <summary>
        /// POST /submit/analysis
        /// </summary>
                /// <param name="code_content">code_content parameter</param>
        /// <param name="language">language parameter</param>
        /// <param name="analysis_type">analysis_type parameter</param>
        /// <param name="rules">rules parameter</param>
        /// <param name="plugins">plugins parameter</param>
        /// <param name="context">context parameter</param>
        public async Task<object> postsubmitanalysis(string? code_content = null, string? language = null, string? analysis_type = null, List<string>? rules = null, List<string>? plugins = null, object? context = null)
        {
                    var url = "/submit/analysis";
                    var content = JsonContent.Create(new { code_content = code_content, language = language, analysis_type = analysis_type, rules = rules, plugins = plugins, context = context });
                    var response = await this.httpClient.PostAsync(url, content);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
        /// <summary>
        /// GET /scans/{scan_id}/status
        /// </summary>
                /// <param name="scan_id">scan_id parameter</param>
        public async Task<object> getscansstatus(string scan_id)
        {
                    var queryParams = new Dictionary<string, object?> { "scan_id", scan_id };
                    var queryString = string.Join("&", queryParams.Where(p => p.Value != null).Select(p => $"{p.Key}={Uri.EscapeDataString(p.Value.ToString())}"));
                    var url = $"{formatted_path}" + (string.IsNullOrEmpty(queryString) ? "" : $"?{queryString}");
                    var content = null;
                    var response = await this.httpClient.GetAsync(url);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadFromJsonAsync<object>();
        }
        /// <summary>
        /// GET /scans/{scan_id}/results/summary
        /// </summary>
                /// <param name="scan_id">scan_id parameter</param>
        public async Task<object> getscansresultssummary(string scan_id)
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
