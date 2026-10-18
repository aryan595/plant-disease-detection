/**
 * AgriSense API Configuration
 * Supports local development, custom remote API URLs via VITE_API_URL,
 * or relative URL when served from the same domain.
 */
export const API_BASE_URL =
  (import.meta.env.VITE_API_URL || "").replace(/\/+$/, "") ||
  (import.meta.env.DEV ? "http://127.0.0.1:8000" : "");
