package net.tavoai.sdk;

import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;

import java.io.*;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.*;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.TimeUnit;

/**
 * Configuration for tavo-scanner execution
 */
class ScannerConfig {
    /** Path to tavo-scanner binary */
    public String scannerPath;

    /** List of plugins to use */
    public List<String> plugins = new ArrayList<>();

    /** Plugin-specific configuration */
    public Map<String, Object> pluginConfig = new HashMap<>();

    /** Path to custom rules file */
    public String rulesPath;

    /** Custom rules configuration */
    public Map<String, Object> customRules = new HashMap<>();

    /** Execution timeout in seconds */
    public int timeout = 300;

    /** Working directory for execution */
    public String workingDirectory;

    /** Output format */
    public String outputFormat = "json";

    /** Output file path */
    public String outputFile;

    public ScannerConfig() {
        this.scannerPath = findScannerBinary();
        this.workingDirectory = System.getProperty("user.dir");
    }

    private String findScannerBinary() {
        // Try relative to this class
        String classLocation = getClass().getProtectionDomain().getCodeSource().getLocation().getPath();
        File classDir = new File(classLocation).getParentFile();
        if (classDir != null) {
            File scannerPath = new File(classDir, "../../../tavo-cli/bin/tavo-scanner");
            if (scannerPath.exists()) {
                return scannerPath.getAbsolutePath();
            }
        }

        // Check PATH
        String pathEnv = System.getenv("PATH");
        if (pathEnv != null) {
            String[] paths = pathEnv.split(File.pathSeparator);
            for (String path : paths) {
                File scannerFile = new File(path, "tavo-scanner");
                if (scannerFile.exists()) {
                    return scannerFile.getAbsolutePath();
                }
            }
        }

        return null;
    }
}

/**
 * Scan options for scanner execution
 */
class ScanOptions {
    /** Static analysis enabled */
    public boolean staticAnalysis = true;

    /** Static analysis plugins */
    public List<String> staticPlugins = new ArrayList<>();

    /** Custom rules path */
    public String staticRules;

    /** Dynamic testing enabled */
    public boolean dynamicTesting = false;

    /** Dynamic testing plugins */
    public List<String> dynamicPlugins = new ArrayList<>();

    /** Output format */
    public String outputFormat = "json";

    /** Output file path */
    public String outputFile;

    /** Execution timeout */
    public int timeout = 300;

    /** Files to exclude */
    public List<String> excludePatterns = new ArrayList<>();

    /** Files to include */
    public List<String> includePatterns = new ArrayList<>();
}

/**
 * Scan result from scanner execution
 */
class ScanResult {
    /** Execution status */
    public String status;

    /** Scan results */
    public List<Object> results;

    /** Raw output */
    public String output;

    /** Error message */
    public String error;
}

/**
 * Wrapper for executing tavo-scanner as a subprocess
 */
public class TavoScanner {
    private final ScannerConfig config;
    private final Gson gson = new Gson();

    public TavoScanner(ScannerConfig config) {
        this.config = config != null ? config : new ScannerConfig();
    }

    public TavoScanner() {
        this(null);
    }

    /**
     * Scan a directory with tavo-scanner
     */
    public CompletableFuture<ScanResult> scanDirectory(String targetPath, ScanOptions scanOptions) {
        return CompletableFuture.supplyAsync(() -> {
            try {
                return scanDirectorySync(targetPath, scanOptions);
            } catch (Exception e) {
                ScanResult result = new ScanResult();
                result.status = "error";
                result.error = e.getMessage();
                return result;
            }
        });
    }

    /**
     * Synchronous scan implementation
     */
    private ScanResult scanDirectorySync(String targetPath, ScanOptions scanOptions) throws IOException, InterruptedException {
        if (config.scannerPath == null) {
            throw new FileNotFoundException("tavo-scanner binary not found. Please install tavo-cli or set scannerPath.");
        }

        // Merge configurations
        ScannerConfig mergedConfig = new ScannerConfig();
        mergedConfig.scannerPath = config.scannerPath;
        mergedConfig.plugins = new ArrayList<>(config.plugins);
        mergedConfig.pluginConfig = new HashMap<>(config.pluginConfig);
        mergedConfig.rulesPath = config.rulesPath;
        mergedConfig.customRules = new HashMap<>(config.customRules);
        mergedConfig.timeout = config.timeout;
        mergedConfig.workingDirectory = config.workingDirectory;
        mergedConfig.outputFormat = config.outputFormat;
        mergedConfig.outputFile = config.outputFile;

        if (scanOptions != null) {
            mergedConfig.plugins = scanOptions.staticPlugins;
            mergedConfig.rulesPath = scanOptions.staticRules;
            mergedConfig.timeout = scanOptions.timeout;
            mergedConfig.outputFormat = scanOptions.outputFormat;
            mergedConfig.outputFile = scanOptions.outputFile;
        }

        // Prepare command arguments
        List<String> command = new ArrayList<>();
        command.add(mergedConfig.scannerPath);
        command.add(targetPath);

        // Add plugins
        if (mergedConfig.plugins != null && !mergedConfig.plugins.isEmpty()) {
            for (String plugin : mergedConfig.plugins) {
                command.add("--plugin");
                command.add(plugin);
            }
        }

        // Add rules
        if (mergedConfig.rulesPath != null) {
            command.add("--rules");
            command.add(mergedConfig.rulesPath);
        }

        // Add output options
        if (mergedConfig.outputFormat != null) {
            command.add("--format");
            command.add(mergedConfig.outputFormat);
        }

        if (mergedConfig.outputFile != null) {
            command.add("--output");
            command.add(mergedConfig.outputFile);
        }

        // Add timeout
        if (mergedConfig.timeout > 0) {
            command.add("--timeout");
            command.add(String.valueOf(mergedConfig.timeout));
        }

        return executeScanner(command, mergedConfig.workingDirectory);
    }

    /**
     * Scan with specific plugins
     */
    public CompletableFuture<ScanResult> scanWithPlugins(String targetPath, List<String> plugins) {
        ScanOptions options = new ScanOptions();
        options.staticPlugins = plugins;
        return scanDirectory(targetPath, options);
    }

    /**
     * Scan with custom rules
     */
    public CompletableFuture<ScanResult> scanWithRules(String targetPath, String rulesPath) {
        ScanOptions options = new ScanOptions();
        options.staticRules = rulesPath;
        return scanDirectory(targetPath, options);
    }

    /**
     * Execute the scanner subprocess
     */
    private ScanResult executeScanner(List<String> command, String workingDirectory)
            throws IOException, InterruptedException {

        ProcessBuilder processBuilder = new ProcessBuilder(command);
        processBuilder.directory(new File(workingDirectory));
        processBuilder.redirectErrorStream(true);

        Process process = processBuilder.start();

        // Read output
        StringBuilder output = new StringBuilder();
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()))) {
            String line;
            while ((line = reader.readLine()) != null) {
                output.append(line).append("\n");
            }
        }

        int exitCode = process.waitFor();

        ScanResult result = new ScanResult();

        if (exitCode != 0) {
            result.status = "error";
            result.error = output.toString().trim();
            if (result.error.isEmpty()) {
                result.error = "Scanner exited with code " + exitCode;
            }
            return result;
        }

        String outputStr = output.toString().trim();
        if (outputStr.isEmpty()) {
            result.status = "success";
            result.results = new ArrayList<>();
            return result;
        }

        try {
            result.results = gson.fromJson(outputStr,
                new TypeToken<List<Object>>(){}.getType());
            result.status = "success";
        } catch (Exception e) {
            result.status = "success";
            result.output = outputStr;
        }

        return result;
    }

    /**
     * Create a temporary plugin configuration file
     */
    public String createPluginConfig(String pluginName, Map<String, Object> config) throws IOException {
        Path tempFile = Files.createTempFile("tavo-plugin-" + pluginName + "-", ".json");
        String json = gson.toJson(config);
        Files.writeString(tempFile, json);
        return tempFile.toString();
    }

    /**
     * Create a temporary rules file
     */
    public String createRulesFile(Map<String, Object> rules) throws IOException {
        Path tempFile = Files.createTempFile("tavo-rules-", ".json");
        String json = gson.toJson(rules);
        Files.writeString(tempFile, json);
        return tempFile.toString();
    }
}
