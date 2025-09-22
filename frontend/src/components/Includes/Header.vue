<template>
  <header class="app-header">
    <div class="container app-header__inner">
      <router-link to="/" class="brand" aria-label="На главную">
        <img class="brand__logo" src="../../assets/logo_ecg.svg" alt="ECG">
      </router-link>

      <nav class="app-nav" aria-label="Основная навигация">
        <router-link to="/" class="app-nav__link">Начать анализ</router-link>
        <router-link to="/analysis" class="app-nav__link">Список анализов</router-link>
      </nav>

      <div class="actions">
        <button v-if="!isLoggedIn" @click="goLogin" type="button" class="btn btn-outline-danger">Войти</button>
        <button v-if="!isLoggedIn" @click="goRegister" type="button" class="btn btn-danger">Зарегистрироваться</button>
        <button v-if="isLoggedIn" @click="goLogout" type="button" class="btn btn-outline-secondary">Выйти</button>
        <button v-if="isLoggedIn" @click="goProfile" type="button" class="btn btn-danger">Профиль</button>
      </div>
    </div>
  </header>
  <div class="header-spacer" aria-hidden="true"></div>
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
    this.checkAuth();
  },

  watch: {
    // react to route changes to update header state
    $route() {
      this.checkAuth();
    }
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

    goProfile() {
      const tokens = JSON.parse(localStorage.getItem('tokens'));
      if (!tokens) {
        this.$router.push({ path: '/login', query: { redirect: '/profile' } });
        return;
      }
      this.$router.push('/profile');
    },

    async checkAuth() {
      const tokensRaw = localStorage.getItem('tokens');
      if (!tokensRaw) { this.isLoggedIn = false; return; }
      const tokens = JSON.parse(tokensRaw);
      try {
        await axios.post('http://localhost:8000/api/auth/token/verify/', { token: tokens.access });
        this.isLoggedIn = true;
      } catch (e) {
        try {
          const resp = await axios.post('http://localhost:8000/api/auth/token/refresh/', { refresh: tokens.refresh });
          const newTokens = { refresh: resp.data.refresh, access: resp.data.access };
          localStorage.setItem('tokens', JSON.stringify(newTokens));
          this.isLoggedIn = true;
        } catch (e2) {
          localStorage.removeItem('tokens');
          this.isLoggedIn = false;
        }
      }
    },
  }
}
</script>

<style scoped>
.brand { display:flex; align-items:center; text-decoration: none; }
.brand__logo { height: 28px; width: auto; display:block; }
.app-nav__link { color: var(--color-text-strong); text-decoration: none; padding:8px 10px; border-radius:8px; }
.app-nav__link[aria-current="page"], .app-nav__link:hover { color:#fff; background: var(--color-primary); }
.actions { display:flex; align-items:center; gap: 8px; }
.header-spacer { height: 64px; }
@media (max-width: 768px) {
  .brand__logo { height: 24px; }
  .actions { gap: 6px; }
  .header-spacer { height: 56px; }
}
</style>
