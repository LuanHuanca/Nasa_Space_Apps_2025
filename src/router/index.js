import { createRouter, createWebHistory } from 'vue-router';
import Home from '@/views/home.vue'; 
import Earth from '@/views/planets/earth/earth.vue'; 
import ExoplanetObserver from '@/views/planets/earth/ExoplanetObserver.vue';
import Jupiter from "@/views/planets/jupiter/jupiter.vue";
import Mars from "@/views/planets/mars/mars.vue";
import Mercury from "@/views/planets/mercury/mercury.vue";
import Neptune from "@/views/planets/neptune/neptune.vue";
import Saturn from "@/views/planets/saturn/saturn.vue";
import Uranus from "@/views/planets/uranus/uranus.vue";
import Venus from "@/views/planets/venus/venus.vue";

const routes = [
  { path: '/', component: Home }, 
  { path: '/planets/Tierra', component: Earth }, 
  { path: '/earth/exoplanet-observer', component: ExoplanetObserver },
  { path: '/planets/Júpiter', component: Jupiter }, 
  { path: '/planets/Marte', component: Mars }, 
  { path: '/planets/Mercurio', component: Mercury }, 
  { path: '/planets/Neptuno', component: Neptune }, 
  { path: '/planets/Saturno', component: Saturn }, 
  { path: '/planets/Urano', component: Uranus }, 
  { path: '/planets/Venus', component: Venus }, 
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
