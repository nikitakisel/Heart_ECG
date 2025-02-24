<template>
  <Header />
  <div class="analysis-container">
    <h1>Анализ: {{ analysis.name }}</h1>
    <img v-if="analysis.result_image" :src="analysis.result_image" alt="Результат анализа" class="result-image" width="50%" height="50%"/>
    <p v-if="analysis.user">Пользователь: {{ analysis.user.username }}</p>
    <p v-if="loading">Загрузка...</p>
    <p v-if="error">{{ error }}</p>
    <a :href="analysis.result_image" class="btn btn-danger" target="_blank">Открыть картинку в новой вкладке</a>
  </div>
</template>

<script>
import Header from '../Includes/Header.vue';
import apiClient from '@/apiClient';

export default {
  data() {
    return {
        analysis: {},
        loading: true,
        error: null,
      };
  },
  components: {
    Header
  },
  async created() {
    const slug = this.$route.params.slug;
    try {
    const response = await apiClient.get(`http://localhost:8000/api/analysis/${slug}`);
        this.analysis = response.data;
    } catch (err) {
    this.error = 'Ошибка при загрузке анализа';
        console.error(err);
    } finally {
        this.loading = false;
    }
  },
};
</script>

<style scoped>
.analysis-container {
text-align: center;
}

.result-image {
max-width: 100%;
height: auto;
}
</style>