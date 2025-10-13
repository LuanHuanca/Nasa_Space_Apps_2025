<template>
  <div class="location-selector">
    <InstructionPanel
      title="Paso 1: Selecciona tu ubicación en la Tierra"
      description="Haz clic en cualquier punto del mapa para establecer tu posición de observación:"
    />
    
    <div class="map-container">
      <WorldMap
        :selected-location="selectedLocation"
        @location-selected="handleLocationSelected"
        @confirm-location="$emit('location-confirmed')"
      />
    </div>
  </div>
</template>

<script>
import InstructionPanel from './InstructionPanel.vue';
import WorldMap from './WorldMap.vue';

export default {
  name: 'LocationSelector',
  components: {
    InstructionPanel,
    WorldMap
  },
  props: {
    selectedLocation: {
      type: Object,
      default: null
    }
  },
  emits: ['location-selected', 'location-confirmed'],
  methods: {
    handleLocationSelected(location) {
      this.$emit('location-selected', location);
    }
  }
};
</script>

<style scoped>
.location-selector {
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  min-height: 100vh;
}

.map-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px;
  border-radius: 15px;
}

/* ========================================= */
/* RESPONSIVE DESIGN PARA LOCATIONSELECTOR */
/* ========================================= */

/* Tablets */
@media (max-width: 1024px) {
  .location-selector {
    padding: 15px;
    min-height: auto;
  }
  
  .map-container {
    max-width: 95%;
    padding: 15px;
    gap: 15px;
  }
}

/* Smartphones */
@media (max-width: 768px) {
  .location-selector {
    padding: 10px;
  }
  
  .map-container {
    max-width: 100%;
    padding: 10px;
    gap: 10px;
    border-radius: 10px;
  }
}

/* Smartphones pequeños */
@media (max-width: 480px) {
  .location-selector {
    padding: 5px;
  }
  
  .map-container {
    padding: 5px;
    gap: 8px;
  }
}
</style>