package net.tavoai.sdk;

import java.util.List;
import java.util.Map;

/**
 * Common types for Tavo SDK
 */
public class TavoTypes {

    /**
     * Pagination information
     */
    public static class PaginationInfo {
        public int page;
        public int limit;
        public int total;
        public int pages;
        public boolean hasNext;
        public boolean hasPrev;
    }

    /**
     * Paginated response wrapper
     */
    public static class PaginatedResponse<T> {
        public List<T> data;
        public PaginationInfo pagination;
    }

    /**
     * List response wrapper
     */
    public static class ListResponse<T> {
        public List<T> data;
        public int count;
    }

    /**
     * Error response
     */
    public static class ErrorResponse {
        public String error;
        public String message;
        public Object details;
    }
}
