import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://localhost:8000/api/',
});

apiClient.interceptors.request.use(config => {
  const tokens = JSON.parse(localStorage.getItem('tokens'));
  if (tokens && tokens.access) {
    config.headers['Authorization'] = `Bearer ${tokens.access}`;
  }
  return config;
}, error => {
  return Promise.reject(error);
});

apiClient.interceptors.response.use(response => {
  return response;
}, async error => {
  const originalRequest = error.config;

  if (error.response.status === 401) {
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
      }
    }
  }

  return Promise.reject(error);
});

export default apiClient;
