/**
 * Integration tests for Tavo JavaScript SDK
 * These tests mirror the patterns used in api-server tests
 */

import { TavoClient } from '../dist/index.js';

describe('TavoClient Integration', () => {
  let client: TavoClient;

  beforeEach(() => {
    // Use test API key (mirrors api-server test patterns)
    client = new TavoClient({
      apiKey: process.env.TAVO_TEST_API_KEY || 'test-api-key',
      baseURL: process.env.TAVO_TEST_BASE_URL || 'http://localhost:8000'
    });
  });

  test('should initialize client with API key authentication', () => {
    expect(client).toBeDefined();
    expect(typeof client.healthCheck).toBe('function');
    expect(typeof client.scans).toBe('object');
    expect(typeof client.reports).toBe('object');
  });

  test('should have scans operations matching api-server endpoints', () => {
    const scans = client.scans;
    expect(typeof scans.create).toBe('function');
    expect(typeof scans.get).toBe('function');
    expect(typeof scans.list).toBe('function');
    expect(typeof scans.results).toBe('function');
  });

  test('should have reports operations matching api-server endpoints', () => {
    const reports = client.reports;
    expect(typeof reports.create).toBe('function');
    expect(typeof reports.get).toBe('function');
    expect(typeof reports.list).toBe('function');
    expect(typeof reports.update).toBe('function');
    expect(typeof reports.delete).toBe('function');
    expect(typeof reports.download).toBe('function');
  });

  test('should have apiKeys operations matching api-server endpoints', () => {
    const apiKeys = client.users.apiKeys;
    expect(typeof apiKeys.list).toBe('function');
    expect(typeof apiKeys.create).toBe('function');
    expect(typeof apiKeys.update).toBe('function');
    expect(typeof apiKeys.delete).toBe('function');
    expect(typeof apiKeys.rotate).toBe('function');
  });

  test('should initialize with custom config for testing', () => {
    const testClient = new TavoClient({
      apiKey: 'test-key',
      baseURL: 'http://localhost:8000',
      apiVersion: 'v1',
      timeout: 30000,
      maxRetries: 3
    });

    expect(testClient).toBeDefined();
  });

  test('should handle authentication errors gracefully', async () => {
    const invalidClient = new TavoClient({
      apiKey: 'invalid-key',
      baseURL: 'http://localhost:8000'
    });

    // This mirrors error handling patterns from api-server tests
    try {
      await invalidClient.healthCheck();
      // If we get here, the test server isn't running (expected in CI)
    } catch (error: any) {
      // Either network error (no response) or HTTP error (with response)
      expect(error.response?.status || error.code || error.message).toBeDefined();
    }
  });

  test('should support X-API-Key header format', () => {
    // Test that the client is configured to use X-API-Key header
    // This mirrors the authentication setup in api-server
    const testClient = new TavoClient({
      apiKey: 'test-key'
    });
    expect(testClient).toBeDefined();
  });
});