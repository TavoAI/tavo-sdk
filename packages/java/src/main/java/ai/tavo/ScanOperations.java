package ai.tavo;

import java.util.HashMap;
import java.util.Map;

/**
 * Operations for security scans
 */
public class ScanOperations {
    private static final String SCANS_ENDPOINT = "/scans";

    private final TavoClient client;

    public ScanOperations(TavoClient client) {
        this.client = client;
    }

    /**
     * Create a new security scan
     */
    public Map<String, Object> create(String repositoryUrl) throws TavoException {
        return create(repositoryUrl, new HashMap<>());
    }

    /**
     * Create a new security scan with additional parameters
     */
    public Map<String, Object> create(String repositoryUrl, Map<String, Object> additionalParams) throws TavoException {
        Map<String, Object> data = new HashMap<>(additionalParams);
        data.put("repository_url", repositoryUrl);
        return client.makeRequest("POST", SCANS_ENDPOINT, data);
    }

    /**
     * Get scan details
     */
    public Map<String, Object> get(String scanId) throws TavoException {
        return client.makeRequest("GET", SCANS_ENDPOINT + "/" + scanId, null);
    }

    /**
     * List scans
     */
    public Map<String, Object> list() throws TavoException {
        return list(new HashMap<>());
    }

    /**
     * List scans with parameters
     */
    public Map<String, Object> list(Map<String, String> params) throws TavoException {
        return client.makeRequest("GET", SCANS_ENDPOINT, null, params);
    }

    /**
     * Get scan results
     */
    public Map<String, Object> results(String scanId) throws TavoException {
        return results(scanId, new HashMap<>());
    }

    /**
     * Get scan results with parameters
     */
    public Map<String, Object> results(String scanId, Map<String, String> params) throws TavoException {
        return client.makeRequest("GET", SCANS_ENDPOINT + "/" + scanId + "/results", null, params);
    }

    /**
     * Cancel a running scan
     */
    public Map<String, Object> cancel(String scanId) throws TavoException {
        return client.makeRequest("POST", SCANS_ENDPOINT + "/" + scanId + "/cancel", null);
    }

    /**
     * Access scan rules operations
     */
    public ScanRuleOperations rules() {
        return new ScanRuleOperations(client);
    }
}