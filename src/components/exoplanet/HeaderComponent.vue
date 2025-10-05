<template>
  <header class="header">
    <button class="nav-button" @click="$emit('go-back')">
      ⬅ Regresar a la Tierra
    </button>
    <h1>🌌 Observador de Exoplanetas</h1>
    <div class="coordinates" v-if="selectedLocation">
      📍 Lat: {{ selectedLocation.lat.toFixed(4) }}°, Lng:
      {{ selectedLocation.lng.toFixed(4) }}°
    </div>
    <button @click="goAddExoplanet" class="primary-button">
      🔄 Consultar Nuevo Exoplaneta
    </button>
  </header>
</template>

<script>
export default {
  name: "HeaderComponent",
  props: {
    selectedLocation: {
      type: Object,
      default: null,
    },
  },
  emits: ["go-back"],
  methods: {
    goAddExoplanet() {
      this.$router.push('/earth/exoplanet-add');
    }
  }
};
</script>

<style scoped>
.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 15px 20px;
  background-color: rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(10px);
}

.header h1 {
  margin: 0;
  font-size: 1.8em;
  text-align: center;
  flex: 1;
}

.coordinates {
  background-color: rgba(74, 144, 226, 0.2);
  padding: 8px 12px;
  border-radius: 8px;
  font-family: monospace;
  font-size: 0.9em;
}

.nav-button {
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  font-size: 1em;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 600;
  background-color: #6c757d;
  color: white;
}

.nav-button:hover {
  background-color: #5a6268;
  transform: translateY(-2px);
}
</style>
