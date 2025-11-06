/**
 * Utility functions for Tavo SDK
 */

import axios, { AxiosInstance } from 'axios'

export interface HttpClientConfig {
  baseURL: string
  apiKey?: string
  deviceToken?: string
  timeout?: number
}

export function createHttpClient(
  baseURL: string,
  apiKey?: string,
  deviceToken?: string,
  timeout: number = 30000
): AxiosInstance {
  const config: HttpClientConfig = {
    baseURL: baseURL.replace(/\/$/, '') + '/api/v1', // Remove trailing slash and add API version
  }

  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    'User-Agent': 'tavo-sdk-typescript/0.1.0',
  }

  // Authentication priority: API Key > Device Token
  if (apiKey) {
    headers['X-API-Key'] = apiKey
  } else if (deviceToken) {
    headers['Authorization'] = `Bearer ${deviceToken}`
  }

  return axios.create({
    ...config,
    headers,
    timeout,
  })
}

/**
 * Handle API errors consistently
 */
export function handleApiError(error: any): never {
  if (error.response) {
    // Server responded with error status
    const { status, data } = error.response
    const message = data?.message || data?.error || `HTTP ${status} error`
    throw new Error(`API Error (${status}): ${message}`)
  } else if (error.request) {
    // Request was made but no response received
    throw new Error('Network error: No response received from server')
  } else {
    // Something else happened
    throw new Error(`Request error: ${error.message}`)
  }
}
