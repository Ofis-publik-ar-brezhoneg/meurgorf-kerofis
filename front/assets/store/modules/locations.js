import Vue from 'vue'

import doAsync from '../services/async-util'
import * as types from '../mutation-types'

const API_URL = '/api/locations/'

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
	searchLocations(store, { search, isAutoComplete=false, isForParent=false }) {
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
	getLocation(store, location_id) {
	  return new Promise((resolve, reject) => {
        doAsync(store, {
	        url: `${API_URL}${location_id}/`,
	        mutationTypes: types.GET_INFO_ASYNC
	      }, resolve)
    })
	},
	updateLocation(store, { location_id, data }) {
	  return new Promise((resolve, reject) => {
        doAsync(store, {
          method: 'patch',
          data,
	        url: `${API_URL}${location_id}/`,
	        mutationTypes: types.GET_INFO_ASYNC
	      }, resolve)
    })
	},
	deleteStandardizedForm(store, { standardized_form_id }) {
	  return new Promise((resolve, reject) => {
        doAsync(store, {
          method: 'delete',
	        url: `/api/standardized_forms/${standardized_form_id}/`,
	        mutationTypes: types.FP_INFO_ASYNC
	      }, resolve)
    })
	},
	deletePhoneticTranscription(store, { phonetic_transcription_id }) {
	  return new Promise((resolve, reject) => {
        doAsync(store, {
          method: 'delete',
	        url: `/api/phonetic_transcriptions/${phonetic_transcription_id}/`,
	        mutationTypes: types.FP_INFO_ASYNC
	      }, resolve)
    })
	},
	deleteOldForm(store, { old_form_id }) {
	  return new Promise((resolve, reject) => {
        doAsync(store, {
          method: 'delete',
	        url: `/api/old_forms/${old_form_id}/`,
	        mutationTypes: types.FP_INFO_ASYNC
	      }, resolve)
    })
	},
	deleteOtherForm(store, { other_form_id }) {
	  return new Promise((resolve, reject) => {
        doAsync(store, {
          method: 'delete',
	        url: `/api/other_forms/${other_form_id}/`,
	        mutationTypes: types.FP_INFO_ASYNC
	      }, resolve)
    })
	},
	deleteAttestedForm(store, { attested_form_id }) {
	  return new Promise((resolve, reject) => {
        doAsync(store, {
          method: 'delete',
	        url: `/api/attested_forms/${attested_form_id}/`,
	        mutationTypes: types.FP_INFO_ASYNC
	      }, resolve)
    })
	},
	reset(store) {
	  store.commit(types.GET_INFO_ASYNC.SUCCESS, {
	    id:	-1,
	  })
	},
}

export default {
  namespaced: true,
  state,
	mutations,
  actions
};
