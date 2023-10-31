import { createStore } from 'vuex'

export default createStore({
  state: {
    user: {
        username: ''
    }
  },
  getters: {
  },
  mutations: {
    initializeStore(state) {
        if(localStorage.getItem('token')) {
            state.token = localStorage.getItem('token')
            state.isAuthenticated = true
        } else {
        state.token = ''
        state.isAuthenticated = false
        }
    },
    setToken(state, token) {
        state.token = token
        state.isAuthenticated = true
    }
  },
  actions: {
  },
  modules: {
  }
})
