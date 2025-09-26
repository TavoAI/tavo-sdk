package net.tavoai;

import java.util.Map;

/**
 * Job operations
 */
public class JobOperations {
    private static final String JOBS_ENDPOINT = "/jobs";

    private final TavoClient client;

    public JobOperations(TavoClient client) {
        this.client = client;
    }

    /**
     * List jobs
     */
    public Map<String, Object> list() throws TavoException {
        return client.makeRequest("GET", JOBS_ENDPOINT, null);
    }

    /**
     * Get job details
     */
    public Map<String, Object> get(String jobId) throws TavoException {
        return client.makeRequest("GET", JOBS_ENDPOINT + "/" + jobId, null);
    }

    /**
     * Cancel job
     */
    public Map<String, Object> cancel(String jobId) throws TavoException {
        return client.makeRequest("POST", JOBS_ENDPOINT + "/" + jobId + "/cancel", null);
    }
}