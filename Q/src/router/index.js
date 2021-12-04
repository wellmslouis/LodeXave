import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    children:[
      {
        path: '/autoImport',
        name: 'AutoImport',
        component: () => import('../views/AutoImport.vue')
      },
      {
        path: '/manualImport',
        name: 'ManualImport',
        component: () => import('../views/ManualImport.vue')
      },
      {
        path: '/shelf',
        name: 'Shelf',
        component: () => import('../views/Shelf.vue')
      },
      {
        path: '/first',
        name: 'First',
        component: () => import('../views/First.vue')
      },
    ]
  },
  
  {
    path: '/about',
    name: 'About',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
