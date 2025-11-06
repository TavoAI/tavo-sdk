/**
 * Jobs API Client
 */

import { AxiosInstance } from 'axios'

export class JobsClient {
  private httpClient: AxiosInstance

  constructor(private baseURL: string, httpClient: AxiosInstance) {
    this.httpClient = httpClient
  }

  /**
   * GET /status/{job_id}
   */
  async getStatus{job_id}(job_id: string): Promise<JobStatus> {
        const params = {'job_id: job_id'}
        const data = undefined
        return this.httpClient.get(`/status/{job_id}`, params)
  }
  /**
   * GET /dashboard
   */
  async getDashboard(limit?: number, authorization?: string, x_api_key?: string): Promise<JobSummary> {
        const params = {'limit: limit, authorization: authorization, x_api_key: x_api_key'}
        const data = undefined
        return this.httpClient.get(`/dashboard`, params)
  }
}
