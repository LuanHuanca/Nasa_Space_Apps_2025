<template>
  <div class="pagina-exoplaneta">
    <!-- Fondo animado -->
    <div class="fondo-espacial"></div>

    <!-- Contenedor principal -->
    <section class="contenedor">
      <header class="encabezado">
        <button class="boton-volver" @click="volverInicio">⬅ Volver</button>
        <h1>🌌 Observador de Exoplanetas</h1>
        <p class="descripcion">
          Registra los datos de un exoplaneta detectado y contribuye a la base del Observatorio Interestelar.
        </p>
      </header>

      <!-- Botón para abrir modal -->
      <div class="acciones">
        <button class="boton" @click="abrirModal = true">🪐 Nuevo Registro</button>
      </div>

      <!-- Modal -->
      <transition name="modal-fade">
        <div v-if="abrirModal" class="modal-fondo" @click.self="cerrarModal">
          <div class="modal-contenido">
            <button class="cerrar" @click="cerrarModal">✖</button>
            <ExoplanetForm />
          </div>
        </div>
      </transition>
    </section>
  </div>
</template>

<script>
import ExoplanetForm from '@/components/formulario.vue';

export default {
  name: 'ExoplanetPage',
  components: { ExoplanetForm },
  data() {
    return {
      abrirModal: false
    };
  },
  methods: {
    volverInicio() {
      this.$router.push('/earth/exoplanet-observer');
    },
    cerrarModal() {
      this.abrirModal = false;
    }
  }
};
</script>

<style scoped>
/* --- Fondo general --- */
.pagina-exoplaneta {
  position: relative;
  min-height: 100vh;
  overflow: hidden;
  color: white;
  font-family: 'Orbitron', sans-serif;
  background: radial-gradient(circle at 20% 20%, #001a33, #000814 80%);
}

.fondo-espacial {
  position: absolute;
  width: 100%;
  height: 100%;
  background: url('https://www.transparenttextures.com/patterns/stardust.png');
  animation: moverEstrellas 60s linear infinite;
  opacity: 0.4;
}

@keyframes moverEstrellas {
  from { background-position: 0 0; }
  to { background-position: 10000px 10000px; }
}

/* --- Contenedor principal --- */
.contenedor {
  position: relative;
  z-index: 2;
  max-width: 900px;
  margin: 0 auto;
  padding: 60px 20px;
  text-align: center;
}

/* --- Encabezado --- */
.encabezado h1 {
  font-size: 2.2rem;
  color: #00ff88;
  margin-bottom: 0.5rem;
}
.descripcion {
  color: #b0d9ff;
  font-size: 1rem;
  max-width: 600px;
  margin: 0 auto;
}

/* --- Botones --- */
.boton, .boton-volver {
  padding: 10px 20px;
  border-radius: 8px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s;
}

.boton {
  background: #00ff88;
  color: #001122;
  border: none;
}
.boton:hover {
  background: #00cc6a;
}

.boton-volver {
  background: transparent;
  color: #00ff88;
  border: 1px solid #00ff88;
  position: absolute;
  left: 20px;
  top: 20px;
}
.boton-volver:hover {
  background: rgba(0, 255, 136, 0.1);
}

/* --- Modal --- */
.modal-fondo {
  position: fixed;
  inset: 0;
  background: rgba(0, 8, 20, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  backdrop-filter: blur(8px);
  z-index: 100;
}

.modal-contenido {
  background: #001122;
  border: 1px solid #00ff88;
  border-radius: 12px;
  padding: 20px;
  width: 90%;
  max-width: 650px;
  box-shadow: 0 0 25px rgba(0, 255, 136, 0.3);
  position: relative;
}

.cerrar {
  position: absolute;
  right: 12px;
  top: 12px;
  background: transparent;
  color: #00ff88;
  border: none;
  font-size: 1.4rem;
  cursor: pointer;
  transition: color 0.3s;
}
.cerrar:hover {
  color: #ff5555;
}

/* --- Transiciones --- */
.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: opacity 0.4s;
}
.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
}
</style>
