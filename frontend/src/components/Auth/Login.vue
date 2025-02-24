<template>
  <Header />
  <div class="auth-container">
    <form class="login-form" @submit.prevent="submitData">
      <img src="../../assets/logo_ecg.svg" class="logo">
      <h2>Вход</h2>
      <br>
      <div class="form-group">
        <input class="form-control" type="email" v-model="formData.username" placeholder="Электронная почта " required/>
      </div>
      <div class="password-container" style="display: flex; flex-direction: row;">
        <input 
          class="form-control" 
          v-model="formData.password" 
          :type="showPassword ? 'text' : 'password'" 
          placeholder="Пароль" 
          required
        />
        <button type="button" @click="togglePasswordVisibility" class="show-password-btn">
          <img v-if="showPassword" src="../../assets/icons/auth/eye.png" width="20px" height="20px">
          <img v-else src="../../assets/icons/auth/eye_closed.png" width="20px" height="20px">
        </button>
      </div>
      <div class="form-group">
        <button type="submit" class="button-login btn btn-danger">Войти</button>
      </div>
      <p>Нет аккаунта? <a href="/register" style="color: #0089ff;">Зарегистрироваться</a></p>
    </form>
  </div>
</template>

<script>
import Header from '../Includes/Header.vue';
import apiClient from '@/apiClient';

export default {
  data() {
    return {
        formData : {
          username: null,
          password: null,
        },
        showPassword: false,
      }
  },
  components: {
    Header
  },
  methods: {
    goMenu() {
      this.$router.push('/');
    },

    submitData() {
      apiClient.post('http://localhost:8000/api/auth/login/', this.formData)
      .then(response => {
        const tokens = {
          refresh: response.data.refresh,
          access: response.data.access,
        };
        localStorage.setItem('tokens', JSON.stringify(tokens));
        this.goMenu();
      })
      .catch(error => {
        alert("Ошибка ввода данных");
      });
    },

    togglePasswordVisibility() {
      this.showPassword = !this.showPassword;
    }
  }
}
</script scoped>

<style>
@import '../../assets/styles/auth.css';

.form-group {
  padding-bottom: 10px;
}
</style>