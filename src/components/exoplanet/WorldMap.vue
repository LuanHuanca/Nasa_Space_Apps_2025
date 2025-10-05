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
import earthTexture from '@/assets/earth.jpg';

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
      marker: null
    };
  },
  mounted() {
    this.initWorldMap();
  },
  beforeUnmount() {
    if (this.renderer) {
      this.renderer.dispose();
    }
  },
  methods: {
    initWorldMap() {
      // Crear el mapa mundial con Three.js
      this.scene = new THREE.Scene();
      this.camera = new THREE.PerspectiveCamera(75, 800 / 600, 0.1, 1000);
      this.renderer = new THREE.WebGLRenderer({ antialias: true });
      
      this.renderer.setSize(800, 600);
      this.renderer.setClearColor(0x001122);
      this.$refs.worldMapContainer.appendChild(this.renderer.domElement);
      
      // Crear una esfera para representar la Tierra
      const geometry = new THREE.SphereGeometry(2, 64, 64);
      
      // Cargar textura de la Tierra
      const textureLoader = new THREE.TextureLoader();
      const earthMap = textureLoader.load(earthTexture);
      
      // Crear material con la textura real de la Tierra
      const material = new THREE.MeshPhongMaterial({
        map: earthMap,
        shininess: 50,
        transparent: false
      });
      
      this.earth = new THREE.Mesh(geometry, material);
      this.scene.add(this.earth);
      
      // Agregar líneas de latitud y longitud
      this.addGridLines();
      
      // Iluminación
      const ambientLight = new THREE.AmbientLight(0x404040, 0.4);
      this.scene.add(ambientLight);
      
      const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
      directionalLight.position.set(5, 5, 5);
      this.scene.add(directionalLight);
      
      this.camera.position.z = 5;
      
      // Agregar controles de ratón
      this.addMapControls();
      
      // Iniciar animación
      this.animate();
    },

    addGridLines() {
      const material = new THREE.LineBasicMaterial({ color: 0x888888 });
      
      // Líneas de latitud
      for (let lat = -80; lat <= 80; lat += 20) {
        const geometry = new THREE.BufferGeometry();
        const points = [];
        for (let lng = 0; lng <= 360; lng += 5) {
          const phi = (90 - lat) * (Math.PI / 180);
          const theta = lng * (Math.PI / 180);
          const x = 2.01 * Math.sin(phi) * Math.cos(theta);
          const y = 2.01 * Math.cos(phi);
          const z = 2.01 * Math.sin(phi) * Math.sin(theta);
          points.push(x, y, z);
        }
        geometry.setAttribute('position', new THREE.Float32BufferAttribute(points, 3));
        const line = new THREE.Line(geometry, material);
        this.scene.add(line);
      }
      
      // Líneas de longitud
      for (let lng = 0; lng < 360; lng += 30) {
        const geometry = new THREE.BufferGeometry();
        const points = [];
        for (let lat = -90; lat <= 90; lat += 5) {
          const phi = (90 - lat) * (Math.PI / 180);
          const theta = lng * (Math.PI / 180);
          const x = 2.01 * Math.sin(phi) * Math.cos(theta);
          const y = 2.01 * Math.cos(phi);
          const z = 2.01 * Math.sin(phi) * Math.sin(theta);
          points.push(x, y, z);
        }
        geometry.setAttribute('position', new THREE.Float32BufferAttribute(points, 3));
        const line = new THREE.Line(geometry, material);
        this.scene.add(line);
      }
    },

    addMapControls() {
      const canvas = this.renderer.domElement;
      let isDragging = false;
      let previousMousePosition = { x: 0, y: 0 };
      
      canvas.addEventListener('mousedown', (event) => {
        isDragging = true;
        previousMousePosition = { x: event.clientX, y: event.clientY };
      });
      
      canvas.addEventListener('mousemove', (event) => {
        if (isDragging) {
          const deltaMove = {
            x: event.clientX - previousMousePosition.x,
            y: event.clientY - previousMousePosition.y
          };
          
          this.earth.rotation.y += deltaMove.x * 0.01;
          this.earth.rotation.x += deltaMove.y * 0.01;
          
          previousMousePosition = { x: event.clientX, y: event.clientY };
        }
      });
      
      canvas.addEventListener('mouseup', () => {
        isDragging = false;
      });
      
      canvas.addEventListener('click', (event) => {
        if (!isDragging) {
          this.handleMapClick(event);
        }
      });
      
      // Zoom con rueda del ratón
      canvas.addEventListener('wheel', (event) => {
        event.preventDefault();
        this.camera.position.z += event.deltaY * 0.01;
        this.camera.position.z = Math.max(3, Math.min(10, this.camera.position.z));
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
      this.marker = new THREE.Mesh(geometry, material);
      
      this.marker.position.copy(position);
      this.marker.position.multiplyScalar(1.02); // Elevar ligeramente sobre la superficie
      
      this.scene.add(this.marker);
    },

    animate() {
      requestAnimationFrame(this.animate);
      if (this.earth) {
        this.earth.rotation.y += 0.005;
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
}

.world-map {
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.map-controls {
  display: flex;
  justify-content: center;
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