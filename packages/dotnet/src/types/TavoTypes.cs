using System;
using System.Collections.Generic;

namespace TavoAI
{
    /// <summary>
    /// Pagination information
    /// </summary>
    public class PaginationInfo
    {
        public int Page { get; set; }
        public int Limit { get; set; }
        public int Total { get; set; }
        public int Pages { get; set; }
        public bool HasNext { get; set; }
        public bool HasPrev { get; set; }
    }

    /// <summary>
    /// Paginated response wrapper
    /// </summary>
    /// <typeparam name="T">Type of items in the response</typeparam>
    public class PaginatedResponse<T>
    {
        public List<T> Data { get; set; } = new List<T>();
        public PaginationInfo Pagination { get; set; } = new PaginationInfo();
    }

    /// <summary>
    /// List response wrapper
    /// </summary>
    /// <typeparam name="T">Type of items in the response</typeparam>
    public class ListResponse<T>
    {
        public List<T> Data { get; set; } = new List<T>();
        public int Count { get; set; }
    }

    /// <summary>
    /// Error response
    /// </summary>
    public class ErrorResponse
    {
        public string Error { get; set; } = "";
        public string Message { get; set; } = "";
        public object? Details { get; set; }
    }
}
