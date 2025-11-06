/**
 * Repository_Connections API Client
 */

import { AxiosInstance } from 'axios'

export class Repository_ConnectionsClient {
  private httpClient: AxiosInstance

  constructor(private baseURL: string, httpClient: AxiosInstance) {
    this.httpClient = httpClient
  }

  /**
   * POST /
   */
  async postRoot(connection_in: RepositoryConnectionCreate): Promise<RepositoryConnectionResponse> {
        const params = {}
        const data = connection_in
        return this.httpClient.post(`/`, data, params)
  }
  /**
   * GET /
   */
  async getRoot(provider_id?: string, connection_type?: string, is_active?: boolean): Promise<List[RepositoryConnectionResponse]> {
        const params = {'provider_id: provider_id, connection_type: connection_type, is_active: is_active'}
        const data = undefined
        return this.httpClient.get(`/`, params)
  }
  /**
   * GET /{connection_id}
   */
  async get{connection_id}(connection_id: string): Promise<RepositoryConnectionResponse> {
        const params = {'connection_id: connection_id'}
        const data = undefined
        return this.httpClient.get(`/{connection_id}`, params)
  }
  /**
   * PUT /{connection_id}
   */
  async put{connection_id}(connection_id: string, connection_update: RepositoryConnectionUpdate): Promise<RepositoryConnectionResponse> {
        const params = {}
        const data = {'connection_id: connection_id, connection_update: connection_update'}
        return this.httpClient.put(`/{connection_id}`, data, params)
  }
  /**
   * DELETE /{connection_id}
   */
  async delete{connection_id}(connection_id: string): Promise<None> {
        const params = {}
        const data = connection_id
        return this.httpClient.delete(`/{connection_id}`, data, params)
  }
  /**
   * POST /{connection_id}/validate
   */
  async post{connection_id}validate(connection_id: string): Promise<ConnectionValidationResponse> {
        const params = {}
        const data = connection_id
        return this.httpClient.post(`/{connection_id}/validate`, data, params)
  }
  /**
   * POST /{connection_id}/refresh
   */
  async post{connection_id}refresh(connection_id: string): Promise<RepositoryConnectionResponse> {
        const params = {}
        const data = connection_id
        return this.httpClient.post(`/{connection_id}/refresh`, data, params)
  }
}
