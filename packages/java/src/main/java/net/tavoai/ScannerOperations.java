package net.tavoai;

import okhttp3.*;
import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;

import java.io.IOException;
import java.lang.reflect.Type;
import java.util.Map;
import java.util.HashMap;

/**
 * Scanner integration operations for CLI tools and scanners.
 */
public class ScannerOperations extends BaseOperations {
    public ScannerOperations(TavoClient client) {
        super(client);
    }

    /**
     * Discover rules optimized for scanner types.
     * @param scannerType optional scanner type filter
     * @param language optional language filter
     * @param category optional category filter
     * @return discovered rules
     * @throws TavoException if the request fails
     */
    public Map<String, Object> discoverRules(String scannerType, String language, String category) throws TavoException {
        try {
            HttpUrl.Builder urlBuilder = HttpUrl.parse(client.getBaseUrl() + "/scanner/rules/discover").newBuilder();
            if (scannerType != null) urlBuilder.addQueryParameter("scanner_type", scannerType);
            if (language != null) urlBuilder.addQueryParameter("language", language);
            if (category != null) urlBuilder.addQueryParameter("category", category);

            Request request = new Request.Builder()
                    .url(urlBuilder.build())
                    .get()
                    .build();

            return executeRequest(request, mapType);
        } catch (IOException e) {
            throw new TavoException("Failed to discover rules", e);
        }
    }

    /**
     * Get rules from a specific bundle.
     * @param bundleId the bundle ID
     * @return bundle rules
     * @throws TavoException if the request fails
     */
    public Map<String, Object> getBundleRules(String bundleId) throws TavoException {
        try {
            Request request = new Request.Builder()
                    .url(client.getBaseUrl() + "/scanner/rules/bundle/" + bundleId + "/rules")
                    .get()
                    .build();

            return executeRequest(request, mapType);
        } catch (IOException e) {
            throw new TavoException("Failed to get bundle rules", e);
        }
    }

    /**
     * Track bundle usage by scanners.
     * @param bundleId the bundle ID
     * @param usageData optional usage data
     * @return tracking response
     * @throws TavoException if the request fails
     */
    public Map<String, Object> trackBundleUsage(String bundleId, Map<String, Object> usageData) throws TavoException {
        try {
            Map<String, Object> requestBody = usageData != null ? usageData : createMap();

            Request request = new Request.Builder()
                    .url(client.getBaseUrl() + "/scanner/rules/bundle/" + bundleId + "/use")
                    .post(RequestBody.create(gson.toJson(requestBody), JSON))
                    .build();

            return executeRequest(request, mapType);
        } catch (IOException e) {
            throw new TavoException("Failed to track bundle usage", e);
        }
    }

    /**
     * Discover plugins optimized for scanner types.
     * @param scannerType optional scanner type filter
     * @param language optional language filter
     * @param category optional category filter
     * @return discovered plugins
     * @throws TavoException if the request fails
     */
    public Map<String, Object> discoverPlugins(String scannerType, String language, String category) throws TavoException {
        try {
            HttpUrl.Builder urlBuilder = HttpUrl.parse(client.getBaseUrl() + "/scanner/plugins/discover").newBuilder();
            if (scannerType != null) urlBuilder.addQueryParameter("scanner_type", scannerType);
            if (language != null) urlBuilder.addQueryParameter("language", language);
            if (category != null) urlBuilder.addQueryParameter("category", category);

            Request request = new Request.Builder()
                    .url(urlBuilder.build())
                    .get()
                    .build();

            return executeRequest(request, mapType);
        } catch (IOException e) {
            throw new TavoException("Failed to discover plugins", e);
        }
    }

    /**
     * Get plugin configuration for scanner use.
     * @param pluginId the plugin ID
     * @return plugin configuration
     * @throws TavoException if the request fails
     */
    public Map<String, Object> getPluginConfig(String pluginId) throws TavoException {
        try {
            Request request = new Request.Builder()
                    .url(client.getBaseUrl() + "/scanner/plugins/" + pluginId + "/config")
                    .get()
                    .build();

            return executeRequest(request, mapType);
        } catch (IOException e) {
            throw new TavoException("Failed to get plugin config", e);
        }
    }

    /**
     * Get AI-powered rule/plugin recommendations.
     * @param language optional language context
     * @param scannerType optional scanner type context
     * @param currentRules current rules being used
     * @param currentPlugins current plugins being used
     * @return recommendations
     * @throws TavoException if the request fails
     */
    public Map<String, Object> getRecommendations(String language, String scannerType, java.util.List<String> currentRules, java.util.List<String> currentPlugins) throws TavoException {
        try {
            HttpUrl.Builder urlBuilder = HttpUrl.parse(client.getBaseUrl() + "/scanner/recommendations").newBuilder();
            if (language != null) urlBuilder.addQueryParameter("language", language);
            if (scannerType != null) urlBuilder.addQueryParameter("scannerType", scannerType);
            if (currentRules != null) {
                for (String rule : currentRules) {
                    urlBuilder.addQueryParameter("currentRules", rule);
                }
            }
            if (currentPlugins != null) {
                for (String plugin : currentPlugins) {
                    urlBuilder.addQueryParameter("currentPlugins", plugin);
                }
            }

            Request request = new Request.Builder()
                    .url(urlBuilder.build())
                    .get()
                    .build();

            return executeRequest(request, mapType);
        } catch (IOException e) {
            throw new TavoException("Failed to get recommendations", e);
        }
    }

    /**
     * Send scanner heartbeat for tracking.
     * @param heartbeatData heartbeat data including version, type, active rules/plugins, system info
     * @return heartbeat response
     * @throws TavoException if the request fails
     */
    public Map<String, Object> sendHeartbeat(Map<String, Object> heartbeatData) throws TavoException {
        try {
            Request request = new Request.Builder()
                    .url(client.getBaseUrl() + "/scanner/heartbeat")
                    .post(RequestBody.create(gson.toJson(heartbeatData), JSON))
                    .build();

            return executeRequest(request, mapType);
        } catch (IOException e) {
            throw new TavoException("Failed to send heartbeat", e);
        }
    }
}
