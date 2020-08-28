import axios from 'axios'

const doAsync = (store, { method='get', url, data=false, mutationTypes, stateKey }, on_success, on_failure) => {
	store.commit(mutationTypes.PENDING)
  axios({method, url, data})
    .then(response => {
      store.commit(mutationTypes.SUCCESS, response.data)
      if(on_success) on_success();
    })
    .catch(error => {
      store.commit(mutationTypes.FAILURE, error.response ? error.response.data : null)
      if(on_failure) on_failure();
    })
}

export default doAsync
