import Vue from 'vue'

import doAsync from '../services/async-util'
import * as types from '../mutation-types'

const API_URL = '/api/cities/'

const state = {
}

const mutations = {
	[types.GET_INFO_ASYNC.SUCCESS] (state, info) {
		state[types.GET_INFO_ASYNC.loadingKey] = false
		Vue.set(state, [types.GET_INFO_ASYNC.stateKey], info)
	},

	[types.GET_INFO_ASYNC.PENDING] (state) {
		Vue.set(state, types.GET_INFO_ASYNC.loadingKey, true)
	},

	[types.GET_INFO_ASYNC.FAILURE] (state) {
	  state[types.GET_INFO_ASYNC.loadingKey] = false
	  Vue.set(state, [types.GET_INFO_ASYNC.stateKey], [])
	},
}

const actions = {
	getAllCities(store, search) {
		return new Promise((resolve, reject) => {
      doAsync(store, {
        url: API_URL,
        mutationTypes: types.GET_INFO_ASYNC
      }, resolve, reject)
    })
	}
}

export default {
  namespaced: true,
  state,
	mutations,
  actions
};
