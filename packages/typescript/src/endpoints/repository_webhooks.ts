/**
 * Repository_Webhooks API Client
 */

import { AxiosInstance } from 'axios'

export class Repository_WebhooksClient {
  private httpClient: AxiosInstance

  constructor(private baseURL: string, httpClient: AxiosInstance) {
    this.httpClient = httpClient
  }

  /**
   * POST /github
   */
  async postGithub(x_hub_signature_256?: string, x_github_event?: string, x_github_delivery?: string): Promise<Dict[str, Any]> {
        const params = {}
        const data = {'x_hub_signature_256: x_hub_signature_256, x_github_event: x_github_event, x_github_delivery: x_github_delivery'}
        return this.httpClient.post(`/github`, data, params)
  }
  /**
   * POST /{repository_id}/setup
   */
  async post{repository_id}setup(repository_id: string): Promise<WebhookSetupResponse> {
        const params = {}
        const data = repository_id
        return this.httpClient.post(`/{repository_id}/setup`, data, params)
  }
  /**
   * GET /{repository_id}/status
   */
  async get{repository_id}status(repository_id: string): Promise<WebhookStatusResponse> {
        const params = {'repository_id: repository_id'}
        const data = undefined
        return this.httpClient.get(`/{repository_id}/status`, params)
  }
  /**
   * DELETE /{repository_id}/webhook
   */
  async delete{repository_id}webhook(repository_id: string): Promise<Dict[str, str]> {
        const params = {}
        const data = repository_id
        return this.httpClient.delete(`/{repository_id}/webhook`, data, params)
  }
}
