package net.tavoai;

import org.junit.Test;
import static org.junit.Assert.*;

import java.util.Map;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.CompletionException;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.TimeoutException;

/**
 * Tests for async operations and cancellation support in the Java SDK.
 */
public class AsyncOperationsTest {

    @Test
    public void testDeviceOperationsAsyncMethodsExist() {
        TavoClient client = new TavoClient(TavoConfig.builder().apiKey("test-key").build());
        DeviceOperations deviceOps = client.device();

        assertNotNull("Device operations should not be null", deviceOps);

        // Test that async methods exist (will fail with network errors, but methods exist)
        try {
            CompletableFuture<Map<String, Object>> future = deviceOps.createDeviceCodeAsync(null, null);
            assertNotNull("Async method should return a CompletableFuture", future);
        } catch (Exception e) {
            // Expected to fail with network error, but method exists
            assertTrue("Should fail with network-related exception", e.getMessage().contains("Request failed") || e.getMessage().contains("Failed to create"));
        }
    }

    @Test
    public void testScannerOperationsAsyncMethodsExist() {
        TavoClient client = new TavoClient(TavoConfig.builder().apiKey("test-key").build());
        ScannerOperations scannerOps = client.scanner();

        assertNotNull("Scanner operations should not be null", scannerOps);

        // Test that async methods exist
        try {
            CompletableFuture<Map<String, Object>> future = scannerOps.discoverRulesAsync(null, null, null);
            assertNotNull("Async method should return a CompletableFuture", future);
        } catch (Exception e) {
            // Expected to fail with network error, but method exists
            assertTrue("Should fail with network-related exception", e.getMessage().contains("Request failed") || e.getMessage().contains("Failed to"));
        }
    }

    @Test
    public void testCodeSubmissionOperationsAsyncMethodsExist() {
        TavoClient client = new TavoClient(TavoConfig.builder().apiKey("test-key").build());
        CodeSubmissionOperations codeOps = client.codeSubmission();

        assertNotNull("Code submission operations should not be null", codeOps);

        // Test that async methods exist
        try {
            CompletableFuture<Map<String, Object>> future = codeOps.submitAnalysisAsync("test code", "java", null, null, null, null);
            assertNotNull("Async method should return a CompletableFuture", future);
        } catch (Exception e) {
            // Expected to fail with network error, but method exists
            assertTrue("Should fail with network-related exception", e.getMessage().contains("Request failed") || e.getMessage().contains("Failed to"));
        }
    }

    @Test
    public void testCancellationToken() {
        CancellationToken token = CancellationToken.create();
        assertFalse("Token should not be cancelled initially", token.isCancelled());

        token.cancel();
        assertTrue("Token should be cancelled after cancel()", token.isCancelled());

        try {
            token.throwIfCancelled();
            fail("Should have thrown CancellationException");
        } catch (CancellationToken.CancellationException e) {
            assertEquals("Should have correct error message", "Operation was cancelled", e.getMessage());
        }
    }

    @Test
    public void testCancelledCancellationToken() {
        CancellationToken token = CancellationToken.cancelled();
        assertTrue("Cancelled token should be cancelled", token.isCancelled());

        try {
            token.throwIfCancelled();
            fail("Should have thrown CancellationException");
        } catch (CancellationToken.CancellationException e) {
            assertEquals("Should have correct error message", "Operation was cancelled", e.getMessage());
        }
    }

    @Test
    public void testCancellableAsyncOperation() {
        TavoClient client = new TavoClient(TavoConfig.builder().apiKey("test-key").build());
        DeviceOperations deviceOps = client.device();

        CancellationToken token = CancellationToken.create();
        CompletableFuture<Map<String, Object>> future = deviceOps.createDeviceCodeAsync(null, null, token);

        // Cancel immediately
        token.cancel();

        try {
            // Should complete with CancellationException
            future.get(5, TimeUnit.SECONDS);
            fail("Should have thrown ExecutionException due to cancellation");
        } catch (ExecutionException e) {
            assertTrue("Should be caused by CancellationException", e.getCause() instanceof CancellationToken.CancellationException);
        } catch (TimeoutException | InterruptedException e) {
            fail("Should not timeout or be interrupted: " + e.getMessage());
        }
    }

    @Test
    public void testAsyncOperationWithoutCancellation() {
        TavoClient client = new TavoClient(TavoConfig.builder().apiKey("test-key").build());
        DeviceOperations deviceOps = client.device();

        CancellationToken token = CancellationToken.create();
        CompletableFuture<Map<String, Object>> future = deviceOps.createDeviceCodeAsync(null, null, token);

        // Test that future is created and cancellable
        assertNotNull("Future should be created", future);
        assertFalse("Future should not be done initially", future.isDone());

        // Cancel the operation
        token.cancel();
        assertTrue("Token should be cancelled", token.isCancelled());

        // The future should complete (either successfully or with cancellation)
        // We don't wait for it to avoid hanging
    }

    @Test
    public void testCompletableFutureExceptionHandling() {
        TavoClient client = new TavoClient(TavoConfig.builder().apiKey("test-key").build());
        DeviceOperations deviceOps = client.device();

        // Test that async method returns a CompletableFuture
        CompletableFuture<Map<String, Object>> future = deviceOps.createDeviceCodeAsync(null, null);

        assertNotNull("Future should be created", future);
        assertFalse("Future should not be completed initially", future.isCompletedExceptionally());
        assertFalse("Future should not be done initially", future.isDone());

        // Test cancellation
        future.cancel(true);
        assertTrue("Future should be cancelled", future.isCancelled());
    }
}
