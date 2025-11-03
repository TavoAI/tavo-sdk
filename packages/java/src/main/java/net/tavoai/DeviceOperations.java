package net.tavoai;

import okhttp3.*;
import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;

import java.io.IOException;
import java.lang.reflect.Type;
import java.util.Map;
import java.util.HashMap;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.CompletionException;

/**
 * Device authentication operations for CLI tools and scanners.
 */
public class DeviceOperations {
    private static final String DEVICE_ENDPOINT = "/device";
    private static final MediaType JSON = MediaType.get("application/json; charset=utf-8");

    private final TavoClient client;
    private final Gson gson;
    private final Type mapType;

    /**
     * Constructor for DeviceOperations.
     * @param client the TavoClient instance
     */
    public DeviceOperations(TavoClient client) {
        this.client = client;
        this.gson = new Gson();
        this.mapType = new TypeToken<Map<String, Object>>(){}.getType();
    }

    /**
     * Helper method to create a new map.
     * @return a new HashMap
     */
    private Map<String, Object> createMap() {
        return new HashMap<>();
    }

    /**
     * Create device code for authentication.
     * @param clientId optional client ID
     * @param clientName optional client name
     * @return device code response
     * @throws TavoException if the request fails
     */
    public Map<String, Object> createDeviceCode(String clientId, String clientName) throws TavoException {
        Map<String, Object> requestBody = createMap();
        if (clientId != null) requestBody.put("client_id", clientId);
        if (clientName != null) requestBody.put("client_name", clientName);

        return client.makeRequest("POST", DEVICE_ENDPOINT + "/code", requestBody);
    }

    /**
     * Create CLI-optimized device code for authentication.
     * @param clientId optional client ID
     * @param clientName optional client name (defaults to "Tavo CLI")
     * @return device code response
     * @throws TavoException if the request fails
     */
    public Map<String, Object> createDeviceCodeForCli(String clientId, String clientName) throws TavoException {
        Map<String, Object> requestBody = createMap();
        if (clientId != null) requestBody.put("client_id", clientId);
        requestBody.put("client_name", clientName != null ? clientName : "Tavo CLI");

        return client.makeRequest("POST", DEVICE_ENDPOINT + "/code/cli", requestBody);
    }

    /**
     * Poll for device token.
     * @param deviceCode the device code to poll for
     * @return token response
     * @throws TavoException if the request fails
     */
    public Map<String, Object> pollDeviceToken(String deviceCode) throws TavoException {
        Map<String, Object> requestBody = createMap();
        requestBody.put("device_code", deviceCode);

        return client.makeRequest("POST", DEVICE_ENDPOINT + "/token", requestBody);
    }

    /**
     * Get device code status (lightweight polling for CLI).
     * @param deviceCode the device code to check
     * @return status response
     * @throws TavoException if the request fails
     */
    public Map<String, Object> getDeviceCodeStatus(String deviceCode) throws TavoException {
        return client.makeRequest("GET", DEVICE_ENDPOINT + "/code/" + deviceCode + "/status", null);
    }

    /**
     * Get usage warnings and limits for CLI tools.
     * @return usage warnings and limits
     * @throws TavoException if the request fails
     */
    public Map<String, Object> getUsageWarnings() throws TavoException {
        return client.makeRequest("GET", DEVICE_ENDPOINT + "/usage/warnings", null);
    }

    /**
     * Get current limits and quotas for CLI tools.
     * @return limits and quotas
     * @throws TavoException if the request fails
     */
    public Map<String, Object> getLimits() throws TavoException {
        return client.makeRequest("GET", DEVICE_ENDPOINT + "/limits", null);
    }

    // ===========================================
    // Async Operations with CompletableFuture
    // ===========================================

    /**
     * Create device code asynchronously.
     * @param clientID optional client ID
     * @param clientName optional client name
     * @return CompletableFuture with device code response
     */
    public CompletableFuture<Map<String, Object>> createDeviceCodeAsync(String clientID, String clientName) {
        return CompletableFuture.supplyAsync(() -> {
            try {
                return createDeviceCode(clientID, clientName);
            } catch (TavoException e) {
                throw new CompletionException(e);
            }
        });
    }

    /**
     * Create CLI-optimized device code asynchronously.
     * @param clientID optional client ID
     * @param clientName optional client name (defaults to "Tavo CLI")
     * @return CompletableFuture with device code response
     */
    public CompletableFuture<Map<String, Object>> createDeviceCodeForCliAsync(String clientID, String clientName) {
        return CompletableFuture.supplyAsync(() -> {
            try {
                return createDeviceCodeForCli(clientID, clientName);
            } catch (TavoException e) {
                throw new CompletionException(e);
            }
        });
    }

    /**
     * Poll for device token asynchronously.
     * @param deviceCode the device code to poll for
     * @return CompletableFuture with token response
     */
    public CompletableFuture<Map<String, Object>> pollDeviceTokenAsync(String deviceCode) {
        return CompletableFuture.supplyAsync(() -> {
            try {
                return pollDeviceToken(deviceCode);
            } catch (TavoException e) {
                throw new CompletionException(e);
            }
        });
    }

    /**
     * Get device code status asynchronously (lightweight polling for CLI).
     * @param deviceCode the device code to check
     * @return CompletableFuture with status response
     */
    public CompletableFuture<Map<String, Object>> getDeviceCodeStatusAsync(String deviceCode) {
        return CompletableFuture.supplyAsync(() -> {
            try {
                return getDeviceCodeStatus(deviceCode);
            } catch (TavoException e) {
                throw new CompletionException(e);
            }
        });
    }

    /**
     * Get usage warnings asynchronously.
     * @return CompletableFuture with usage warnings
     */
    public CompletableFuture<Map<String, Object>> getUsageWarningsAsync() {
        return CompletableFuture.supplyAsync(() -> {
            try {
                return getUsageWarnings();
            } catch (TavoException e) {
                throw new CompletionException(e);
            }
        });
    }

    /**
     * Get limits asynchronously.
     * @return CompletableFuture with limits and quotas
     */
    public CompletableFuture<Map<String, Object>> getLimitsAsync() {
        return CompletableFuture.supplyAsync(() -> {
            try {
                return getLimits();
            } catch (TavoException e) {
                throw new CompletionException(e);
            }
        });
    }

    // ===========================================
    // Cancellable Async Operations
    // ===========================================

    /**
     * Create device code with cancellation support.
     * @param clientID optional client ID
     * @param clientName optional client name
     * @param cancellationToken optional cancellation token
     * @return CompletableFuture with device code response
     */
    public CompletableFuture<Map<String, Object>> createDeviceCodeAsync(String clientID, String clientName, CancellationToken cancellationToken) {
        return CompletableFuture.supplyAsync(() -> {
            try {
                if (cancellationToken != null) {
                    cancellationToken.throwIfCancelled();
                }
                return createDeviceCode(clientID, clientName);
            } catch (TavoException | CancellationToken.CancellationException e) {
                throw new CompletionException(e);
            }
        });
    }

    /**
     * Poll device token with cancellation support.
     * @param deviceCode the device code to poll for
     * @param cancellationToken optional cancellation token
     * @return CompletableFuture with token response
     */
    public CompletableFuture<Map<String, Object>> pollDeviceTokenAsync(String deviceCode, CancellationToken cancellationToken) {
        return CompletableFuture.supplyAsync(() -> {
            try {
                if (cancellationToken != null) {
                    cancellationToken.throwIfCancelled();
                }
                return pollDeviceToken(deviceCode);
            } catch (TavoException | CancellationToken.CancellationException e) {
                throw new CompletionException(e);
            }
        });
    }
}
