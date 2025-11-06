/**
 * Ai_Performance_Quality API Client
 */

import { AxiosInstance } from 'axios'

export class Ai_Performance_QualityClient {
  private httpClient: AxiosInstance

  constructor(private baseURL: string, httpClient: AxiosInstance) {
    this.httpClient = httpClient
  }

  /**
   * GET /performance-metrics
   */
  async getPerformancemetrics(start_date?: string, end_date?: string, analysis_type?: string): Promise<Dict[str, Any]> {
        const params = {'start_date: start_date, end_date: end_date, analysis_type: analysis_type'}
        const data = undefined
        return this.httpClient.get(`/performance-metrics`, params)
  }
  /**
   * GET /quality-review/{scan_id}
   */
  async getQualityreview{scan_id}(scan_id: string): Promise<Dict[str, Any]> {
        const params = {'scan_id: scan_id'}
        const data = undefined
        return this.httpClient.get(`/quality-review/{scan_id}`, params)
  }
}
