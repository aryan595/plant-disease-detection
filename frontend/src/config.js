/**
 * AgriSense API Configuration
 * - If VITE_API_URL is provided (e.g. on Vercel pointing to Render/HuggingFace), use it.
 * - Otherwise (local development), use "" so requests route through Vite's local proxy
 *   with zero CORS or network resolution errors.
 */
export const API_BASE_URL = (import.meta.env.VITE_API_URL || "").replace(/\/+$/, "");
