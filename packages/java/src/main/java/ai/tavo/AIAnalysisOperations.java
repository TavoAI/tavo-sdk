package ai.tavo;

import java.util.Map;

/**
 * AI analysis operations
 */
public class AIAnalysisOperations {
    private static final String AI_ENDPOINT = "/ai";

    private final TavoClient client;

    public AIAnalysisOperations(TavoClient client) {
        this.client = client;
    }

    /**
     * Analyze scan results with AI
     */
    public Map<String, Object> analyze(String scanId) throws TavoException {
        return analyze(scanId, null);
    }

    /**
     * Analyze scan results with AI and custom parameters
     */
    public Map<String, Object> analyze(String scanId, Map<String, Object> params) throws TavoException {
        String endpoint = AI_ENDPOINT + "/analyze/" + scanId;
        return client.makeRequest("POST", endpoint, params);
    }

    /**
     * Get AI analysis results
     */
    public Map<String, Object> getAnalysis(String analysisId) throws TavoException {
        return client.makeRequest("GET", AI_ENDPOINT + "/analysis/" + analysisId, null);
    }
}