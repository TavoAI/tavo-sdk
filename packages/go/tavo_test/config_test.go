package tavo_test
package tavo_test

import (
	"testing"

	"github.com/TavoAI/tavo-go-sdk/tavo"
)

func TestNewConfig(t *testing.T) {
	config := tavo.NewConfig()
	if config == nil {
		t.Fatal("NewConfig() returned nil")
	}

	if config.BaseURL != "https://api.tavoai.net" {
		t.Errorf("Expected BaseURL to be 'https://api.tavoai.net', got '%s'", config.BaseURL)
	}

	if config.APIVersion != "v1" {
		t.Errorf("Expected APIVersion to be 'v1', got '%s'", config.APIVersion)
	}

	if config.MaxRetries != 3 {
		t.Errorf("Expected MaxRetries to be 3, got %d", config.MaxRetries)
	}
}

func TestConfigWithAPIKey(t *testing.T) {
	config := tavo.NewConfig().WithAPIKey("test-key")
	if config.APIKey != "test-key" {
		t.Errorf("Expected APIKey to be 'test-key', got '%s'", config.APIKey)
	}
}

func TestConfigWithBaseURL(t *testing.T) {
	config := tavo.NewConfig().WithBaseURL("https://test.example.com")
	if config.BaseURL != "https://test.example.com" {
		t.Errorf("Expected BaseURL to be 'https://test.example.com', got '%s'", config.BaseURL)
	}
}

func TestNewClient(t *testing.T) {
	config := tavo.NewConfig()
	client := tavo.NewClient(config)

	if client == nil {
		t.Fatal("NewClient() returned nil")
	}

	// Test that operations are accessible
	if client.Auth() == nil {
		t.Error("Auth() returned nil")
	}

	if client.Users() == nil {
		t.Error("Users() returned nil")
	}

	if client.Scans() == nil {
		t.Error("Scans() returned nil")
	}
}