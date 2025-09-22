/**
 * Unit tests for Tavo JavaScript SDK
 */

import { TavoClient } from '../dist/index.js';

describe('TavoClient', () => {
  let client: TavoClient;
  const mockApiKey = 'test-api-key';

  beforeEach(() => {
    client = new TavoClient({ apiKey: mockApiKey });
  });

  describe('constructor', () => {
    test('should initialize with default config', () => {
      const client = new TavoClient({ apiKey: mockApiKey });
      expect(client).toBeDefined();
    });

    test('should initialize with custom config', () => {
      const client = new TavoClient({
        apiKey: mockApiKey,
        baseURL: 'https://custom.api.com',
        apiVersion: 'v2',
        timeout: 60000,
        maxRetries: 5
      });
      expect(client).toBeDefined();
    });

    test('should throw error without apiKey', () => {
      expect(() => {
        // @ts-ignore - Testing invalid input
        new TavoClient({});
      }).toThrow();
    });
  });

  describe('API structure', () => {
    test('should have healthCheck method', () => {
      expect(typeof client.healthCheck).toBe('function');
    });

    test('should have scans operations', () => {
      const scans = client.scans;
      expect(typeof scans).toBe('object');
      expect(typeof scans.create).toBe('function');
      expect(typeof scans.get).toBe('function');
      expect(typeof scans.list).toBe('function');
    });

    test('should have reports operations', () => {
      const reports = client.reports;
      expect(typeof reports).toBe('object');
      expect(typeof reports.get).toBe('function');
      expect(typeof reports.list).toBe('function');
    });
  });
});