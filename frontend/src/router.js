import Vue from 'vue'
import Router from 'vue-router'
import WebSearchEngineFrontend from '@/components/WebSearchEngineFrontend.vue'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'WebSearchEngineFrontend',
      component: WebSearchEngineFrontend
    }
  ]
})
