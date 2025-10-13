import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  base: './', 
  plugins: [
    vue(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  server: {
    host: true, // Permite acceso desde la red
    port: 5173, // Puerto por defecto
    strictPort: false, // Si el puerto está ocupado, usar el siguiente disponible
    open: false, // No abrir automáticamente el navegador
    cors: true // Habilitar CORS
  },
  preview: {
    host: true, // También para el preview
    port: 4173,
    strictPort: false,
    open: false
  }
})
