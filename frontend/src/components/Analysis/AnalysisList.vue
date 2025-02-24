<template>
  <Header />
  <div class="analysis-list">
    <h1>Список анализов</h1>
    <div v-if="loading">Загрузка...</div>
    <div v-if="error">{{ error }}</div>
    <div v-if="analyses.length === 0 && !loading">Анализы не найдены.</div>
    <div v-for="analysis in analyses" :key="analysis.slug" class="analysis-item">
      <div class="card">
        <h5 class="card-header">{{ analysis.name }}</h5>
        <div class="card-body">
          <img :src="analysis.result_image" alt="Результат анализа" class="result-image" width="30%" height="30%"/>
          <h5 class="card-title">Пользователь: {{ analysis.user.username }}</h5>
          <router-link :to="`/analysis/${analysis.slug}`" class="btn btn-primary">Перейти к анализу</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Header from '../Includes/Header.vue';
import apiClient from '@/apiClient'; // Импортируйте ваш apiClient

export default {
  data() {
    return {
      analyses: [],
      loading: true,
      error: null,
    };
  },
  components: {
    Header
  },
  async created() {
    try {
      const response = await apiClient.get('http://localhost:8000/api/analysis/');
      this.analyses = response.data;
    } catch (err) {
      this.error = 'Ошибка при загрузке анализов';
      console.error(err);
    } finally {
      this.loading = false;
    }
  },
};
</script>

<style scoped>
.analysis-list {
  text-align: center;
}
.card {
  margin: 20px;
}
</style>
