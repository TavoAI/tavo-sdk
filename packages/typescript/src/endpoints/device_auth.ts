/**
 * Device_Auth API Client
 */

import { AxiosInstance } from 'axios'

export class Device_AuthClient {
  private httpClient: AxiosInstance

  constructor(private baseURL: string, httpClient: AxiosInstance) {
    this.httpClient = httpClient
  }

  /**
   * POST /code
   */
  async postCode(client_id?: string, client_name?: string): Promise<dict> {
        const params = {}
        const data = {'client_id: client_id, client_name: client_name'}
        return this.httpClient.post(`/code`, data, params)
  }
  /**
   * POST /token
   */
  async postToken(device_code: string): Promise<dict> {
        const params = {}
        const data = device_code
        return this.httpClient.post(`/token`, data, params)
  }
  /**
   * GET /info
   */
  async getInfo(user_code: string): Promise<dict> {
        const params = {'user_code: user_code'}
        const data = undefined
        return this.httpClient.get(`/info`, params)
  }
  /**
   * POST /approve
   */
  async postApprove(): Promise<dict> {
        const params = {}
        const data = undefined
        return this.httpClient.post(`/approve`, data, params)
  }
  /**
   * POST /code/cli
   */
  async postCodecli(client_name?: string): Promise<dict> {
        const params = {}
        const data = client_name
        return this.httpClient.post(`/code/cli`, data, params)
  }
  /**
   * GET /code/{device_code}/status
   */
  async getCode{device_code}status(device_code: string): Promise<dict> {
        const params = {'device_code: device_code'}
        const data = undefined
        return this.httpClient.get(`/code/{device_code}/status`, params)
  }
  /**
   * GET /usage/warnings
   */
  async getUsagewarnings(): Promise<dict> {
        const params = {}
        const data = undefined
        return this.httpClient.get(`/usage/warnings`, params)
  }
  /**
   * GET /limits
   */
  async getLimits(): Promise<dict> {
        const params = {}
        const data = undefined
        return this.httpClient.get(`/limits`, params)
  }
}
