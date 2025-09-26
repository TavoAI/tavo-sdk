package tavo

import "fmt"

// TavoError represents an error from the Tavo API
type TavoError struct {
	Message    string                 `json:"message"`
	StatusCode int                    `json:"status_code,omitempty"`
	Details    map[string]interface{} `json:"details,omitempty"`
}

func (e *TavoError) Error() string {
	if e.StatusCode > 0 {
		return fmt.Sprintf("Tavo API error (%d): %s", e.StatusCode, e.Message)
	}
	return fmt.Sprintf("Tavo API error: %s", e.Message)
}

// NewTavoError creates a new TavoError
func NewTavoError(message string, statusCode int) *TavoError {
	return &TavoError{
		Message:    message,
		StatusCode: statusCode,
		Details:    make(map[string]interface{}),
	}
}
