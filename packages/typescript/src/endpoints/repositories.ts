/**
 * Repositories API Client
 */

import { AxiosInstance } from 'axios'

export class RepositoriesClient {
  private httpClient: AxiosInstance

  constructor(private baseURL: string, httpClient: AxiosInstance) {
    this.httpClient = httpClient
  }

  /**
   * POST /sync
   */
  async postSync(background_tasks: BackgroundTasks): Promise<List[RepositoryResponse]> {
        const params = {}
        const data = background_tasks
        return this.httpClient.post(`/sync`, data, params)
  }
  /**
   * GET /
   */
  async getRoot(connection_id?: string, language?: string, scan_enabled?: boolean, search?: string, page?: number, per_page?: number): Promise<RepositoryListResponse> {
        const params = {'connection_id: connection_id, language: language, scan_enabled: scan_enabled, search: search, page: page, per_page: per_page'}
        const data = undefined
        return this.httpClient.get(`/`, params)
  }
  /**
   * GET /{repository_id}
   */
  async get{repository_id}(repository_id: string): Promise<RepositoryResponse> {
        const params = {'repository_id: repository_id'}
        const data = undefined
        return this.httpClient.get(`/{repository_id}`, params)
  }
  /**
   * PUT /{repository_id}
   */
  async put{repository_id}(repository_id: string, repository_update: RepositoryUpdate): Promise<RepositoryResponse> {
        const params = {}
        const data = {'repository_id: repository_id, repository_update: repository_update'}
        return this.httpClient.put(`/{repository_id}`, data, params)
  }
  /**
   * DELETE /{repository_id}
   */
  async delete{repository_id}(repository_id: string): Promise<None> {
        const params = {}
        const data = repository_id
        return this.httpClient.delete(`/{repository_id}`, data, params)
  }
  /**
   * GET /{repository_id}/scans
   */
  async get{repository_id}scans(repository_id: string, limit?: number): Promise<List[ScanInDB]> {
        const params = {'repository_id: repository_id, limit: limit'}
        const data = undefined
        return this.httpClient.get(`/{repository_id}/scans`, params)
  }
  /**
   * POST /{repository_id}/scan
   */
  async post{repository_id}scan(repository_id: string, background_tasks: BackgroundTasks): Promise<ScanInDB> {
        const params = {}
        const data = {'repository_id: repository_id, background_tasks: background_tasks'}
        return this.httpClient.post(`/{repository_id}/scan`, data, params)
  }
  /**
   * GET /{repository_id}/branches
   */
  async get{repository_id}branches(repository_id: string): Promise<List[RepositoryBranchResponse]> {
        const params = {'repository_id: repository_id'}
        const data = undefined
        return this.httpClient.get(`/{repository_id}/branches`, params)
  }
  /**
   * POST /{repository_id}/pause
   */
  async post{repository_id}pause(repository_id: string): Promise<RepositoryResponse> {
        const params = {}
        const data = repository_id
        return this.httpClient.post(`/{repository_id}/pause`, data, params)
  }
  /**
   * POST /{repository_id}/resume
   */
  async post{repository_id}resume(repository_id: string): Promise<RepositoryResponse> {
        const params = {}
        const data = repository_id
        return this.httpClient.post(`/{repository_id}/resume`, data, params)
  }
  /**
   * GET /{repository_id}/analytics
   */
  async get{repository_id}analytics(repository_id: string, timeframe?: string): Promise<Dict[str, Any]> {
        const params = {'repository_id: repository_id, timeframe: timeframe'}
        const data = undefined
        return this.httpClient.get(`/{repository_id}/analytics`, params)
  }
  /**
   * GET /{repository_id}/badge
   */
  async get{repository_id}badge(repository_id: string, style?: string): Promise<Dict[str, Any]> {
        const params = {'repository_id: repository_id, style: style'}
        const data = undefined
        return this.httpClient.get(`/{repository_id}/badge`, params)
  }
  /**
   * GET /{repository_id}/activity
   */
  async get{repository_id}activity(repository_id: string, limit?: number): Promise<List[Dict[str, Any]]> {
        const params = {'repository_id: repository_id, limit: limit'}
        const data = undefined
        return this.httpClient.get(`/{repository_id}/activity`, params)
  }
}
