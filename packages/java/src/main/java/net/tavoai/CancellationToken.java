package net.tavoai;

import java.util.concurrent.atomic.AtomicBoolean;

/**
 * Simple cancellation token for async operations.
 * Provides a way to cancel ongoing operations cooperatively.
 */
public class CancellationToken {
    private final AtomicBoolean cancelled = new AtomicBoolean(false);

    /**
     * Create a new cancellation token.
     * @return a new CancellationToken
     */
    public static CancellationToken create() {
        return new CancellationToken();
    }

    /**
     * Create a cancelled cancellation token.
     * @return a cancelled CancellationToken
     */
    public static CancellationToken cancelled() {
        CancellationToken token = new CancellationToken();
        token.cancel();
        return token;
    }

    /**
     * Check if the operation has been cancelled.
     * @return true if cancelled, false otherwise
     */
    public boolean isCancelled() {
        return cancelled.get();
    }

    /**
     * Cancel the operation.
     */
    public void cancel() {
        cancelled.set(true);
    }

    /**
     * Throw CancellationException if cancelled.
     * @throws CancellationException if the operation is cancelled
     */
    public void throwIfCancelled() throws CancellationException {
        if (isCancelled()) {
            throw new CancellationException("Operation was cancelled");
        }
    }

    /**
     * Exception thrown when an operation is cancelled.
     */
    public static class CancellationException extends Exception {
        public CancellationException(String message) {
            super(message);
        }

        public CancellationException(String message, Throwable cause) {
            super(message, cause);
        }
    }
}
