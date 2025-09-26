package tavo

import "fmt"

// UserOperations handles user-related operations
type UserOperations struct {
	client *Client
}

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
	return u.client.makeRequest("GET", "/users"+query, nil)
}

// GetUser returns a specific user's information
func (u *UserOperations) GetUser(userID string) (map[string]interface{}, error) {
	return u.client.makeRequest("GET", "/users/"+userID, nil)
}

// UpdateUser updates a specific user's information (admin only)
func (u *UserOperations) UpdateUser(userID string, userData map[string]interface{}) (map[string]interface{}, error) {
	return u.client.makeRequest("PUT", "/users/"+userID, userData)
}

// DeleteUser deletes a user (admin only)
func (u *UserOperations) DeleteUser(userID string) error {
	_, err := u.client.makeRequest("DELETE", "/users/"+userID, nil)
	return err
}
