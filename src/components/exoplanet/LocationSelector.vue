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
  gap: 30px;
}

.map-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
  width: 100%;
  max-width: 1000px;
  /* Centrar mejor el contenido */
  margin: 0 auto;
  padding: 20px;
  background: rgba(0, 20, 40, 0.8);
  border-radius: 15px;
  border: 1px solid #4a90e2;
}
</style>