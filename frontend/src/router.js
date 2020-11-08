import Vue from 'vue'
import Router from 'vue-router'
import GeoSearchFrontend from '@/components/GeoSearchFrontend.vue'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'GeoSearchFrontend',
      component: GeoSearchFrontend
    }
  ]
})
