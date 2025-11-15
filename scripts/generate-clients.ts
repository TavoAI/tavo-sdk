#!/usr/bin/env ts-node

/**
 * Client Generation Script
 *
 * Generates TypeScript API clients from OpenAPI specifications.
 * Uses openapi-typescript-codegen or similar tools to generate clients.
 *
 * Usage:
 *   npm run generate:rule-client
 *   npm run generate:ai-client
 *   npm run generate:sample-client
 */

import { execSync } from 'child_process';
import * as fs from 'fs';
import * as path from 'path';

interface ClientConfig {
  name: string;
  openApiSpec: string;
  outputDir: string;
  baseUrl: string;
}

const CLIENT_CONFIGS: Record<string, ClientConfig> = {
  'rule-client': {
    name: 'RuleRegistryClient',
    openApiSpec: 'https://registry.tavoai.net/api/v1/openapi.json',
    outputDir: 'packages/rule-client/src/generated',
    baseUrl: 'https://registry.tavoai.net/api/v1',
  },
  'ai-client': {
    name: 'AIClient',
    openApiSpec: 'https://api.tavoai.net/v1/openapi.json',
    outputDir: 'packages/ai-client/src/generated',
    baseUrl: 'https://api.tavoai.net/v1',
  },
  'sample-client': {
    name: 'SampleClient',
    openApiSpec: 'https://api.tavoai.net/v1/openapi.json',
    outputDir: 'packages/sample-client/src/generated',
    baseUrl: 'https://api.tavoai.net/v1',
  },
};

function generateClient(clientName: string): void {
  const config = CLIENT_CONFIGS[clientName];
  if (!config) {
    throw new Error(`Unknown client: ${clientName}`);
  }

  console.log(`Generating ${clientName} client...`);

  // Ensure output directory exists
  if (!fs.existsSync(config.outputDir)) {
    fs.mkdirSync(config.outputDir, { recursive: true });
  }

  try {
    // Use openapi-typescript-codegen or similar tool
    // For now, we'll create a placeholder implementation
    // In production, this would use a proper OpenAPI codegen tool

    const clientCode = generateClientTemplate(config);

    const outputPath = path.join(config.outputDir, 'client.ts');
    fs.writeFileSync(outputPath, clientCode);

    console.log(`✅ Generated ${clientName} client at ${outputPath}`);

  } catch (error) {
    console.error(`❌ Failed to generate ${clientName} client:`, error);
    throw error;
  }
}

function generateClientTemplate(config: ClientConfig): string {
  // This is a simplified template. In production, this would use
  // openapi-typescript-codegen or similar to generate proper client code.

  return `/**
 * Auto-generated ${config.name} from OpenAPI spec
 * Generated from: ${config.openApiSpec}
 * Base URL: ${config.baseUrl}
 */

import axios, { AxiosInstance } from 'axios';

export class ${config.name} {
  private client: AxiosInstance;

  constructor(options: {
    apiKey?: string;
    baseURL?: string;
    timeout?: number;
  } = {}) {
    this.client = axios.create({
      baseURL: options.baseURL || '${config.baseUrl}',
      timeout: options.timeout || 30000,
      headers: {
        'Content-Type': 'application/json',
        ...(options.apiKey && { 'X-API-Key': options.apiKey }),
      },
    });

    // Add response interceptor for error handling
    this.client.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.data?.message) {
          const enhancedError = new Error(error.response.data.message);
          (enhancedError as any).code = error.response.data.code;
          (enhancedError as any).details = error.response.data.details;
          throw enhancedError;
        }
        throw error;
      }
    );
  }

  // Placeholder methods - these would be auto-generated from OpenAPI spec
  async health(): Promise<any> {
    const response = await this.client.get('/health');
    return response.data;
  }

  // Add more auto-generated methods here based on OpenAPI spec
}
`;
}

function main(): void {
  const args = process.argv.slice(2);

  if (args.length === 0) {
    console.log('Usage: generate-clients.ts <client-name>');
    console.log('Available clients:', Object.keys(CLIENT_CONFIGS).join(', '));
    process.exit(1);
  }

  const clientName = args[0];

  try {
    generateClient(clientName);
    console.log('🎉 Client generation completed successfully!');
  } catch (error) {
    console.error('💥 Client generation failed:', error);
    process.exit(1);
  }
}

if (require.main === module) {
  main();
}
