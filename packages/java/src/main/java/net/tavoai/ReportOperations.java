package net.tavoai;

import java.util.Map;

/**
 * Report operations
 */
public class ReportOperations {
    private static final String REPORTS_ENDPOINT = "/reports";

    private final TavoClient client;

    /**
     * Constructor for ReportOperations.
     * @param client the TavoClient instance
     */
    public ReportOperations(TavoClient client) {
        this.client = client;
    }

    /**
     * Generate a report with the given parameters.
     * @param reportRequest a map containing report generation parameters
     * @return a map containing the generated report
     * @throws TavoException if the request fails
     */
    public Map<String, Object> generate(Map<String, Object> reportRequest) throws TavoException {
        return client.makeRequest("POST", REPORTS_ENDPOINT + "/generate", reportRequest);
    }

    /**
     * Get report by report ID.
     * @param reportId the ID of the report to retrieve
     * @return a map containing the report data
     * @throws TavoException if the request fails
     */
    public Map<String, Object> get(String reportId) throws TavoException {
        return client.makeRequest("GET", REPORTS_ENDPOINT + "/" + reportId, null);
    }

    /**
     * List all reports.
     * @return a map containing the list of reports
     * @throws TavoException if the request fails
     */
    public Map<String, Object> list() throws TavoException {
        return client.makeRequest("GET", REPORTS_ENDPOINT, null);
    }

    /**
     * Delete a report by report ID.
     * @param reportId the ID of the report to delete
     * @return a map containing the deletion response
     * @throws TavoException if the request fails
     */
    public Map<String, Object> delete(String reportId) throws TavoException {
        return client.makeRequest("DELETE", REPORTS_ENDPOINT + "/" + reportId, null);
    }

    /**
     * Get report summary statistics.
     * @return a map containing summary statistics
     * @throws TavoException if the request fails
     */
    public Map<String, Object> getSummary() throws TavoException {
        return client.makeRequest("GET", REPORTS_ENDPOINT + "/summary", null);
    }
}