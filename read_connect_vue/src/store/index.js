import { createStore } from 'vuex'

export default createStore({
  state: {
    user: {
        username: ''
    },
    isAuthenticated: false, // Add a isAuthenticated property
    token: '' // Add a token property
  },
  mutations: {
    initializeStore(state) {
        if (localStorage.getItem('token')) {
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
