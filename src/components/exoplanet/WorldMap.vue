<template>
  <div class="world-map-component">
    <div ref="worldMapContainer" class="world-map"></div>
    <div class="map-controls">
      <button 
        v-if="selectedLocation" 
        @click="$emit('confirm-location')" 
        class="confirm-button"
      >
        ✅ Confirmar Ubicación
      </button>
    </div>
  </div>
</template>

<script>
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls';
import { markRaw } from 'vue'; // Importar markRaw para evitar proxificación
import earthTexture from '@/assets/tierra.png'; // MISMA TEXTURA QUE EARTH.VUE

export default {
  name: 'WorldMap',
  props: {
    selectedLocation: {
      type: Object,
      default: null
    }
  },
  emits: ['location-selected', 'confirm-location'],
  data() {
    return {
      scene: null,
      camera: null,
      renderer: null,
      earth: null,
      marker: null,
      controls: null
    };
  },
  mounted() {
    this.initWorldMap();
  },
  beforeUnmount() {
    if (this.controls) {
      this.controls.dispose();
    }
    if (this.renderer) {
      this.renderer.dispose();
    }
  },
  methods: {
    initWorldMap() {
      // IMPLEMENTACION EXACTA DE EARTH.VUE
      this.scene = markRaw(new THREE.Scene());
      this.camera = markRaw(new THREE.PerspectiveCamera(75, 800 / 600, 0.1, 1000));
      this.camera.position.z = 5;

      this.renderer = markRaw(new THREE.WebGLRenderer({ alpha: true }));
      this.renderer.setSize(800, 600);
      this.$refs.worldMapContainer.appendChild(this.renderer.domElement);

      // Crear la esfera de la Tierra EXACTAMENTE como en earth.vue
      const earthGeometry = new THREE.SphereGeometry(2, 32, 32); // Escalado para el mapa
      const textureLoader = new THREE.TextureLoader();
      const earthMaterial = new THREE.MeshBasicMaterial({
        map: textureLoader.load(earthTexture),
      });
      this.earth = markRaw(new THREE.Mesh(earthGeometry, earthMaterial));
      this.scene.add(this.earth);

      console.log('🌍 Tierra creada con implementación EXACTA de earth.vue usando tierra.png');

      // Controles de cámara EXACTOS de earth.vue
      this.controls = markRaw(new OrbitControls(this.camera, this.renderer.domElement));
      this.controls.enableDamping = true;
      this.controls.dampingFactor = 0.25;
      this.controls.enableZoom = true;

      // Controles para colocar pin
      this.addMapControls();

      // Iniciar animación
      this.animate();
    },

    addMapControls() {
      const canvas = this.renderer.domElement;
      
      canvas.addEventListener('click', (event) => {
        this.handleMapClick(event);
      });
    },

    handleMapClick(event) {
      const canvas = this.renderer.domElement;
      const rect = canvas.getBoundingClientRect();
      const mouse = new THREE.Vector2();
      mouse.x = ((event.clientX - rect.left) / canvas.width) * 2 - 1;
      mouse.y = -((event.clientY - rect.top) / canvas.height) * 2 + 1;
      
      const raycaster = new THREE.Raycaster();
      raycaster.setFromCamera(mouse, this.camera);
      
      const intersects = raycaster.intersectObject(this.earth);
      
      if (intersects.length > 0) {
        const intersectionPoint = intersects[0].point;
        
        // Convertir punto 3D a coordenadas lat/lng
        const lat = Math.asin(intersectionPoint.y / 2) * (180 / Math.PI);
        const lng = Math.atan2(intersectionPoint.z, intersectionPoint.x) * (180 / Math.PI);
        
        const location = { lat, lng };
        this.$emit('location-selected', location);
        
        // Crear marcador visual
        this.addLocationMarker(intersectionPoint);
      }
    },

    addLocationMarker(position) {
      // Remover marcador anterior si existe
      if (this.marker) {
        this.scene.remove(this.marker);
      }
      
      const geometry = new THREE.SphereGeometry(0.05, 16, 16);
      const material = new THREE.MeshBasicMaterial({ color: 0xff0000 });
      this.marker = markRaw(new THREE.Mesh(geometry, material));
      
      this.marker.position.copy(position);
      this.marker.position.multiplyScalar(1.02); // Elevar ligeramente sobre la superficie
      
      this.scene.add(this.marker);
    },

    animate() {
      requestAnimationFrame(this.animate);
      
      // Rotación suave de la Tierra como en earth.vue
      if (this.earth) {
        this.earth.rotation.y += 0.01; // MISMA VELOCIDAD QUE EARTH.VUE
      }
      
      // Actualizar controles
      if (this.controls) {
        this.controls.update();
      }
      
      if (this.renderer && this.scene && this.camera) {
        this.renderer.render(this.scene, this.camera);
      }
    }
  }
};
</script>

<style scoped>
.world-map-component {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
  width: 100%;
  max-width: 900px;
  margin: 0 auto;
}

.world-map {
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  position: relative;
  width: 800px;
  height: 600px;
  /* Agregar scroll visible */
  border: 2px solid #00ff88;
}

.world-map canvas {
  display: block;
  cursor: crosshair;
  border-radius: 10px;
}

.map-controls {
  display: flex;
  justify-content: center;
  margin-top: 10px;
}

.confirm-button {
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  font-size: 1em;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 600;
  background-color: #00ff88;
  color: #001122;
}

.confirm-button:hover {
  background-color: #00cc6a;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 255, 136, 0.3);
}
</style>