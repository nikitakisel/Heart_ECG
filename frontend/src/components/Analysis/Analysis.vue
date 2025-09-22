<template>
  <Header />
  <div class="analysis container">
    <div class="analysis__header">
      <div>
        <h1 class="analysis__title">{{ analysis.name || 'Загрузка анализа…' }}</h1>
        <p v-if="analysis.user && !loading" class="analysis__meta p-muted">Пользователь: <strong>{{ analysis.user.username }}</strong></p>
        <p v-if="error" class="analysis__error">{{ error }}</p>
      </div>
      <div class="analysis__actions">
        <router-link to="/analysis" class="button button--ghost">Назад к списку</router-link>
        <a v-if="analysis.result_image && !loading" :href="analysis.result_image" target="_blank" class="button button--primary">Открыть изображение</a>
      </div>
    </div>

    <div class="analysis__content">
      <div v-if="loading" class="skeleton analysis__skeleton"></div>
      <div v-else class="analysis__image-card card">
        <div class="analysis__image-wrap">
          <img v-if="analysis.result_image" :src="analysis.result_image" alt="Результат анализа" class="analysis__image"/>
          <div v-else class="analysis__empty">
            <h3>Нет изображения результата</h3>
            <p class="p-muted">Загрузите изображение, чтобы увидеть результат анализа.</p>
          </div>
        </div>
      </div>
    </div>
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
.analysis { display:flex; flex-direction:column; gap: var(--space-5); }
.analysis__header { display:flex; align-items:flex-start; justify-content:space-between; gap: var(--space-4); padding-top: var(--space-5); }
.analysis__title { margin: 0; }
.analysis__meta { margin-top: 6px; }
.analysis__error { color: var(--color-error); margin-top: var(--space-2); }
.analysis__actions { display:flex; gap: var(--space-2); flex-wrap: wrap; }

.analysis__content { display:flex; }
.analysis__skeleton { height: 420px; width:100%; border-radius: var(--radius-m); }
.analysis__image-card { width:100%; overflow:hidden; }
.analysis__image-wrap { position: relative; background: var(--color-background-mute); display:flex; align-items:center; justify-content:center; }
.analysis__image { display:block; width:auto; max-width:70%; height:auto; max-height:70vh; object-fit:contain; margin:0 auto; }
.analysis__empty { text-align:center; padding: var(--space-6); }

.skeleton { background: linear-gradient(90deg, rgba(0,0,0,0.04), rgba(0,0,0,0.08), rgba(0,0,0,0.04)); background-size: 200% 100%; animation: shimmer 1.2s infinite; }
@keyframes shimmer { 0% { background-position: 200% 0; } 100% { background-position: -200% 0; } }

@media (max-width: 768px) {
  .analysis__header { flex-direction: column; align-items: stretch; gap: var(--space-3); }
  .analysis__actions { justify-content: flex-start; }
  .analysis__image { max-width: 100%; max-height: 60vh; }
}
</style>
