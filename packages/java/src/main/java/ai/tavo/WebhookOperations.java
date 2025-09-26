package ai.tavo;

import java.util.Map;

/**
 * Webhook operations
 */
public class WebhookOperations {
    private static final String WEBHOOKS_ENDPOINT = "/webhooks";

    private final TavoClient client;

    public WebhookOperations(TavoClient client) {
        this.client = client;
    }

    /**
     * List webhooks
     */
    public Map<String, Object> list() throws TavoException {
        return client.makeRequest("GET", WEBHOOKS_ENDPOINT, null);
    }

    /**
     * Create webhook
     */
    public Map<String, Object> create(Map<String, Object> webhookData) throws TavoException {
        return client.makeRequest("POST", WEBHOOKS_ENDPOINT, webhookData);
    }

    /**
     * Delete webhook
     */
    public Map<String, Object> delete(String webhookId) throws TavoException {
        return client.makeRequest("DELETE", WEBHOOKS_ENDPOINT + "/" + webhookId, null);
    }
}