import Vue from 'vue'

import doAsync from '../services/async-util'
import * as types from '../mutation-types'

const API_URL = '/api/terms/'

const state = {
  isAutoComplete: true,
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
//		state[types.POST_INFO_ASYNC.loadingKey] = false
//		state[types.POST_INFO_ASYNC.stateKey] = true
		state[types.POST_INFO_ASYNC.loadingKey] = false
		Vue.set(state, [types.POST_INFO_ASYNC.stateKey], info)
	},

	[types.POST_INFO_ASYNC.PENDING] (state) {
		state[types.POST_INFO_ASYNC.loadingKey] = true
	},

	[types.POST_INFO_ASYNC.FAILURE] (state) {
	  state[types.POST_INFO_ASYNC.loadingKey] = false
	  state[types.POST_INFO_ASYNC.stateKey] = false
	},

	[types.FP_INFO_ASYNC.SUCCESS] (state, info) {
//		state[types.POST_INFO_ASYNC.loadingKey] = false
//		state[types.POST_INFO_ASYNC.stateKey] = true
		state[types.FP_INFO_ASYNC.loadingKey] = false
		Vue.set(state, [types.FP_INFO_ASYNC.stateKey], info)
	},

	[types.FP_INFO_ASYNC.PENDING] (state) {
		state[types.FP_INFO_ASYNC.loadingKey] = true
	},

	[types.FP_INFO_ASYNC.FAILURE] (state) {
	  state[types.FP_INFO_ASYNC.loadingKey] = false
	  state[types.FP_INFO_ASYNC.stateKey] = false
	},
}

const actions = {
	searchTerms(store, { search, isAutoComplete=false, isForParent=false }) {
		return new Promise((resolve, reject) => {
      doAsync(store, {
        url: `${API_URL}?${search}`,
        mutationTypes: !isForParent ? types.GET_INFO_ASYNC : types.FP_INFO_ASYNC
      }, () => {
	      store.state.isAutoComplete = isAutoComplete
        resolve()
      })
    })
	},
	addNewTerm(store, data) {
    return new Promise((resolve, reject) => {
      doAsync(store, {
        method: 'post',
        url: API_URL,
        data,
        mutationTypes: types.POST_INFO_ASYNC
      }, resolve)
    })
	},
	getTerm(store, term_id) {
	  return new Promise((resolve, reject) => {
        doAsync(store, {
	        url: `${API_URL}${term_id}/`,
	        mutationTypes: types.GET_INFO_ASYNC
	      }, resolve)
    })
	},
	deleteTerm(store, term_id) {
	  return new Promise((resolve, reject) => {
        doAsync(store, {
          method: 'delete',
	        url: `${API_URL}${term_id}/`,
	        mutationTypes: types.GET_INFO_ASYNC
	      }, resolve)
    })
	},
	updateTerm(store, { term_id, data }) {
	  return new Promise((resolve, reject) => {
        doAsync(store, {
          method: 'patch',
          data,
	        url: `${API_URL}${term_id}/`,
	        mutationTypes: types.GET_INFO_ASYNC
	      }, resolve)
    })
	},
	deleteVariant(store, { variant_id }) {
	  return new Promise((resolve, reject) => {
        doAsync(store, {
          method: 'delete',
	        url: `/api/variants/${variant_id}/`,
	        mutationTypes: types.GET_INFO_ASYNC
	      }, resolve)
    })
	},
	reset(store) {
	  store.commit(types.GET_INFO_ASYNC.SUCCESS, {
	    id:	-1,
	    grammatical_category: {
	      title: ''
	    },
	  })
	},
}

export default {
  namespaced: true,
  state,
	mutations,
  actions
};
