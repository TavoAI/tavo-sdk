/**
 * Plugin_Execution API Client
 */

import { AxiosInstance } from 'axios'

export class Plugin_ExecutionClient {
  private httpClient: AxiosInstance

  constructor(private baseURL: string, httpClient: AxiosInstance) {
    this.httpClient = httpClient
  }

  /**
   * POST /execute
   */
  async postExecute(background_tasks: BackgroundTasks): Promise<PluginExecutionResponse> {
        const params = {}
        const data = background_tasks
        return this.httpClient.post(`/execute`, data, params)
  }
  /**
   * GET /executions/{execution_id}
   */
  async getExecutions{execution_id}(execution_id: string): Promise<PluginExecutionResponse> {
        const params = {'execution_id: execution_id'}
        const data = undefined
        return this.httpClient.get(`/executions/{execution_id}`, params)
  }
  /**
   * GET /executions
   */
  async getExecutions(plugin_id?: string, limit?: number): Promise<List[PluginExecutionResponse]> {
        const params = {'plugin_id: plugin_id, limit: limit'}
        const data = undefined
        return this.httpClient.get(`/executions`, params)
  }
}
