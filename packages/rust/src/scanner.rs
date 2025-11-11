//! Tavo Scanner Wrapper
//!
//! Executes tavo-scanner as a subprocess with plugin/rule configuration.

use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::path::{Path, PathBuf};
use std::process::Stdio;
use tokio::process::Command;
use tokio::time::{timeout, Duration};

/// Configuration for tavo-scanner execution
#[derive(Debug, Clone)]
pub struct ScannerConfig {
    /// Path to tavo-scanner binary
    pub scanner_path: Option<PathBuf>,

    /// List of plugins to use
    pub plugins: Vec<String>,

    /// Plugin-specific configuration
    pub plugin_config: HashMap<String, serde_json::Value>,

    /// Path to custom rules file
    pub rules_path: Option<PathBuf>,

    /// Custom rules configuration
    pub custom_rules: HashMap<String, serde_json::Value>,

    /// Execution timeout in seconds
    pub timeout: u64,

    /// Working directory for execution
    pub working_directory: Option<PathBuf>,

    /// Output format
    pub output_format: String,

    /// Output file path
    pub output_file: Option<PathBuf>,
}

impl Default for ScannerConfig {
    fn default() -> Self {
        Self {
            scanner_path: Self::find_scanner_binary(),
            plugins: Vec::new(),
            plugin_config: HashMap::new(),
            rules_path: None,
            custom_rules: HashMap::new(),
            timeout: 300,
            working_directory: Some(std::env::current_dir().unwrap_or_default()),
            output_format: "json".to_string(),
            output_file: None,
        }
    }
}

impl ScannerConfig {
    /// Find the tavo-scanner binary in common locations
    fn find_scanner_binary() -> Option<PathBuf> {
        // Try relative to Cargo.toml
        if let Ok(manifest_dir) = std::env::var("CARGO_MANIFEST_DIR") {
            let scanner_path = Path::new(&manifest_dir)
                .parent()
                .unwrap_or(Path::new(&manifest_dir))
                .join("tavo-cli")
                .join("bin")
                .join("tavo-scanner");

            if scanner_path.exists() {
                return Some(scanner_path);
            }
        }

        // Check PATH
        if let Ok(path_var) = std::env::var("PATH") {
            for dir in std::env::split_paths(&path_var) {
                let scanner_path = dir.join("tavo-scanner");
                if scanner_path.exists() {
                    return Some(scanner_path);
                }
            }
        }

        None
    }
}

/// Scan options for scanner execution
#[derive(Debug, Clone)]
pub struct ScanOptions {
    /// Static analysis enabled
    pub static_analysis: bool,

    /// Static analysis plugins
    pub static_plugins: Vec<String>,

    /// Custom rules path
    pub static_rules: Option<PathBuf>,

    /// Dynamic testing enabled
    pub dynamic_testing: bool,

    /// Dynamic testing plugins
    pub dynamic_plugins: Vec<String>,

    /// Output format
    pub output_format: String,

    /// Output file path
    pub output_file: Option<PathBuf>,

    /// Execution timeout
    pub timeout: u64,

    /// Files to exclude
    pub exclude_patterns: Vec<String>,

    /// Files to include
    pub include_patterns: Vec<String>,
}

impl Default for ScanOptions {
    fn default() -> Self {
        Self {
            static_analysis: true,
            static_plugins: Vec::new(),
            static_rules: None,
            dynamic_testing: false,
            dynamic_plugins: Vec::new(),
            output_format: "json".to_string(),
            output_file: None,
            timeout: 300,
            exclude_patterns: Vec::new(),
            include_patterns: Vec::new(),
        }
    }
}

/// Scan result from scanner execution
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ScanResult {
    /// Execution status
    pub status: String,

    /// Scan results
    pub results: Option<Vec<serde_json::Value>>,

    /// Raw output
    pub output: Option<String>,

    /// Error message
    pub error: Option<String>,
}

/// Wrapper for executing tavo-scanner as a subprocess
pub struct TavoScanner {
    config: ScannerConfig,
}

impl TavoScanner {
    /// Create a new scanner wrapper
    pub fn new(config: Option<ScannerConfig>) -> Self {
        Self {
            config: config.unwrap_or_default(),
        }
    }

    /// Scan a directory with tavo-scanner
    pub async fn scan_directory<P: AsRef<Path>>(
        &self,
        target_path: P,
        scan_options: Option<ScanOptions>,
    ) -> Result<ScanResult, Box<dyn std::error::Error>> {
        let scanner_path = self.config.scanner_path.as_ref()
            .ok_or("tavo-scanner binary not found. Please install tavo-cli or set scanner_path.")?;

        // Merge configurations
        let mut merged_config = self.config.clone();

        if let Some(options) = scan_options {
            merged_config.plugins = options.static_plugins;
            merged_config.rules_path = options.static_rules;
            merged_config.timeout = options.timeout;
            merged_config.output_format = options.output_format;
            merged_config.output_file = options.output_file;
        }

        // Prepare command arguments
        let mut args = vec![target_path.as_ref().to_string_lossy().to_string()];

        // Add plugins
        for plugin in &merged_config.plugins {
            args.push("--plugin".to_string());
            args.push(plugin.clone());
        }

        // Add rules
        if let Some(rules_path) = &merged_config.rules_path {
            args.push("--rules".to_string());
            args.push(rules_path.to_string_lossy().to_string());
        }

        // Add output options
        args.push("--format".to_string());
        args.push(merged_config.output_format.clone());

        if let Some(output_file) = &merged_config.output_file {
            args.push("--output".to_string());
            args.push(output_file.to_string_lossy().to_string());
        }

        // Add timeout
        args.push("--timeout".to_string());
        args.push(merged_config.timeout.to_string());

        self.execute_scanner(&args, merged_config.working_directory.as_deref()).await
    }

    /// Scan with specific plugins
    pub async fn scan_with_plugins<P: AsRef<Path>>(
        &self,
        target_path: P,
        plugins: Vec<String>,
    ) -> Result<ScanResult, Box<dyn std::error::Error>> {
        let options = ScanOptions {
            static_plugins: plugins,
            ..Default::default()
        };

        self.scan_directory(target_path, Some(options)).await
    }

    /// Scan with custom rules
    pub async fn scan_with_rules<P: AsRef<Path>, R: AsRef<Path>>(
        &self,
        target_path: P,
        rules_path: R,
    ) -> Result<ScanResult, Box<dyn std::error::Error>> {
        let options = ScanOptions {
            static_rules: Some(rules_path.as_ref().to_path_buf()),
            ..Default::default()
        };

        self.scan_directory(target_path, Some(options)).await
    }

    /// Execute the scanner subprocess
    async fn execute_scanner(
        &self,
        args: &[String],
        working_directory: Option<&Path>,
    ) -> Result<ScanResult, Box<dyn std::error::Error>> {
        let scanner_path = self.config.scanner_path.as_ref()
            .ok_or("Scanner path not configured")?;

        let mut command = Command::new(scanner_path);
        command.args(args);
        command.stdout(Stdio::piped());
        command.stderr(Stdio::piped());

        if let Some(cwd) = working_directory {
            command.current_dir(cwd);
        }

        let timeout_duration = Duration::from_secs(self.config.timeout);

        let output = timeout(timeout_duration, command.output()).await??;

        if !output.status.success() {
            let stderr = String::from_utf8_lossy(&output.stderr);
            return Ok(ScanResult {
                status: "error".to_string(),
                results: None,
                output: None,
                error: Some(stderr.trim().to_string()),
            });
        }

        let stdout = String::from_utf8_lossy(&output.stdout).trim().to_string();

        if stdout.is_empty() {
            return Ok(ScanResult {
                status: "success".to_string(),
                results: Some(Vec::new()),
                output: None,
                error: None,
            });
        }

        // Try to parse as JSON
        match serde_json::from_str::<Vec<serde_json::Value>>(&stdout) {
            Ok(results) => Ok(ScanResult {
                status: "success".to_string(),
                results: Some(results),
                output: None,
                error: None,
            }),
            Err(_) => Ok(ScanResult {
                status: "success".to_string(),
                results: None,
                output: Some(stdout),
                error: None,
            }),
        }
    }

    /// Create a temporary plugin configuration file
    pub async fn create_plugin_config(
        &self,
        plugin_name: &str,
        config: &HashMap<String, serde_json::Value>,
    ) -> Result<PathBuf, Box<dyn std::error::Error>> {
        let temp_path = std::env::temp_dir()
            .join(format!("tavo-plugin-{}-{}.json", plugin_name, uuid::Uuid::new_v4()));

        let json = serde_json::to_string_pretty(config)?;
        tokio::fs::write(&temp_path, json).await?;

        Ok(temp_path)
    }

    /// Create a temporary rules file
    pub async fn create_rules_file(
        &self,
        rules: &HashMap<String, serde_json::Value>,
    ) -> Result<PathBuf, Box<dyn std::error::Error>> {
        let temp_path = std::env::temp_dir()
            .join(format!("tavo-rules-{}.json", uuid::Uuid::new_v4()));

        let json = serde_json::to_string_pretty(rules)?;
        tokio::fs::write(&temp_path, json).await?;

        Ok(temp_path)
    }
}

impl Default for TavoScanner {
    fn default() -> Self {
        Self::new(None)
    }
}
