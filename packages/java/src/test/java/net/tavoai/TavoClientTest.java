package net.tavoai;

import net.tavoai.TavoClient;
import net.tavoai.TavoConfig;
import java.util.Map;

/**
 * Simple integration test for the Tavo Java SDK
 */
public class TavoClientTest {

    public static void main(String[] args) {
        try {
            // Create configuration for mock API
            TavoConfig config = TavoConfig.builder()
                .apiKey("test-key")
                .baseUrl("http://127.0.0.1:3001")
                .build();

            // Create client
            TavoClient client = new TavoClient(config);

            // Test health check
            Map<String, Object> health = client.healthCheck();
            System.out.println("Java SDK: API health check passed - " + health);

        } catch (Exception e) {
            System.err.println("Java SDK: Health check failed - " + e.getMessage());
            System.exit(1);
        }
    }
}