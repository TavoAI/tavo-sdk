package net.tavoai;

import java.util.Map;

/**
 * Organization operations
 */
public class OrganizationOperations {
    private static final String ORGS_ENDPOINT = "/organizations";

    private final TavoClient client;

    /**
     * Constructor for OrganizationOperations.
     * @param client the TavoClient instance
     */
    public OrganizationOperations(TavoClient client) {
        this.client = client;
    }

    /**
     * List all organizations.
     * @return a map containing the list of organizations
     * @throws TavoException if the request fails
     */
    public Map<String, Object> list() throws TavoException {
        return client.makeRequest("GET", ORGS_ENDPOINT, null);
    }

    /**
     * Get organization details by organization ID.
     * @param orgId the ID of the organization to retrieve
     * @return a map containing the organization details
     * @throws TavoException if the request fails
     */
    public Map<String, Object> get(String orgId) throws TavoException {
        return client.makeRequest("GET", ORGS_ENDPOINT + "/" + orgId, null);
    }

    /**
     * Create a new organization.
     * @param orgData a map containing organization data
     * @return a map containing the created organization
     * @throws TavoException if the request fails
     */
    public Map<String, Object> create(Map<String, Object> orgData) throws TavoException {
        return client.makeRequest("POST", ORGS_ENDPOINT, orgData);
    }

    /**
     * Update an organization by organization ID.
     * @param orgId the ID of the organization to update
     * @param orgData a map containing updated organization data
     * @return a map containing the updated organization
     * @throws TavoException if the request fails
     */
    public Map<String, Object> update(String orgId, Map<String, Object> orgData) throws TavoException {
        return client.makeRequest("PUT", ORGS_ENDPOINT + "/" + orgId, orgData);
    }
}