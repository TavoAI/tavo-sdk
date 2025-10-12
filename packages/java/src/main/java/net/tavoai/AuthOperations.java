package net.tavoai;

import java.util.Map;

/**
 * Authentication operations
 */
public class AuthOperations {
    private static final String AUTH_ENDPOINT = "/auth";

    private final TavoClient client;

    /**
     * Constructor for AuthOperations.
     * @param client the TavoClient instance
     */
    public AuthOperations(TavoClient client) {
        this.client = client;
    }

    /**
     * Authenticate user and get JWT token.
     * @param username the username for authentication
     * @param password the password for authentication
     * @return a map containing the authentication response with JWT token
     * @throws TavoException if the authentication fails
     */
    public Map<String, Object> login(String username, String password) throws TavoException {
        Map<String, Object> data = Map.of(
            "username", username,
            "password", password
        );
        return client.makeRequest("POST", AUTH_ENDPOINT + "/login", data);
    }

    /**
     * Register a new user.
     * @param userData a map containing user registration data
     * @return a map containing the registration response
     * @throws TavoException if the registration fails
     */
    public Map<String, Object> register(Map<String, Object> userData) throws TavoException {
        return client.makeRequest("POST", AUTH_ENDPOINT + "/register", userData);
    }

    /**
     * Refresh JWT token using refresh token.
     * @param refreshToken the refresh token
     * @return a map containing the new JWT token
     * @throws TavoException if the token refresh fails
     */
    public Map<String, Object> refreshToken(String refreshToken) throws TavoException {
        Map<String, Object> data = Map.of("refresh_token", refreshToken);
        return client.makeRequest("POST", AUTH_ENDPOINT + "/refresh", data);
    }

    /**
     * Get current user information.
     * @return a map containing the current user information
     * @throws TavoException if the request fails
     */
    public Map<String, Object> me() throws TavoException {
        return client.makeRequest("GET", AUTH_ENDPOINT + "/me", null);
    }
}