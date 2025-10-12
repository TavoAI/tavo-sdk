package net.tavoai;

import java.util.Map;

/**
 * AI analysis operations
 */
public class AIAnalysisOperations {
    private static final String AI_ENDPOINT = "/ai";

    private final TavoClient client;

    /**
     * Constructor for AIAnalysisOperations.
     * @param client the TavoClient instance
     */
    public AIAnalysisOperations(TavoClient client) {
        this.client = client;
    }

    /**
     * Analyze scan results with AI using default parameters.
     * @param scanId the ID of the scan to analyze
     * @return a map containing the analysis results
     * @throws TavoException if the API request fails
     */
    public Map<String, Object> analyze(String scanId) throws TavoException {
        return analyze(scanId, null);
    }

    /**
     * Analyze scan results with AI and custom parameters.
     * @param scanId the ID of the scan to analyze
     * @param params additional parameters for the analysis
     * @return a map containing the analysis results
     * @throws TavoException if the API request fails
     */
    public Map<String, Object> analyze(String scanId, Map<String, Object> params) throws TavoException {
        String endpoint = AI_ENDPOINT + "/analyze/" + scanId;
        return client.makeRequest("POST", endpoint, params);
    }

    /**
     * Get AI analysis results by analysis ID.
     * @param analysisId the ID of the analysis to retrieve
     * @return a map containing the analysis results
     * @throws TavoException if the API request fails
     */
    public Map<String, Object> getAnalysis(String analysisId) throws TavoException {
        return client.makeRequest("GET", AI_ENDPOINT + "/analysis/" + analysisId, null);
    }
}