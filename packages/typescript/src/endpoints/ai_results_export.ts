/**
 * Ai_Results_Export API Client
 */

import { AxiosInstance } from 'axios'

export class Ai_Results_ExportClient {
  private httpClient: AxiosInstance

  constructor(private baseURL: string, httpClient: AxiosInstance) {
    this.httpClient = httpClient
  }

  /**
   * GET /results
   */
  async getResults(skip?: number, limit?: number, scan_id?: string, analysis_type?: string, severity?: string, start_date?: string, end_date?: string): Promise<Dict[str, Any]> {
        const params = {'skip: skip, limit: limit, scan_id: scan_id, analysis_type: analysis_type, severity: severity, start_date: start_date, end_date: end_date'}
        const data = undefined
        return this.httpClient.get(`/results`, params)
  }
  /**
   * GET /results/export
   */
  async getResultsexport(format?: string, scan_id?: string, analysis_type?: string, start_date?: string, end_date?: string): Promise<Response> {
        const params = {'format: format, scan_id: scan_id, analysis_type: analysis_type, start_date: start_date, end_date: end_date'}
        const data = undefined
        return this.httpClient.get(`/results/export`, params)
  }
}
