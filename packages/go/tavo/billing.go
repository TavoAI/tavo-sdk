package tavo

import "fmt"

// BillingOperations handles billing-related operations
type BillingOperations struct {
	client *Client
}

// GetUsage returns current usage statistics
func (b *BillingOperations) GetUsage() (map[string]interface{}, error) {
	return b.client.makeRequest("GET", "/billing/usage", nil)
}

// GetInvoices returns billing invoices
func (b *BillingOperations) GetInvoices(params map[string]interface{}) (map[string]interface{}, error) {
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
	return b.client.makeRequest("GET", "/billing/invoices"+query, nil)
}

// GetSubscription returns current subscription information
func (b *BillingOperations) GetSubscription() (map[string]interface{}, error) {
	return b.client.makeRequest("GET", "/billing/subscription", nil)
}
