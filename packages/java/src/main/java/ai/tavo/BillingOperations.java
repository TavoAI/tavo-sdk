package ai.tavo;

import java.util.Map;

/**
 * Billing operations
 */
public class BillingOperations {
    private static final String BILLING_ENDPOINT = "/billing";

    private final TavoClient client;

    public BillingOperations(TavoClient client) {
        this.client = client;
    }

    /**
     * Get billing information
     */
    public Map<String, Object> get() throws TavoException {
        return client.makeRequest("GET", BILLING_ENDPOINT, null);
    }

    /**
     * Get usage statistics
     */
    public Map<String, Object> usage() throws TavoException {
        return client.makeRequest("GET", BILLING_ENDPOINT + "/usage", null);
    }

    /**
     * Get invoices
     */
    public Map<String, Object> invoices() throws TavoException {
        return client.makeRequest("GET", BILLING_ENDPOINT + "/invoices", null);
    }
}