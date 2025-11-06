/**
 * Rules API Client
 */

import { AxiosInstance } from 'axios'

export class RulesClient {
  private httpClient: AxiosInstance

  constructor(private baseURL: string, httpClient: AxiosInstance) {
    this.httpClient = httpClient
  }

  /**
   * GET /bundles
   */
  async getBundles(category?: string, official_only?: boolean, page?: number, per_page?: number): Promise<RuleBundleList> {
        const params = {'category: category, official_only: official_only, page: page, per_page: per_page'}
        const data = undefined
        return this.httpClient.get(`/bundles`, params)
  }
  /**
   * POST /bundles/{bundle_id}/install
   */
  async postBundles{bundle_id}install(bundle_id: string, installation: RuleBundleInstallationCreate): Promise<RuleBundleInstallationSchema> {
        const params = {}
        const data = {'bundle_id: bundle_id, installation: installation'}
        return this.httpClient.post(`/bundles/{bundle_id}/install`, data, params)
  }
  /**
   * GET /bundles/{bundle_id}/rules
   */
  async getBundles{bundle_id}rules(bundle_id: string): Promise<List[RuleSchema]> {
        const params = {'bundle_id: bundle_id'}
        const data = undefined
        return this.httpClient.get(`/bundles/{bundle_id}/rules`, params)
  }
  /**
   * POST /validate
   */
  async postValidate(): Promise<RuleValidationResult> {
        const params = {}
        const data = undefined
        return this.httpClient.post(`/validate`, data, params)
  }
  /**
   * GET /updates
   */
  async getUpdates(): Promise<List[RuleBundleUpdates]> {
        const params = {}
        const data = undefined
        return this.httpClient.get(`/updates`, params)
  }
  /**
   * DELETE /bundles/{bundle_id}/install
   */
  async deleteBundles{bundle_id}install(bundle_id: string): Promise<any> {
        const params = {}
        const data = bundle_id
        return this.httpClient.delete(`/bundles/{bundle_id}/install`, data, params)
  }
  /**
   * GET /organizations/{organization_id}/bundles
   */
  async getOrganizations{organization_id}bundles(organization_id: string): Promise<List[RuleBundleSchema]> {
        const params = {'organization_id: organization_id'}
        const data = undefined
        return this.httpClient.get(`/organizations/{organization_id}/bundles`, params)
  }
  /**
   * POST /organizations/{organization_id}/bundles/{bundle_id}/install
   */
  async postOrganizations{organization_id}bundles{bundle_id}install(organization_id: string, bundle_id: string): Promise<any> {
        const params = {}
        const data = {'organization_id: organization_id, bundle_id: bundle_id'}
        return this.httpClient.post(`/organizations/{organization_id}/bundles/{bundle_id}/install`, data, params)
  }
  /**
   * DELETE /organizations/{organization_id}/bundles/{bundle_id}
   */
  async deleteOrganizations{organization_id}bundles{bundle_id}(organization_id: string, bundle_id: string): Promise<any> {
        const params = {}
        const data = {'organization_id: organization_id, bundle_id: bundle_id'}
        return this.httpClient.delete(`/organizations/{organization_id}/bundles/{bundle_id}`, data, params)
  }
  /**
   * GET /organizations/{organization_id}/rules
   */
  async getOrganizations{organization_id}rules(organization_id: string, category?: string, severity?: string): Promise<List[RuleSchema]> {
        const params = {'organization_id: organization_id, category: category, severity: severity'}
        const data = undefined
        return this.httpClient.get(`/organizations/{organization_id}/rules`, params)
  }
  /**
   * GET /organizations/{organization_id}/rules/stats
   */
  async getOrganizations{organization_id}rulesstats(organization_id: string): Promise<any> {
        const params = {'organization_id: organization_id'}
        const data = undefined
        return this.httpClient.get(`/organizations/{organization_id}/rules/stats`, params)
  }
}
