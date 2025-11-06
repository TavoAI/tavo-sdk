/**
 * Scan_Schedules API Client
 */

import { AxiosInstance } from 'axios'

export class Scan_SchedulesClient {
  private httpClient: AxiosInstance

  constructor(private baseURL: string, httpClient: AxiosInstance) {
    this.httpClient = httpClient
  }

  /**
   * POST /
   */
  async postRoot(schedule_in: ScanScheduleCreate): Promise<ScanScheduleResponse> {
        const params = {}
        const data = schedule_in
        return this.httpClient.post(`/`, data, params)
  }
  /**
   * GET /repository/{repository_id}
   */
  async getRepository{repository_id}(repository_id: string): Promise<List[ScanScheduleResponse]> {
        const params = {'repository_id: repository_id'}
        const data = undefined
        return this.httpClient.get(`/repository/{repository_id}`, params)
  }
  /**
   * GET /{schedule_id}
   */
  async get{schedule_id}(schedule_id: string): Promise<ScanScheduleResponse> {
        const params = {'schedule_id: schedule_id'}
        const data = undefined
        return this.httpClient.get(`/{schedule_id}`, params)
  }
  /**
   * PUT /{schedule_id}
   */
  async put{schedule_id}(schedule_id: string, schedule_update: ScanScheduleUpdate): Promise<ScanScheduleResponse> {
        const params = {}
        const data = {'schedule_id: schedule_id, schedule_update: schedule_update'}
        return this.httpClient.put(`/{schedule_id}`, data, params)
  }
  /**
   * DELETE /{schedule_id}
   */
  async delete{schedule_id}(schedule_id: string): Promise<None> {
        const params = {}
        const data = schedule_id
        return this.httpClient.delete(`/{schedule_id}`, data, params)
  }
}
