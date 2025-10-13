<template>
  <div class="world-map-component" style="position: relative;">
    <!-- Tarjeta del mundo - intacta -->
    <div class="map-container">
      <div ref="worldMapContainer" class="world-map"></div>
    </div>
    
    <!-- Botón lateral flotante - separado de la tarjeta -->
    <div v-if="selectedLocation" class="floating-controls">
      <button 
        @click="$emit('confirm-location')" 
        class="confirm-button"
      >
        ✅ Confirmar Ubicación
      </button>
      <div class="location-info">
        <p><strong>Lat:</strong> {{ selectedLocation.lat.toFixed(2) }}°</p>
        <p><strong>Lng:</strong> {{ selectedLocation.lng.toFixed(2) }}°</p>
      </div>
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
      // IMPLEMENTACION EXACTA DE EARTH.VUE CON RESPONSIVE
      const container = this.$refs.worldMapContainer;
      const containerWidth = container.clientWidth;
      const containerHeight = container.clientHeight;
      
      // Dimensiones responsive
      const width = containerWidth > 0 ? containerWidth : 800;
      const height = containerHeight > 0 ? containerHeight : 600;
      
      this.scene = markRaw(new THREE.Scene());
      this.camera = markRaw(new THREE.PerspectiveCamera(75, width / height, 0.1, 1000));
      this.camera.position.z = 5;

      this.renderer = markRaw(new THREE.WebGLRenderer({ alpha: true }));
      this.renderer.setSize(width, height);
      this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2)); // Optimización móvil
      container.appendChild(this.renderer.domElement);

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
      
      // Manejar resize responsive
      this.addResizeHandler();

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
    },

    addResizeHandler() {
      const handleResize = () => {
        const container = this.$refs.worldMapContainer;
        if (container && this.renderer && this.camera) {
          const width = container.clientWidth;
          const height = container.clientHeight;
          
          // Actualizar cámara
          this.camera.aspect = width / height;
          this.camera.updateProjectionMatrix();
          
          // Actualizar renderer
          this.renderer.setSize(width, height);
          this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        }
      };
      
      window.addEventListener('resize', handleResize);
      window.addEventListener('orientationchange', handleResize);
      
      // Limpiar listeners en unmount
      this.$once('hook:beforeUnmount', () => {
        window.removeEventListener('resize', handleResize);
        window.removeEventListener('orientationchange', handleResize);
      });
    }
  }
};
</script>

<style scoped>
.world-map-component {
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  width: 100%;
  background: radial-gradient(circle at center, #0a1a2f, #020c1b);
  overflow: hidden;
}

/* Contenedor del mapa */
.map-container {
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
  z-index: 1;
}

.world-map {
  border-radius: 14px;
  overflow: hidden;
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.5);
  border: 2px solid #2e6eb5;
  width: 800px;
  height: 600px;
  position: relative;
  background: rgba(0, 10, 25, 0.4);
}

.world-map canvas {
  display: block;
  cursor: crosshair;
  border-radius: 12px;
  z-index: 0;
}

/* Panel flotante lateral */
.floating-controls {
  position: absolute;
  top: 50%;
  right: 40px;
  transform: translateY(-50%);
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 15px;
  padding: 20px;
  background: rgba(10, 20, 40, 0.85);
  border-radius: 12px;
  border: 1px solid #4a90e2;
  box-shadow: 0 0 20px rgba(74, 144, 226, 0.2);
  color: #e0f0ff;
  z-index: 5;
  width: 240px;
}

/* Información de coordenadas */
.location-info {
  width: 100%;
  background: rgba(20, 30, 50, 0.8);
  padding: 12px 15px;
  border-radius: 8px;
  font-size: 0.9rem;
  border-left: 3px solid #4a90e2;
}

/* Botón de confirmación */
.confirm-button {
  align-self: center;
  padding: 12px 20px;
  background: linear-gradient(135deg, #4a90e2, #2e6eb5);
  border: none;
  border-radius: 10px;
  color: white;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(74, 144, 226, 0.4);
}

.confirm-button:hover {
  background: linear-gradient(135deg, #2e6eb5, #1f4c82);
  transform: scale(1.05);
  box-shadow: 0 8px 25px rgba(74, 144, 226, 0.6);
}

/* Adaptación responsive completa */
@media (max-width: 1200px) {
  .floating-controls {
    position: static;
    transform: none;
    margin-top: 20px;
    width: 90%;
    max-width: 400px;
    align-self: center;
  }
  
  .world-map-component {
    flex-direction: column;
    align-items: center;
  }
}

@media (max-width: 900px) {
  .world-map {
    width: 90vw;
    height: calc(90vw * 0.75);
    max-width: 600px;
    max-height: 450px;
  }
  
  .floating-controls {
    width: 90vw;
    max-width: 600px;
    padding: 15px;
  }
  
  .confirm-button {
    width: 100%;
    padding: 15px;
    font-size: 1.1rem;
  }
  
  .location-info {
    text-align: center;
  }
}

@media (max-width: 600px) {
  .world-map {
    width: 95vw;
    height: calc(95vw * 0.75);
    border-width: 1px;
  }
  
  .world-map-component {
    padding: 10px;
    min-height: auto;
  }
  
  .floating-controls {
    width: 95vw;
    padding: 12px;
    gap: 10px;
  }
  
  .confirm-button {
    padding: 12px;
    font-size: 1rem;
  }
  
  .location-info {
    padding: 10px;
    font-size: 0.85rem;
  }
  
  .location-info p {
    margin: 3px 0;
  }
}

@media (max-width: 480px) {
  .world-map {
    width: 98vw;
    height: calc(98vw * 0.75);
  }
  
  .floating-controls {
    width: 98vw;
    padding: 10px;
  }
  
  .confirm-button {
    padding: 10px;
    font-size: 0.9rem;
  }
  
  .location-info {
    font-size: 0.8rem;
  }
}

/* Orientación horizontal */
@media (max-height: 500px) and (orientation: landscape) {
  .world-map {
    height: 70vh;
    width: auto;
    max-width: 90vw;
  }
  
  .world-map-component {
    flex-direction: row;
    align-items: flex-start;
    gap: 20px;
  }
  
  .floating-controls {
    position: static;
    transform: none;
    width: 250px;
    height: fit-content;
  }
}
</style>