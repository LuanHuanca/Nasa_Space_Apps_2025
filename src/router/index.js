import { createRouter, createWebHistory } from 'vue-router';
import Home from '@/views/home.vue'; 
import Earth from '@/views/planets/earth/earth.vue'; 
import Menu from '@/views/menu.vue'; 
import Jupiter from "@/views/planets/jupiter/jupiter.vue";
import Mars from "@/views/planets/mars/mars.vue";
import Mercury from "@/views/planets/mercury/mercury.vue";
import Neptune from "@/views/planets/neptune/neptune.vue";
import Saturn from "@/views/planets/saturn/saturn.vue";
import Uranus from "@/views/planets/uranus/uranus.vue";
import Venus from "@/views/planets/venus/venus.vue";

const routes = [
  { path: '/', component: Menu }, // Página principal con el mapa del sistema solar
  { path: '/planets/Tierra', component: Earth }, // Ruta para la página de la Tierra
  { path: '/home', component: Home }, // Página del Home (anteriormente principal)
  { path: '/planets/Júpiter', component: Jupiter }, // Ruta para la página de Júpiter
  { path: '/planets/Marte', component: Mars }, // Ruta para la página de Marte
  { path: '/planets/Mercurio', component: Mercury }, // Ruta para la página de Mercurio
  { path: '/planets/Neptuno', component: Neptune }, // Ruta para la página de Neptuno
  { path: '/planets/Saturno', component: Saturn }, // Ruta para la página de Saturno
  { path: '/planets/Urano', component: Uranus }, // Ruta para la página de Urano
  { path: '/planets/Venus', component: Venus }, // Ruta para la página de Venus
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
