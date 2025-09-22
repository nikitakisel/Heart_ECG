import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://localhost:8000/api/',
});

apiClient.interceptors.request.use(config => {
  const tokens = JSON.parse(localStorage.getItem('tokens'));
  if (tokens && tokens.access) {
    config.headers['Authorization'] = `Bearer ${tokens.access}`;
  }
  // Only set JSON content-type when not sending FormData and when not already defined
  const isFormData = typeof FormData !== 'undefined' && config.data instanceof FormData;
  if (isFormData) {
    // Let the browser set the correct multipart/form-data boundary
    if (config.headers && config.headers['Content-Type']) {
      delete config.headers['Content-Type'];
    }
  } else if (!config.headers || !config.headers['Content-Type']) {
    config.headers = config.headers || {};
    config.headers['Content-Type'] = 'application/json';
  }
  return config;
}, error => {
  return Promise.reject(error);
});

apiClient.interceptors.response.use(response => {
  return response;
}, async error => {
  const originalRequest = error.config;

  if (error.response && error.response.status === 401) {
    const tokens = JSON.parse(localStorage.getItem('tokens'));

    if (tokens && tokens.refresh) {
      try {
        const response = await axios.post('http://localhost:8000/api/auth/token/refresh/', {
          refresh: tokens.refresh
        });

        const newTokens = {
          refresh: response.data.refresh,
          access: response.data.access,
        };
        localStorage.setItem('tokens', JSON.stringify(newTokens));

        originalRequest.headers['Authorization'] = `Bearer ${newTokens.access}`;
        return apiClient(originalRequest);
      } catch (refreshError) {
        console.error('Unable to refresh token:', refreshError);
        try { localStorage.removeItem('tokens'); } catch (_) {}
        // cannot use this.$router here; return a rejected promise with a marker so caller can redirect
        error.isAuthFailed = true;
      }
    }
  }

  return Promise.reject(error);
});

export default apiClient;
