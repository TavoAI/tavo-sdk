package tavo

import (
	"encoding/json"
	"fmt"
	"time"

	"github.com/go-resty/resty/v2"
)

// Client is the main client for interacting with the Tavo AI API
type Client struct {
	config     *Config
	httpClient *resty.Client
}

// NewClient creates a new Tavo API client
func NewClient(config *Config) *Client {
	if config == nil {
		config = NewConfig()
	}

	httpClient := resty.New().
		SetBaseURL(config.BaseURL).
		SetTimeout(config.Timeout).
		SetRetryCount(config.MaxRetries).
		SetRetryWaitTime(1 * time.Second).
		SetRetryMaxWaitTime(30 * time.Second).
		AddRetryCondition(func(r *resty.Response, err error) bool {
			// Retry on 5xx errors or network errors
			return r.StatusCode() >= 500 || err != nil
		})

	client := &Client{
		config:     config,
		httpClient: httpClient,
	}

	// Set authentication headers
	if config.JWTToken != "" {
		httpClient.SetAuthToken(config.JWTToken)
	} else if config.SessionToken != "" {
		httpClient.SetHeader("X-Session-Token", config.SessionToken)
	} else if config.APIKey != "" {
		httpClient.SetHeader("X-API-Key", config.APIKey)
	}

	return client
}

// makeRequest performs an HTTP request with proper error handling
func (c *Client) makeRequest(method, path string, body interface{}) (map[string]interface{}, error) {
	var resp *resty.Response
	var err error

	// Prepare request
	req := c.httpClient.R().
		SetHeader("Content-Type", "application/json").
		SetHeader("Accept", "application/json")

	if body != nil {
		req.SetBody(body)
	}

	// Make request based on method
	switch method {
	case "GET":
		resp, err = req.Get(path)
	case "POST":
		resp, err = req.Post(path)
	case "PUT":
		resp, err = req.Put(path)
	case "DELETE":
		resp, err = req.Delete(path)
	case "PATCH":
		resp, err = req.Patch(path)
	default:
		return nil, fmt.Errorf("unsupported HTTP method: %s", method)
	}

	if err != nil {
		return nil, &TavoError{
			Message:    fmt.Sprintf("Request failed: %v", err),
			StatusCode: 0,
		}
	}

	// Handle non-2xx responses
	if resp.StatusCode() < 200 || resp.StatusCode() >= 300 {
		tavoErr := &TavoError{
			StatusCode: resp.StatusCode(),
		}

		// Try to parse error response
		if err := json.Unmarshal(resp.Body(), tavoErr); err != nil {
			// If we can't parse the error, use the status text
			tavoErr.Message = resp.Status()
		}

		return nil, tavoErr
	}

	// Parse successful response
	var result map[string]interface{}
	if len(resp.Body()) > 0 {
		if err := json.Unmarshal(resp.Body(), &result); err != nil {
			return nil, &TavoError{
				Message:    fmt.Sprintf("Failed to parse response: %v", err),
				StatusCode: resp.StatusCode(),
			}
		}
	} else {
		result = make(map[string]interface{})
	}

	return result, nil
}

// HealthCheck performs a health check on the API
func (c *Client) HealthCheck() (map[string]interface{}, error) {
	return c.makeRequest("GET", "/api/v1/health", nil)
}

// Auth returns the authentication operations
func (c *Client) Auth() *AuthOperations {
	return &AuthOperations{client: c}
}

// Users returns the user operations
func (c *Client) Users() *UserOperations {
	return &UserOperations{client: c}
}

// Organizations returns the organization operations
func (c *Client) Organizations() *OrganizationOperations {
	return &OrganizationOperations{client: c}
}

// Jobs returns the job operations
func (c *Client) Jobs() *JobOperations {
	return &JobOperations{client: c}
}

// Scans returns the scan operations
func (c *Client) Scans() *ScanOperations {
	return &ScanOperations{client: c}
}

// Webhooks returns the webhook operations
func (c *Client) Webhooks() *WebhookOperations {
	return &WebhookOperations{client: c}
}

// AIAnalysis returns the AI analysis operations
func (c *Client) AIAnalysis() *AIAnalysisOperations {
	return &AIAnalysisOperations{client: c}
}

// Billing returns the billing operations
func (c *Client) Billing() *BillingOperations {
	return &BillingOperations{client: c}
}

// Reports returns the report operations
func (c *Client) Reports() *ReportOperations {
	return &ReportOperations{client: c}
}

// ScanRules returns the scan rule operations
func (c *Client) ScanRules() *ScanRuleOperations {
	return &ScanRuleOperations{client: c}
}
