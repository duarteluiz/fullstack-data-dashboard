import { createRouter, createWebHistory } from 'vue-router'
import ProductsView from './views/ProductsView.vue'
import UsersView from './views/UsersView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', redirect: '/users' },
    { path: '/users', component: UsersView },
    { path: '/products', component: ProductsView },
  ],
})

export default router
