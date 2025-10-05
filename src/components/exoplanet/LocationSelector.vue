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
}

.map-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}
</style>