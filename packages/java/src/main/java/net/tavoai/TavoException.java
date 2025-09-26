package net.tavoai;

/**
 * Exception thrown by Tavo API client operations
 */
public class TavoException extends Exception {
    private final int statusCode;

    /**
     * Create a new TavoException with a message
     */
    public TavoException(String message) {
        super(message);
        this.statusCode = 0;
    }

    /**
     * Create a new TavoException with a message and status code
     */
    public TavoException(String message, int statusCode) {
        super(message);
        this.statusCode = statusCode;
    }

    /**
     * Create a new TavoException with a message and cause
     */
    public TavoException(String message, Throwable cause) {
        super(message, cause);
        this.statusCode = 0;
    }

    /**
     * Create a new TavoException with a message, status code, and cause
     */
    public TavoException(String message, int statusCode, Throwable cause) {
        super(message, cause);
        this.statusCode = statusCode;
    }

    /**
     * Get the HTTP status code associated with this exception
     */
    public int getStatusCode() {
        return statusCode;
    }

    /**
     * Check if this exception represents a client error (4xx)
     */
    public boolean isClientError() {
        return statusCode >= 400 && statusCode < 500;
    }

    /**
     * Check if this exception represents a server error (5xx)
     */
    public boolean isServerError() {
        return statusCode >= 500 && statusCode < 600;
    }

    /**
     * Check if this exception represents an authentication error
     */
    public boolean isAuthenticationError() {
        return statusCode == 401;
    }

    /**
     * Check if this exception represents an authorization error
     */
    public boolean isAuthorizationError() {
        return statusCode == 403;
    }

    /**
     * Check if this exception represents a not found error
     */
    public boolean isNotFoundError() {
        return statusCode == 404;
    }

    /**
     * Check if this exception represents a rate limit error
     */
    public boolean isRateLimitError() {
        return statusCode == 429;
    }
}