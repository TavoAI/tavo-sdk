package net.tavoai;

import java.util.Map;

/**
 * Billing operations
 */
public class BillingOperations {
    private static final String BILLING_ENDPOINT = "/billing";

    private final TavoClient client;

    /**
     * Constructor for BillingOperations.
     * @param client the TavoClient instance
     */
    public BillingOperations(TavoClient client) {
        this.client = client;
    }

    /**
     * Get billing information.
     * @return a map containing billing information
     * @throws TavoException if the request fails
     */
    public Map<String, Object> get() throws TavoException {
        return client.makeRequest("GET", BILLING_ENDPOINT, null);
    }

    /**
     * Get usage statistics.
     * @return a map containing usage statistics
     * @throws TavoException if the request fails
     */
    public Map<String, Object> usage() throws TavoException {
        return client.makeRequest("GET", BILLING_ENDPOINT + "/usage", null);
    }

    /**
     * Get invoices.
     * @return a map containing invoice information
     * @throws TavoException if the request fails
     */
    public Map<String, Object> invoices() throws TavoException {
        return client.makeRequest("GET", BILLING_ENDPOINT + "/invoices", null);
    }
}