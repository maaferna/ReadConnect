<template>
  <div class="page-login">
    <!-- Login -->
    <div class="container border p-3 mb-3 bg-light text-dark">
      <h1>Login</h1>
    </div>
    <div class="container border p-3 mb-3 bg-light text-dark">
      <form @submit.prevent="loginUser">
        <input type="hidden" name="csrfmiddlewaretoken" ref="csrfTokenInput" v-model="csrfToken">
        <!-- You can bind your form fields to data properties here -->
        <div class="form-group">
          <label for="username">Username:</label>
          <input type="text" class="form-control" id="username" name="username" v-model="username">
        </div>
        <div class="form-group">
          <label for="password">Password:</label>
          <input type="password" class="form-control" id="password" name="password" v-model="password">
        </div>
        <button class="btn btn-primary" type="submit">Login</button>
      </form>
      <p class="text-center">
        Don't have an account? <router-link to="/register">Register</router-link> to create one.
      </p>
      <!-- Google Sign-up Button (You can integrate this using Vue Router) -->
      <a href="#" class="btn btn-danger">Register with Google</a>
    </div>
  </div>
</template>
  
<script>
import axios from 'axios';
import { mapMutations } from 'vuex'; // Import mapMutations from Vuex

export default {
  data() {
    return {
      username: "",
      password: "",
      csrfToken: "",
    };
  },
  methods: {
    // Use mapMutations to access mutations from the store
    ...mapMutations(['setToken', 'initializeStore', 'setIsAuthenticated']),
    // Handle user login (you can use Axios to send the login request to your Django backend)
    async loginUser() {
      console.log('Username:', this.username);
      const loginData = {
        username: this.username,
        password: this.password,
      };

      console.log('loginData:', loginData); // Log the loginData object

      // Use Axios or another HTTP library to send the loginData to your Django backend.
      // Handle success and error responses as needed.
      try {
        const response = await axios.post('http://127.0.0.1:8000/registration/api/login/vue/', JSON.stringify(loginData), {
          'Origin': ['http://localhost:8081', 'http://localhost:8080'],
          headers: {
            'Content-Type': 'application/json',
          },
        });

        // Handle a successful login (e.g., redirect to a dashboard or update the UI)
        console.log('Logged in successfully', response.data);
        // In your Login.vue component after a successful login
        this.$store.commit('setIsAuthenticated', true);

        // Set the token in the Vuex store
        this.setToken(response.data.token);

        // Initialize the store
        this.initializeStore();

        // Inside your Vue component after successful login
        this.$router.push({ name: 'Dashboard' });
      } catch (error) {
        // Handle login errors (e.g., display an error message)
        console.error('Login error', error);

        // You can display an error message to the user
        this.errorMessage = 'Invalid username or password. Please try again.';
      }
    },
  },
  mounted() {
  },
};
</script>
