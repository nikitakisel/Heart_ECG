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
      <p style="text-align: left;">Регистрационные данные</p>
      <div class="form-group">
        <input class="form-control" v-model="formData.username" placeholder="Логин" required/>
      </div>
      <div class="form-group">
        <input class="form-control" type="email" v-model="formData.email" placeholder="Электропочта" required/>
      </div>
      <div class="form-group" v-if="!formData.is_staff">
        <input class="form-control" v-model="formData.passport_series" placeholder="Серия паспорта" maxlength="4"/>
        <input class="form-control" v-model="formData.passport_number" placeholder="Номер паспорта" maxlength="6"/>
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
      <div class="form-check">
        <input 
          class="form-check-input" 
          type="checkbox" 
          v-model="formData.is_staff" 
          id="flexCheck" 
        >
        <label class="form-check-label" for="flexCheck">
          Зарегистрироваться как врач
        </label>
      </div>
      <div v-if="formData.is_staff">
        <div class="form-group">
          <select class="form-select" v-model="formData.institution" required>
            <option value="" disabled selected>Выберите медицинское учреждение</option>
            <option 
              v-for="institution in medicalInstitutions" 
              :key="institution.id" 
              :value="institution.id"
            >
              {{ institution.name }} - {{ institution.address }}
            </option>
          </select>
        </div>
        <div class="form-group">
          <input class="form-control" v-model="formData.subdivision" placeholder="Название подразделения" />
        </div>
      </div>
      <div class="form-group" v-if="formData.is_staff">
        <select class="form-select" v-model="formData.role" required>
          <option value="" disabled>Выберите роль</option>
          <option value="doctor">Врач</option>
          <option value="nurse">Средний мед. персонал</option>
        </select>
      </div>
      <div class="form-group">
        <button type="submit" class="button-login btn btn-danger">Зарегистрироваться</button>
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
      formData: {
        username: null,
        email: null,
        first_name: null,
        last_name: null,
        patronymic: null,
        password: null,
        is_staff: false,
        institution: null,
        subdivision: null,
        role: null,
        passport_series: null,
        passport_number: null,
      },
      medicalInstitutions: [],
      showPassword: false,
      loading: false,
    }
  },
  components: {
    Header
  },
  mounted() {
    this.loadMedicalInstitutions();
  },
  methods: {
    goMenu() {
      this.$router.push('/');
    },

    async loadMedicalInstitutions() {
      try {
        this.loading = true;
        const response = await apiClient.get('http://localhost:8000/api/medical-institutions/');
        this.medicalInstitutions = response.data.results || response.data;
      } catch (error) {
        console.error('Ошибка загрузки медицинских учреждений:', error);
        alert("Ошибка загрузки списка медицинских учреждений");
      } finally {
        this.loading = false;
      }
    },

    submitData() {
      const submitData = {
        ...this.formData,
        ...(!this.formData.is_staff && {
          institution: null,
          subdivision: null,
          role: null
        })
      };

      apiClient.post('http://localhost:8000/api/auth/register/', submitData)
      .then(response => {
        const tokens = {
          refresh: response.data.refresh,
          access: response.data.access,
        };
        localStorage.setItem('tokens', JSON.stringify(tokens));
        this.goMenu();
      })
      .catch(error => {
        console.error('Ошибка регистрации:', error);
        alert("Ошибка ввода данных: " + (error.response?.data?.message || error.message));
      });
    },

    togglePasswordVisibility() {
      this.showPassword = !this.showPassword;
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
  margin-bottom: 20px;
}

@media (max-width: 600px) {
  .form-group {
    flex-direction: column !important;
  }
}

.form-check {
  text-align: left;
  margin-top: 10px;
  margin-bottom: 10px;
}

.loading {
  opacity: 0.6;
  pointer-events: none;
}
</style>
