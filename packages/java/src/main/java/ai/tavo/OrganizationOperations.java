package ai.tavo;

import java.util.Map;

/**
 * Organization operations
 */
public class OrganizationOperations {
    private static final String ORGS_ENDPOINT = "/organizations";

    private final TavoClient client;

    public OrganizationOperations(TavoClient client) {
        this.client = client;
    }

    /**
     * List organizations
     */
    public Map<String, Object> list() throws TavoException {
        return client.makeRequest("GET", ORGS_ENDPOINT, null);
    }

    /**
     * Get organization details
     */
    public Map<String, Object> get(String orgId) throws TavoException {
        return client.makeRequest("GET", ORGS_ENDPOINT + "/" + orgId, null);
    }

    /**
     * Create organization
     */
    public Map<String, Object> create(Map<String, Object> orgData) throws TavoException {
        return client.makeRequest("POST", ORGS_ENDPOINT, orgData);
    }

    /**
     * Update organization
     */
    public Map<String, Object> update(String orgId, Map<String, Object> orgData) throws TavoException {
        return client.makeRequest("PUT", ORGS_ENDPOINT + "/" + orgId, orgData);
    }
}