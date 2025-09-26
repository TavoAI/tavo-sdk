package ai.tavo;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import static org.junit.jupiter.api.Assertions.*;

/**
 * Unit tests for TavoConfig
 */
class TavoConfigTest {
    private static final String TEST_API_KEY = "test-api-key";
    private static final String TEST_JWT_TOKEN = "test-jwt-token";
    private static final String TEST_BASE_URL = "https://custom.api.com";
    private static final String TEST_API_VERSION = "v2";

    @Test
    void testDefaultConfig() {
        TavoConfig config = new TavoConfig();

        assertEquals(TavoConfig.DEFAULT_BASE_URL, config.getBaseUrl());
        assertEquals(TavoConfig.DEFAULT_API_VERSION, config.getApiVersion());
        assertEquals(TavoConfig.DEFAULT_TIMEOUT, config.getTimeout());
        assertEquals(TavoConfig.DEFAULT_MAX_RETRIES, config.getMaxRetries());
    }

    @Test
    void testApiKeyConfig() {
        TavoConfig config = new TavoConfig(TEST_API_KEY);

        assertEquals(TEST_API_KEY, config.getApiKey());
        assertNull(config.getJwtToken());
    }

    @Test
    void testFullConfig() {
        int timeout = 60;
        int maxRetries = 5;

        TavoConfig config = new TavoConfig(TEST_API_KEY, TEST_JWT_TOKEN, TEST_BASE_URL, TEST_API_VERSION, timeout, maxRetries);

        assertEquals(TEST_API_KEY, config.getApiKey());
        assertEquals(TEST_JWT_TOKEN, config.getJwtToken());
        assertEquals(TEST_BASE_URL, config.getBaseUrl());
        assertEquals(TEST_API_VERSION, config.getApiVersion());
        assertEquals(timeout, config.getTimeout());
        assertEquals(maxRetries, config.getMaxRetries());
    }

    @Test
    void testBuilder() {
        TavoConfig config = TavoConfig.builder()
                .apiKey(TEST_API_KEY)
                .jwtToken(TEST_JWT_TOKEN)
                .baseUrl(TEST_BASE_URL)
                .apiVersion(TEST_API_VERSION)
                .timeout(45)
                .maxRetries(3)
                .build();

        assertEquals(TEST_API_KEY, config.getApiKey());
        assertEquals(TEST_JWT_TOKEN, config.getJwtToken());
        assertEquals(TEST_BASE_URL, config.getBaseUrl());
        assertEquals(TEST_API_VERSION, config.getApiVersion());
        assertEquals(45, config.getTimeout());
        assertEquals(3, config.getMaxRetries());
    }

    @Test
    void testValidationWithApiKey() {
        TavoConfig config = new TavoConfig(TEST_API_KEY);
        assertDoesNotThrow(config::validate);
    }

    @Test
    void testValidationWithJwtToken() {
        TavoConfig config = TavoConfig.builder().jwtToken(TEST_JWT_TOKEN).build();
        assertDoesNotThrow(config::validate);
    }

    @Test
    void testValidationFailure() {
        TavoConfig config = new TavoConfig();
        IllegalArgumentException exception = assertThrows(IllegalArgumentException.class, config::validate);
        assertTrue(exception.getMessage().contains("API key or JWT token"));
    }
}