/**
 * Scan_Tools API Client
 */

import { AxiosInstance } from 'axios'

export class Scan_ToolsClient {
  private httpClient: AxiosInstance

  constructor(private baseURL: string, httpClient: AxiosInstance) {
    this.httpClient = httpClient
  }

  /**
   * GET /tools
   */
  async getTools(active_only?: boolean): Promise<List[ScanToolInfo]> {
        const params = {'active_only: active_only'}
        const data = undefined
        return this.httpClient.get(`/tools`, params)
  }
  /**
   * GET /tools/{tool_name}
   */
  async getTools{tool_name}(tool_name: string): Promise<ScanToolInfo> {
        const params = {'tool_name: tool_name'}
        const data = undefined
        return this.httpClient.get(`/tools/{tool_name}`, params)
  }
  /**
   * GET /templates
   */
  async getTemplates(tool?: string, category?: string, language?: string, active_only?: boolean): Promise<List[ScanTemplateInfo]> {
        const params = {'tool: tool, category: category, language: language, active_only: active_only'}
        const data = undefined
        return this.httpClient.get(`/templates`, params)
  }
  /**
   * GET /templates/{template_id}
   */
  async getTemplates{template_id}(template_id: string): Promise<ScanTemplateInfo> {
        const params = {'template_id: template_id'}
        const data = undefined
        return this.httpClient.get(`/templates/{template_id}`, params)
  }
  /**
   * POST /validate-configuration
   */
  async postValidateconfiguration(): Promise<ScanConfigurationValidationResponse> {
        const params = {}
        const data = undefined
        return this.httpClient.post(`/validate-configuration`, data, params)
  }
  /**
   * GET /repositories/{repository_id}/settings
   */
  async getRepositories{repository_id}settings(repository_id: string): Promise<RepositoryScanSettings> {
        const params = {'repository_id: repository_id'}
        const data = undefined
        return this.httpClient.get(`/repositories/{repository_id}/settings`, params)
  }
  /**
   * PUT /repositories/{repository_id}/settings
   */
  async putRepositories{repository_id}settings(repository_id: string, settings: RepositoryScanSettings): Promise<RepositoryScanSettings> {
        const params = {}
        const data = {'repository_id: repository_id, settings: settings'}
        return this.httpClient.put(`/repositories/{repository_id}/settings`, data, params)
  }
  /**
   * POST /validate-access
   */
  async postValidateaccess(): Promise<RepositoryAccessValidationResponse> {
        const params = {}
        const data = undefined
        return this.httpClient.post(`/validate-access`, data, params)
  }
}
