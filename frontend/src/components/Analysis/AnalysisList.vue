<template>
  <Header />
  <div class="analysis-list container">
    <div class="analysis-list__header">
      <div>
        <h1>Анализы</h1>
        <p class="p-muted">Ваши результаты обработанных изображений</p>
      </div>
    </div>

    <div v-if="loading" class="skeleton analysis-list__skeleton"></div>

    <div v-else>
      <div v-if="error" class="card analysis-list__error">
        {{ error }}
      </div>

      <div v-if="analyses.length === 0" class="card analysis-list__empty">
        <h3>Анализы не найдены</h3>
        <p class="p-muted">Загрузите первое изображение, чтобы увидеть результат анализа.</p>
        <router-link to="/analysis/upload" class="button button--primary">Загрузить изображение</router-link>
      </div>

      <div v-else class="analysis-grid">
        <div v-for="analysis in analyses" :key="analysis.slug" class="analysis-card card">
          <div class="analysis-card__media">
            <img :src="analysis.result_image" :alt="`Результат: ${analysis.name}`" />
          </div>
          <div class="analysis-card__body">
            <div>
              <h3 class="analysis-card__title">{{ analysis.name }}</h3>
              <p class="p-muted">Пользователь: <strong>{{ analysis.user.username }}</strong></p>
            </div>
            <router-link :to="`/analysis/${analysis.slug}`" class="button button--ghost">Открыть</router-link>
          </div>
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
.analysis-list { display:flex; flex-direction:column; gap: var(--space-5); padding-top: var(--space-5); }
.analysis-list__header { display:flex; align-items:flex-end; justify-content:space-between; }
.analysis-list__skeleton { height: 180px; border-radius: var(--radius-m); }
.analysis-list__error { padding: var(--space-4); color: var(--color-error); }
.analysis-list__empty { padding: var(--space-6); display:flex; flex-direction:column; gap: var(--space-3); align-items:flex-start; }

.analysis-grid { display:grid; grid-template-columns: repeat(3, 1fr); gap: var(--space-4); }
.analysis-card { overflow:hidden; display:flex; flex-direction:column; }
.analysis-card__media { aspect-ratio: 16/9; background: var(--color-background-mute); display:flex; align-items:center; justify-content:center; overflow:hidden; }
.analysis-card__media img { width:100%; height:100%; object-fit:cover; display:block; }
.analysis-card__body { display:flex; align-items:center; justify-content:space-between; gap: var(--space-3); padding: var(--space-4); }
.analysis-card__title { margin: 0 0 4px; }

.skeleton { background: linear-gradient(90deg, rgba(0,0,0,0.04), rgba(0,0,0,0.08), rgba(0,0,0,0.04)); background-size: 200% 100%; animation: shimmer 1.2s infinite; }
@keyframes shimmer { 0% { background-position: 200% 0; } 100% { background-position: -200% 0; } }

@media (max-width: 992px) { .analysis-grid { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 640px) { .analysis-grid { grid-template-columns: 1fr; } }
</style>
