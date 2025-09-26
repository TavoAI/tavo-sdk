package ai.tavo;

import java.util.Map;

/**
 * Authentication operations
 */
public class AuthOperations {
    private static final String AUTH_ENDPOINT = "/auth";

    private final TavoClient client;

    public AuthOperations(TavoClient client) {
        this.client = client;
    }

    /**
     * Authenticate user and get JWT token
     */
    public Map<String, Object> login(String username, String password) throws TavoException {
        Map<String, Object> data = Map.of(
            "username", username,
            "password", password
        );
        return client.makeRequest("POST", AUTH_ENDPOINT + "/login", data);
    }

    /**
     * Register a new user
     */
    public Map<String, Object> register(Map<String, Object> userData) throws TavoException {
        return client.makeRequest("POST", AUTH_ENDPOINT + "/register", userData);
    }

    /**
     * Refresh JWT token
     */
    public Map<String, Object> refreshToken(String refreshToken) throws TavoException {
        Map<String, Object> data = Map.of("refresh_token", refreshToken);
        return client.makeRequest("POST", AUTH_ENDPOINT + "/refresh", data);
    }

    /**
     * Get current user information
     */
    public Map<String, Object> me() throws TavoException {
        return client.makeRequest("GET", AUTH_ENDPOINT + "/me", null);
    }
}