<template>
  <div id="exoplanet-observer">
    <!-- Header -->
    <header class="header">
      <button class="nav-button" @click="goBack">⬅ Regresar a la Tierra</button>
      <h1>🌌 Observador de Exoplanetas</h1>
      <div class="coordinates" v-if="selectedLocation">
        📍 Lat: {{ selectedLocation.lat.toFixed(4) }}°, Lng: {{ selectedLocation.lng.toFixed(4) }}°
      </div>
    </header>

    <!-- Paso 1: Selección de ubicación en el mapa -->
    <div v-if="currentStep === 1" class="step-container">
      <div class="instruction-panel">
        <h2>Paso 1: Selecciona tu ubicación en la Tierra</h2>
        <p>Haz clic en cualquier punto del mapa para establecer tu posición de 22observación:</p>
      </div>

      <div class="map-container">
        <div ref="worldMap" class="world-map"></div>
        <div class="map-controls">
          <button
            v-if="selectedLocation"
            @click="confirmLocation"
            class="confirm-button"
          >
            ✅ Confirmar Ubicación
          </button>
        </div>
      </div>
    </div>

    <!-- Paso 2: Vista de horizonte 360° -->
    <div v-if="currentStep === 2" class="step-container">
      <div class="instruction-panel">
        <h2>Paso 2: Vista del Horizonte desde tu Ubicación</h2>
        <p>Observa el cielo dividido en secciones para localizar exoplanetas visibles:</p>
        <div class="info-panel">
          <p><strong>Ubicación:</strong> {{ getLocationName() }}</p>
          <p><strong>Exoplanetas detectados:</strong> {{ detectedExoplanets.length }}</p>
        </div>
      </div>

      <div class="horizon-container">
        <div ref="horizonView" class="horizon-view"></div>

        <!-- Panel de información de exoplanetas -->
        <div class="exoplanet-info-panel">
          <h3>Exoplanetas Visibles</h3>
          <div v-if="detectedExoplanets.length === 0" class="no-exoplanets">
            🔭 No hay exoplanetas visibles desde esta ubicación en este momento.
          </div>
          <div v-else class="exoplanet-list">
            <div
              v-for="(exoplanet, index) in detectedExoplanets"
              :key="index"
              class="exoplanet-item"
              @click="focusOnExoplanet(exoplanet)"
            >
              <h4>{{ exoplanet.name }}</h4>
              <p><strong>Dirección:</strong> {{ exoplanet.direction }}°</p>
              <p><strong>Elevación:</strong> {{ exoplanet.elevation }}°</p>
              <p><strong>Distancia:</strong> {{ exoplanet.distance }} años luz</p>
              <p><strong>Probabilidad de vida:</strong> {{ exoplanet.habitability }}%</p>
            </div>
          </div>
        </div>
      </div>

      <div class="controls">
        <button @click="goBackToMap" class="secondary-button">🗺️ Cambiar Ubicación</button>
        <button @click="refreshExoplanets" class="primary-button">🔄 Actualizar Observación</button>
        <button @click="goAddExoplanet" class="primary-button">🔄 Consultar Nuevo Exoplaneta </button>
      </div>
    </div>
  </div>
</template>

<script>
import * as THREE from 'three';

export default {
  name: 'ExoplanetObserver',
  data() {
    return {
      currentStep: 1,
      selectedLocation: null,
      detectedExoplanets: [],
      worldMap: null,
      horizonScene: null,
      horizonCamera: null,
      horizonRenderer: null,
      // Base de datos simulada de exoplanetas
      exoplanetDatabase: [
        {
          name: "Kepler-452b",
          distance: 1402,
          habitability: 85,
          baseDirection: 180,
          baseElevation: 45
        },
        {
          name: "Proxima Centauri b",
          distance: 4.24,
          habitability: 75,
          baseDirection: 270,
          baseElevation: 30
        },
        {
          name: "TRAPPIST-1e",
          distance: 39.6,
          habitability: 90,
          baseDirection: 90,
          baseElevation: 60
        },
        {
          name: "TOI-715 b",
          distance: 137,
          habitability: 70,
          baseDirection: 45,
          baseElevation: 25
        },
        {
          name: "K2-18 b",
          distance: 124,
          habitability: 80,
          baseDirection: 315,
          baseElevation: 50
        }
      ]
    };
  },
  mounted() {
    this.initWorldMap();
  },
  beforeUnmount() {
    if (this.horizonRenderer) {
      this.horizonRenderer.dispose();
    }
  },
  methods: {
    goBack() {
      this.$router.go(-1);
    },

    initWorldMap() {
      // Crear el mapa mundial con Three.js
      const scene = new THREE.Scene();
      const camera = new THREE.PerspectiveCamera(75, 800 / 600, 0.1, 1000);
      const renderer = new THREE.WebGLRenderer({ antialias: true });

      renderer.setSize(800, 600);
      renderer.setClearColor(0x001122);
      this.$refs.worldMap.appendChild(renderer.domElement);

      // Crear una esfera para representar la Tierra
      const geometry = new THREE.SphereGeometry(2, 64, 64);
      const textureLoader = new THREE.TextureLoader();

      // Crear material con color azul-verde para simular la Tierra
      const material = new THREE.MeshPhongMaterial({
        color: 0x4a90e2,
        shininess: 100
      });

      const earth = new THREE.Mesh(geometry, material);
      scene.add(earth);

      // Agregar líneas de latitud y longitud
      this.addGridLines(scene);

      // Iluminación
      const ambientLight = new THREE.AmbientLight(0x404040, 0.4);
      scene.add(ambientLight);

      const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
      directionalLight.position.set(5, 5, 5);
      scene.add(directionalLight);

      camera.position.z = 5;

      // Agregar controles de ratón
      this.addMapControls(renderer.domElement, camera, earth);

      const animate = () => {
        requestAnimationFrame(animate);
        earth.rotation.y += 0.005;
        renderer.render(scene, camera);
      };
      animate();

      this.worldMap = { scene, camera, renderer, earth };
    },

    addGridLines(scene) {
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
        scene.add(line);
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
        scene.add(line);
      }
    },

    addMapControls(canvas, camera, earth) {
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

          earth.rotation.y += deltaMove.x * 0.01;
          earth.rotation.x += deltaMove.y * 0.01;

          previousMousePosition = { x: event.clientX, y: event.clientY };
        }
      });

      canvas.addEventListener('mouseup', () => {
        isDragging = false;
      });

      canvas.addEventListener('click', (event) => {
        if (!isDragging) {
          this.handleMapClick(event, canvas, camera, earth);
        }
      });

      // Zoom con rueda del ratón
      canvas.addEventListener('wheel', (event) => {
        event.preventDefault();
        camera.position.z += event.deltaY * 0.01;
        camera.position.z = Math.max(3, Math.min(10, camera.position.z));
      });
    },

    handleMapClick(event, canvas, camera, earth) {
      const rect = canvas.getBoundingClientRect();
      const mouse = new THREE.Vector2();
      mouse.x = ((event.clientX - rect.left) / canvas.width) * 2 - 1;
      mouse.y = -((event.clientY - rect.top) / canvas.height) * 2 + 1;

      const raycaster = new THREE.Raycaster();
      raycaster.setFromCamera(mouse, camera);

      const intersects = raycaster.intersectObject(earth);

      if (intersects.length > 0) {
        const intersectionPoint = intersects[0].point;

        // Convertir punto 3D a coordenadas lat/lng
        const lat = Math.asin(intersectionPoint.y / 2) * (180 / Math.PI);
        const lng = Math.atan2(intersectionPoint.z, intersectionPoint.x) * (180 / Math.PI);

        this.selectedLocation = { lat, lng };

        // Crear marcador visual
        this.addLocationMarker(intersectionPoint);
      }
    },

    addLocationMarker(position) {
      // Remover marcador anterior si existe
      if (this.worldMap.marker) {
        this.worldMap.scene.remove(this.worldMap.marker);
      }

      const geometry = new THREE.SphereGeometry(0.05, 16, 16);
      const material = new THREE.MeshBasicMaterial({ color: 0xff0000 });
      const marker = new THREE.Mesh(geometry, material);

      marker.position.copy(position);
      marker.position.multiplyScalar(1.02); // Elevar ligeramente sobre la superficie

      this.worldMap.scene.add(marker);
      this.worldMap.marker = marker;
    },

    confirmLocation() {
      this.currentStep = 2;
      this.$nextTick(() => {
        this.initHorizonView();
        this.calculateVisibleExoplanets();
      });
    },

    initHorizonView() {
      const scene = new THREE.Scene();
      const camera = new THREE.PerspectiveCamera(75, 800 / 400, 0.1, 1000);
      const renderer = new THREE.WebGLRenderer({ antialias: true });

      renderer.setSize(800, 400);
      renderer.setClearColor(0x000033);
      this.$refs.horizonView.appendChild(renderer.domElement);

      // Crear el horizonte (semi-esfera)
      this.createHorizonSphere(scene);

      // Crear las secciones del cielo
      this.createSkySections(scene);

      // Agregar estrellas de fondo
      this.addBackgroundStars(scene);

      camera.position.set(0, 0, 0);

      // Controles de cámara para mirar alrededor
      this.addHorizonControls(renderer.domElement, camera);

      const animate = () => {
        requestAnimationFrame(animate);
        renderer.render(scene, camera);
      };
      animate();

      this.horizonScene = scene;
      this.horizonCamera = camera;
      this.horizonRenderer = renderer;
    },

    createHorizonSphere(scene) {
      const geometry = new THREE.SphereGeometry(50, 64, 32, 0, Math.PI * 2, 0, Math.PI / 2);
      const material = new THREE.MeshBasicMaterial({
        color: 0x87CEEB,
        side: THREE.BackSide,
        transparent: true,
        opacity: 0.3
      });
      const horizon = new THREE.Mesh(geometry, material);
      scene.add(horizon);
    },

    createSkySections(scene) {
      // Crear líneas divisorias para las secciones del cielo
      const material = new THREE.LineBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0.5 });

      // Líneas de azimut (direcciones cardinales)
      for (let azimuth = 0; azimuth < 360; azimuth += 45) {
        const geometry = new THREE.BufferGeometry();
        const points = [];
        for (let elevation = 0; elevation <= 90; elevation += 5) {
          const x = 45 * Math.cos((elevation * Math.PI) / 180) * Math.cos((azimuth * Math.PI) / 180);
          const y = 45 * Math.sin((elevation * Math.PI) / 180);
          const z = 45 * Math.cos((elevation * Math.PI) / 180) * Math.sin((azimuth * Math.PI) / 180);
          points.push(x, y, z);
        }
        geometry.setAttribute('position', new THREE.Float32BufferAttribute(points, 3));
        const line = new THREE.Line(geometry, material);
        scene.add(line);
      }

      // Líneas de elevación
      for (let elevation = 15; elevation <= 75; elevation += 15) {
        const geometry = new THREE.BufferGeometry();
        const points = [];
        for (let azimuth = 0; azimuth <= 360; azimuth += 5) {
          const x = 45 * Math.cos((elevation * Math.PI) / 180) * Math.cos((azimuth * Math.PI) / 180);
          const y = 45 * Math.sin((elevation * Math.PI) / 180);
          const z = 45 * Math.cos((elevation * Math.PI) / 180) * Math.sin((azimuth * Math.PI) / 180);
          points.push(x, y, z);
        }
        geometry.setAttribute('position', new THREE.Float32BufferAttribute(points, 3));
        const line = new THREE.Line(geometry, material);
        scene.add(line);
      }
    },

    addBackgroundStars(scene) {
      const starGeometry = new THREE.BufferGeometry();
      const starMaterial = new THREE.PointsMaterial({ color: 0xffffff, size: 0.5 });

      const starVertices = [];
      for (let i = 0; i < 1000; i++) {
        const x = (Math.random() - 0.5) * 200;
        const y = Math.random() * 100;
        const z = (Math.random() - 0.5) * 200;
        starVertices.push(x, y, z);
      }

      starGeometry.setAttribute('position', new THREE.Float32BufferAttribute(starVertices, 3));
      const stars = new THREE.Points(starGeometry, starMaterial);
      scene.add(stars);
    },

    addHorizonControls(canvas, camera) {
      let isLooking = false;
      let phi = 0;
      let theta = 0;

      canvas.addEventListener('mousedown', () => {
        isLooking = true;
      });

      canvas.addEventListener('mousemove', (event) => {
        if (isLooking) {
          phi -= event.movementX * 0.01;
          theta = Math.max(-Math.PI / 2, Math.min(Math.PI / 2, theta - event.movementY * 0.01));

          camera.rotation.x = theta;
          camera.rotation.y = phi;
        }
      });

      canvas.addEventListener('mouseup', () => {
        isLooking = false;
      });
    },

    calculateVisibleExoplanets() {
      // Algoritmo simulado para calcular exoplanetas visibles basado en la ubicación
      this.detectedExoplanets = [];

      const { lat, lng } = this.selectedLocation;

      this.exoplanetDatabase.forEach(exoplanet => {
        // Simulación: la visibilidad depende de la latitud y longitud
        const latFactor = Math.sin((lat * Math.PI) / 180);
        const lngFactor = Math.cos((lng * Math.PI) / 180);

        // Algoritmo básico de visibilidad (esto sería mucho más complejo en realidad)
        const visibility = Math.random() > 0.3; // 70% de probabilidad de visibilidad

        if (visibility) {
          const direction = (exoplanet.baseDirection + lng + Math.random() * 60 - 30) % 360;
          const elevation = Math.max(5, Math.min(85, exoplanet.baseElevation + latFactor * 30 + Math.random() * 20 - 10));

          this.detectedExoplanets.push({
            ...exoplanet,
            direction: Math.round(direction),
            elevation: Math.round(elevation)
          });

          // Agregar marcador visual en el horizonte
          this.addExoplanetMarker(direction, elevation, exoplanet.name);
        }
      });
    },

    addExoplanetMarker(direction, elevation, name) {
      if (!this.horizonScene) return;

      const phi = (direction * Math.PI) / 180;
      const theta = (elevation * Math.PI) / 180;

      const x = 40 * Math.cos(theta) * Math.cos(phi);
      const y = 40 * Math.sin(theta);
      const z = 40 * Math.cos(theta) * Math.sin(phi);

      // Crear marcador del exoplaneta
      const geometry = new THREE.SphereGeometry(0.8, 16, 16);
      const material = new THREE.MeshBasicMaterial({
        color: 0x00ff88,
        transparent: true,
        opacity: 0.8
      });
      const marker = new THREE.Mesh(geometry, material);
      marker.position.set(x, y, z);

      // Agregar efecto de pulsación
      marker.userData = { name, originalScale: 1 };
      marker.scale.setScalar(1);

      this.horizonScene.add(marker);

      // Animación de pulsación
      const pulsate = () => {
        const time = Date.now() * 0.005;
        marker.scale.setScalar(1 + Math.sin(time) * 0.3);
        requestAnimationFrame(pulsate);
      };
      pulsate();
    },

    goAddExoplanet() {
      this.$router.push('/earth/exoplanet-add');
    },

    goBackToMap() {
      this.currentStep = 1;
      this.selectedLocation = null;
      this.detectedExoplanets = [];

      if (this.horizonRenderer) {
        this.horizonRenderer.dispose();
        this.$refs.horizonView.innerHTML = '';
      }
    },

    refreshExoplanets() {
      // Limpiar marcadores existentes
      if (this.horizonScene) {
        const markersToRemove = [];
        this.horizonScene.traverse((child) => {
          if (child.userData && child.userData.name) {
            markersToRemove.push(child);
          }
        });
        markersToRemove.forEach(marker => this.horizonScene.remove(marker));
      }

      // Recalcular exoplanetas visibles
      this.calculateVisibleExoplanets();
    },

    focusOnExoplanet(exoplanet) {
      if (!this.horizonCamera) return;

      const phi = (exoplanet.direction * Math.PI) / 180;
      const theta = (exoplanet.elevation * Math.PI) / 180;

      // Animar la cámara hacia el exoplaneta
      this.horizonCamera.rotation.y = phi;
      this.horizonCamera.rotation.x = theta - Math.PI / 2;

      alert(`Enfocando en ${exoplanet.name}\nDirección: ${exoplanet.direction}°\nElevación: ${exoplanet.elevation}°`);
    },

    getLocationName() {
      if (!this.selectedLocation) return 'Ubicación no seleccionada';

      const { lat, lng } = this.selectedLocation;
      return `${lat.toFixed(2)}°${lat >= 0 ? 'N' : 'S'}, ${lng.toFixed(2)}°${lng >= 0 ? 'E' : 'W'}`;
    }
  }
};
</script>

<style scoped>
#exoplanet-observer {
  min-height: 100vh;
  background: linear-gradient(135deg, #001122 0%, #003366 100%);
  color: white;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

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

.step-container {
  padding: 20px;
}

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
  border-left: 4px solid #00ff88;
}

.map-container {
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

.horizon-container {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
}

.horizon-view {
  flex: 2;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.exoplanet-info-panel {
  flex: 1;
  background-color: rgba(0, 0, 0, 0.6);
  padding: 20px;
  border-radius: 12px;
  backdrop-filter: blur(10px);
  max-height: 400px;
  overflow-y: auto;
}

.exoplanet-info-panel h3 {
  margin-top: 0;
  color: #00ff88;
  border-bottom: 2px solid #00ff88;
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

.exoplanet-item p {
  margin: 5px 0;
  font-size: 0.9em;
}

.controls {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 20px;
}

.nav-button,
.confirm-button,
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

.nav-button {
  background-color: #6c757d;
  color: white;
}

.nav-button:hover {
  background-color: #5a6268;
  transform: translateY(-2px);
}

.confirm-button,
.primary-button {
  background-color: #00ff88;
  color: #001122;
}

.confirm-button:hover,
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