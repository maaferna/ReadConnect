<template>
  <div class="page-dashboard">
    <div class="columns is-multiline">
      <div class="column is-12">
        <h1 class="title">Dashboard</h1>
        <p v-if="isAuthenticated">Welcome, {{ userProfile.user_name }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Dashboard',
  props: ['isAuthenticated'], // Receive isAuthenticated as a prop
  data() {
    return {
      userProfile: {},
      userStatuses: [],
    };
  },
  mounted() {
    // Execute the fetchUserWithToken() function immediately after the component is mounted
    this.fetchUserWithToken();
  },
  methods: {
    async fetchUserWithToken() {
      console.log('Began fetch User data');
      const jwtToken = localStorage.getItem('yourJWTToken'); // Use the correct token variable
      if (jwtToken) {
        try {
          const authResponse = await axios.get('/api/get-user-profile/', {
            headers: {
              Authorization: `Bearer ${jwtToken}`,
            },
          });
          console.log('Authenticated Dashboard section');
          this.userProfile = authResponse.data.userProfile;
          this.userStatuses = authResponse.data.userStatuses;
        } catch (error) {
          console.error('Error fetching user profile data', error);
        }
      } else {
        console.error('JWT Token not found. User is not authenticated.');
      }
    },
  },
};
</script>








