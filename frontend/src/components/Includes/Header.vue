<template>
  <header class="d-flex flex-wrap align-items-center justify-content-center justify-content-md-between py-3 mb-4 border-bottom">
    <a href="/" class="d-flex align-items-center col-md-3 mb-2 mb-md-0 text-dark text-decoration-none">
      <img src="../../assets/logo_ecg.svg">
      <p></p>
    </a>

    <ul class="nav col-12 col-md-auto mb-2 justify-content-center mb-md-0">
      <li><a href="/" class="nav-link px-2 link-dark">Начать анализ</a></li>
      <li><a href="/analysis" class="nav-link px-2 link-dark">Список анализов</a></li>
    </ul>

    <div class="col-md-3 text-end">
      <button v-if="!isLoggedIn" @click="goLogin" type="button" class="btn btn-outline-danger me-2">Войти</button>
      <button v-if="!isLoggedIn" @click="goRegister" type="button" class="btn btn-danger">Зарегистрироваться</button>
      <button v-if="isLoggedIn" @click="goLogout" type="button" class="btn btn-outline-secondary me-2">Выйти</button>
      <button v-if="isLoggedIn" @click="goProfile" type="button" class="btn btn-danger">Профиль</button>
    </div>
  </header>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      isLoggedIn: false
    };
  },

  mounted() {
    this.checkRefreshToken();
  },

  methods: {
    goRegister() {
      this.$router.push('/register');
    },

    goLogin() {
      this.$router.push('/login');
    },

    goLogout() {
      this.isLoggedIn = false;
      this.$router.push('/logout');
    },

    async checkRefreshToken() {
      const tokens = JSON.parse(localStorage.getItem('tokens'));

      if (tokens && tokens.refresh) {
        try {
          const response = await axios.post('http://localhost:8000/api/auth/token/verify/', {
            token: tokens.refresh,
          });

          if (response.status === 200) {
            this.isLoggedIn = true; // Устанавливаем статус входа
          }
        } catch (error) {
          console.log(error)
          if (error.response && error.response.status === 401) {
            this.isLoggedIn = false;
          } else {
            console.error('Ошибка при проверке токена:', error);
          }
        }
      } else {
        this.isLoggedIn = false;
      }
    },
  }
}
</script>

<style>
header {
  padding-left: 10px;
  padding-right: 10px;
}
</style>
