/**
 * Scanner_Integration API Client
 */

import { AxiosInstance } from 'axios'

export class Scanner_IntegrationClient {
  private httpClient: AxiosInstance

  constructor(private baseURL: string, httpClient: AxiosInstance) {
    this.httpClient = httpClient
  }

  /**
   * GET /rules/discover
   */
  async getRulesdiscover(category?: string, language?: string, scanner_type?: string, limit?: number): Promise<ListResponse[RuleBundleSchema]> {
        const params = {'category: category, language: language, scanner_type: scanner_type, limit: limit'}
        const data = undefined
        return this.httpClient.get(`/rules/discover`, params)
  }
  /**
   * GET /rules/bundle/{bundle_id}/rules
   */
  async getRulesbundle{bundle_id}rules(bundle_id: string, severity?: string, language?: string, limit?: number): Promise<ListResponse[RuleSchema]> {
        const params = {'bundle_id: bundle_id, severity: severity, language: language, limit: limit'}
        const data = undefined
        return this.httpClient.get(`/rules/bundle/{bundle_id}/rules`, params)
  }
  /**
   * POST /rules/bundle/{bundle_id}/use
   */
  async postRulesbundle{bundle_id}use(bundle_id: string, scan_id?: string): Promise<any> {
        const params = {}
        const data = {'bundle_id: bundle_id, scan_id: scan_id'}
        return this.httpClient.post(`/rules/bundle/{bundle_id}/use`, data, params)
  }
  /**
   * GET /plugins/discover
   */
  async getPluginsdiscover(plugin_type?: string, language?: string, scanner_integration?: boolean, limit?: number): Promise<ListResponse[PluginResponse]> {
        const params = {'plugin_type: plugin_type, language: language, scanner_integration: scanner_integration, limit: limit'}
        const data = undefined
        return this.httpClient.get(`/plugins/discover`, params)
  }
  /**
   * GET /plugins/{plugin_id}/config
   */
  async getPlugins{plugin_id}config(plugin_id: string): Promise<any> {
        const params = {'plugin_id: plugin_id'}
        const data = undefined
        return this.httpClient.get(`/plugins/{plugin_id}/config`, params)
  }
  /**
   * POST /scanner/heartbeat
   */
  async postScannerheartbeat(scanner_version: string, scanner_type?: string, active_rules?: string[], active_plugins?: string[]): Promise<any> {
        const params = {}
        const data = {'scanner_version: scanner_version, scanner_type: scanner_type, active_rules: active_rules, active_plugins: active_plugins'}
        return this.httpClient.post(`/scanner/heartbeat`, data, params)
  }
  /**
   * GET /scanner/recommendations
   */
  async getScannerrecommendations(scanner_type?: string, current_rules?: string[], current_plugins?: string[]): Promise<any> {
        const params = {'scanner_type: scanner_type, current_rules: current_rules, current_plugins: current_plugins'}
        const data = undefined
        return this.httpClient.get(`/scanner/recommendations`, params)
  }
}
