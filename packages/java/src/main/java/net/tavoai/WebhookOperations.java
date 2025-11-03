package net.tavoai;

import java.util.Map;

/**
 * Webhook operations (DEPRECATED - use GitHub App webhook endpoints instead)
 * @deprecated Use GitHub App installation webhook management for CLI tools
 */
@Deprecated
public class WebhookOperations {
    private static final String WEBHOOKS_ENDPOINT = "/webhooks";

    private final TavoClient client;

    public WebhookOperations(TavoClient client) {
        this.client = client;
    }

    /**
     * List webhooks (DEPRECATED)
     * @deprecated Use GitHub App webhook management instead
     */
    @Deprecated
    public Map<String, Object> list() throws TavoException {
        System.err.println("WARNING: WebhookOperations.list() is deprecated. Use GitHub App webhook management instead.");
        return client.makeRequest("GET", WEBHOOKS_ENDPOINT, null);
    }

    /**
     * Create webhook (DEPRECATED)
     * @deprecated Use GitHub App webhook management instead
     */
    @Deprecated
    public Map<String, Object> create(Map<String, Object> webhookData) throws TavoException {
        System.err.println("WARNING: WebhookOperations.create() is deprecated. Use GitHub App webhook management instead.");
        return client.makeRequest("POST", WEBHOOKS_ENDPOINT, webhookData);
    }

    /**
     * Delete webhook (DEPRECATED)
     * @deprecated Use GitHub App webhook management instead
     */
    @Deprecated
    public Map<String, Object> delete(String webhookId) throws TavoException {
        System.err.println("WARNING: WebhookOperations.delete() is deprecated. Use GitHub App webhook management instead.");
        return client.makeRequest("DELETE", WEBHOOKS_ENDPOINT + "/" + webhookId, null);
    }
}
