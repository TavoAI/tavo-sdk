package tavo

import "fmt"

// ScanRuleOperations handles scan rule operations
type ScanRuleOperations struct {
	client *Client
}

// ListRules lists all scan rules
func (s *ScanRuleOperations) ListRules(params map[string]interface{}) (map[string]interface{}, error) {
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
	return s.client.makeRequest("GET", "/scan-rules"+query, nil)
}

// GetRule returns a specific scan rule
func (s *ScanRuleOperations) GetRule(ruleID string) (map[string]interface{}, error) {
	return s.client.makeRequest("GET", "/scan-rules/"+ruleID, nil)
}

// CreateRule creates a new scan rule
func (s *ScanRuleOperations) CreateRule(ruleData map[string]interface{}) (map[string]interface{}, error) {
	return s.client.makeRequest("POST", "/scan-rules", ruleData)
}

// UpdateRule updates a scan rule
func (s *ScanRuleOperations) UpdateRule(ruleID string, ruleData map[string]interface{}) (map[string]interface{}, error) {
	return s.client.makeRequest("PUT", "/scan-rules/"+ruleID, ruleData)
}

// DeleteRule deletes a scan rule
func (s *ScanRuleOperations) DeleteRule(ruleID string) error {
	_, err := s.client.makeRequest("DELETE", "/scan-rules/"+ruleID, nil)
	return err
}

// EnableRule enables a scan rule
func (s *ScanRuleOperations) EnableRule(ruleID string) (map[string]interface{}, error) {
	return s.client.makeRequest("POST", "/scan-rules/"+ruleID+"/enable", nil)
}

// DisableRule disables a scan rule
func (s *ScanRuleOperations) DisableRule(ruleID string) (map[string]interface{}, error) {
	return s.client.makeRequest("POST", "/scan-rules/"+ruleID+"/disable", nil)
}
