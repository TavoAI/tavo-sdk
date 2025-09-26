package ai.tavo;

import java.util.Map;

/**
 * Report operations
 */
public class ReportOperations {
    private static final String REPORTS_ENDPOINT = "/reports";

    private final TavoClient client;

    public ReportOperations(TavoClient client) {
        this.client = client;
    }

    /**
     * Generate report
     */
    public Map<String, Object> generate(Map<String, Object> reportRequest) throws TavoException {
        return client.makeRequest("POST", REPORTS_ENDPOINT + "/generate", reportRequest);
    }

    /**
     * Get report
     */
    public Map<String, Object> get(String reportId) throws TavoException {
        return client.makeRequest("GET", REPORTS_ENDPOINT + "/" + reportId, null);
    }

    /**
     * List reports
     */
    public Map<String, Object> list() throws TavoException {
        return client.makeRequest("GET", REPORTS_ENDPOINT, null);
    }

    /**
     * Delete report
     */
    public Map<String, Object> delete(String reportId) throws TavoException {
        return client.makeRequest("DELETE", REPORTS_ENDPOINT + "/" + reportId, null);
    }
}