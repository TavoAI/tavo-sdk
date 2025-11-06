/**
 * Ai_Analysis API Client
 */

import { AxiosInstance } from 'axios'

export class Ai_AnalysisClient {
  private httpClient: AxiosInstance

  constructor(private baseURL: string, httpClient: AxiosInstance) {
    this.httpClient = httpClient
  }

  /**
   * POST /analyze/{scan_id}
   */
  async postAnalyze{scan_id}(scan_id: string, background_tasks: BackgroundTasks): Promise<CodeFixResponse> {
        const params = {}
        const data = {'scan_id: scan_id, background_tasks: background_tasks'}
        return this.httpClient.post(`/analyze/{scan_id}`, data, params)
  }
  /**
   * POST /classify/{scan_id}
   */
  async postClassify{scan_id}(scan_id: string, background_tasks: BackgroundTasks): Promise<VulnerabilityClassificationResponse> {
        const params = {}
        const data = {'scan_id: scan_id, background_tasks: background_tasks'}
        return this.httpClient.post(`/classify/{scan_id}`, data, params)
  }
  /**
   * POST /risk-score/{scan_id}
   */
  async postRiskscore{scan_id}(scan_id: string): Promise<RiskScoreResponse> {
        const params = {}
        const data = scan_id
        return this.httpClient.post(`/risk-score/{scan_id}`, data, params)
  }
  /**
   * POST /compliance/{scan_id}
   */
  async postCompliance{scan_id}(scan_id: number, framework?: string): Promise<ComplianceReportResponse> {
        const params = {}
        const data = {'scan_id: scan_id, framework: framework'}
        return this.httpClient.post(`/compliance/{scan_id}`, data, params)
  }
  /**
   * POST /predictive/{scan_id}
   */
  async postPredictive{scan_id}(scan_id: string): Promise<PredictiveAnalysisResponse> {
        const params = {}
        const data = scan_id
        return this.httpClient.post(`/predictive/{scan_id}`, data, params)
  }
  /**
   * GET /fix-suggestions
   */
  async getFixsuggestions(search?: string, status?: string, severity?: string, analysis_type?: string, limit?: number, offset?: number): Promise<Dict[str, Any]> {
        const params = {'search: search, status: status, severity: severity, analysis_type: analysis_type, limit: limit, offset: offset'}
        const data = undefined
        return this.httpClient.get(`/fix-suggestions`, params)
  }
  /**
   * GET /predictive
   */
  async getPredictive(time_horizon?: string, severity?: string, prediction_type?: string, analysis_type?: string): Promise<Dict[str, Any]> {
        const params = {'time_horizon: time_horizon, severity: severity, prediction_type: prediction_type, analysis_type: analysis_type'}
        const data = undefined
        return this.httpClient.get(`/predictive`, params)
  }
  /**
   * GET /compliance
   */
  async getCompliance(framework?: string, status?: string, risk_level?: string, category?: string): Promise<Dict[str, Any]> {
        const params = {'framework: framework, status: status, risk_level: risk_level, category: category'}
        const data = undefined
        return this.httpClient.get(`/compliance`, params)
  }
}
