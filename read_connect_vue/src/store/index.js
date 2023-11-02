import { createStore } from 'vuex'

export default createStore({
  state: {
    user: {
      username: ''
      // Add other user-related properties here
    },
    isAuthenticated: false,
    token: ''
  },
  mutations: {
    initializeStore(state) {
      if (localStorage.getItem('token')) {
        state.token = localStorage.getItem('token');
        state.isAuthenticated = true;
      } else {
        state.token = '';
        state.isAuthenticated = false;
      }
    },
    setToken(state, token) {
      state.token = token;
      state.isAuthenticated = true;
      // You can also decode the token to get user information and set it in the state.
      // Example:
      // state.user.username = decodedToken.username;
    },
    // Mutation to update user information
    updateUser(state, userData) {
      state.user = { ...state.user, ...userData };
    },
  },
  actions: {
    // Action to update user information
    updateUser({ commit }, userData) {
      commit('updateUser', userData);
    },
  },
  modules: {}
})

