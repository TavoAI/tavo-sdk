using System;
using System.Net.Http;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;
using Newtonsoft.Json;

namespace TavoAI
{
    /// <summary>
    /// Tavo AI SDK for .NET
    /// </summary>
    public class TavoClient
    {
        private readonly HttpClient _httpClient;
        private readonly string _apiKey;

        /// <summary>
        /// Initializes a new instance of the TavoClient
        /// </summary>
        /// <param name="apiKey">Your Tavo AI API key</param>
        /// <param name="baseUrl">Base URL for the API (optional)</param>
        public TavoClient(string apiKey, string baseUrl = "https://api.tavo.ai")
        {
            _apiKey = apiKey ?? throw new ArgumentNullException(nameof(apiKey));
            _httpClient = new HttpClient
            {
                BaseAddress = new Uri(baseUrl)
            };
            _httpClient.DefaultRequestHeaders.Add("Authorization", $"Bearer {_apiKey}");
        }

        /// <summary>
        /// Scans code for security vulnerabilities
        /// </summary>
        /// <param name="code">The code to scan</param>
        /// <param name="language">Programming language</param>
        /// <returns>Scan results</returns>
        public async Task<ScanResult> ScanCodeAsync(string code, string language = "csharp")
        {
            var request = new
            {
                code = code,
                language = language
            };

            var json = System.Text.Json.JsonSerializer.Serialize(request);
            var content = new StringContent(json, Encoding.UTF8, "application/json");

            var response = await _httpClient.PostAsync("/api/v1/scan", content);
            response.EnsureSuccessStatusCode();

            var result = await response.Content.ReadAsStringAsync();
            return JsonConvert.DeserializeObject<ScanResult>(result);
        }

        /// <summary>
        /// Analyzes AI model for security risks
        /// </summary>
        /// <param name="modelConfig">Model configuration</param>
        /// <returns>Analysis results</returns>
        public async Task<ModelAnalysisResult> AnalyzeModelAsync(object modelConfig)
        {
            var json = System.Text.Json.JsonSerializer.Serialize(modelConfig);
            var content = new StringContent(json, Encoding.UTF8, "application/json");

            var response = await _httpClient.PostAsync("/api/v1/analyze/model", content);
            response.EnsureSuccessStatusCode();

            var result = await response.Content.ReadAsStringAsync();
            return JsonConvert.DeserializeObject<ModelAnalysisResult>(result);
        }
    }

    /// <summary>
    /// Result of a security scan
    /// </summary>
    public class ScanResult
    {
        public bool Success { get; set; }
        public List<Vulnerability> Vulnerabilities { get; set; } = new();
        public int TotalIssues { get; set; }
        public string ScanId { get; set; }
    }

    /// <summary>
    /// Security vulnerability
    /// </summary>
    public class Vulnerability
    {
        public string Id { get; set; }
        public string Title { get; set; }
        public string Description { get; set; }
        public string Severity { get; set; }
        public string Category { get; set; }
        public Location Location { get; set; }
    }

    /// <summary>
    /// Location of a vulnerability
    /// </summary>
    public class Location
    {
        public string File { get; set; }
        public int Line { get; set; }
        public int Column { get; set; }
    }

    /// <summary>
    /// Result of AI model analysis
    /// </summary>
    public class ModelAnalysisResult
    {
        public bool Safe { get; set; }
        public List<string> Risks { get; set; } = new();
        public Dictionary<string, object> Recommendations { get; set; } = new();
    }
}