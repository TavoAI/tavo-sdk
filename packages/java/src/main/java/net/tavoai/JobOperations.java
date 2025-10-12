package net.tavoai;

import java.util.Map;

/**
 * Job operations
 */
public class JobOperations {
    private static final String JOBS_ENDPOINT = "/jobs";

    private final TavoClient client;

    /**
     * Constructor for JobOperations.
     * @param client the TavoClient instance
     */
    public JobOperations(TavoClient client) {
        this.client = client;
    }

    /**
     * List all jobs.
     * @return a map containing the list of jobs
     * @throws TavoException if the request fails
     */
    public Map<String, Object> list() throws TavoException {
        return client.makeRequest("GET", JOBS_ENDPOINT, null);
    }

    /**
     * Get job details by job ID.
     * @param jobId the ID of the job to retrieve
     * @return a map containing the job details
     * @throws TavoException if the request fails
     */
    public Map<String, Object> get(String jobId) throws TavoException {
        return client.makeRequest("GET", JOBS_ENDPOINT + "/" + jobId, null);
    }

    /**
     * Cancel a job by job ID.
     * @param jobId the ID of the job to cancel
     * @return a map containing the cancellation response
     * @throws TavoException if the request fails
     */
    public Map<String, Object> cancel(String jobId) throws TavoException {
        return client.makeRequest("POST", JOBS_ENDPOINT + "/" + jobId + "/cancel", null);
    }
}