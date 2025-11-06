/**
 * Repository_Providers API Client
 */

import { AxiosInstance } from 'axios'

export class Repository_ProvidersClient {
  private httpClient: AxiosInstance

  constructor(private baseURL: string, httpClient: AxiosInstance) {
    this.httpClient = httpClient
  }

  /**
   * GET /
   */
  async getRoot(enabled_only?: boolean): Promise<List[RepositoryProviderResponse]> {
        const params = {'enabled_only: enabled_only'}
        const data = undefined
        return this.httpClient.get(`/`, params)
  }
  /**
   * GET /{provider_id}
   */
  async get{provider_id}(provider_id: string): Promise<RepositoryProviderResponse> {
        const params = {'provider_id: provider_id'}
        const data = undefined
        return this.httpClient.get(`/{provider_id}`, params)
  }
}
