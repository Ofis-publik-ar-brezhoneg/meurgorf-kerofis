import Vue from 'vue'
import axios from 'axios'
import Meta from 'vue-meta'
import VueCsrf from 'vue-csrf'
import router from './router'
import { store } from './store'
import Main from './Main.vue'
import i18n from './i18n'
import VueClipboard from 'vue-clipboard2'

import vuetify from './plugins/vuetify'
import './plugins/base'

// Axios csrf settings
axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = 'X-CSRFToken'

Vue.use(Meta)
Vue.use(VueCsrf)
Vue.use(VueClipboard)

Vue.prototype.$static_url = '/static/commun/'

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  vuetify,
  i18n,
  render: h => h(Main),
})
