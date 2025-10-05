<template>
  <div class="horizon-view-step">
    <InstructionPanel
      title="Paso 2: Vista del Horizonte desde tu Ubicación"
      description="Observa el cielo dividido en secciones para localizar exoplanetas visibles:"
      :show-info-panel="true"
    >
      <template #info>
        <p><strong>Ubicación:</strong> {{ getLocationName() }}</p>
        <p><strong>Exoplanetas detectados:</strong> {{ detectedExoplanets.length }}</p>
      </template>
    </InstructionPanel>

    <div class="horizon-container">
      <div class="horizon-view-wrapper">
        <HorizonViewer
          :selected-location="selectedLocation"
          :detected-exoplanets="detectedExoplanets"
          @exoplanet-focused="handleExoplanetFocused"
          ref="horizonViewer"
        />
      </div>
      
      <div class="exoplanet-panel-wrapper">
        <ExoplanetList
          :exoplanets="detectedExoplanets"
          @focus-exoplanet="focusOnExoplanet"
        />
      </div>
    </div>

    <div class="controls">
      <button @click="$emit('go-back-to-map')" class="secondary-button">
        🗺️ Cambiar Ubicación
      </button>
      <button @click="$emit('refresh-exoplanets')" class="primary-button">
        🔄 Actualizar Observación
      </button>
    </div>
  </div>
</template>

<script>
import InstructionPanel from './InstructionPanel.vue';
import HorizonViewer from './HorizonViewer.vue';
import ExoplanetList from './ExoplanetList.vue';

export default {
  name: 'HorizonViewStep',
  components: {
    InstructionPanel,
    HorizonViewer,
    ExoplanetList
  },
  props: {
    selectedLocation: {
      type: Object,
      required: true
    },
    detectedExoplanets: {
      type: Array,
      required: true
    }
  },
  emits: ['go-back-to-map', 'refresh-exoplanets', 'exoplanet-focused'],
  methods: {
    getLocationName() {
      if (!this.selectedLocation) return 'Ubicación no seleccionada';
      
      const { lat, lng } = this.selectedLocation;
      return `${lat.toFixed(2)}°${lat >= 0 ? 'N' : 'S'}, ${lng.toFixed(2)}°${lng >= 0 ? 'E' : 'W'}`;
    },

    focusOnExoplanet(exoplanet) {
      if (this.$refs.horizonViewer) {
        this.$refs.horizonViewer.focusOnExoplanet(exoplanet);
      }
    },

    handleExoplanetFocused(exoplanet) {
      this.$emit('exoplanet-focused', exoplanet);
    }
  }
};
</script>

<style scoped>
.horizon-view-step {
  padding: 20px;
}

.horizon-container {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
}

.horizon-view-wrapper {
  flex: 2;
}

.exoplanet-panel-wrapper {
  flex: 1;
}

.controls {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 20px;
}

.primary-button,
.secondary-button {
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  font-size: 1em;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 600;
}

.primary-button {
  background-color: #00ff88;
  color: #001122;
}

.primary-button:hover {
  background-color: #00cc6a;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 255, 136, 0.3);
}

.secondary-button {
  background-color: #4a90e2;
  color: white;
}

.secondary-button:hover {
  background-color: #357abd;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(74, 144, 226, 0.3);
}
</style>