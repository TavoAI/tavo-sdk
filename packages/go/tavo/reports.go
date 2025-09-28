package tavo

import "fmt"

// ReportOperations handles report-related operations
type ReportOperations struct {
	client *Client
}

// GenerateReport generates a new report
func (r *ReportOperations) GenerateReport(params map[string]interface{}) (map[string]interface{}, error) {
	return r.client.makeRequest("POST", "/reports", params)
}

// GetReport returns a specific report
func (r *ReportOperations) GetReport(reportID string) (map[string]interface{}, error) {
	return r.client.makeRequest("GET", "/reports/"+reportID, nil)
}

// ListReports lists all reports
func (r *ReportOperations) ListReports(params map[string]interface{}) (map[string]interface{}, error) {
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
	return r.client.makeRequest("GET", "/reports"+query, nil)
}

// DeleteReport deletes a report
func (r *ReportOperations) DeleteReport(reportID string) error {
	_, err := r.client.makeRequest("DELETE", "/reports/"+reportID, nil)
	return err
}

// DownloadReport downloads a report file
func (r *ReportOperations) DownloadReport(reportID string) (map[string]interface{}, error) {
	return r.client.makeRequest("GET", "/reports/"+reportID+"/download", nil)
}

// GetSummary returns report summary statistics
func (r *ReportOperations) GetSummary() (map[string]interface{}, error) {
	return r.client.makeRequest("GET", "/reports/summary", nil)
}
