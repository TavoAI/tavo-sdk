using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Net.Http.Json;
using System.Threading.Tasks;

namespace TavoAI
{
    /// <summary>
    /// Client for scan_schedules endpoints
    /// </summary>
    public class ScanSchedulesClient
    {
        private readonly HttpClient httpClient;

        /// <summary>
        /// Create a new scan_schedules client
        /// </summary>
        /// <param name="httpClient">HTTP client instance</param>
        public ScanSchedulesClient(HttpClient httpClient)
        {
            this.httpClient = httpClient;
        }


        /// <summary>
        /// POST /
        /// </summary>
                /// <param name="schedule_in">schedule_in parameter</param>
        public async Task<Task<ScanScheduleResponse>> postRoot(object schedule_in)
        {'                    var url = "/";\n                    var content = JsonContent.Create(schedule_in);\n                    var response = await this.httpClient.PostAsync(url, content);\n                    response.EnsureSuccessStatusCode();\n                    return await response.Content.ReadFromJsonAsync<object>();'}

        /// <summary>
        /// GET /repository/{repository_id}
        /// </summary>
                /// <param name="repository_id">repository_id parameter</param>
        public async Task<Task<List[ScanScheduleResponse]>> getrepository{repository_id}(string repository_id)
        {'                    var queryParams = new Dictionary<string, object?> { "repository_id", repository_id };\n                    var queryString = string.Join("&", queryParams.Where(p => p.Value != null).Select(p => $"{p.Key}={Uri.EscapeDataString(p.Value.ToString())}"));\n                    var url = "/repository/{repository_id}" + (string.IsNullOrEmpty(queryString) ? "" : $"?{queryString}");\n                    var content = null;\n                    var response = await this.httpClient.GetAsync(url);\n                    response.EnsureSuccessStatusCode();\n                    return await response.Content.ReadFromJsonAsync<object>();'}

        /// <summary>
        /// GET /{schedule_id}
        /// </summary>
                /// <param name="schedule_id">schedule_id parameter</param>
        public async Task<Task<ScanScheduleResponse>> get{schedule_id}(string schedule_id)
        {'                    var queryParams = new Dictionary<string, object?> { "schedule_id", schedule_id };\n                    var queryString = string.Join("&", queryParams.Where(p => p.Value != null).Select(p => $"{p.Key}={Uri.EscapeDataString(p.Value.ToString())}"));\n                    var url = "/{schedule_id}" + (string.IsNullOrEmpty(queryString) ? "" : $"?{queryString}");\n                    var content = null;\n                    var response = await this.httpClient.GetAsync(url);\n                    response.EnsureSuccessStatusCode();\n                    return await response.Content.ReadFromJsonAsync<object>();'}

        /// <summary>
        /// PUT /{schedule_id}
        /// </summary>
                /// <param name="schedule_id">schedule_id parameter</param>
        /// <param name="schedule_update">schedule_update parameter</param>
        public async Task<Task<ScanScheduleResponse>> put{schedule_id}(string schedule_id, object schedule_update)
        {'                    var url = "/{schedule_id}";\n                    var content = JsonContent.Create(new { "schedule_id", schedule_id, "schedule_update", schedule_update });\n                    var response = await this.httpClient.PutAsync(url, content);\n                    response.EnsureSuccessStatusCode();\n                    return await response.Content.ReadFromJsonAsync<object>();'}

        /// <summary>
        /// DELETE /{schedule_id}
        /// </summary>
                /// <param name="schedule_id">schedule_id parameter</param>
        public async Task<Task<None>> delete{schedule_id}(string schedule_id)
        {'                    var url = "/{schedule_id}";\n                    var content = JsonContent.Create(schedule_id);\n                    var response = await this.httpClient.DeleteAsync(url);\n                    response.EnsureSuccessStatusCode();\n                    return await response.Content.ReadFromJsonAsync<object>();'}
    }
}
