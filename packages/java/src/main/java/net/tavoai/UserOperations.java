package net.tavoai;

import java.util.Map;

/**
 * User management operations
 */
public class UserOperations {
    private static final String USERS_ENDPOINT = "/users";
    private static final String CURRENT_USER_ENDPOINT = "/users/me";
    private static final String API_KEYS_ENDPOINT = "/users/me/api-keys";

    private final TavoClient client;

    public UserOperations(TavoClient client) {
        this.client = client;
    }

    /**
     * Create a new user (admin only)
     */
    public Map<String, Object> create(Map<String, Object> userData) throws TavoException {
        return client.makeRequest("POST", USERS_ENDPOINT, userData);
    }

    /**
     * List all users (admin only)
     */
    public Map<String, Object> list() throws TavoException {
        return client.makeRequest("GET", USERS_ENDPOINT, null);
    }

    /**
     * Get user details
     */
    public Map<String, Object> get(String userId) throws TavoException {
        return client.makeRequest("GET", USERS_ENDPOINT + "/" + userId, null);
    }

    /**
     * Update user (admin only)
     */
    public Map<String, Object> update(String userId, Map<String, Object> userData) throws TavoException {
        return client.makeRequest("PUT", USERS_ENDPOINT + "/" + userId, userData);
    }

    /**
     * Delete user (admin only)
     */
    public Map<String, Object> delete(String userId) throws TavoException {
        return client.makeRequest("DELETE", USERS_ENDPOINT + "/" + userId, null);
    }

    /**
     * Get current user profile
     */
    public Map<String, Object> getCurrentUser() throws TavoException {
        return client.makeRequest("GET", CURRENT_USER_ENDPOINT, null);
    }

    /**
     * Update current user profile
     */
    public Map<String, Object> updateCurrentUser(Map<String, Object> userData) throws TavoException {
        return client.makeRequest("PUT", CURRENT_USER_ENDPOINT, userData);
    }

    /**
     * List current user's API keys
     */
    public Map<String, Object> listApiKeys() throws TavoException {
        return client.makeRequest("GET", API_KEYS_ENDPOINT, null);
    }

    /**
     * Create a new API key
     */
    public Map<String, Object> createApiKey(String name, Map<String, Object> additionalData) throws TavoException {
        Map<String, Object> data = additionalData != null ? new java.util.HashMap<>(additionalData) : new java.util.HashMap<>();
        data.put("name", name);
        return client.makeRequest("POST", API_KEYS_ENDPOINT, data);
    }

    /**
     * Update an API key
     */
    public Map<String, Object> updateApiKey(String apiKeyId, Map<String, Object> updateData) throws TavoException {
        return client.makeRequest("PUT", API_KEYS_ENDPOINT + "/" + apiKeyId, updateData);
    }

    /**
     * Delete an API key
     */
    public Map<String, Object> deleteApiKey(String apiKeyId) throws TavoException {
        client.makeRequest("DELETE", API_KEYS_ENDPOINT + "/" + apiKeyId, null);
        return Map.of("message", "API key deleted successfully");
    }

    /**
     * Rotate an API key
     */
    public Map<String, Object> rotateApiKey(String apiKeyId, Map<String, Object> additionalData) throws TavoException {
        return client.makeRequest("POST", API_KEYS_ENDPOINT + "/" + apiKeyId + "/rotate", additionalData);
    }
}