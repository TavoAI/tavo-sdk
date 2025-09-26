package tavo

import (
	"os"
	"time"
)

// Config holds configuration for the Tavo API client
type Config struct {
	APIKey     string        `json:"api_key,omitempty"`
	JWTToken   string        `json:"jwt_token,omitempty"`
	BaseURL    string        `json:"base_url"`
	APIVersion string        `json:"api_version"`
	Timeout    time.Duration `json:"timeout"`
	MaxRetries int           `json:"max_retries"`
}

// NewConfig creates a new configuration with default values
func NewConfig() *Config {
	config := &Config{
		BaseURL:    "https://api.tavoai.net",
		APIVersion: "v1",
		Timeout:    30 * time.Second,
		MaxRetries: 3,
	}

	// Load from environment variables if available
	if apiKey := os.Getenv("TAVO_API_KEY"); apiKey != "" {
		config.APIKey = apiKey
	}

	if baseURL := os.Getenv("TAVO_BASE_URL"); baseURL != "" {
		config.BaseURL = baseURL
	}

	if apiVersion := os.Getenv("TAVO_API_VERSION"); apiVersion != "" {
		config.APIVersion = apiVersion
	}

	return config
}

// WithAPIKey sets the API key
func (c *Config) WithAPIKey(apiKey string) *Config {
	c.APIKey = apiKey
	return c
}

// WithJWTToken sets the JWT token
func (c *Config) WithJWTToken(token string) *Config {
	c.JWTToken = token
	return c
}

// WithBaseURL sets the base URL
func (c *Config) WithBaseURL(url string) *Config {
	c.BaseURL = url
	return c
}

// WithTimeout sets the request timeout
func (c *Config) WithTimeout(timeout time.Duration) *Config {
	c.Timeout = timeout
	return c
}

// WithMaxRetries sets the maximum number of retries
func (c *Config) WithMaxRetries(retries int) *Config {
	c.MaxRetries = retries
	return c
}
