using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Text.Json;
using System.Threading;
using System.Threading.Tasks;

namespace TavoAI
{
    /// <summary>
    /// Configuration for tavo-scanner execution
    /// </summary>
    public class ScannerConfig
    {
        /// <summary>
        /// Path to tavo-scanner binary
        /// </summary>
        public string? ScannerPath { get; set; }

        /// <summary>
        /// List of plugins to use
        /// </summary>
        public List<string> Plugins { get; set; } = new();

        /// <summary>
        /// Plugin-specific configuration
        /// </summary>
        public Dictionary<string, object> PluginConfig { get; set; } = new();

        /// <summary>
        /// Path to custom rules file
        /// </summary>
        public string? RulesPath { get; set; }

        /// <summary>
        /// Custom rules configuration
        /// </summary>
        public Dictionary<string, object> CustomRules { get; set; } = new();

        /// <summary>
        /// Execution timeout in seconds
        /// </summary>
        public int Timeout { get; set; } = 300;

        /// <summary>
        /// Working directory for execution
        /// </summary>
        public string? WorkingDirectory { get; set; }

        /// <summary>
        /// Output format
        /// </summary>
        public string OutputFormat { get; set; } = "json";

        /// <summary>
        /// Output file path
        /// </summary>
        public string? OutputFile { get; set; }

        public ScannerConfig()
        {
            ScannerPath = FindScannerBinary();
        }

        private string? FindScannerBinary()
        {
            // Try relative to this assembly
            var assemblyLocation = typeof(ScannerConfig).Assembly.Location;
            var assemblyDir = Path.GetDirectoryName(assemblyLocation);
            if (assemblyDir != null)
            {
                var scannerPath = Path.Combine(assemblyDir, "..", "..", "..", "..", "tavo-cli", "bin", "tavo-scanner");
                if (File.Exists(scannerPath))
                {
                    return Path.GetFullPath(scannerPath);
                }
            }

            // Check PATH
            var paths = Environment.GetEnvironmentVariable("PATH")?.Split(Path.PathSeparator);
            if (paths != null)
            {
                foreach (var path in paths)
                {
                    var scannerPath = Path.Combine(path, "tavo-scanner");
                    if (File.Exists(scannerPath))
                    {
                        return scannerPath;
                    }
                    scannerPath = Path.Combine(path, "tavo-scanner.exe");
                    if (File.Exists(scannerPath))
                    {
                        return scannerPath;
                    }
                }
            }

            return null;
        }
    }

    /// <summary>
    /// Scan options for scanner execution
    /// </summary>
    public class ScanOptions
    {
        /// <summary>
        /// Static analysis enabled
        /// </summary>
        public bool StaticAnalysis { get; set; } = true;

        /// <summary>
        /// Static analysis plugins
        /// </summary>
        public List<string> StaticPlugins { get; set; } = new();

        /// <summary>
        /// Custom rules path
        /// </summary>
        public string? StaticRules { get; set; }

        /// <summary>
        /// Dynamic testing enabled
        /// </summary>
        public bool DynamicTesting { get; set; } = false;

        /// <summary>
        /// Dynamic testing plugins
        /// </summary>
        public List<string> DynamicPlugins { get; set; } = new();

        /// <summary>
        /// Output format
        /// </summary>
        public string OutputFormat { get; set; } = "json";

        /// <summary>
        /// Output file path
        /// </summary>
        public string? OutputFile { get; set; }

        /// <summary>
        /// Execution timeout
        /// </summary>
        public int Timeout { get; set; } = 300;

        /// <summary>
        /// Files to exclude
        /// </summary>
        public List<string> ExcludePatterns { get; set; } = new();

        /// <summary>
        /// Files to include
        /// </summary>
        public List<string> IncludePatterns { get; set; } = new();
    }

    /// <summary>
    /// Scan result from scanner execution
    /// </summary>
    public class ScanResult
    {
        /// <summary>
        /// Execution status
        /// </summary>
        public string Status { get; set; } = "";

        /// <summary>
        /// Scan results
        /// </summary>
        public List<object>? Results { get; set; }

        /// <summary>
        /// Raw output
        /// </summary>
        public string? Output { get; set; }

        /// <summary>
        /// Error message
        /// </summary>
        public string? Error { get; set; }
    }

    /// <summary>
    /// Wrapper for executing tavo-scanner as a subprocess
    /// </summary>
    public class TavoScanner
    {
        private readonly ScannerConfig _config;

        public TavoScanner(ScannerConfig? config = null)
        {
            _config = config ?? new ScannerConfig();
        }

        /// <summary>
        /// Scan a directory with tavo-scanner
        /// </summary>
        public async Task<ScanResult> ScanDirectoryAsync(
            string targetPath,
            ScanOptions? scanOptions = null,
            CancellationToken cancellationToken = default)
        {
            if (string.IsNullOrEmpty(_config.ScannerPath))
            {
                throw new FileNotFoundException("tavo-scanner binary not found. Please install tavo-cli or set ScannerPath.");
            }

            // Merge configurations
            var mergedConfig = new ScannerConfig
            {
                ScannerPath = _config.ScannerPath,
                Plugins = new List<string>(_config.Plugins),
                PluginConfig = new Dictionary<string, object>(_config.PluginConfig),
                RulesPath = _config.RulesPath,
                CustomRules = new Dictionary<string, object>(_config.CustomRules),
                Timeout = _config.Timeout,
                WorkingDirectory = _config.WorkingDirectory,
                OutputFormat = _config.OutputFormat,
                OutputFile = _config.OutputFile
            };

            if (scanOptions != null)
            {
                mergedConfig.Plugins = scanOptions.StaticPlugins;
                mergedConfig.RulesPath = scanOptions.StaticRules;
                mergedConfig.Timeout = scanOptions.Timeout;
                mergedConfig.OutputFormat = scanOptions.OutputFormat;
                mergedConfig.OutputFile = scanOptions.OutputFile;
            }

            // Prepare scanner command
            var arguments = new List<string> { targetPath };

            // Add plugins
            if (mergedConfig.Plugins != null)
            {
                foreach (var plugin in mergedConfig.Plugins)
                {
                    arguments.Add("--plugin");
                    arguments.Add(plugin);
                }
            }

            // Add rules
            if (!string.IsNullOrEmpty(mergedConfig.RulesPath))
            {
                arguments.Add("--rules");
                arguments.Add(mergedConfig.RulesPath);
            }

            // Add output options
            if (!string.IsNullOrEmpty(mergedConfig.OutputFormat))
            {
                arguments.Add("--format");
                arguments.Add(mergedConfig.OutputFormat);
            }

            if (!string.IsNullOrEmpty(mergedConfig.OutputFile))
            {
                arguments.Add("--output");
                arguments.Add(mergedConfig.OutputFile);
            }

            // Add timeout
            if (mergedConfig.Timeout > 0)
            {
                arguments.Add("--timeout");
                arguments.Add(mergedConfig.Timeout.ToString());
            }

            return await ExecuteScannerAsync(arguments.ToArray(), mergedConfig.WorkingDirectory, cancellationToken);
        }

        /// <summary>
        /// Scan with specific plugins
        /// </summary>
        public async Task<ScanResult> ScanWithPluginsAsync(
            string targetPath,
            IEnumerable<string> plugins,
            CancellationToken cancellationToken = default)
        {
            var config = new ScannerConfig { Plugins = plugins.ToList() };
            var scanner = new TavoScanner(config);
            return await scanner.ScanDirectoryAsync(targetPath, cancellationToken: cancellationToken);
        }

        /// <summary>
        /// Scan with custom rules
        /// </summary>
        public async Task<ScanResult> ScanWithRulesAsync(
            string targetPath,
            string rulesPath,
            CancellationToken cancellationToken = default)
        {
            var config = new ScannerConfig { RulesPath = rulesPath };
            var scanner = new TavoScanner(config);
            return await scanner.ScanDirectoryAsync(targetPath, cancellationToken: cancellationToken);
        }

        /// <summary>
        /// Execute the scanner subprocess
        /// </summary>
        private async Task<ScanResult> ExecuteScannerAsync(
            string[] arguments,
            string? workingDirectory = null,
            CancellationToken cancellationToken = default)
        {
            var startInfo = new ProcessStartInfo
            {
                FileName = _config.ScannerPath,
                Arguments = string.Join(" ", arguments.Select(arg => $"\"{arg}\"")),
                UseShellExecute = false,
                RedirectStandardOutput = true,
                RedirectStandardError = true,
                CreateNoWindow = true,
                WorkingDirectory = workingDirectory ?? Environment.CurrentDirectory
            };

            using var process = Process.Start(startInfo);
            if (process == null)
            {
                throw new InvalidOperationException("Failed to start scanner process");
            }

            using var cts = CancellationTokenSource.CreateLinkedTokenSource(cancellationToken);
            cts.CancelAfter(TimeSpan.FromSeconds(_config.Timeout));

            try
            {
                await process.WaitForExitAsync(cts.Token);

                var stdout = await process.StandardOutput.ReadToEndAsync();
                var stderr = await process.StandardError.ReadToEndAsync();

                if (process.ExitCode != 0)
                {
                    return new ScanResult
                    {
                        Status = "error",
                        Error = stderr.Trim() ?? $"Scanner exited with code {process.ExitCode}"
                    };
                }

                if (string.IsNullOrWhiteSpace(stdout))
                {
                    return new ScanResult
                    {
                        Status = "success",
                        Results = new List<object>()
                    };
                }

                try
                {
                    var results = JsonSerializer.Deserialize<List<object>>(stdout);
                    return new ScanResult
                    {
                        Status = "success",
                        Results = results
                    };
                }
                catch (JsonException)
                {
                    return new ScanResult
                    {
                        Status = "success",
                        Output = stdout.Trim()
                    };
                }
            }
            catch (OperationCanceledException)
            {
                process.Kill();
                throw new TimeoutException($"Scanner timed out after {_config.Timeout} seconds");
            }
        }

        /// <summary>
        /// Create a temporary plugin configuration file
        /// </summary>
        public async Task<string> CreatePluginConfigAsync(string pluginName, Dictionary<string, object> config)
        {
            var tempPath = Path.Combine(Path.GetTempPath(), $"tavo-plugin-{pluginName}-{Guid.NewGuid()}.json");
            var json = JsonSerializer.Serialize(config, new JsonSerializerOptions { WriteIndented = true });
            await File.WriteAllTextAsync(tempPath, json);
            return tempPath;
        }

        /// <summary>
        /// Create a temporary rules file
        /// </summary>
        public async Task<string> CreateRulesFileAsync(Dictionary<string, object> rules)
        {
            var tempPath = Path.Combine(Path.GetTempPath(), $"tavo-rules-{Guid.NewGuid()}.json");
            var json = JsonSerializer.Serialize(rules, new JsonSerializerOptions { WriteIndented = true });
            await File.WriteAllTextAsync(tempPath, json);
            return tempPath;
        }
    }
}
