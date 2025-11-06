/**
 * Scan_Rules API Client
 */

import { AxiosInstance } from 'axios'

export class Scan_RulesClient {
  private httpClient: AxiosInstance

  constructor(private baseURL: string, httpClient: AxiosInstance) {
    this.httpClient = httpClient
  }

  /**
   * POST /rules
   */
  async postRules(rule_in: ScanRuleCreate): Promise<ScanRuleSchema> {
        const params = {}
        const data = rule_in
        return this.httpClient.post(`/rules`, data, params)
  }
  /**
   * GET /rules
   */
  async getRules(skip?: number, limit?: number, tool_filter?: string, category_filter?: string, severity_filter?: string, language_filter?: string, is_active?: boolean, organization_id?: string): Promise<List[ScanRuleSchema]> {
        const params = {'skip: skip, limit: limit, tool_filter: tool_filter, category_filter: category_filter, severity_filter: severity_filter, language_filter: language_filter, is_active: is_active, organization_id: organization_id'}
        const data = undefined
        return this.httpClient.get(`/rules`, params)
  }
  /**
   * GET /rules/{rule_id}
   */
  async getRules{rule_id}(rule_id: string): Promise<ScanRuleSchema> {
        const params = {'rule_id: rule_id'}
        const data = undefined
        return this.httpClient.get(`/rules/{rule_id}`, params)
  }
  /**
   * POST /rules/upload
   */
  async postRulesupload(file?: UploadFile, organization_id?: string): Promise<any> {
        const params = {}
        const data = {'file: file, organization_id: organization_id'}
        return this.httpClient.post(`/rules/upload`, data, params)
  }
  /**
   * PUT /rules/{rule_id}
   */
  async putRules{rule_id}(rule_id: string, rule_update: ScanRuleUpdate): Promise<ScanRuleSchema> {
        const params = {}
        const data = {'rule_id: rule_id, rule_update: rule_update'}
        return this.httpClient.put(`/rules/{rule_id}`, data, params)
  }
  /**
   * DELETE /rules/{rule_id}
   */
  async deleteRules{rule_id}(rule_id: string): Promise<any> {
        const params = {}
        const data = rule_id
        return this.httpClient.delete(`/rules/{rule_id}`, data, params)
  }
}
