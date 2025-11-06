/**
 * Registry API Client
 */

import { AxiosInstance } from 'axios'

export class RegistryClient {
  private httpClient: AxiosInstance

  constructor(private baseURL: string, httpClient: AxiosInstance) {
    this.httpClient = httpClient
  }

  /**
   * GET /marketplace
   */
  async getMarketplace(): Promise<PaginatedResponse[ArtifactBundleList]> {
        const params = {}
        const data = undefined
        return this.httpClient.get(`/marketplace`, params)
  }
  /**
   * GET /categories
   */
  async getCategories(): Promise<List[CategoryResponse]> {
        const params = {}
        const data = undefined
        return this.httpClient.get(`/categories`, params)
  }
  /**
   * POST /bundles
   */
  async postBundles(bundle: ArtifactBundleCreate): Promise<ArtifactBundleDetail> {
        const params = {}
        const data = bundle
        return this.httpClient.post(`/bundles`, data, params)
  }
  /**
   * GET /bundles/{bundle_id}
   */
  async getBundles{bundle_id}(bundle_id: string): Promise<ArtifactBundleDetail> {
        const params = {'bundle_id: bundle_id'}
        const data = undefined
        return this.httpClient.get(`/bundles/{bundle_id}`, params)
  }
  /**
   * PUT /bundles/{bundle_id}
   */
  async putBundles{bundle_id}(bundle_id: string, bundle_update: ArtifactBundleUpdate): Promise<ArtifactBundleDetail> {
        const params = {}
        const data = {'bundle_id: bundle_id, bundle_update: bundle_update'}
        return this.httpClient.put(`/bundles/{bundle_id}`, data, params)
  }
  /**
   * DELETE /bundles/{bundle_id}
   */
  async deleteBundles{bundle_id}(bundle_id: string): Promise<any> {
        const params = {}
        const data = bundle_id
        return this.httpClient.delete(`/bundles/{bundle_id}`, data, params)
  }
  /**
   * GET /bundles/{bundle_id}/download
   */
  async getBundles{bundle_id}download(bundle_id: string): Promise<any> {
        const params = {'bundle_id: bundle_id'}
        const data = undefined
        return this.httpClient.get(`/bundles/{bundle_id}/download`, params)
  }
  /**
   * POST /bundles/{bundle_id}/install
   */
  async postBundles{bundle_id}install(bundle_id: string, installation: BundleInstallationCreate): Promise<BundleInstallationResponse> {
        const params = {}
        const data = {'bundle_id: bundle_id, installation: installation'}
        return this.httpClient.post(`/bundles/{bundle_id}/install`, data, params)
  }
  /**
   * GET /my-bundles
   */
  async getMybundles(): Promise<List[BundleInstallationResponse]> {
        const params = {}
        const data = undefined
        return this.httpClient.get(`/my-bundles`, params)
  }
  /**
   * POST /execute/code-rule
   */
  async postExecutecoderule(): Promise<ArtifactExecutionResponse> {
        const params = {}
        const data = undefined
        return this.httpClient.post(`/execute/code-rule`, data, params)
  }
  /**
   * GET /executions/{execution_id}
   */
  async getExecutions{execution_id}(execution_id: string): Promise<ArtifactExecutionResponse> {
        const params = {'execution_id: execution_id'}
        const data = undefined
        return this.httpClient.get(`/executions/{execution_id}`, params)
  }
  /**
   * GET /my-executions
   */
  async getMyexecutions(page?: number, per_page?: number): Promise<PaginatedResponse[ArtifactExecutionResponse]> {
        const params = {'page: page, per_page: per_page'}
        const data = undefined
        return this.httpClient.get(`/my-executions`, params)
  }
  /**
   * POST /bundles/{bundle_id}/rate
   */
  async postBundles{bundle_id}rate(bundle_id: string, rating: BundleRatingCreate): Promise<BundleRatingResponse> {
        const params = {}
        const data = {'bundle_id: bundle_id, rating: rating'}
        return this.httpClient.post(`/bundles/{bundle_id}/rate`, data, params)
  }
  /**
   * POST /bundles/{bundle_id}/review
   */
  async postBundles{bundle_id}review(bundle_id: string, review: BundleReviewCreate): Promise<BundleReviewResponse> {
        const params = {}
        const data = {'bundle_id: bundle_id, review: review'}
        return this.httpClient.post(`/bundles/{bundle_id}/review`, data, params)
  }
  /**
   * GET /bundles/{bundle_id}/reviews
   */
  async getBundles{bundle_id}reviews(bundle_id: string, page?: number, per_page?: number): Promise<PaginatedResponse[BundleReviewResponse]> {
        const params = {'bundle_id: bundle_id, page: page, per_page: per_page'}
        const data = undefined
        return this.httpClient.get(`/bundles/{bundle_id}/reviews`, params)
  }
  /**
   * GET /bundles/{bundle_id}/versions
   */
  async getBundles{bundle_id}versions(bundle_id: string): Promise<any> {
        const params = {'bundle_id: bundle_id'}
        const data = undefined
        return this.httpClient.get(`/bundles/{bundle_id}/versions`, params)
  }
  /**
   * GET /bundles/{bundle_id}/changelog
   */
  async getBundles{bundle_id}changelog(bundle_id: string): Promise<any> {
        const params = {'bundle_id: bundle_id'}
        const data = undefined
        return this.httpClient.get(`/bundles/{bundle_id}/changelog`, params)
  }
}
