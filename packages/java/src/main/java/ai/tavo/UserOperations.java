package net.tavoai;

import java.util.Map;

/**
 * User management operations
 */
public class UserOperations {
    private static final String USERS_ENDPOINT = "/users";

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
}