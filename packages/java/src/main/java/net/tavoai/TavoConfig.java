package net.tavoai;

/**
 * Configuration for Tavo API client
 */
public class TavoConfig {
    public static final String DEFAULT_BASE_URL = "https://api.tavoai.net";
    public static final String DEFAULT_API_VERSION = "v1";
    public static final int DEFAULT_TIMEOUT = 30;
    public static final int DEFAULT_MAX_RETRIES = 3;

    private String apiKey;
    private String jwtToken;
    private String sessionToken;
    private String baseUrl;
    private String apiVersion;
    private int timeout;
    private int maxRetries;

    /**
     * Default constructor with default values
     */
    public TavoConfig() {
        this.baseUrl = DEFAULT_BASE_URL;
        this.apiVersion = DEFAULT_API_VERSION;
        this.timeout = DEFAULT_TIMEOUT;
        this.maxRetries = DEFAULT_MAX_RETRIES;
    }

    /**
     * Constructor with API key authentication.
     * @param apiKey the API key for authentication
     */
    public TavoConfig(String apiKey) {
        this();
        this.apiKey = apiKey;
    }

    /**
     * Constructor with API key and JWT token authentication.
     * @param apiKey the API key for authentication
     * @param jwtToken the JWT token for authentication
     */
    public TavoConfig(String apiKey, String jwtToken) {
        this();
        this.apiKey = apiKey;
        this.jwtToken = jwtToken;
    }

    /**
     * Constructor with API key, JWT token, and session token authentication.
     * @param apiKey the API key for authentication
     * @param jwtToken the JWT token for authentication
     * @param sessionToken the session token for authentication
     */
    public TavoConfig(String apiKey, String jwtToken, String sessionToken) {
        this();
        this.apiKey = apiKey;
        this.jwtToken = jwtToken;
        this.sessionToken = sessionToken;
    }

    /**
     * Full constructor with all configuration options.
     * @param apiKey the API key for authentication
     * @param jwtToken the JWT token for authentication
     * @param sessionToken the session token for authentication
     * @param baseUrl the base URL for the API
     * @param apiVersion the API version to use
     * @param timeout the request timeout in seconds
     * @param maxRetries the maximum number of retries for failed requests
     */
    public TavoConfig(String apiKey, String jwtToken, String sessionToken, String baseUrl, String apiVersion, int timeout, int maxRetries) {
        this.apiKey = apiKey;
        this.jwtToken = jwtToken;
        this.sessionToken = sessionToken;
        this.baseUrl = baseUrl != null ? baseUrl : DEFAULT_BASE_URL;
        this.apiVersion = apiVersion != null ? apiVersion : DEFAULT_API_VERSION;
        this.timeout = timeout > 0 ? timeout : DEFAULT_TIMEOUT;
        this.maxRetries = maxRetries >= 0 ? maxRetries : DEFAULT_MAX_RETRIES;
    }

    // Getters and setters
    public String getApiKey() {
        return apiKey;
    }

    public void setApiKey(String apiKey) {
        this.apiKey = apiKey;
    }

    public String getJwtToken() {
        return jwtToken;
    }

    public void setJwtToken(String jwtToken) {
        this.jwtToken = jwtToken;
    }

    public String getSessionToken() {
        return sessionToken;
    }

    public void setSessionToken(String sessionToken) {
        this.sessionToken = sessionToken;
    }

    public String getBaseUrl() {
        return baseUrl;
    }

    public void setBaseUrl(String baseUrl) {
        this.baseUrl = baseUrl;
    }

    public String getApiVersion() {
        return apiVersion;
    }

    public void setApiVersion(String apiVersion) {
        this.apiVersion = apiVersion;
    }

    public int getTimeout() {
        return timeout;
    }

    public void setTimeout(int timeout) {
        this.timeout = timeout;
    }

    public int getMaxRetries() {
        return maxRetries;
    }

    public void setMaxRetries(int maxRetries) {
        this.maxRetries = maxRetries;
    }

    /**
     * Validate that authentication credentials are provided
     * @throws IllegalArgumentException if no credentials are provided
     */
    public void validate() {
        if ((apiKey == null || apiKey.trim().isEmpty()) &&
            (jwtToken == null || jwtToken.trim().isEmpty()) &&
            (sessionToken == null || sessionToken.trim().isEmpty())) {
            throw new IllegalArgumentException(
                "Either API key, JWT token, or session token must be provided, or set " +
                "TAVO_API_KEY, TAVO_JWT_TOKEN, or TAVO_SESSION_TOKEN environment variables"
            );
        }
    }

    /**
     * Create config from environment variables.
     * @return a TavoConfig instance configured from environment variables
     */
    public static TavoConfig fromEnvironment() {
        String apiKey = System.getenv("TAVO_API_KEY");
        String jwtToken = System.getenv("TAVO_JWT_TOKEN");
        String sessionToken = System.getenv("TAVO_SESSION_TOKEN");

        TavoConfig config = new TavoConfig();
        config.setApiKey(apiKey);
        config.setJwtToken(jwtToken);
        config.setSessionToken(sessionToken);

        return config;
    }

    /**
     * Builder pattern for fluent configuration.
     * @return a new Builder instance
     */
    public static Builder builder() {
        return new Builder();
    }

    /**
     * Builder class for fluent TavoConfig construction.
     */
    public static class Builder {
        private String apiKey;
        private String jwtToken;
        private String sessionToken;
        private String baseUrl = DEFAULT_BASE_URL;
        private String apiVersion = DEFAULT_API_VERSION;
        private int timeout = DEFAULT_TIMEOUT;
        private int maxRetries = DEFAULT_MAX_RETRIES;

        public Builder apiKey(String apiKey) {
            this.apiKey = apiKey;
            return this;
        }

        public Builder jwtToken(String jwtToken) {
            this.jwtToken = jwtToken;
            return this;
        }

        public Builder sessionToken(String sessionToken) {
            this.sessionToken = sessionToken;
            return this;
        }

        public Builder baseUrl(String baseUrl) {
            this.baseUrl = baseUrl;
            return this;
        }

        public Builder apiVersion(String apiVersion) {
            this.apiVersion = apiVersion;
            return this;
        }

        public Builder timeout(int timeout) {
            this.timeout = timeout;
            return this;
        }

        public Builder maxRetries(int maxRetries) {
            this.maxRetries = maxRetries;
            return this;
        }

        public TavoConfig build() {
            return new TavoConfig(apiKey, jwtToken, sessionToken, baseUrl, apiVersion, timeout, maxRetries);
        }
    }
}