<template>
    <div class="page-dashboard">
      <div class="columns is-multiline">
        <div class="column is-12">
          <h1 class="title">Dashboard</h1>
          <p v-if="userProfile">Welcome, {{ userProfile.user_name }}</p>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: 'Dashboard',
    props: {
      userProfile: Object,
    },
    data() {
      return {
        userStatuses: [],
        isAuthenticated: false,
      };
    },
    created() {
      this.fetchAuthenticationStatus();
    },
    methods: {
      async fetchDashboardData() {
        if (this.isAuthenticated) {
          try {
            const response = await axios.get('/api/dashboard-data');
            this.userStatuses = response.data.user_statuses;
          } catch (error) {
            console.error('Error fetching dashboard data', error);
          }
        } else {
          console.error('User is not authenticated');
        }
      },
      async fetchAuthenticationStatus() {
        try {
          const response = await axios.get('/api/get-auth-status');
          this.isAuthenticated = response.data.isAuthenticated;
          this.fetchDashboardData(); // Fetch dashboard data after authentication status is obtained
        } catch (error) {
          console.error('Error fetching authentication status:', error);
        }
      },
    },
    mounted() {
      console.log('User Profile in Dashboard:', this.userProfile);
    },
  };
  </script>
  

