package tavo

import "fmt"

// WebhookOperations handles webhook operations
type WebhookOperations struct {
	client *Client
}

// ListWebhooks lists all webhooks
func (w *WebhookOperations) ListWebhooks(params map[string]interface{}) (map[string]interface{}, error) {
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
	return w.client.makeRequest("GET", "/webhooks"+query, nil)
}

// GetWebhook returns a specific webhook
func (w *WebhookOperations) GetWebhook(webhookID string) (map[string]interface{}, error) {
	return w.client.makeRequest("GET", "/webhooks/"+webhookID, nil)
}

// CreateWebhook creates a new webhook
func (w *WebhookOperations) CreateWebhook(webhookData map[string]interface{}) (map[string]interface{}, error) {
	return w.client.makeRequest("POST", "/webhooks", webhookData)
}

// UpdateWebhook updates a webhook
func (w *WebhookOperations) UpdateWebhook(webhookID string, webhookData map[string]interface{}) (map[string]interface{}, error) {
	return w.client.makeRequest("PUT", "/webhooks/"+webhookID, webhookData)
}

// DeleteWebhook deletes a webhook
func (w *WebhookOperations) DeleteWebhook(webhookID string) error {
	_, err := w.client.makeRequest("DELETE", "/webhooks/"+webhookID, nil)
	return err
}

// TestWebhook tests a webhook by sending a test payload
func (w *WebhookOperations) TestWebhook(webhookID string) (map[string]interface{}, error) {
	return w.client.makeRequest("POST", "/webhooks/"+webhookID+"/test", nil)
}

// GetWebhookDeliveries returns delivery history for a webhook
func (w *WebhookOperations) GetWebhookDeliveries(webhookID string, params map[string]interface{}) (map[string]interface{}, error) {
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
	return w.client.makeRequest("GET", "/webhooks/"+webhookID+"/deliveries"+query, nil)
}
