package net.tavoai.sdk;

/**
 * Main entry point for Tavo AI SDK
 * Provides access to both API client and scanner functionality
 */
public class TavoSdk {

    /** SDK version */
    public static final String VERSION = "0.1.0";

    /**
     * Create a new API client instance
     */
    public static TavoClient createClient() {
        return new TavoClient();
    }

    /**
     * Create a new API client instance with authentication
     */
    public static TavoClient createClient(String apiKey, String jwtToken, String sessionToken) {
        return new TavoClient(apiKey, jwtToken, sessionToken);
    }

    /**
     * Create a new scanner instance
     */
    public static TavoScanner createScanner() {
        return new TavoScanner(new ScannerConfig());
    }

    /**
     * Create a new scanner instance with configuration
     */
    public static TavoScanner createScanner(ScannerConfig config) {
        return new TavoScanner(config);
    }

    /**
     * Create a scanner with specific plugins
     */
    public static TavoScanner createScannerWithPlugins(String... plugins) {
        ScannerConfig config = new ScannerConfig();
        config.plugins = java.util.Arrays.asList(plugins);
        return new TavoScanner(config);
    }

    /**
     * Create a scanner with custom rules
     */
    public static TavoScanner createScannerWithRules(String rulesPath) {
        ScannerConfig config = new ScannerConfig();
        config.rulesPath = rulesPath;
        return new TavoScanner(config);
    }
}
