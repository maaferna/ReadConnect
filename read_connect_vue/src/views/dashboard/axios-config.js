// Create a new file, e.g., axios-config.js
import axios from 'axios';

// Add your base URL and other Axios configuration options here
const axiosInstance = axios.create({
  baseURL: 'http://127.0.0.1:8000', // Replace with your API base URL
  // Add other options like headers, timeout, etc.
});

// Add an Axios request interceptor to set the Authorization header
axiosInstance.interceptors.request.use(
  (config) => {
    const jwtToken = localStorage.getItem('token');
    console.log("axios-config",jwtToken)
    if (jwtToken) {
      config.headers.Authorization = `Bearer ${jwtToken}`;
    }
    console.log(config.headers.Authorization)
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default axiosInstance;
