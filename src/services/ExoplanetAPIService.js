// Servicio para conectar con la API de exoplanetas
class ExoplanetAPIService {
  constructor(baseURL = 'http://localhost:8000') {
    this.baseURL = baseURL;
  }
  async getConfirmedExoplanets(limit = 50) {
    try {
      const response = await fetch(`${this.baseURL}/api/coordenadas-confirmadas?limit=${limit}`);
      
      if (!response.ok) {
        throw new Error(`Error HTTP: ${response.status}`);
      }
      
      const data = await response.json();
      
      // Transformar datos de la API al formato esperado por tu aplicación
      return data.map(exoplanet => ({
        name: exoplanet.kepoi_name,
        ra: exoplanet.ra,
        dec: exoplanet.dec,
        coordinates: {
          x: exoplanet.X,
          y: exoplanet.Y,
          z: exoplanet.Z
        },
        // Simular datos adicionales para compatibilidad
        distance: this.calculateSimulatedDistance(exoplanet.X, exoplanet.Y, exoplanet.Z),
        habitability: this.calculateHabitabilityScore(exoplanet.kepoi_name),
        baseDirection: this.raToAzimuth(exoplanet.ra),
        baseElevation: this.decToElevation(exoplanet.dec)
      }));
      console.log('Si regresaron los datos');
    } catch (error) {
      console.error('Error al obtener exoplanetas:', error);
      return [];
    }
  }

  /**
   * Obtiene coordenadas para partículas de estrellas (específico para home.vue)
   * @param {number} limit - Número máximo de coordenadas
   * @returns {Promise<Array>} Array de vertices para Three.js
   */
  async getStarParticleCoordinates(limit = 1000) {
    try {
      const response = await fetch(`${this.baseURL}/api/coordenadas-confirmadas?limit=${limit}`);
      
      if (!response.ok) {
        throw new Error(`Error HTTP: ${response.status}`);
      }
      
      const data = await response.json();
      
      if (!Array.isArray(data) || data.length === 0) {
        throw new Error('Datos inválidos recibidos de la API');
      }

      // Transformar coordenadas para Three.js
      const vertices = [];
      const scaleFactor = 100; // Factor de escala para visualización

      data.forEach(exoplanet => {
        if (typeof exoplanet.X === 'number' && 
            typeof exoplanet.Y === 'number' && 
            typeof exoplanet.Z === 'number') {
          
          const x = exoplanet.X * scaleFactor;
          const y = exoplanet.Y * scaleFactor;
          const z = exoplanet.Z * scaleFactor;
          
          // Validar que las coordenadas estén en un rango razonable
          if (Math.abs(x) < 2000 && Math.abs(y) < 2000 && Math.abs(z) < 2000) {
            vertices.push(x, y, z);
          }
        }
      });

      console.log(`✅ Coordenadas de estrellas obtenidas: ${vertices.length / 3} partículas`);
      return vertices;

    } catch (error) {
      console.error('❌ Error al obtener coordenadas de estrellas:', error);
      return this.generateFallbackStarCoordinates();
    }
  }

  /**
   * Genera coordenadas de respaldo para partículas de estrellas
   * @returns {Array} Array de vertices de respaldo
   */
  generateFallbackStarCoordinates() {
    console.warn('🔄 Usando coordenadas de respaldo para estrellas');
    
    const vertices = [];
    const starCount = 800; // Número de partículas de respaldo
    
    for (let i = 0; i < starCount; i++) {
      const x = 2000 * Math.random() - 1000;
      const y = 2000 * Math.random() - 1000;
      const z = 2000 * Math.random() - 1000;
      
      vertices.push(x, y, z);
    }
    
    return vertices;
  }

  /**
   * Obtiene candidatos con predicción ML
   * @param {number} limit - Número de candidatos
   * @returns {Promise<Array>} Lista de candidatos con ML
   */
  async getCandidatesWithML(limit = 20) {
    try {
      const response = await fetch(`${this.baseURL}/api/exoplanetas-candidatos-ml?limit=${limit}`);
      
      if (!response.ok) {
        throw new Error(`Error HTTP: ${response.status}`);
      }
      
      const data = await response.json();
      
      return data.map(candidate => ({
        name: candidate.kepoi_name,
        kepid: candidate.kepid,
        coordinates: {
          x: candidate.X,
          y: candidate.Y,
          z: candidate.Z
        },
        mlPrediction: candidate.ml_result,
        // Transformar a formato compatible
        distance: this.calculateSimulatedDistance(candidate.X, candidate.Y, candidate.Z),
        habitability: this.mlPredictionToHabitability(candidate.ml_result),
        baseDirection: Math.random() * 360,
        baseElevation: Math.random() * 90
      }));
    } catch (error) {
      console.error('Error al obtener candidatos ML:', error);
      return [];
    }
  }

  // Funciones auxiliares para transformar datos
  calculateSimulatedDistance(x, y, z) {
    // Simular distancia basada en coordenadas (en años luz)
    const magnitude = Math.sqrt(x*x + y*y + z*z);
    return Math.round((1 / magnitude) * 1000 + Math.random() * 500);
  }

  calculateHabitabilityScore(name) {
    // Simular puntuación de habitabilidad basada en el nombre
    const hash = name.split('').reduce((a, b) => a + b.charCodeAt(0), 0);
    return Math.round((hash % 100) * 0.4 + 40); // Entre 40-80%
  }

  raToAzimuth(ra) {
    // Convertir ascensión recta a azimuth aproximado
    return ra % 360;
  }

  decToElevation(dec) {
    // Convertir declinación a elevación aproximada
    return Math.max(5, Math.min(85, dec + 45));
  }

  mlPredictionToHabitability(mlResult) {
    // Convertir predicción ML a habitabilidad
    if (mlResult.prediction === 'Candidate') {
      return Math.round((mlResult.probability || 0.5) * 100);
    }
    return Math.round(20 + Math.random() * 30); // 20-50% para falsos positivos
  }
}

// Exportar la clase con nombre y como default
export { ExoplanetAPIService };
export default ExoplanetAPIService;