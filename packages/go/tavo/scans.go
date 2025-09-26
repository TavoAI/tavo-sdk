package tavo

import "fmt"

// ScanOperations handles scan-related operations
type ScanOperations struct {
	client *Client
}

// ListScans lists all scans
func (s *ScanOperations) ListScans(params map[string]interface{}) (map[string]interface{}, error) {
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
	return s.client.makeRequest("GET", "/scans"+query, nil)
}

// GetScan returns a specific scan's information
func (s *ScanOperations) GetScan(scanID string) (map[string]interface{}, error) {
	return s.client.makeRequest("GET", "/scans/"+scanID, nil)
}

// CreateScan creates a new scan
func (s *ScanOperations) CreateScan(scanData map[string]interface{}) (map[string]interface{}, error) {
	return s.client.makeRequest("POST", "/scans", scanData)
}

// UpdateScan updates a scan's information
func (s *ScanOperations) UpdateScan(scanID string, scanData map[string]interface{}) (map[string]interface{}, error) {
	return s.client.makeRequest("PUT", "/scans/"+scanID, scanData)
}

// DeleteScan deletes a scan
func (s *ScanOperations) DeleteScan(scanID string) error {
	_, err := s.client.makeRequest("DELETE", "/scans/"+scanID, nil)
	return err
}

// GetScanResults returns the results of a specific scan
func (s *ScanOperations) GetScanResults(scanID string, params map[string]interface{}) (map[string]interface{}, error) {
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
	return s.client.makeRequest("GET", "/scans/"+scanID+"/results"+query, nil)
}

// StartScan starts a scan
func (s *ScanOperations) StartScan(scanID string) (map[string]interface{}, error) {
	return s.client.makeRequest("POST", "/scans/"+scanID+"/start", nil)
}

// StopScan stops a running scan
func (s *ScanOperations) StopScan(scanID string) (map[string]interface{}, error) {
	return s.client.makeRequest("POST", "/scans/"+scanID+"/stop", nil)
}

// GetScanStatus returns the status of a scan
func (s *ScanOperations) GetScanStatus(scanID string) (map[string]interface{}, error) {
	return s.client.makeRequest("GET", "/scans/"+scanID+"/status", nil)
}
