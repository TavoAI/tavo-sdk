/**
 * Code_Submission API Client
 */

import { AxiosInstance } from 'axios'

export class Code_SubmissionClient {
  private httpClient: AxiosInstance

  constructor(private baseURL: string, httpClient: AxiosInstance) {
    this.httpClient = httpClient
  }

  /**
   * POST /submit/code
   */
  async postSubmitcode(files?: UploadFile[], scan_config?: Dict, repository_name?: string, branch?: string, commit_sha?: string): Promise<dict> {
        const params = {}
        const data = {'files: files, scan_config: scan_config, repository_name: repository_name, branch: branch, commit_sha: commit_sha'}
        return this.httpClient.post(`/submit/code`, data, params)
  }
  /**
   * POST /submit/repository
   */
  async postSubmitrepository(repository_url?: string, snapshot_data?: Dict, scan_config?: Dict, branch?: string, commit_sha?: string): Promise<dict> {
        const params = {}
        const data = {'repository_url: repository_url, snapshot_data: snapshot_data, scan_config: scan_config, branch: branch, commit_sha: commit_sha'}
        return this.httpClient.post(`/submit/repository`, data, params)
  }
  /**
   * POST /submit/analysis
   */
  async postSubmitanalysis(code_content?: string, language?: string, analysis_type?: string, rules?: string[], plugins?: string[], context?: Dict): Promise<dict> {
        const params = {}
        const data = {'code_content: code_content, language: language, analysis_type: analysis_type, rules: rules, plugins: plugins, context: context'}
        return this.httpClient.post(`/submit/analysis`, data, params)
  }
  /**
   * GET /scans/{scan_id}/status
   */
  async getScans{scan_id}status(scan_id: string): Promise<any> {
        const params = {'scan_id: scan_id'}
        const data = undefined
        return this.httpClient.get(`/scans/{scan_id}/status`, params)
  }
  /**
   * GET /scans/{scan_id}/results/summary
   */
  async getScans{scan_id}resultssummary(scan_id: string): Promise<any> {
        const params = {'scan_id: scan_id'}
        const data = undefined
        return this.httpClient.get(`/scans/{scan_id}/results/summary`, params)
  }
}
