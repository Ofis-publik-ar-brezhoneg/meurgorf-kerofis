import Vue from 'vue'

import doAsync from '../services/async-util'
import * as types from '../mutation-types'

const API_URL = '/api/categories/'

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

	[types.POST_INFO_ASYNC.SUCCESS] (state, info) {
		state[types.POST_INFO_ASYNC.loadingKey] = false
		state[types.POST_INFO_ASYNC.stateKey] = true
	},

	[types.POST_INFO_ASYNC.PENDING] (state) {
		state[types.POST_INFO_ASYNC.loadingKey] = true
	},

	[types.POST_INFO_ASYNC.FAILURE] (state) {
	  state[types.POST_INFO_ASYNC.loadingKey] = false
	  state[types.POST_INFO_ASYNC.stateKey] = false
	},
}

const actions = {
	getAllCategories(store, search) {
		return new Promise((resolve, reject) => {
        doAsync(store, {
	        url: API_URL,
	        mutationTypes: types.GET_INFO_ASYNC
	      }, resolve)
      }, 1000)
	},
	AddNewBook(store, book) {
    return new Promise((resolve, reject) => {
      doAsync(store, {
        method: 'post',
        url: API_URL,
        data: book,
        mutationTypes: types.POST_INFO_ASYNC
      }, resolve)
    }, 1000)
	}
}

export default {
  namespaced: true,
  state,
	mutations,
  actions
};
