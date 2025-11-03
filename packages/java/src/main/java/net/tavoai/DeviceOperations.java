package net.tavoai;

import okhttp3.*;
import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;

import java.io.IOException;
import java.lang.reflect.Type;
import java.util.Map;

/**
 * Device authentication operations for CLI tools and scanners.
 */
public class DeviceOperations extends BaseOperations {
    public DeviceOperations(TavoClient client) {
        super(client);
    }

    /**
     * Create device code for authentication.
     * @param clientId optional client ID
     * @param clientName optional client name
     * @return device code response
     * @throws TavoException if the request fails
     */
    public Map<String, Object> createDeviceCode(String clientId, String clientName) throws TavoException {
        try {
            Map<String, Object> requestBody = createMap();
            if (clientId != null) requestBody.put("client_id", clientId);
            if (clientName != null) requestBody.put("client_name", clientName);

            Request request = new Request.Builder()
                    .url(client.getBaseUrl() + "/device/code")
                    .post(RequestBody.create(gson.toJson(requestBody), JSON))
                    .build();

            return executeRequest(request, mapType);
        } catch (IOException e) {
            throw new TavoException("Failed to create device code", e);
        }
    }

    /**
     * Create CLI-optimized device code for authentication.
     * @param clientId optional client ID
     * @param clientName optional client name (defaults to "Tavo CLI")
     * @return device code response
     * @throws TavoException if the request fails
     */
    public Map<String, Object> createDeviceCodeForCli(String clientId, String clientName) throws TavoException {
        try {
            Map<String, Object> requestBody = createMap();
            if (clientId != null) requestBody.put("client_id", clientId);
            requestBody.put("client_name", clientName != null ? clientName : "Tavo CLI");

            Request request = new Request.Builder()
                    .url(client.getBaseUrl() + "/device/code/cli")
                    .post(RequestBody.create(gson.toJson(requestBody), JSON))
                    .build();

            return executeRequest(request, mapType);
        } catch (IOException e) {
            throw new TavoException("Failed to create CLI device code", e);
        }
    }

    /**
     * Poll for device token.
     * @param deviceCode the device code to poll for
     * @return token response
     * @throws TavoException if the request fails
     */
    public Map<String, Object> pollDeviceToken(String deviceCode) throws TavoException {
        try {
            Map<String, Object> requestBody = createMap();
            requestBody.put("device_code", deviceCode);

            Request request = new Request.Builder()
                    .url(client.getBaseUrl() + "/device/token")
                    .post(RequestBody.create(gson.toJson(requestBody), JSON))
                    .build();

            return executeRequest(request, mapType);
        } catch (IOException e) {
            throw new TavoException("Failed to poll device token", e);
        }
    }

    /**
     * Get device code status (lightweight polling for CLI).
     * @param deviceCode the device code to check
     * @return status response
     * @throws TavoException if the request fails
     */
    public Map<String, Object> getDeviceCodeStatus(String deviceCode) throws TavoException {
        try {
            Request request = new Request.Builder()
                    .url(client.getBaseUrl() + "/device/code/" + deviceCode + "/status")
                    .get()
                    .build();

            return executeRequest(request, mapType);
        } catch (IOException e) {
            throw new TavoException("Failed to get device code status", e);
        }
    }

    /**
     * Get usage warnings and limits for CLI tools.
     * @return usage warnings and limits
     * @throws TavoException if the request fails
     */
    public Map<String, Object> getUsageWarnings() throws TavoException {
        try {
            Request request = new Request.Builder()
                    .url(client.getBaseUrl() + "/device/usage/warnings")
                    .get()
                    .build();

            return executeRequest(request, mapType);
        } catch (IOException e) {
            throw new TavoException("Failed to get usage warnings", e);
        }
    }

    /**
     * Get current limits and quotas for CLI tools.
     * @return limits and quotas
     * @throws TavoException if the request fails
     */
    public Map<String, Object> getLimits() throws TavoException {
        try {
            Request request = new Request.Builder()
                    .url(client.getBaseUrl() + "/device/limits")
                    .get()
                    .build();

            return executeRequest(request, mapType);
        } catch (IOException e) {
            throw new TavoException("Failed to get limits", e);
        }
    }
}
