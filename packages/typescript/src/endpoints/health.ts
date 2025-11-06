/**
 * Health API Client
 */

import { AxiosInstance } from 'axios'

export class HealthClient {
  private httpClient: AxiosInstance

  constructor(private baseURL: string, httpClient: AxiosInstance) {
    this.httpClient = httpClient
  }

  /**
   * GET /health
   */
  async getHealth(): Promise<Dict[str, Any]> {
        const params = {}
        const data = undefined
        return this.httpClient.get(`/health`, params)
  }
  /**
   * GET /health/ready
   */
  async getHealthready(): Promise<Dict[str, Any]> {
        const params = {}
        const data = undefined
        return this.httpClient.get(`/health/ready`, params)
  }
  /**
   * GET /health/live
   */
  async getHealthlive(): Promise<Dict[str, Any]> {
        const params = {}
        const data = undefined
        return this.httpClient.get(`/health/live`, params)
  }
}
