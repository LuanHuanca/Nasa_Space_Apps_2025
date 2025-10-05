<template>
  <div class="horizon-viewer-component">
    <div ref="horizonContainer" class="horizon-view"></div>
  </div>
</template>

<script>
import * as THREE from 'three';
import earthTexture from '@/assets/earth.jpg';

export default {
  name: 'HorizonViewer',
  props: {
    selectedLocation: {
      type: Object,
      required: true
    },
    detectedExoplanets: {
      type: Array,
      default: () => []
    }
  },
  emits: ['exoplanet-focused'],
  data() {
    return {
      scene: null,
      camera: null,
      renderer: null
    };
  },
  mounted() {
    this.initHorizonView();
  },
  beforeUnmount() {
    if (this.renderer) {
      this.renderer.dispose();
    }
  },
  watch: {
    detectedExoplanets: {
      handler(newExoplanets) {
        if (this.scene) {
          this.updateExoplanetMarkers();
        }
      },
      deep: true
    }
  },
  methods: {
    initHorizonView() {
      this.scene = new THREE.Scene();
      this.camera = new THREE.PerspectiveCamera(75, 800 / 400, 0.1, 1000);
      this.renderer = new THREE.WebGLRenderer({ antialias: true });
      
      this.renderer.setSize(800, 400);
      this.renderer.setClearColor(0x000033);
      this.$refs.horizonContainer.appendChild(this.renderer.domElement);
      
      // Crear el horizonte (semi-esfera)
      this.createHorizonSphere();
      
      // Crear el suelo verde
      this.createGreenGround();
      
      // Crear las secciones del cielo
      this.createSkySections();
      
      // Agregar estrellas de fondo
      this.addBackgroundStars();
      
      this.camera.position.set(0, 0, 0);
      
      // Controles de cámara para mirar alrededor
      this.addHorizonControls();
      
      // Iniciar animación
      this.animate();
    },

    createHorizonSphere() {
      const geometry = new THREE.SphereGeometry(50, 64, 32, 0, Math.PI * 2, 0, Math.PI / 2);
      const material = new THREE.MeshBasicMaterial({ 
        color: 0x87CEEB, 
        side: THREE.BackSide,
        transparent: true,
        opacity: 0.3
      });
      const horizon = new THREE.Mesh(geometry, material);
      this.scene.add(horizon);
    },

    createGreenGround() {
      // Crear un plano circular verde como suelo
      const groundGeometry = new THREE.CircleGeometry(50, 64);
      const groundMaterial = new THREE.MeshBasicMaterial({ 
        color: 0x2d5a27, // Verde oscuro natural
        side: THREE.DoubleSide,
        transparent: true,
        opacity: 0.8
      });
      const ground = new THREE.Mesh(groundGeometry, groundMaterial);
      
      // Rotar el plano para que sea horizontal
      ground.rotation.x = -Math.PI / 2;
      ground.position.y = -0.1; // Ligeramente debajo del nivel del horizonte
      
      this.scene.add(ground);

      // Agregar textura de hierba opcional (patrón verde)
      const grassGeometry = new THREE.CircleGeometry(45, 64);
      const grassMaterial = new THREE.MeshBasicMaterial({ 
        color: 0x4a7c59, // Verde hierba más claro
        side: THREE.DoubleSide,
        transparent: true,
        opacity: 0.6
      });
      const grass = new THREE.Mesh(grassGeometry, grassMaterial);
      grass.rotation.x = -Math.PI / 2;
      grass.position.y = -0.05;
      
      this.scene.add(grass);
    },

    createSkySections() {
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
        this.scene.add(line);
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
        this.scene.add(line);
      }
    },

    addBackgroundStars() {
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
      this.scene.add(stars);
    },

    addHorizonControls() {
      const canvas = this.renderer.domElement;
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
          
          this.camera.rotation.x = theta;
          this.camera.rotation.y = phi;
        }
      });
      
      canvas.addEventListener('mouseup', () => {
        isLooking = false;
      });
    },

    updateExoplanetMarkers() {
      // Limpiar marcadores existentes
      const markersToRemove = [];
      this.scene.traverse((child) => {
        if (child.userData && child.userData.isExoplanetMarker) {
          markersToRemove.push(child);
        }
      });
      markersToRemove.forEach(marker => this.scene.remove(marker));

      // Agregar nuevos marcadores
      this.detectedExoplanets.forEach(exoplanet => {
        this.addExoplanetMarker(exoplanet.direction, exoplanet.elevation, exoplanet.name);
      });
    },

    addExoplanetMarker(direction, elevation, name) {
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
      
      // Marcar como marcador de exoplaneta para poder eliminar después
      marker.userData = { 
        name, 
        originalScale: 1,
        isExoplanetMarker: true
      };
      marker.scale.setScalar(1);
      
      this.scene.add(marker);
      
      // Animación de pulsación
      this.addPulsationAnimation(marker);
    },

    addPulsationAnimation(marker) {
      const pulsate = () => {
        if (marker.parent) { // Solo animar si el marker aún está en la escena
          const time = Date.now() * 0.005;
          marker.scale.setScalar(1 + Math.sin(time) * 0.3);
          requestAnimationFrame(pulsate);
        }
      };
      pulsate();
    },

    focusOnExoplanet(exoplanet) {
      const phi = (exoplanet.direction * Math.PI) / 180;
      const theta = (exoplanet.elevation * Math.PI) / 180;
      
      // Animar la cámara hacia el exoplaneta
      this.camera.rotation.y = phi;
      this.camera.rotation.x = theta - Math.PI / 2;
      
      this.$emit('exoplanet-focused', exoplanet);
    },

    animate() {
      requestAnimationFrame(this.animate);
      if (this.renderer && this.scene && this.camera) {
        this.renderer.render(this.scene, this.camera);
      }
    }
  }
};
</script>

<style scoped>
.horizon-viewer-component {
  width: 100%;
  height: 100%;
}

.horizon-view {
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  width: 100%;
  height: 100%;
}
</style>