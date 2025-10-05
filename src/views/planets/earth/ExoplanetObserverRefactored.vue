<template>
  <div id="exoplanet-observer">
    <!-- Indicador de carga -->
    <LoadingIndicator 
      :is-loading="isLoadingExoplanets"
      :error="apiError"
      :loading-title="currentStep === 1 ? 'Cargando Base de Datos de Exoplanetas...' : 'Calculando Exoplanetas Visibles...'"
      :loading-message="currentStep === 1 ? 'Descargando datos de NASA/Kepler Observatory' : `Analizando visibilidad desde ${selectedLocation?.lat?.toFixed(2) || 0}°, ${selectedLocation?.lng?.toFixed(2) || 0}°`"
      @retry="loadExoplanetData"
    />

    <!-- Header Component -->
    <HeaderComponent 
      :selected-location="selectedLocation"
      @go-back="goBack"
    />

    <!-- Paso 1: Selección de ubicación en el mapa -->
    <LocationSelector
      v-if="currentStep === 1"
      :selected-location="selectedLocation"
      @location-selected="handleLocationSelected"
      @location-confirmed="confirmLocation"
    />

    <!-- Paso 2: Vista de horizonte 360° -->
    <HorizonViewStep
      v-if="currentStep === 2"
      :selected-location="selectedLocation"
      :detected-exoplanets="detectedExoplanets"
      @go-back-to-map="goBackToMap"
      @refresh-exoplanets="refreshExoplanets"
      @exoplanet-focused="handleExoplanetFocused"
    />
  </div>
</template>

<script>
// Importar componentes
import HeaderComponent from '@/components/exoplanet/HeaderComponent.vue';
import LocationSelector from '@/components/exoplanet/LocationSelector.vue';
import HorizonViewStep from '@/components/exoplanet/HorizonViewStep.vue';
import LoadingIndicator from '@/components/exoplanet/LoadingIndicator.vue';
// Importar servicio API
import ExoplanetAPIService from '@/services/ExoplanetAPIService.js';

export default {
  name: 'ExoplanetObserver',
  components: {
    HeaderComponent,
    LocationSelector,
    HorizonViewStep,
    LoadingIndicator
  },
  data() {
    return {
      currentStep: 1,
      selectedLocation: null,
      detectedExoplanets: [],
      isLoadingExoplanets: false,
      apiError: null,
      
      // Servicio API
      exoplanetAPI: new ExoplanetAPIService(),
      
      // Cache de exoplanetas descargados
      confirmedExoplanets: [],
      candidateExoplanets: [],
      
      // Base de datos de respaldo (fallback)
      fallbackExoplanets: [
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
  async mounted() {
    // Cargar datos de exoplanetas al iniciar
    await this.loadExoplanetData();
  },
  methods: {
    // 🌐 Métodos de carga de datos API
    async loadExoplanetData() {
      this.isLoadingExoplanets = true;
      this.apiError = null;
      
      try {
        console.log('🔄 Cargando datos de exoplanetas desde la API...');
        
        // Cargar datos confirmados y candidatos en paralelo
        const [confirmed, candidates] = await Promise.all([
          this.exoplanetAPI.getConfirmedExoplanets(100),
          this.exoplanetAPI.getCandidatesWithML(50)
        ]);
        
        this.confirmedExoplanets = confirmed;
        this.candidateExoplanets = candidates;
        
        console.log(`✅ Cargados ${confirmed.length} exoplanetas confirmados y ${candidates.length} candidatos`);
        
      } catch (error) {
        console.error('❌ Error al cargar datos de exoplanetas:', error);
        this.apiError = 'No se pudieron cargar los datos de exoplanetas. Usando datos de respaldo.';
        
        // Usar datos de respaldo
        this.confirmedExoplanets = this.fallbackExoplanets;
        this.candidateExoplanets = [];
      } finally {
        this.isLoadingExoplanets = false;
      }
    },
    
    // 🎯 Obtener base de datos combinada para cálculos
    getExoplanetDatabase() {
      // Combinar confirmados y candidatos, priorizando confirmados
      const combined = [
        ...this.confirmedExoplanets,
        ...this.candidateExoplanets.filter(candidate => 
          candidate.mlPrediction?.prediction === 'Candidate'
        )
      ];
      
      // Si no hay datos de API, usar fallback
      return combined.length > 0 ? combined : this.fallbackExoplanets;
    },

    // Navegación
    goBack() {
      this.$router.push('/planets/tierra');
    },

    // Manejo de eventos del LocationSelector
    handleLocationSelected(location) {
      this.selectedLocation = location;
    },

    async confirmLocation() {
      this.currentStep = 2;
      this.$nextTick(async () => {
        await this.calculateVisibleExoplanets();
      });
    },

    // Manejo de eventos del HorizonViewStep
    async goBackToMap() {
      this.currentStep = 1;
      this.selectedLocation = null;
      this.detectedExoplanets = [];
    },

    async refreshExoplanets() {
      // Recargar datos de la API y recalcular
      await this.loadExoplanetData();
      await this.calculateVisibleExoplanets();
    },

    handleExoplanetFocused(exoplanet) {
      // Mostrar información adicional del exoplaneta enfocado
      this.showExoplanetInfo(exoplanet);
    },

    // 🔭 Lógica de cálculo de exoplanetas mejorada
    async calculateVisibleExoplanets() {
      this.isLoadingExoplanets = true;
      this.detectedExoplanets = [];
      
      if (!this.selectedLocation) return;
      
      const { lat, lng } = this.selectedLocation;
      const exoplanetDatabase = this.getExoplanetDatabase();
      
      console.log(`🔭 Calculando exoplanetas visibles desde ${lat.toFixed(2)}°, ${lng.toFixed(2)}°`);
      console.log(`📊 Base de datos: ${exoplanetDatabase.length} exoplanetas disponibles`);
      
      // Simular tiempo de cálculo astronómico
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      exoplanetDatabase.forEach(exoplanet => {
        // Algoritmo mejorado de visibilidad
        const latFactor = Math.sin((lat * Math.PI) / 180);
        const lngFactor = Math.cos((lng * Math.PI) / 180);
        
        // Factores de visibilidad más realistas
        let visibilityChance = 0.4; // Base 40%
        
        // Incrementar probabilidad para exoplanetas confirmados
        if (this.confirmedExoplanets.includes(exoplanet)) {
          visibilityChance += 0.3;
        }
        
        // Considerar habitabilidad
        if (exoplanet.habitability > 70) {
          visibilityChance += 0.2;
        }
        
        // Considerar predicción ML si existe
        if (exoplanet.mlPrediction?.prediction === 'Candidate') {
          visibilityChance += (exoplanet.mlPrediction.probability || 0.5) * 0.3;
        }
        
        const isVisible = Math.random() < visibilityChance;
        
        if (isVisible) {
          const direction = (exoplanet.baseDirection + lng + Math.random() * 60 - 30) % 360;
          const elevation = Math.max(5, Math.min(85, 
            exoplanet.baseElevation + latFactor * 30 + Math.random() * 20 - 10
          ));
          
          this.detectedExoplanets.push({
            ...exoplanet,
            direction: Math.round(direction),
            elevation: Math.round(elevation),
            source: this.confirmedExoplanets.includes(exoplanet) ? 'confirmed' : 'candidate'
          });
        }
      });
      
      console.log(`✅ ${this.detectedExoplanets.length} exoplanetas visibles detectados`);
      this.isLoadingExoplanets = false;
    },

    // Utilidades
    showExoplanetInfo(exoplanet) {
      const source = exoplanet.source === 'confirmed' ? 'Confirmado' : 'Candidato';
      const mlInfo = exoplanet.mlPrediction ? 
        `\nPredicción ML: ${exoplanet.mlPrediction.prediction} (${(exoplanet.mlPrediction.probability * 100).toFixed(1)}%)` : '';
      
      alert(`🌟 ${exoplanet.name}\n` +
        `📍 Dirección: ${exoplanet.direction}°\n` +
        `📐 Elevación: ${exoplanet.elevation}°\n` +
        `📏 Distancia: ${exoplanet.distance} años luz\n` +
        `🌱 Habitabilidad: ${exoplanet.habitability}%\n` +
        `🔬 Fuente: ${source}${mlInfo}`);
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
</style>