import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://localhost:8000/api/',
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
        return apiClient(originalRequest); // Повторяем запрос с новым токеном
      } catch (refreshError) {
        console.error('Unable to refresh token:', refreshError);
        this.$router.push('/login');
      }
    }
  }
  return Promise.reject(error);
});

export default apiClient;
