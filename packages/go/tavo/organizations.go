package tavo

import "fmt"

// OrganizationOperations handles organization-related operations
type OrganizationOperations struct {
	client *Client
}

// ListOrganizations lists all organizations the user has access to
func (o *OrganizationOperations) ListOrganizations(params map[string]interface{}) (map[string]interface{}, error) {
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
	return o.client.makeRequest("GET", "/organizations"+query, nil)
}

// GetOrganization returns a specific organization's information
func (o *OrganizationOperations) GetOrganization(orgID string) (map[string]interface{}, error) {
	return o.client.makeRequest("GET", "/organizations/"+orgID, nil)
}

// CreateOrganization creates a new organization
func (o *OrganizationOperations) CreateOrganization(orgData map[string]interface{}) (map[string]interface{}, error) {
	return o.client.makeRequest("POST", "/organizations", orgData)
}

// UpdateOrganization updates an organization's information
func (o *OrganizationOperations) UpdateOrganization(orgID string, orgData map[string]interface{}) (map[string]interface{}, error) {
	return o.client.makeRequest("PUT", "/organizations/"+orgID, orgData)
}

// DeleteOrganization deletes an organization
func (o *OrganizationOperations) DeleteOrganization(orgID string) error {
	_, err := o.client.makeRequest("DELETE", "/organizations/"+orgID, nil)
	return err
}

// AddMember adds a user to an organization
func (o *OrganizationOperations) AddMember(orgID, userID string, role string) (map[string]interface{}, error) {
	body := map[string]interface{}{
		"user_id": userID,
		"role":    role,
	}
	return o.client.makeRequest("POST", "/organizations/"+orgID+"/members", body)
}

// RemoveMember removes a user from an organization
func (o *OrganizationOperations) RemoveMember(orgID, userID string) error {
	_, err := o.client.makeRequest("DELETE", "/organizations/"+orgID+"/members/"+userID, nil)
	return err
}
