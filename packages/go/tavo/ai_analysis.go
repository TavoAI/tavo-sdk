package tavo

import "fmt"

// AIAnalysisOperations handles AI analysis operations
type AIAnalysisOperations struct {
	client *Client
}

// AnalyzeCode performs AI analysis on code
func (a *AIAnalysisOperations) AnalyzeCode(codeData map[string]interface{}) (map[string]interface{}, error) {
	return a.client.makeRequest("POST", "/ai/analyze", codeData)
}

// GetAnalysisResults returns the results of an AI analysis
func (a *AIAnalysisOperations) GetAnalysisResults(analysisID string) (map[string]interface{}, error) {
	return a.client.makeRequest("GET", "/ai/analysis/"+analysisID, nil)
}

// ListAnalyses lists all AI analyses
func (a *AIAnalysisOperations) ListAnalyses(params map[string]interface{}) (map[string]interface{}, error) {
	query := ""
	if params != nil {
		query = "?"
		for key, value := range params {
			if query != "?" {
				query += "&"
			}
			query += fmt.Sprintf("%s=%v", key, value)
		}
	}
	return a.client.makeRequest("GET", "/ai/analyses"+query, nil)
}
