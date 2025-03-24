// Composables
import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/', name: 'Home', component: () => import('@/views/Home.vue'), meta:{ transition: 'fade'} },
  { path: '/broadcast', name: 'Station', component: () => import('@/views/Station.vue'), meta:{ transition: 'fade'} },
  { path: '/graphs', name: 'Graphs', component: () => import('@/views/Graphs.vue'), meta:{ transition: 'fade'} },
  { path: '/backcast', name: 'Backcast', component: () => import('@/views/Backcast.vue'), meta:{ transition: 'fade'} }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
})

export default router
