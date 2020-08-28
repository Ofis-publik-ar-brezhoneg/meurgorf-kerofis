import Vue from 'vue'

import doAsync from '../services/async-util'
import * as types from '../mutation-types'

const API_URL = '/api/books/'

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
	  console.log('success', info)
		state[types.POST_INFO_ASYNC.loadingKey] = false
		state[types.POST_INFO_ASYNC.stateKey] = true
	},

	[types.POST_INFO_ASYNC.PENDING] (state) {
		state[types.POST_INFO_ASYNC.loadingKey] = true
	},

	[types.POST_INFO_ASYNC.FAILURE] (state, info) {
	  console.log('failure', info)
	  state[types.POST_INFO_ASYNC.loadingKey] = false
	  Vue.set(state, [types.POST_INFO_ASYNC.stateKey], info)
	},
}

const actions = {
	getAllBooks(store, search) {
		return new Promise((resolve, reject) => {
      doAsync(store, {
        url: API_URL,
        mutationTypes: types.GET_INFO_ASYNC
      }, resolve, reject)
    })
	},
	getBook(store, book_id) {
	  return new Promise((resolve, reject) => {
      doAsync(store, {
        url: `${API_URL}${book_id}`,
        mutationTypes: types.GET_INFO_ASYNC
      }, resolve, reject)
    })
	},
	AddNewBook(store, book) {
    return new Promise((resolve, reject) => {
      doAsync(store, {
        method: 'post',
        url: API_URL,
        data: book,
        mutationTypes: types.POST_INFO_ASYNC
      }, resolve, reject)
    })
	},
	UpdateBook(store, { book_id, data }) {
    return new Promise((resolve, reject) => {
      doAsync(store, {
        method: 'put',
        url: `${API_URL}${book_id}`,
        data,
        mutationTypes: types.POST_INFO_ASYNC
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
