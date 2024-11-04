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
      <div class="form-group">
        <input class="form-control" v-model="formData.password" type="password" placeholder="Пароль" required>
      </div>
      <div class="form-group">
        <button type="submit" class="button-login btn btn-danger">Войти</button>
      </div>
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
        show_password: null,
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
    }
  }
}
</script>

<style>
@import '../../assets/styles/auth.css';
</style>