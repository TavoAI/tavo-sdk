package tavo

import "fmt"

// UserOperations handles user-related operations
type UserOperations struct {
	client *Client
}

const (
	usersEndpoint   = "/users"
	apiKeysEndpoint = "/users/me/api-keys"
)

// GetCurrentUser returns the current user's profile
func (u *UserOperations) GetCurrentUser() (map[string]interface{}, error) {
	return u.client.makeRequest("GET", "/users/me", nil)
}

// UpdateProfile updates the current user's profile
func (u *UserOperations) UpdateProfile(profileData map[string]interface{}) (map[string]interface{}, error) {
	return u.client.makeRequest("PUT", "/users/me", profileData)
}

// ListUsers lists users (admin only)
func (u *UserOperations) ListUsers(params map[string]interface{}) (map[string]interface{}, error) {
	// Build query parameters
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
	return u.client.makeRequest("GET", usersEndpoint+query, nil)
}

// GetUser returns a specific user's information
func (u *UserOperations) GetUser(userID string) (map[string]interface{}, error) {
	return u.client.makeRequest("GET", usersEndpoint+"/"+userID, nil)
}

// UpdateUser updates a specific user's information (admin only)
func (u *UserOperations) UpdateUser(userID string, userData map[string]interface{}) (map[string]interface{}, error) {
	return u.client.makeRequest("PUT", usersEndpoint+"/"+userID, userData)
}

// DeleteUser deletes a user (admin only)
func (u *UserOperations) DeleteUser(userID string) error {
	_, err := u.client.makeRequest("DELETE", usersEndpoint+"/"+userID, nil)
	return err
}

// ListAPIKeys lists the current user's API keys
func (u *UserOperations) ListAPIKeys() (map[string]interface{}, error) {
	return u.client.makeRequest("GET", apiKeysEndpoint, nil)
}

// CreateAPIKey creates a new API key
func (u *UserOperations) CreateAPIKey(name string, additionalData map[string]interface{}) (map[string]interface{}, error) {
	data := make(map[string]interface{})
	data["name"] = name
	if additionalData != nil {
		for k, v := range additionalData {
			data[k] = v
		}
	}
	return u.client.makeRequest("POST", apiKeysEndpoint, data)
}

// UpdateAPIKey updates an existing API key
func (u *UserOperations) UpdateAPIKey(apiKeyID string, updateData map[string]interface{}) (map[string]interface{}, error) {
	return u.client.makeRequest("PUT", apiKeysEndpoint+"/"+apiKeyID, updateData)
}

// DeleteAPIKey deletes an API key
func (u *UserOperations) DeleteAPIKey(apiKeyID string) error {
	_, err := u.client.makeRequest("DELETE", apiKeysEndpoint+"/"+apiKeyID, nil)
	return err
}

// RotateAPIKey rotates an API key (generates new secret)
func (u *UserOperations) RotateAPIKey(apiKeyID string, additionalData map[string]interface{}) (map[string]interface{}, error) {
	return u.client.makeRequest("POST", apiKeysEndpoint+"/"+apiKeyID+"/rotate", additionalData)
}
