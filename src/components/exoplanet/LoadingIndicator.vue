<template>
  <div class="loading-indicator" v-if="isLoading || error">
    <div class="loading-content">
      <!-- Estado de carga -->
      <div v-if="isLoading && !error" class="loading-state">
        <div class="spinner">🌌</div>
        <h3>{{ loadingTitle }}</h3>
        <p>{{ loadingMessage }}</p>
        <div class="progress-bar">
          <div class="progress-fill" :style="{ width: progress + '%' }"></div>
        </div>
      </div>
      
      <!-- Estado de error -->
      <div v-if="error" class="error-state">
        <div class="error-icon">⚠️</div>
        <h3>Error de Conexión</h3>
        <p>{{ error }}</p>
        <button @click="$emit('retry')" class="retry-button">
          🔄 Reintentar
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LoadingIndicator',
  props: {
    isLoading: {
      type: Boolean,
      default: false
    },
    error: {
      type: String,
      default: null
    },
    loadingTitle: {
      type: String,
      default: 'Cargando Datos de Exoplanetas...'
    },
    loadingMessage: {
      type: String,
      default: 'Conectando con la base de datos astronómica NASA/Kepler'
    },
    progress: {
      type: Number,
      default: 0
    }
  },
  emits: ['retry']
};
</script>

<style scoped>
.loading-indicator {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 17, 34, 0.95);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  backdrop-filter: blur(10px);
}

.loading-content {
  text-align: center;
  color: white;
  max-width: 400px;
  padding: 40px;
  background: rgba(0, 0, 0, 0.8);
  border-radius: 20px;
  border: 2px solid rgba(74, 144, 226, 0.3);
}

.loading-state {
  animation: fadeIn 0.5s ease-in;
}

.spinner {
  font-size: 4em;
  animation: rotate 2s linear infinite;
  margin-bottom: 20px;
}

.loading-state h3 {
  color: #4a90e2;
  margin: 0 0 10px 0;
  font-size: 1.4em;
}

.loading-state p {
  color: #ccc;
  margin: 0 0 20px 0;
  font-size: 0.9em;
}

.progress-bar {
  width: 100%;
  height: 6px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 3px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #4a90e2, #00ff88);
  transition: width 0.3s ease;
  animation: pulse 2s infinite;
}

.error-state {
  animation: slideIn 0.5s ease-out;
}

.error-icon {
  font-size: 3em;
  margin-bottom: 15px;
}

.error-state h3 {
  color: #ff6b35;
  margin: 0 0 10px 0;
}

.error-state p {
  color: #ccc;
  margin: 0 0 20px 0;
}

.retry-button {
  padding: 12px 24px;
  background: #4a90e2;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1em;
  cursor: pointer;
  transition: all 0.3s ease;
}

.retry-button:hover {
  background: #357abd;
  transform: translateY(-2px);
}

@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes slideIn {
  from { opacity: 0; transform: scale(0.9); }
  to { opacity: 1; transform: scale(1); }
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.7; }
}
</style>