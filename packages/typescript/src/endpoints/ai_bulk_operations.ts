/**
 * Ai_Bulk_Operations API Client
 */

import { AxiosInstance } from 'axios'

export class Ai_Bulk_OperationsClient {
  private httpClient: AxiosInstance

  constructor(private baseURL: string, httpClient: AxiosInstance) {
    this.httpClient = httpClient
  }

  /**
   * DELETE /bulk/delete
   */
  async deleteBulkdelete(analysis_ids?: string[]): Promise<Dict[str, Any]> {
        const params = {}
        const data = analysis_ids
        return this.httpClient.delete(`/bulk/delete`, data, params)
  }
  /**
   * PUT /bulk/update-status
   */
  async putBulkupdatestatus(analysis_updates?: Dict[str, Any][]): Promise<Dict[str, Any]> {
        const params = {}
        const data = analysis_updates
        return this.httpClient.put(`/bulk/update-status`, data, params)
  }
  /**
   * GET /bulk/export
   */
  async getBulkexport(analysis_ids?: string[], export_format?: string): Promise<Any> {
        const params = {'analysis_ids: analysis_ids, export_format: export_format'}
        const data = undefined
        return this.httpClient.get(`/bulk/export`, params)
  }
}
