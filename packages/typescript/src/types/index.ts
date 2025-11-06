/**
 * Common Types for Tavo SDK
 */

export interface PaginationInfo {
  page: number
  limit: number
  total: number
  pages: number
  has_next: boolean
  has_prev: boolean
}

export interface ListResponse<T> {
  data: T[]
  count: number
}

export interface PaginatedResponse<T> {
  data: T[]
  pagination: PaginationInfo
}

export interface ErrorResponse {
  error: string
  message: string
  details?: any
}
