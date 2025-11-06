/**
 * Plugin_Marketplace API Client
 */

import { AxiosInstance } from 'axios'

export class Plugin_MarketplaceClient {
  private httpClient: AxiosInstance

  constructor(private baseURL: string, httpClient: AxiosInstance) {
    this.httpClient = httpClient
  }

  /**
   * GET /marketplace
   */
  async getMarketplace(plugin_type?: string, category?: string, pricing_tier?: string, search?: string, is_official?: boolean, is_vetted?: boolean, min_rating?: number, page?: number, per_page?: number, sort_by?: string, sort_order?: string): Promise<PluginListResponse> {
        const params = {'plugin_type: plugin_type, category: category, pricing_tier: pricing_tier, search: search, is_official: is_official, is_vetted: is_vetted, min_rating: min_rating, page: page, per_page: per_page, sort_by: sort_by, sort_order: sort_order'}
        const data = undefined
        return this.httpClient.get(`/marketplace`, params)
  }
  /**
   * GET /{plugin_id}
   */
  async get{plugin_id}(plugin_id: string): Promise<PluginResponse> {
        const params = {'plugin_id: plugin_id'}
        const data = undefined
        return this.httpClient.get(`/{plugin_id}`, params)
  }
  /**
   * POST /{plugin_id}/install
   */
  async post{plugin_id}install(plugin_id: string, organization_id?: string): Promise<PluginInstallationResponse> {
        const params = {}
        const data = {'plugin_id: plugin_id, organization_id: organization_id'}
        return this.httpClient.post(`/{plugin_id}/install`, data, params)
  }
  /**
   * GET /{plugin_id}/download
   */
  async get{plugin_id}download(plugin_id: string, version?: string): Promise<any> {
        const params = {'plugin_id: plugin_id, version: version'}
        const data = undefined
        return this.httpClient.get(`/{plugin_id}/download`, params)
  }
  /**
   * GET /installed
   */
  async getInstalled(): Promise<List[PluginInstallationResponse]> {
        const params = {}
        const data = undefined
        return this.httpClient.get(`/installed`, params)
  }
  /**
   * PUT /{plugin_id}
   */
  async put{plugin_id}(plugin_id: string, plugin_data: PluginUpdate): Promise<PluginResponse> {
        const params = {}
        const data = {'plugin_id: plugin_id, plugin_data: plugin_data'}
        return this.httpClient.put(`/{plugin_id}`, data, params)
  }
  /**
   * DELETE /{plugin_id}
   */
  async delete{plugin_id}(plugin_id: string): Promise<any> {
        const params = {}
        const data = plugin_id
        return this.httpClient.delete(`/{plugin_id}`, data, params)
  }
  /**
   * POST /{plugin_id}/publish
   */
  async post{plugin_id}publish(plugin_id: string): Promise<PluginResponse> {
        const params = {}
        const data = plugin_id
        return this.httpClient.post(`/{plugin_id}/publish`, data, params)
  }
  /**
   * POST /{plugin_id}/versions
   */
  async post{plugin_id}versions(plugin_id: string, version_data: PluginVersionCreate): Promise<PluginVersionResponse> {
        const params = {}
        const data = {'plugin_id: plugin_id, version_data: version_data'}
        return this.httpClient.post(`/{plugin_id}/versions`, data, params)
  }
  /**
   * GET /{plugin_id}/versions
   */
  async get{plugin_id}versions(plugin_id: string): Promise<List[PluginVersionResponse]> {
        const params = {'plugin_id: plugin_id'}
        const data = undefined
        return this.httpClient.get(`/{plugin_id}/versions`, params)
  }
  /**
   * GET /{plugin_id}/reviews
   */
  async get{plugin_id}reviews(plugin_id: string, page?: number, limit?: number, min_rating?: number, sort_by?: string, sort_order?: string): Promise<List[PluginReviewResponse]> {
        const params = {'plugin_id: plugin_id, page: page, limit: limit, min_rating: min_rating, sort_by: sort_by, sort_order: sort_order'}
        const data = undefined
        return this.httpClient.get(`/{plugin_id}/reviews`, params)
  }
  /**
   * POST /{plugin_id}/reviews
   */
  async post{plugin_id}reviews(plugin_id: string, review_data: PluginReviewCreate): Promise<PluginReviewResponse> {
        const params = {}
        const data = {'plugin_id: plugin_id, review_data: review_data'}
        return this.httpClient.post(`/{plugin_id}/reviews`, data, params)
  }
  /**
   * GET /{plugin_id}/reviews/{review_id}
   */
  async get{plugin_id}reviews{review_id}(plugin_id: string, review_id: string): Promise<PluginReviewResponse> {
        const params = {'plugin_id: plugin_id, review_id: review_id'}
        const data = undefined
        return this.httpClient.get(`/{plugin_id}/reviews/{review_id}`, params)
  }
  /**
   * PUT /{plugin_id}/reviews/{review_id}
   */
  async put{plugin_id}reviews{review_id}(plugin_id: string, review_id: string, review_update: PluginReviewUpdate): Promise<PluginReviewResponse> {
        const params = {}
        const data = {'plugin_id: plugin_id, review_id: review_id, review_update: review_update'}
        return this.httpClient.put(`/{plugin_id}/reviews/{review_id}`, data, params)
  }
  /**
   * DELETE /{plugin_id}/reviews/{review_id}
   */
  async delete{plugin_id}reviews{review_id}(plugin_id: string, review_id: string): Promise<any> {
        const params = {}
        const data = {'plugin_id: plugin_id, review_id: review_id'}
        return this.httpClient.delete(`/{plugin_id}/reviews/{review_id}`, data, params)
  }
  /**
   * POST /{plugin_id}/reviews/{review_id}/helpful
   */
  async post{plugin_id}reviews{review_id}helpful(plugin_id: string, review_id: string): Promise<any> {
        const params = {}
        const data = {'plugin_id: plugin_id, review_id: review_id'}
        return this.httpClient.post(`/{plugin_id}/reviews/{review_id}/helpful`, data, params)
  }
}
