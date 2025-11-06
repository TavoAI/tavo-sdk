/**
 * Ai_Analysis_Core API Client
 */

import { AxiosInstance } from 'axios'

export class Ai_Analysis_CoreClient {
  private httpClient: AxiosInstance

  constructor(private baseURL: string, httpClient: AxiosInstance) {
    this.httpClient = httpClient
  }

  /**
   * GET /analyses
   */
  async getAnalyses(skip?: number, limit?: number, scan_id?: string, analysis_type?: string, status?: string, start_date?: string, end_date?: string): Promise<Dict[str, Any]> {
        const params = {'skip: skip, limit: limit, scan_id: scan_id, analysis_type: analysis_type, status: status, start_date: start_date, end_date: end_date'}
        const data = undefined
        return this.httpClient.get(`/analyses`, params)
  }
  /**
   * GET /analyses/{analysis_id}
   */
  async getAnalyses{analysis_id}(analysis_id: string): Promise<Dict[str, Any]> {
        const params = {'analysis_id: analysis_id'}
        const data = undefined
        return this.httpClient.get(`/analyses/{analysis_id}`, params)
  }
}
