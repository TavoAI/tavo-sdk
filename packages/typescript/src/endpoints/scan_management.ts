/**
 * Scan_Management API Client
 */

import { AxiosInstance } from 'axios'

export class Scan_ManagementClient {
  private httpClient: AxiosInstance

  constructor(private baseURL: string, httpClient: AxiosInstance) {
    this.httpClient = httpClient
  }

  /**
   * POST /
   */
  async postRoot(scan_in: ScanCreate): Promise<dict> {
        const params = {}
        const data = scan_in
        return this.httpClient.post(`/`, data, params)
  }
  /**
   * GET /
   */
  async getRoot(skip?: number, limit?: number, status_filter?: string, organization_id?: string): Promise<List[ScanSchema]> {
        const params = {'skip: skip, limit: limit, status_filter: status_filter, organization_id: organization_id'}
        const data = undefined
        return this.httpClient.get(`/`, params)
  }
  /**
   * GET /{scan_id:uuid}
   */
  async get{scan_id:uuid}(scan_id: string): Promise<Dict[str, Any]> {
        const params = {'scan_id: scan_id'}
        const data = undefined
        return this.httpClient.get(`/{scan_id:uuid}`, params)
  }
  /**
   * GET /{scan_id:uuid}/results
   */
  async get{scan_id:uuid}results(scan_id: string, severity_filter?: string, rule_type_filter?: string, limit?: number): Promise<List[ScanResultSchema]> {
        const params = {'scan_id: scan_id, severity_filter: severity_filter, rule_type_filter: rule_type_filter, limit: limit'}
        const data = undefined
        return this.httpClient.get(`/{scan_id:uuid}/results`, params)
  }
  /**
   * POST /{scan_id:uuid}/cancel
   */
  async post{scan_id:uuid}cancel(scan_id: string): Promise<dict> {
        const params = {}
        const data = scan_id
        return this.httpClient.post(`/{scan_id:uuid}/cancel`, data, params)
  }
}
