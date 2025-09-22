/**
 * Integration tests for Tavo JavaScript SDK
 */

import { TavoClient } from '../dist/index.js';

describe('TavoClient Integration', () => {
  let client: TavoClient;

  beforeEach(() => {
    client = new TavoClient({
      apiKey: 'test-api-key',
      baseURL: 'https://api.tavo.ai'
    });
  });

  test('should initialize client', () => {
    expect(client).toBeDefined();
    expect(typeof client.healthCheck).toBe('function');
    expect(typeof client.scans).toBe('object');
    expect(typeof client.reports).toBe('object');
  });

  test('should have scans operations', () => {
    const scans = client.scans;
    expect(typeof scans.create).toBe('function');
    expect(typeof scans.get).toBe('function');
    expect(typeof scans.list).toBe('function');
  });

  test('should have reports operations', () => {
    const reports = client.reports;
    expect(typeof reports.get).toBe('function');
    expect(typeof reports.list).toBe('function');
  });

  test('should initialize with custom config', () => {
    const customClient = new TavoClient({
      apiKey: 'test-key',
      baseURL: 'https://custom.api.com',
      apiVersion: 'v2',
      timeout: 60000,
      maxRetries: 5
    });

    expect(customClient).toBeDefined();
  });
});