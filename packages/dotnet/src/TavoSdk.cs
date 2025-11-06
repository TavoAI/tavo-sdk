using System;

namespace TavoAI
{
    /// <summary>
    /// Main entry point for Tavo AI SDK
    /// Provides access to both API client and scanner functionality
    /// </summary>
    public static class TavoSdk
    {
        /// <summary>
        /// Create a new API client instance
        /// </summary>
        public static TavoClient CreateClient(string? apiKey = null, string? jwtToken = null, string? sessionToken = null)
        {
            return new TavoClient(apiKey, jwtToken, sessionToken);
        }

        /// <summary>
        /// Create a new scanner instance
        /// </summary>
        public static TavoScanner CreateScanner(ScannerConfig? config = null)
        {
            return new TavoScanner(config);
        }

        /// <summary>
        /// Create a scanner with specific plugins
        /// </summary>
        public static TavoScanner CreateScannerWithPlugins(params string[] plugins)
        {
            var config = new ScannerConfig { Plugins = plugins.ToList() };
            return new TavoScanner(config);
        }

        /// <summary>
        /// Create a scanner with custom rules
        /// </summary>
        public static TavoScanner CreateScannerWithRules(string rulesPath)
        {
            var config = new ScannerConfig { RulesPath = rulesPath };
            return new TavoScanner(config);
        }

        /// <summary>
        /// SDK version
        /// </summary>
        public const string Version = "0.1.0";
    }
}
