import Vue from 'vue'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import locale from 'element-ui/lib/locale/lang/de'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import 'leaflet/dist/leaflet'
import VueWordCloud from 'vuewordcloud'
import App from './App.vue'
import './registerServiceWorker'
import router from './router'

Vue.component(VueWordCloud.name, VueWordCloud)
Vue.use(ElementUI, { locale })
Vue.config.productionTip = false

delete L.Icon.Default.prototype._getIconUrl

L.Icon.Default.mergeOptions({
  iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
  iconUrl: require('leaflet/dist/images/marker-icon.png'),
  shadowUrl: require('leaflet/dist/images/marker-shadow.png')
})

new Vue({
  router,
  render: (h) => h(App)
}).$mount('#app')
