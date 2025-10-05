<template>
  <div class="exoplanet-list-component">
    <div class="exoplanet-info-panel">
      <h3>{{ title }}</h3>
      
      <!-- Slot para contenido personalizado cuando no hay exoplanetas -->
      <div v-if="exoplanets.length === 0" class="no-exoplanets">
        <slot name="empty-state">
          🔭 No hay exoplanetas visibles desde esta ubicación en este momento.
        </slot>
      </div>
      
      <!-- Lista de exoplanetas -->
      <div v-else class="exoplanet-list">
        <div 
          v-for="(exoplanet, index) in exoplanets" 
          :key="index"
          class="exoplanet-item"
          @click="$emit('focus-exoplanet', exoplanet)"
        >
          <h4>{{ exoplanet.name }}</h4>
          <div class="exoplanet-details">
            <p><strong>Dirección:</strong> {{ exoplanet.direction }}°</p>
            <p><strong>Elevación:</strong> {{ exoplanet.elevation }}°</p>
            <p><strong>Distancia:</strong> {{ exoplanet.distance }} años luz</p>
            <p class="habitability">
              <strong>Probabilidad de vida:</strong> 
              <span class="habitability-value" :style="{ color: getHabitabilityColor(exoplanet.habitability) }">
                {{ exoplanet.habitability }}%
              </span>
            </p>
          </div>
          
          <!-- Indicador visual de habitabilidad -->
          <div class="habitability-indicator">
            <div 
              class="habitability-bar" 
              :style="{ 
                width: exoplanet.habitability + '%',
                backgroundColor: getHabitabilityColor(exoplanet.habitability)
              }"
            ></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ExoplanetList',
  props: {
    title: {
      type: String,
      default: 'Exoplanetas Visibles'
    },
    exoplanets: {
      type: Array,
      required: true
    }
  },
  emits: ['focus-exoplanet'],
  methods: {
    getHabitabilityColor(habitability) {
      // Retorna un color basado en el porcentaje de habitabilidad
      if (habitability >= 80) return '#4a90e2'; // Azul para alta habitabilidad
      if (habitability >= 60) return '#ffaa00'; // Naranja para habitabilidad media
      if (habitability >= 40) return '#ff6b35'; // Rojo-naranja para habitabilidad baja
      return '#ff4444'; // Rojo para habitabilidad muy baja
    }
  }
};
</script>

<style scoped>
.exoplanet-list-component {
  height: 100%;
}

.exoplanet-info-panel {
  background-color: rgba(0, 0, 0, 0.6);
  padding: 20px;
  border-radius: 12px;
  backdrop-filter: blur(10px);
  max-height: 400px;
  overflow-y: auto;
  height: 100%;
}

.exoplanet-info-panel h3 {
  margin-top: 0;
  color: #4a90e2;
  border-bottom: 2px solid #4a90e2;
  padding-bottom: 10px;
}

.no-exoplanets {
  text-align: center;
  color: #888;
  font-style: italic;
  padding: 20px;
}

.exoplanet-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.exoplanet-item {
  background-color: rgba(74, 144, 226, 0.1);
  padding: 15px;
  border-radius: 8px;
  border-left: 4px solid #4a90e2;
  cursor: pointer;
  transition: all 0.3s ease;
}

.exoplanet-item:hover {
  background-color: rgba(74, 144, 226, 0.2);
  transform: translateX(5px);
}

.exoplanet-item h4 {
  margin: 0 0 10px 0;
  color: #4a90e2;
}

.exoplanet-details p {
  margin: 5px 0;
  font-size: 0.9em;
}

.habitability {
  margin-top: 10px !important;
}

.habitability-value {
  font-weight: bold;
}

.habitability-indicator {
  margin-top: 10px;
  width: 100%;
  height: 4px;
  background-color: rgba(255, 255, 255, 0.1);
  border-radius: 2px;
  overflow: hidden;
}

.habitability-bar {
  height: 100%;
  border-radius: 2px;
  transition: width 0.3s ease;
}

/* Scrollbar personalizada */
.exoplanet-info-panel::-webkit-scrollbar {
  width: 8px;
}

.exoplanet-info-panel::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
}

.exoplanet-info-panel::-webkit-scrollbar-thumb {
  background: rgba(74, 144, 226, 0.5);
  border-radius: 4px;
}

.exoplanet-info-panel::-webkit-scrollbar-thumb:hover {
  background: rgba(74, 144, 226, 0.7);
}
</style>