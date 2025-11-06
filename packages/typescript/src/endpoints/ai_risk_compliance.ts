/**
 * Ai_Risk_Compliance API Client
 */

import { AxiosInstance } from 'axios'

export class Ai_Risk_ComplianceClient {
  private httpClient: AxiosInstance

  constructor(private baseURL: string, httpClient: AxiosInstance) {
    this.httpClient = httpClient
  }

  /**
   * GET /risk-scores
   */
  async getRiskscores(skip?: number, limit?: number, scan_id?: string, min_score?: number, max_score?: number): Promise<Dict[str, Any]> {
        const params = {'skip: skip, limit: limit, scan_id: scan_id, min_score: min_score, max_score: max_score'}
        const data = undefined
        return this.httpClient.get(`/risk-scores`, params)
  }
  /**
   * GET /compliance-reports
   */
  async getCompliancereports(skip?: number, limit?: number, scan_id?: string, framework?: string, status?: string): Promise<Dict[str, Any]> {
        const params = {'skip: skip, limit: limit, scan_id: scan_id, framework: framework, status: status'}
        const data = undefined
        return this.httpClient.get(`/compliance-reports`, params)
  }
  /**
   * GET /predictive-analyses
   */
  async getPredictiveanalyses(skip?: number, limit?: number, scan_id?: string, prediction_type?: string, confidence_threshold?: number): Promise<Dict[str, Any]> {
        const params = {'skip: skip, limit: limit, scan_id: scan_id, prediction_type: prediction_type, confidence_threshold: confidence_threshold'}
        const data = undefined
        return this.httpClient.get(`/predictive-analyses`, params)
  }
}
