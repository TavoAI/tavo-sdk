/**
 * TavoAI AI Analysis Client
 *
 * Supports hybrid analysis modes:
 * - Backend: Uses TavoAI infrastructure (metered, optimized)
 * - Local: Direct LLM API calls (user's API keys, unlimited)
 * - Hybrid: Backend for heuristics, local for deep analysis
 */

import axios, { AxiosInstance } from 'axios';

export interface AIAnalysisRequest {
  code?: string;
  findings?: any[];
  ruleId?: string;
  context?: Record<string, any>;
  prompt?: string;
  mode?: 'backend' | 'local' | 'hybrid';
}

export interface AIAnalysisResponse {
  analysis: string;
  confidence: number;
  recommendations: string[];
  metadata: Record<string, any>;
}

export interface LocalAnalysisOptions {
  provider: 'openai' | 'anthropic' | 'google';
  model: string;
  apiKey: string;
  temperature?: number;
  maxTokens?: number;
}

export class AIClient {
  private backendClient: AxiosInstance;
  private localClients: Map<string, any> = new Map();

  constructor(options: {
    apiKey?: string;
    baseURL?: string;
    timeout?: number;
    localProviders?: Record<string, LocalAnalysisOptions>;
  } = {}) {
    // Backend client for TavoAI infrastructure
    this.backendClient = axios.create({
      baseURL: options.baseURL || 'https://api.tavoai.net/v1',
      timeout: options.timeout || 30000,
      headers: {
        'Content-Type': 'application/json',
        ...(options.apiKey && { 'X-API-Key': options.apiKey }),
      },
    });

    // Initialize local LLM clients
    if (options.localProviders) {
      this.initializeLocalClients(options.localProviders);
    }
  }

  private initializeLocalClients(providers: Record<string, LocalAnalysisOptions>): void {
    for (const [name, config] of Object.entries(providers)) {
      switch (config.provider) {
        case 'openai':
          this.localClients.set(name, this.createOpenAIClient(config));
          break;
        case 'anthropic':
          this.localClients.set(name, this.createAnthropicClient(config));
          break;
        case 'google':
          this.localClients.set(name, this.createGoogleClient(config));
          break;
      }
    }
  }

  private createOpenAIClient(config: LocalAnalysisOptions): any {
    // Simplified OpenAI client initialization
    return {
      analyze: async (prompt: string) => {
        // This would use the actual OpenAI SDK
        return {
          analysis: `OpenAI analysis of: ${prompt.substring(0, 100)}...`,
          confidence: 0.85,
          recommendations: ['Consider input validation'],
          metadata: { provider: 'openai', model: config.model }
        };
      }
    };
  }

  private createAnthropicClient(config: LocalAnalysisOptions): any {
    // Simplified Anthropic client initialization
    return {
      analyze: async (prompt: string) => {
        return {
          analysis: `Claude analysis of: ${prompt.substring(0, 100)}...`,
          confidence: 0.90,
          recommendations: ['Add authentication checks'],
          metadata: { provider: 'anthropic', model: config.model }
        };
      }
    };
  }

  private createGoogleClient(config: LocalAnalysisOptions): any {
    // Simplified Google AI client initialization
    return {
      analyze: async (prompt: string) => {
        return {
          analysis: `Gemini analysis of: ${prompt.substring(0, 100)}...`,
          confidence: 0.80,
          recommendations: ['Implement rate limiting'],
          metadata: { provider: 'google', model: config.model }
        };
      }
    };
  }

  async analyze(request: AIAnalysisRequest): Promise<AIAnalysisResponse> {
    const mode = request.mode || 'backend';

    switch (mode) {
      case 'backend':
        return this.analyzeBackend(request);
      case 'local':
        return this.analyzeLocal(request);
      case 'hybrid':
        return this.analyzeHybrid(request);
      default:
        throw new Error(`Unknown analysis mode: ${mode}`);
    }
  }

  private async analyzeBackend(request: AIAnalysisRequest): Promise<AIAnalysisResponse> {
    try {
      const response = await this.backendClient.post('/ai/analyze', request);
      return response.data;
    } catch (error) {
      throw new Error(`Backend analysis failed: ${error}`);
    }
  }

  async analyzeLocal(
    request: AIAnalysisRequest,
    providerName: string = 'default'
  ): Promise<AIAnalysisResponse> {
    const client = this.localClients.get(providerName);
    if (!client) {
      throw new Error(`Local provider '${providerName}' not configured`);
    }

    const prompt = request.prompt || this.buildAnalysisPrompt(request);

    try {
      return await client.analyze(prompt);
    } catch (error) {
      throw new Error(`Local analysis failed: ${error}`);
    }
  }

  private async analyzeHybrid(request: AIAnalysisRequest): Promise<AIAnalysisResponse> {
    // First try backend for fast, cost-effective analysis
    try {
      const backendResult = await this.analyzeBackend(request);
      if (backendResult.confidence > 0.7) {
        return backendResult;
      }
    } catch (error) {
      // Backend failed, fall back to local
    }

    // Fall back to local analysis for complex cases
    return this.analyzeLocal(request);
  }

  private buildAnalysisPrompt(request: AIAnalysisRequest): string {
    let prompt = 'Analyze the following code for security vulnerabilities:\n\n';

    if (request.code) {
      prompt += `Code:\n${request.code}\n\n`;
    }

    if (request.findings && request.findings.length > 0) {
      prompt += `Existing findings:\n${JSON.stringify(request.findings, null, 2)}\n\n`;
    }

    if (request.context) {
      prompt += `Context:\n${JSON.stringify(request.context, null, 2)}\n\n`;
    }

    prompt += 'Provide:\n1. Security analysis\n2. Confidence score (0-1)\n3. Specific recommendations\n\nRespond in JSON format.';

    return prompt;
  }

  // Cost optimization methods
  getEstimatedCost(request: AIAnalysisRequest): number {
    // Estimate token usage and cost
    const estimatedTokens = this.estimateTokenUsage(request);
    return estimatedTokens * 0.00002; // Rough estimate per token
  }

  private estimateTokenUsage(request: AIAnalysisRequest): number {
    let tokens = 0;

    if (request.code) {
      tokens += request.code.length / 4; // Rough character to token conversion
    }

    if (request.findings) {
      tokens += JSON.stringify(request.findings).length / 4;
    }

    return Math.max(tokens, 100); // Minimum token estimate
  }

  // Configuration methods
  addLocalProvider(name: string, config: LocalAnalysisOptions): void {
    switch (config.provider) {
      case 'openai':
        this.localClients.set(name, this.createOpenAIClient(config));
        break;
      case 'anthropic':
        this.localClients.set(name, this.createAnthropicClient(config));
        break;
      case 'google':
        this.localClients.set(name, this.createGoogleClient(config));
        break;
      default:
        throw new Error(`Unsupported provider: ${config.provider}`);
    }
  }

  removeLocalProvider(name: string): void {
    this.localClients.delete(name);
  }

  listLocalProviders(): string[] {
    return Array.from(this.localClients.keys());
  }

  setApiKey(apiKey: string): void {
    this.backendClient.defaults.headers.common['X-API-Key'] = apiKey;
  }
}
