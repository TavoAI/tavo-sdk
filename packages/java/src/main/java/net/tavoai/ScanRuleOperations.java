package net.tavoai;

import java.util.Map;

/**
 * Scan rules operations
 */
public class ScanRuleOperations {
    private static final String RULES_ENDPOINT = "/scan-rules";

    private final TavoClient client;

    /**
     * Constructor for ScanRuleOperations.
     * @param client the TavoClient instance
     */
    public ScanRuleOperations(TavoClient client) {
        this.client = client;
    }

    /**
     * List all scan rules.
     * @return a map containing the list of scan rules
     * @throws TavoException if the request fails
     */
    public Map<String, Object> list() throws TavoException {
        return client.makeRequest("GET", RULES_ENDPOINT, null);
    }

    /**
     * Get scan rule by rule ID.
     * @param ruleId the ID of the scan rule to retrieve
     * @return a map containing the scan rule details
     * @throws TavoException if the request fails
     */
    public Map<String, Object> get(String ruleId) throws TavoException {
        return client.makeRequest("GET", RULES_ENDPOINT + "/" + ruleId, null);
    }

    /**
     * Create a new scan rule.
     * @param ruleData a map containing scan rule data
     * @return a map containing the created scan rule
     * @throws TavoException if the request fails
     */
    public Map<String, Object> create(Map<String, Object> ruleData) throws TavoException {
        return client.makeRequest("POST", RULES_ENDPOINT, ruleData);
    }

    /**
     * Update a scan rule by rule ID.
     * @param ruleId the ID of the scan rule to update
     * @param ruleData a map containing updated scan rule data
     * @return a map containing the updated scan rule
     * @throws TavoException if the request fails
     */
    public Map<String, Object> update(String ruleId, Map<String, Object> ruleData) throws TavoException {
        return client.makeRequest("PUT", RULES_ENDPOINT + "/" + ruleId, ruleData);
    }

    /**
     * Delete a scan rule by rule ID.
     * @param ruleId the ID of the scan rule to delete
     * @return a map containing the deletion response
     * @throws TavoException if the request fails
     */
    public Map<String, Object> delete(String ruleId) throws TavoException {
        return client.makeRequest("DELETE", RULES_ENDPOINT + "/" + ruleId, null);
    }
}