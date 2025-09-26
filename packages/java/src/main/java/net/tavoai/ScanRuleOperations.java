package net.tavoai;

import java.util.Map;

/**
 * Scan rules operations
 */
public class ScanRuleOperations {
    private static final String RULES_ENDPOINT = "/scan-rules";

    private final TavoClient client;

    public ScanRuleOperations(TavoClient client) {
        this.client = client;
    }

    /**
     * List scan rules
     */
    public Map<String, Object> list() throws TavoException {
        return client.makeRequest("GET", RULES_ENDPOINT, null);
    }

    /**
     * Get scan rule
     */
    public Map<String, Object> get(String ruleId) throws TavoException {
        return client.makeRequest("GET", RULES_ENDPOINT + "/" + ruleId, null);
    }

    /**
     * Create scan rule
     */
    public Map<String, Object> create(Map<String, Object> ruleData) throws TavoException {
        return client.makeRequest("POST", RULES_ENDPOINT, ruleData);
    }

    /**
     * Update scan rule
     */
    public Map<String, Object> update(String ruleId, Map<String, Object> ruleData) throws TavoException {
        return client.makeRequest("PUT", RULES_ENDPOINT + "/" + ruleId, ruleData);
    }

    /**
     * Delete scan rule
     */
    public Map<String, Object> delete(String ruleId) throws TavoException {
        return client.makeRequest("DELETE", RULES_ENDPOINT + "/" + ruleId, null);
    }
}