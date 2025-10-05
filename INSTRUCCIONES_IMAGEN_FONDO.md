# 📸 INSTRUCCIONES: Cómo Agregar Imagen de Fondo al HorizonViewer

## 🎯 Pasos para configurar imagen de fondo:

### 1. **Agregar tu imagen**
- Coloca tu imagen en la carpeta: `src/assets/`
- Formatos recomendados: `.jpg`, `.png`, `.webp`
- Resolución recomendada: 2048x1024px (panorámica)

### 2. **Actualizar el import**
En `HorizonViewer.vue`, línea 11:
```javascript
// Cambiar esta línea:
// import backgroundHorizonImage from '@/assets/tu-imagen-fondo.jpg';

// Por tu imagen real:
import backgroundHorizonImage from '@/assets/cielo-estrellado.jpg';
```

### 3. **Activar la imagen en el código**
En el método `createHorizonSphere()`, líneas 97-106:

**COMENTAR estas líneas (Opción 1):**
```javascript
// material = new THREE.MeshBasicMaterial({ 
//   color: 0x4169e1,
//   side: THREE.BackSide,
//   transparent: true,
//   opacity: 0.4
// });
```

**DESCOMENTAR estas líneas (Opción 2):**
```javascript
const textureLoader = new THREE.TextureLoader();
material = new THREE.MeshBasicMaterial({
  map: textureLoader.load(backgroundHorizonImage),
  side: THREE.BackSide,
  transparent: true,
  opacity: 0.8
});
```

### 4. **Imagen de fondo del contenedor (Opcional)**
En el CSS, línea 318:
```css
/* Descomentar y cambiar por tu imagen: */
background-image: url('@/assets/tu-imagen-fondo.jpg');
```

## 🎨 Tipos de imágenes recomendadas:
- **Panorámica espacial**: Cielo estrellado, nebulosas
- **Paisaje nocturno**: Horizontes con estrellas
- **Mapas estelares**: Constelaciones
- **Simulaciones astronómicas**: Vistas desde observatorios

## ✅ Resultado:
Tu vista de horizonte tendrá una imagen de fondo realista en lugar del color azul sólido.

## 🔧 Troubleshooting:
- Si la imagen no carga, verifica la ruta del import
- Si se ve distorsionada, ajusta el `opacity` (0.5 - 1.0)
- Para mejor rendimiento, usa imágenes optimizadas (&lt;2MB)