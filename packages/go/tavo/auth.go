package tavo

// AuthOperations handles authentication-related operations
type AuthOperations struct {
	client *Client
}

// Login authenticates a user and returns a JWT token
func (a *AuthOperations) Login(username, password string) (map[string]interface{}, error) {
	body := map[string]interface{}{
		"username": username,
		"password": password,
	}
	return a.client.makeRequest("POST", "/auth/login", body)
}

// Register creates a new user account
func (a *AuthOperations) Register(userData map[string]interface{}) (map[string]interface{}, error) {
	return a.client.makeRequest("POST", "/auth/register", userData)
}

// RefreshToken refreshes a JWT token
func (a *AuthOperations) RefreshToken(refreshToken string) (map[string]interface{}, error) {
	body := map[string]interface{}{
		"refresh_token": refreshToken,
	}
	return a.client.makeRequest("POST", "/auth/refresh", body)
}

// Me returns the current user's information
func (a *AuthOperations) Me() (map[string]interface{}, error) {
	return a.client.makeRequest("GET", "/auth/me", nil)
}
