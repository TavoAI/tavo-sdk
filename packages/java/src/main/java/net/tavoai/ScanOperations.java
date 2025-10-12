package net.tavoai;

import java.util.HashMap;
import java.util.Map;

/**
 * Operations for security scans
 */
public class ScanOperations {
    private static final String SCANS_ENDPOINT = "/scans";

    private final TavoClient client;

    /**
     * Constructor for ScanOperations.
     * @param client the TavoClient instance
     */
    public ScanOperations(TavoClient client) {
        this.client = client;
    }

    /**
     * Create a new security scan for a repository.
     * @param repositoryUrl the URL of the repository to scan
     * @return a map containing the created scan information
     * @throws TavoException if the request fails
     */
    public Map<String, Object> create(String repositoryUrl) throws TavoException {
        return create(repositoryUrl, new HashMap<>());
    }

    /**
     * Create a new security scan for a repository with additional parameters.
     * @param repositoryUrl the URL of the repository to scan
     * @param additionalParams additional parameters for the scan
     * @return a map containing the created scan information
     * @throws TavoException if the request fails
     */
    public Map<String, Object> create(String repositoryUrl, Map<String, Object> additionalParams) throws TavoException {
        Map<String, Object> data = new HashMap<>(additionalParams);
        data.put("repository_url", repositoryUrl);
        return client.makeRequest("POST", SCANS_ENDPOINT, data);
    }

    /**
     * Get scan details by scan ID.
     * @param scanId the ID of the scan to retrieve
     * @return a map containing the scan details
     * @throws TavoException if the request fails
     */
    public Map<String, Object> get(String scanId) throws TavoException {
        return client.makeRequest("GET", SCANS_ENDPOINT + "/" + scanId, null);
    }

    /**
     * List all scans.
     * @return a map containing the list of scans
     * @throws TavoException if the request fails
     */
    public Map<String, Object> list() throws TavoException {
        return list(new HashMap<>());
    }

    /**
     * List scans with query parameters.
     * @param params query parameters for filtering scans
     * @return a map containing the list of scans
     * @throws TavoException if the request fails
     */
    public Map<String, Object> list(Map<String, String> params) throws TavoException {
        return client.makeRequest("GET", SCANS_ENDPOINT, null, params);
    }

    /**
     * Get scan results by scan ID.
     * @param scanId the ID of the scan
     * @return a map containing the scan results
     * @throws TavoException if the request fails
     */
    public Map<String, Object> results(String scanId) throws TavoException {
        return results(scanId, new HashMap<>());
    }

    /**
     * Get scan results by scan ID with parameters.
     * @param scanId the ID of the scan
     * @param params additional parameters for the results query
     * @return a map containing the scan results
     * @throws TavoException if the request fails
     */
    public Map<String, Object> results(String scanId, Map<String, String> params) throws TavoException {
        return client.makeRequest("GET", SCANS_ENDPOINT + "/" + scanId + "/results", null, params);
    }

    /**
     * Cancel a running scan by scan ID.
     * @param scanId the ID of the scan to cancel
     * @return a map containing the cancellation response
     * @throws TavoException if the request fails
     */
    public Map<String, Object> cancel(String scanId) throws TavoException {
        return client.makeRequest("POST", SCANS_ENDPOINT + "/" + scanId + "/cancel", null);
    }

    /**
     * Access scan rules operations.
     * @return a ScanRuleOperations instance
     */
    public ScanRuleOperations rules() {
        return new ScanRuleOperations(client);
    }
}