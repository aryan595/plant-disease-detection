import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

const backendProxy = {
  '/analyze': 'http://127.0.0.1:8000',
  '/predict': 'http://127.0.0.1:8000',
  '/weather': 'http://127.0.0.1:8000',
  '/forecast': 'http://127.0.0.1:8000',
  '/districts': 'http://127.0.0.1:8000',
  '/krishi-kendras': 'http://127.0.0.1:8000',
  '/mandi-rates': 'http://127.0.0.1:8000',
  '/tts': 'http://127.0.0.1:8000',
  '/download-report': 'http://127.0.0.1:8000',
  '/download-pmfby-certificate': 'http://127.0.0.1:8000',
  '/check-compatibility': 'http://127.0.0.1:8000',
  '/compare-recovery': 'http://127.0.0.1:8000',
  '/chat': 'http://127.0.0.1:8000',
  '/compatibility-chemicals': 'http://127.0.0.1:8000',
}

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: backendProxy,
  },
  preview: {
    port: 4173,
    proxy: backendProxy,
  },
})
