import Vue from 'vue'
import Vuex from 'vuex'

import books from './modules/books.js'
import categories from './modules/categories.js'
import cities from './modules/cities.js'
import exports from './modules/exports.js'
import historicalOccurrences from './modules/historical_occurrences.js'
import informants from './modules/informants.js'
import locations from './modules/locations.js'
import location_categories from './modules/location_categories.js'
import terms from './modules/terms.js'
import users from './modules/users.js'
import stats from './modules/stats.js'
import variants from './modules/variants.js'

Vue.use(Vuex)

export const store = new Vuex.Store({
  state: {
    barColor: 'rgba(0, 0, 0, .8), rgba(0, 0, 0, .8)',
    barImage: '/static/commun/sidebar-1.jpg',
    drawer: null,
  },
  mutations: {
    SET_BAR_IMAGE (state, payload) {
      state.barImage = payload
    },
    SET_DRAWER (state, payload) {
      state.drawer = payload
    },
  },
  actions: {
  },
  modules: {
    books,
    categories,
    cities,
    exports,
    historicalOccurrences,
    informants,
    locations,
    location_categories,
    terms,
    users,
    stats,
    variants,
  },
})
