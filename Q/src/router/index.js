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
        path: '/tagShelf',
        name: 'TagShelf',
        component: () => import('../views/TagShelf.vue')
      },
      {
        path: '/tag',
        name: 'Tag',
        component: () => import('../views/Tag.vue')
      },
      {
        path: '/collectionShelf',
        name: 'CollectionShelf',
        component: () => import('../views/CollectionShelf.vue')
      },
      {
        path: '/collection',
        name: 'Collection',
        component: () => import('../views/Collection.vue')
      },
      {
        path: '/first',
        name: 'First',
        component: () => import('../views/First.vue')
      },
    ]
  },
  {
    path: '/article',
    name: 'Article',
    component: () => import('../views/Article.vue')
  },
  {
    path: '/editArticle',
    name: 'EditArticle',
    component: () => import('../views/EditArticle.vue')
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
