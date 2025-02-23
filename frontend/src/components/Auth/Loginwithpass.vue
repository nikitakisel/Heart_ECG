/*
Набросок регистрации с паспортом
*/
<template>
  <Header />
  <div class="auth-container">
    <form class="login-form" @submit.prevent="submitData">
      <img src="../../assets/logo_ecg.svg" class="logo">
      <h2>Регистрация</h2>
      <br>
      <p style="text-align: left;">ФИО</p>
      <div class="form-group" style="display: flex; flex-direction: row;">
        <input class="form-control" v-model="formData.last_name" placeholder="Фамилия" required/>
        <input class="form-control" v-model="formData.first_name" placeholder="Имя" required/>
        <input class="form-control" v-model="formData.patronymic" placeholder="Отчество" required/>
      </div>
      <p style="text-align: left;">Паспорт</p>
      <div class="passport-data-container">
        <div class="form-group">
          <div style="width: 100%;">
            <input 
              class="form-control" 
              v-model="formData.series"
              placeholder="Серия"
              required 
              @blur="validateSeries"
            />
            <div v-if="seriesError" class="error-message"><p style="color: rgb(244,71,107); font-size: 12px;">{{ seriesError }}</p></div>
          </div>
          <div style="width: 100%;">
            <input 
              class="form-control" 
              v-model="formData.number" 
              placeholder="Номер" 
              required 
              @blur="validateNumber"
            />
            <div v-if="numberError" class="error-message"><p style="color: rgb(244,71,107); font-size: 12px;">{{ numberError }}</p></div>
          </div>
        </div>
      </div>
      <p style="text-align: left;">Регистрационные данные</p>
      <div class="form-group">
        <input class="form-control" v-model="formData.username" placeholder="Логин" required/>
      </div>
      <div class="form-group">
        <input class="form-control" type="email" v-model="formData.email" placeholder="Электропочта" required/>
      </div>
      <div class="form-group">
        <div class="password-container" style="display: flex; flex-direction: row; width: 100%;">
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
            series: '',
            number: '',
          },
          showPassword: false,
          seriesError: '',
          numberError: '',
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
        if (this.validateFields()) {
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
      },
  
      togglePasswordVisibility() {
        this.showPassword = !this.showPassword;
      },
  
      validateSeries() {
        const regex = /^\d{4}$/;
        if (!regex.test(this.formData.series)) {
          this.seriesError = 'Серия должна состоять из 4 цифр.';
        } else {
          this.seriesError = '';
        }
      },
  
      validateNumber() {
        const regex = /^\d{6}$/;
        if (!regex.test(this.formData.number)) {
          this.numberError = 'Номер должен состоять из 6 цифр.';
        } else {
          this.numberError = '';
        }
      },
  
      validateFields() {
        this.validateSeries();
        this.validateNumber();
        return !this.seriesError && !this.numberError;
      },
    }
  }
  </script>
  
  <style scoped>
  @import '../../assets/styles/auth.css';
  
  .form-group {
    padding-bottom: 10px;
    display: flex;
    flex-direction: row;
    gap: 5px;
  }
  
  .auth-container form {
    max-width: 600px;
  }
  
  @media (max-width: 600px) {
    .form-group {
      flex-direction: column !important;
    }
  
    .passport-data-container {
      display: flex;
      flex-direction: column;
    }
  }
</style>