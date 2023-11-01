<template>
    <div>
      <!-- Login -->
      <div class="container border p-3 mb-3 bg-light text-dark">
        <h1>Login</h1>
      </div>
      <div class="container border p-3 mb-3 bg-light text-dark">
        <form @submit.prevent="loginUser">
            <input type="hidden" name="csrfmiddlewaretoken" ref="csrfTokenInput">
          <!-- You can bind your form fields to data properties here -->
          <div class="form-group">
            <label for="username">Username:</label>
            <input type="text" class="form-control" id="username" v-model="username">
          </div>
          <div class="form-group">
            <label for="password">Password:</label>
            <input type="password" class="form-control" id="password" v-model="password">
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
  export default {
    data() {
      return {
        username: "",
        password: "",
        csrfToken: "",
      };
    },
    methods: {
      // Handle user login (you can use Axios to send the login request to your Django backend)
      loginUser() {
        const loginData = {
          username: this.username,
          password: this.password,
          csrfmiddlewaretoken: this.csrfToken, // Include the CSRF token
        };
  
        // Use Axios or another HTTP library to send the loginData to your Django backend.
        // Handle success and error responses as needed.
         // Make a POST request to your Django backend
         axios
            .post('http://127.0.0.1:8000/registration/api/login/vue/', loginData, {
                'Origin': 'http://localhost:8081',  
                'X-CSRFToken': this.csrfToken, // Keep the CSRF token header
                withCredentials: true, // Add this line if not already included
            })
            .then((response) => {
                // Handle a successful login (e.g., redirect to a dashboard or update the UI)
                console.log('Logged in successfully', response.data);
                // Commit the setToken mutation to update the store
                this.$store.commit('setToken', response.data.token);
                console.log('Logged in successfully', response.data);

                // Pass the user's information to the Dashboard route
                console.log('User Profile Data:', response.data.user_profile);

                this.$router.push({
                    name: 'Dashboard',
                    params: { userProfile: response.data.user_profile },
                });
                this.successMessage = 'Login successful';
            })
            .catch((error) => {
                // Handle login errors (e.g., display an error message)
                console.error('Login error', error);

                // You can display an error message to the user
                this.errorMessage = 'Invalid username or password. Please try again.';
            });
      },
    },
    mounted() {
    // Retrieve the CSRF token from the ref and set it in data
    this.csrfToken = this.$refs.csrfTokenInput.value;
    },

  };
  </script>
  
