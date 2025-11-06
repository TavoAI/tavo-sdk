/**
 * Scan_Bulk_Operations API Client
 */

import { AxiosInstance } from 'axios'

export class Scan_Bulk_OperationsClient {
  private httpClient: AxiosInstance

  constructor(private baseURL: string, httpClient: AxiosInstance) {
    this.httpClient = httpClient
  }

  /**
   * POST /bulk/initiate
   */
  async postBulkinitiate(scan_requests: ScanCreate[]): Promise<Dict[str, Any]> {
        const params = {}
        const data = scan_requests
        return this.httpClient.post(`/bulk/initiate`, data, params)
  }
  /**
   * POST /bulk/cancel
   */
  async postBulkcancel(scan_ids: string[]): Promise<Dict[str, Any]> {
        const params = {}
        const data = scan_ids
        return this.httpClient.post(`/bulk/cancel`, data, params)
  }
  /**
   * DELETE /bulk/delete
   */
  async deleteBulkdelete(scan_ids: string[]): Promise<Dict[str, Any]> {
        const params = {}
        const data = scan_ids
        return this.httpClient.delete(`/bulk/delete`, data, params)
  }
  /**
   * GET /bulk/status
   */
  async getBulkstatus(scan_ids?: string[], organization_id?: string, status_filter?: string, limit?: number): Promise<Dict[str, Any]> {
        const params = {'scan_ids: scan_ids, organization_id: organization_id, status_filter: status_filter, limit: limit'}
        const data = undefined
        return this.httpClient.get(`/bulk/status`, params)
  }
}
