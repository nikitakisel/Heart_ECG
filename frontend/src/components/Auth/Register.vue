<template>
  <Header />
  <div class="auth-container">
    <form class="login-form" @submit.prevent="submitData">
      <img src="../../assets/logo_ecg.svg" class="logo">
      <h2>Регистрация</h2>
      <br>
      <div class="form-group">
        <input class="form-control" v-model="formData.last_name" placeholder="Фамилия" required/>
      </div>
      <div class="form-group">
        <input class="form-control" v-model="formData.first_name" placeholder="Имя" required/>
      </div>
      <div class="form-group">
        <input class="form-control" v-model="formData.patronymic" placeholder="Отчество" required/>
      </div>
      <div class="form-group">
        <input class="form-control" v-model="formData.username" placeholder="Логин" required/>
      </div>
      <div class="form-group">
        <input class="form-control" type="email" v-model="formData.email" placeholder="Электропочта" required/>
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
          email: null,
          first_name: null,
          last_name: null,
          patronymic: null,
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
      apiClient.post('http://localhost:8000/api/auth/register/', this.formData)
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

.form-group {
  padding-bottom: 10px;
}
</style>