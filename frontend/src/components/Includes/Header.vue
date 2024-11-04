<template>
  <header class="d-flex flex-wrap align-items-center justify-content-center justify-content-md-between py-3 mb-4 border-bottom">
    <a href="/" class="d-flex align-items-center col-md-3 mb-2 mb-md-0 text-dark text-decoration-none">
      <img src="../../assets/logo_ecg.svg">
    </a>

    <ul class="nav col-12 col-md-auto mb-2 justify-content-center mb-md-0">
      <li><a href="/" class="nav-link px-2 link-dark">Начать анализ</a></li>
      <li><a href="/analysis" class="nav-link px-2 link-dark">Список анализов</a></li>
    </ul>

    <div class="col-md-3 text-end">
      <button @click="goLogin" type="button" class="btn btn-outline-danger me-2">Войти</button>
      <button @click="goRegister" type="button" class="btn btn-danger">Создать аккаунт</button>
    </div>
  </header>
</template>

<script>
export default {
  methods: {
    goRegister() {
      this.$router.push('/register');
    },

    goLogin() {
      this.$router.push('/login');
    }
  }
}
</script>

<style>
header {
  padding-left: 10px;
  padding-right: 10px;
}
</style>
