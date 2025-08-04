// src/utils/api.js
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add response interceptor for better error handling
api.interceptors.response.use(
  response => response,
  error => {
    const errorMessage = error.response?.data?.error || 
                         error.response?.data?.message || 
                         'Request failed';
    return Promise.reject(new Error(errorMessage));
  }
);

export { api };