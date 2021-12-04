import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
Vue.use(ElementUI);

import VueAxios from 'vue-axios'
Vue.use(VueAxios,axios)

import axios from "axios";
Vue.prototype.$axios = axios;
axios.defaults.baseURL = 'http://127.0.0.1:8000/'

Vue.config.productionTip = false

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
