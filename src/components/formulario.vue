<template>
  <form @submit.prevent="enviarFormulario" class="formulario-exoplaneta">
    <h2 class="titulo">🚀 Registro de Exoplaneta</h2>

    <div class="campos-grid">
      <div
          v-for="(tipo, key) in campos"
          :key="key"
          class="campo"
      >
        <label :for="key" class="label">{{ formatearEtiqueta(key) }}</label>
        <input
            :id="key"
            v-model="formulario[key]"
            :type="getTipoInput(tipo)"
            :step="getStep(tipo)"
            :placeholder="formatearEtiqueta(key)"
            :class="{ 'input-error': errores[key] }"
        />
        <small v-if="errores[key]" class="mensaje-error">{{ errores[key] }}</small>
      </div>
    </div>

    <button type="submit" class="boton">💾 Enviar</button>

    <transition name="fade">
      <div v-if="mensaje" class="mensaje" :class="{ exito: exito, error: !exito }">
        {{ mensaje }}
      </div>
    </transition>
  </form>
</template>

<script>
export default {
  name: 'ExoplanetForm',
  data() {
    return {
      formulario: {},
      mensaje: '',
      exito: false,
      errores: {},
      campos: {
        kepid: 'number',
        kepoi_name: 'string',
        koi_score: 'number',
        koi_fpflag_nt: 'number',
        koi_fpflag_ss: 'number',
        koi_fpflag_co: 'number',
        koi_fpflag_ec: 'number',
        koi_period: 'number',
        koi_depth: 'number',
        koi_prad: 'number',
        koi_teq: 'number',
        koi_tce_delivname: 'string',
        ra_str: 'string',
        dec_str: 'string',
        koi_kepmag: 'number'
      }
    };
  },
  mounted() {
    // Inicializar los valores vacíos según el tipo
    for (const [campo, tipo] of Object.entries(this.campos)) {
      this.formulario[campo] = tipo === 'number' ? null : '';
    }
  },
  methods: {
    getTipoInput(tipo) {
      return tipo === 'number' ? 'number' : 'text';
    },
    getStep(tipo) {
      return tipo === 'number' ? 'any' : undefined;
    },
    formatearEtiqueta(key) {
      return key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
    },
    validarFormulario() {
      this.errores = {};
      for (const [key, tipo] of Object.entries(this.campos)) {
        const valor = this.formulario[key];
        if (tipo === 'number' && (valor === null || valor === '' || isNaN(valor))) {
          this.errores[key] = 'Debe ingresar un número válido';
        }
        if (tipo === 'string' && (!valor || valor.trim() === '')) {
          this.errores[key] = 'Este campo es obligatorio';
        }
      }
      return Object.keys(this.errores).length === 0;
    },
    async enviarFormulario() {
      if (!this.validarFormulario()) {
        this.mensaje = 'Corrige los errores antes de enviar.';
        this.exito = false;
        return;
      }

      try {
        const respuesta = await fetch('http://0.0.0.0/api/form', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(this.formulario)
        });

        if (respuesta.ok) {
          this.mensaje = '✅ ¡Formulario enviado correctamente!';
          this.exito = true;
          this.formulario = Object.fromEntries(Object.entries(this.campos).map(([k, t]) => [k, t === 'number' ? null : '']));
        } else {
          this.mensaje = '⚠️ Error al enviar el formulario.';
          this.exito = false;
        }
      } catch (e) {
        this.mensaje = '❌ Error de red o servidor.';
        this.exito = false;
      }
    }
  }
};
</script>

<style scoped>
.formulario-exoplaneta {
  background: linear-gradient(180deg, #001a33, #000814);
  color: #fff;
  border-radius: 16px;
  padding: 24px;
  max-width: 700px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 20px;
  box-shadow: 0 0 20px rgba(0, 255, 136, 0.2);
  animation: fadeIn 0.6s ease-in;
}

.titulo {
  text-align: center;
  color: #00ff88;
  font-size: 1.6rem;
  font-weight: bold;
}

.campos-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 16px;
}

.campo {
  display: flex;
  flex-direction: column;
}

.label {
  font-weight: bold;
  margin-bottom: 6px;
  color: #a8d0e6;
}

input {
  padding: 8px;
  border-radius: 6px;
  border: 1px solid #2a9df4;
  background: #002b5b;
  color: white;
  transition: border-color 0.3s;
}

input:focus {
  border-color: #00ff88;
  outline: none;
}

.input-error {
  border-color: #ff5555 !important;
}

.mensaje-error {
  color: #ff7777;
  font-size: 0.8rem;
  margin-top: 4px;
}

.boton {
  align-self: center;
  background: #00ff88;
  color: #001122;
  border: none;
  border-radius: 10px;
  padding: 10px 30px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s;
}

.boton:hover {
  background: #00cc6a;
}

.mensaje {
  text-align: center;
  font-weight: bold;
  padding: 10px;
  border-radius: 8px;
}

.exito {
  background: rgba(0, 255, 136, 0.15);
  color: #00ff88;
}

.error {
  background: rgba(255, 85, 85, 0.15);
  color: #ff5555;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.4s;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
