<template>
  <div class="instruction-panel">
    <h2>{{ title }}</h2>
    <p>{{ description }}</p>
    
    <!-- Slot para contenido adicional -->
    <slot></slot>
    
    <!-- Panel de información opcional -->
    <div v-if="showInfoPanel" class="info-panel">
      <slot name="info"></slot>
    </div>
  </div>
</template>

<script>
export default {
  name: 'InstructionPanel',
  props: {
    title: {
      type: String,
      required: true
    },
    description: {
      type: String,
      required: true
    },
    showInfoPanel: {
      type: Boolean,
      default: false
    }
  }
};
</script>

<style scoped>
.instruction-panel {
  background-color: rgba(255, 255, 255, 0.1);
  padding: 20px;
  border-radius: 12px;
  margin-bottom: 20px;
  backdrop-filter: blur(5px);
}

.instruction-panel h2 {
  margin-top: 0;
  color: #4a90e2;
}

.info-panel {
  background-color: rgba(0, 255, 136, 0.1);
  padding: 15px;
  border-radius: 8px;
  margin-top: 15px;
  border-left: 4px solid #4a90e2;
}
</style>