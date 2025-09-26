package net.tavoai;

import okhttp3.*;
import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;

import java.io.IOException;
import java.lang.reflect.Type;
import java.util.Map;
import java.util.concurrent.TimeUnit;

/**
 * Main client for interacting with Tavo AI API
 */
public class TavoClient implements AutoCloseable {
    private static final String VERSION = "0.1.0";
    private static final MediaType JSON = MediaType.get("application/json; charset=utf-8");

    private final TavoConfig config;
    private final OkHttpClient httpClient;
    private final Gson gson;

    /**
     * Create a new TavoClient with API key authentication
     */
    public TavoClient(String apiKey) {
        this(TavoConfig.builder().apiKey(apiKey).build());
    }

    /**
     * Create a new TavoClient with JWT token authentication
     */
    public TavoClient(String apiKey, String jwtToken) {
        this(TavoConfig.builder().apiKey(apiKey).jwtToken(jwtToken).build());
    }

    /**
     * Create a new TavoClient with custom configuration
     */
    public TavoClient(TavoConfig config) {
        this.config = config;
        this.config.validate();

        this.httpClient = new OkHttpClient.Builder()
                .connectTimeout(config.getTimeout(), TimeUnit.SECONDS)
                .readTimeout(config.getTimeout(), TimeUnit.SECONDS)
                .writeTimeout(config.getTimeout(), TimeUnit.SECONDS)
                .build();

        this.gson = new Gson();
    }

    /**
     * Get the base URL for API requests
     */
    private String getBaseUrl() {
        return config.getBaseUrl() + "/api/" + config.getApiVersion();
    }

    /**
     * Create authentication headers
     */
    private Headers getAuthHeaders() {
        Headers.Builder headers = new Headers.Builder()
                .add("Content-Type", "application/json")
                .add("User-Agent", "tavo-java-sdk/" + VERSION);

        if (config.getJwtToken() != null && !config.getJwtToken().trim().isEmpty()) {
            headers.add("Authorization", "Bearer " + config.getJwtToken());
        } else if (config.getApiKey() != null && !config.getApiKey().trim().isEmpty()) {
            headers.add("X-API-Key", config.getApiKey());
        }

        return headers.build();
    }

    /**
     * Make an HTTP request to the API
     */
    private Map<String, Object> request(String method, String endpoint, Map<String, Object> data) throws TavoException {
        return request(method, endpoint, data, null);
    }

    /**
     * Make an HTTP request to the API with query parameters
     */
    private Map<String, Object> request(String method, String endpoint, Map<String, Object> data, Map<String, String> params) throws TavoException {
        String url = buildUrl(endpoint, params);
        Request request = buildRequest(method, url, data);

        return executeWithRetry(request);
    }

    /**
     * Build the full URL with query parameters
     */
    private String buildUrl(String endpoint, Map<String, String> params) {
        String url = getBaseUrl() + endpoint;

        if (params != null && !params.isEmpty()) {
            HttpUrl.Builder urlBuilder = HttpUrl.parse(url).newBuilder();
            for (Map.Entry<String, String> param : params.entrySet()) {
                urlBuilder.addQueryParameter(param.getKey(), param.getValue());
            }
            url = urlBuilder.build().toString();
        }

        return url;
    }

    /**
     * Build the HTTP request
     */
    private Request buildRequest(String method, String url, Map<String, Object> data) {
        RequestBody requestBody = null;
        if (data != null && !data.isEmpty()) {
            String jsonBody = gson.toJson(data);
            requestBody = RequestBody.create(jsonBody, JSON);
        }

        Request.Builder requestBuilder = new Request.Builder()
                .url(url)
                .headers(getAuthHeaders());

        switch (method.toUpperCase()) {
            case "GET":
                requestBuilder.get();
                break;
            case "POST":
                requestBuilder.post(requestBody != null ? requestBody : RequestBody.create("", JSON));
                break;
            case "PUT":
                requestBuilder.put(requestBody != null ? requestBody : RequestBody.create("", JSON));
                break;
            case "DELETE":
                if (requestBody != null) {
                    requestBuilder.delete(requestBody);
                } else {
                    requestBuilder.delete();
                }
                break;
            default:
                throw new IllegalArgumentException("Unsupported HTTP method: " + method);
        }

        return requestBuilder.build();
    }

    /**
     * Execute request with retry logic
     */
    private Map<String, Object> executeWithRetry(Request request) throws TavoException {
        TavoException lastException = null;

        for (int attempt = 0; attempt <= config.getMaxRetries(); attempt++) {
            try {
                return executeRequest(request);
            } catch (TavoException e) {
                lastException = e;

                // Only retry on server errors (5xx) or network issues
                if (shouldRetry(e, attempt)) {
                    sleepWithBackoff(attempt);
                } else {
                    throw lastException;
                }
            }
        }

        throw lastException;
    }

    /**
     * Execute a single HTTP request
     */
    private Map<String, Object> executeRequest(Request request) throws TavoException {
        try (Response response = httpClient.newCall(request).execute()) {
            int statusCode = response.code();

            if (response.isSuccessful()) {
                return parseResponseBody(response);
            } else {
                String errorBody = response.body() != null ? response.body().string() : "Unknown error";
                throw new TavoException("HTTP " + statusCode + ": " + errorBody, statusCode);
            }
        } catch (IOException e) {
            throw new TavoException("Network error: " + e.getMessage(), e);
        }
    }

    /**
     * Parse response body as JSON
     */
    private Map<String, Object> parseResponseBody(Response response) throws IOException {
        ResponseBody responseBody = response.body();
        if (responseBody != null) {
            String responseString = responseBody.string();
            Type type = new TypeToken<Map<String, Object>>(){}.getType();
            return gson.fromJson(responseString, type);
        } else {
            return Map.of();
        }
    }

    /**
     * Check if request should be retried
     */
    private boolean shouldRetry(TavoException e, int attempt) {
        return attempt < config.getMaxRetries() &&
               (e.getStatusCode() >= 500 || e.getCause() instanceof IOException);
    }

    /**
     * Sleep with exponential backoff
     */
    private void sleepWithBackoff(int attempt) {
        try {
            Thread.sleep((long) Math.pow(2, attempt) * 1000);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            // Don't throw exception during retry backoff, just log and continue
            System.err.println("Retry backoff interrupted: " + e.getMessage());
        }
    }

    /**
     * Health check endpoint
     */
    public Map<String, Object> healthCheck() throws TavoException {
        return request("GET", "/health", null);
    }

    /**
     * Access authentication operations
     */
    public AuthOperations auth() {
        return new AuthOperations(this);
    }

    /**
     * Access user management operations
     */
    public UserOperations users() {
        return new UserOperations(this);
    }

    /**
     * Access organization operations
     */
    public OrganizationOperations organizations() {
        return new OrganizationOperations(this);
    }

    /**
     * Access job operations
     */
    public JobOperations jobs() {
        return new JobOperations(this);
    }

    /**
     * Access scan operations
     */
    public ScanOperations scans() {
        return new ScanOperations(this);
    }

    /**
     * Access webhook operations
     */
    public WebhookOperations webhooks() {
        return new WebhookOperations(this);
    }

    /**
     * Access AI analysis operations
     */
    public AIAnalysisOperations ai() {
        return new AIAnalysisOperations(this);
    }

    /**
     * Access billing operations
     */
    public BillingOperations billing() {
        return new BillingOperations(this);
    }

    /**
     * Access report operations
     */
    public ReportOperations reports() {
        return new ReportOperations(this);
    }

    @Override
    public void close() {
        // OkHttpClient doesn't need explicit closing in modern versions
        // but we keep this for the AutoCloseable interface
    }

    // Package-private method for operations classes to access request method
    Map<String, Object> makeRequest(String method, String endpoint, Map<String, Object> data) throws TavoException {
        return request(method, endpoint, data);
    }

    Map<String, Object> makeRequest(String method, String endpoint, Map<String, Object> data, Map<String, String> params) throws TavoException {
        return request(method, endpoint, data, params);
    }
}