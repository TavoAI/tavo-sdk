package ai.tavo.examples;

import ai.tavo.TavoClient;
import ai.tavo.TavoConfig;
import java.util.Map;

/**
 * Example usage of the Tavo Java SDK
 */
public class TavoExample {

    public static void main(String[] args) {
        // Create configuration
        TavoConfig config = TavoConfig.builder()
            .apiKey("your-api-key-here")
            .baseUrl("https://api.tavo.ai")
            .build();

        // Create client
        TavoClient client = new TavoClient(config);

        try {
            // Health check
            Map<String, Object> health = client.healthCheck();
            System.out.println("Health check: " + health);

            // Authenticate
            Map<String, Object> auth = client.auth().login("user@example.com", "password");
            System.out.println("Authentication: " + auth);

            // Get user profile
            Map<String, Object> user = client.auth().me();
            System.out.println("User: " + user);

        } catch (Exception e) {
            System.err.println("Error: " + e.getMessage());
        }
    }
}