import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const routes = [{
  path: '/',
  name: 'home',
  meta: {
    title: 'Главная'
  },
  component: () => import('@/views/Home.vue').default
},
{
  path: '/login',
  name: 'Login',
  component: () => import('@/views/Login.vue'),
  meta: {
    layout: 'centered',
    title: 'Войти в сервис'
  }
}
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
