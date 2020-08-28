import Vue from 'vue'

import doAsync from '../services/async-util'
import * as types from '../mutation-types'

const state = {
	info: {},
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
	  Vue.set(state, [types.GET_INFO_ASYNC.stateKey], {id: 0})
	}
}

const actions = {
	getCurrentUser(store, search) {
	  var url = '/api/users/me'
		return new Promise((resolve, reject) => {
        doAsync(store, {
	        url: url,
	        mutationTypes: types.GET_INFO_ASYNC
	      }, resolve)
      }, 1000)
	},
}

export default {
  namespaced: true,
  state,
	mutations,
  actions
};
