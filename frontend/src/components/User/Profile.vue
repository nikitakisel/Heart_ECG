<template>
  <Header />
  <div class="container my-4">
    <div class="profile-grid">
      <section class="section-card">
        <div class="section-card__header">
          <h3>Профиль пользователя</h3>
          <small class="p-muted">Личные данные и контакты</small>
        </div>
        <form @submit.prevent="saveProfile">
          <div class="row g-3">
            <div class="col-md-6">
              <label class="form-label">Фамилия</label>
              <input v-model="form.last_name" type="text" class="form-control" placeholder="Фамилия" />
            </div>
            <div class="col-md-6">
              <label class="form-label">Имя</label>
              <input v-model="form.first_name" type="text" class="form-control" placeholder="Имя" />
            </div>
            <div class="col-md-6">
              <label class="form-label">Отчество</label>
              <input v-model="form.patronymic" type="text" class="form-control" placeholder="Отчество" />
            </div>
            <div class="col-md-6">
              <label class="form-label">Email</label>
              <input v-model="form.email" type="email" class="form-control" placeholder="example@mail.com" />
            </div>
            <div class="col-md-6">
              <label class="form-label">Пол</label>
              <select v-model="form.sex" class="form-select">
                <option value="m">мужской</option>
                <option value="w">женский</option>
              </select>
            </div>
            <div class="col-md-6">
              <label class="form-label">Дата рождения</label>
              <input v-model="form.date_of_birth" type="date" class="form-control" />
            </div>
          </div>

          <div class="section-divider"></div>
          <div class="section-card__header small">
            <h5>Медицинские данные</h5>
            <small class="p-muted">Необязательно, но поможет точности анализа</small>
          </div>
          <div class="row g-3">
            <div class="col-md-4">
              <label class="form-label">Рост (см)</label>
              <input v-model.number="form.profile.height" type="number" class="form-control" min="0" />
            </div>
            <div class="col-md-4">
              <label class="form-label">Вес (кг)</label>
              <input v-model.number="form.profile.weight" type="number" class="form-control" min="0" />
            </div>
            <div class="col-md-4">
              <label class="form-label">Полис ОМС</label>
              <input v-model="form.profile.cmi_policy" type="text" class="form-control" />
            </div>
            <div class="col-md-6">
              <label class="form-label">АД систолическое</label>
              <input v-model.number="form.profile.systolic_blood_pressure" type="number" class="form-control" min="0" />
            </div>
            <div class="col-md-6">
              <label class="form-label">АД диастолическое</label>
              <input v-model.number="form.profile.diastolic_blood_pressure" type="number" class="form-control" min="0" />
            </div>
            <div class="col-md-6">
              <label class="form-label">Семейный статус</label>
              <select v-model="form.profile.family_status" class="form-select">
                <option :value="null">Не указан</option>
                <option value="married">женат</option>
                <option value="not_married">не женат</option>
              </select>
            </div>
            <div class="col-md-6 d-flex align-items-end">
              <div class="form-check">
                <input class="form-check-input" type="checkbox" v-model="form.profile.has_children" id="hasChildren">
                <label class="form-check-label" for="hasChildren">Есть дети</label>
              </div>
            </div>
          </div>

          <div class="mt-4 d-flex gap-2">
            <button type="submit" class="btn btn-danger" :disabled="loading">
              {{ loading ? 'Сохранение...' : 'Сохранить' }}
            </button>
            <button type="button" class="btn btn-outline-secondary" @click="resetForm" :disabled="loading">Сбросить</button>
          </div>
        </form>
      </section>

      <section class="section-card">
        <div class="section-card__header">
          <h4>Мои обследования</h4>
        </div>
        <div v-if="analyses.length === 0" class="empty-state">
          <div class="empty-state__content">
            <h5>Пока нет обследований</h5>
            <p class="p-muted">Загрузите первое изображение ЭКГ и получите результат.</p>
            <router-link to="/" class="btn btn-danger">Начать анализ</router-link>
          </div>
        </div>
        <div v-else class="analysis-grid">
          <div class="analysis-card" v-for="item in analyses" :key="item.slug">
            <div class="analysis-card__media" v-if="item.result_image">
              <img :src="item.result_image" alt="Результат" />
            </div>
            <div class="analysis-card__body">
              <div class="analysis-card__title">{{ item.name || 'ЭКГ' }}</div>
              <router-link class="button button--ghost" :to="'/analysis/' + item.slug">Открыть</router-link>
            </div>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script>
import Header from '../Includes/Header.vue';
import apiClient from '@/apiClient';

export default {
  data() {
    return {
      form: {
        id: null,
        username: null,
        first_name: null,
        last_name: null,
        patronymic: null,
        email: null,
        sex: 'm',
        date_of_birth: null,
        profile: {
          height: null,
          weight: null,
          cmi_policy: null,
          systolic_blood_pressure: null,
          diastolic_blood_pressure: null,
          family_status: null,
          has_children: false,
        }
      },
      original: null,
      loading: false,
      analyses: [],
    };
  },
  components: { Header },
  created() {
    this.fetchProfile();
  },
  methods: {
    async fetchProfile() {
      this.loading = true;
      try {
        const { data } = await apiClient.get('profile/me/');
        // Ensure profile object exists
        if (!data.profile) {
          data.profile = { height: null, weight: null, cmi_policy: null, systolic_blood_pressure: null, diastolic_blood_pressure: null, family_status: null, has_children: false };
        }
        this.form = JSON.parse(JSON.stringify(data));
        this.original = JSON.parse(JSON.stringify(data));
        // Populate analyses after profile is fetched to avoid race conditions
        this.analyses = Array.isArray(data.analyses) ? data.analyses : [];
      } catch (e) {
        if (e.response && e.response.status === 401) {
          this.$router.push({ path: '/login', query: { redirect: '/profile' } });
        }
      } finally {
        this.loading = false;
      }
    },
    async fetchAnalyses() {
      // No-op: now analyses come with profile
      this.analyses = this.form && this.form.analyses ? this.form.analyses : [];
    },
    resetForm() {
      this.form = JSON.parse(JSON.stringify(this.original));
    },
    async saveProfile() {
      this.loading = true;
      try {
        const payload = {
          first_name: this.form.first_name,
          last_name: this.form.last_name,
          patronymic: this.form.patronymic,
          email: this.form.email,
          sex: this.form.sex,
          date_of_birth: this.form.date_of_birth,
          profile: {
            height: this.form.profile.height,
            weight: this.form.profile.weight,
            cmi_policy: this.form.profile.cmi_policy,
            systolic_blood_pressure: this.form.profile.systolic_blood_pressure,
            diastolic_blood_pressure: this.form.profile.diastolic_blood_pressure,
            family_status: this.form.profile.family_status,
            has_children: this.form.profile.has_children,
          }
        };
        const { data } = await apiClient.put('profile/me/', payload);
        this.form = JSON.parse(JSON.stringify(data));
        this.original = JSON.parse(JSON.stringify(data));
      } catch (e) {
        alert('Не удалось сохранить профиль');
      } finally {
        this.loading = false;
      }
    }
  }
}
</script>

<style scoped>
.form-label { font-weight: 500; }

.profile-grid { display: grid; grid-template-columns: 1fr; gap: var(--space-6); }
@media (min-width: 992px) { .profile-grid { grid-template-columns: 1.1fr .9fr; } }

.section-card { background: var(--color-surface); border:1px solid var(--color-border-strong); border-radius: var(--radius-m); box-shadow: var(--shadow-1); padding: 20px; }
.section-card__header { display:flex; align-items: baseline; justify-content: space-between; gap: 12px; margin-bottom: 12px; }
.section-card__header.small h5 { margin: 0; }
.section-divider { height: 1px; background: var(--color-border-strong); margin: 16px 0; }

.analysis-grid { display:grid; grid-template-columns: 1fr; gap: 12px; }
@media (min-width: 576px) { .analysis-grid { grid-template-columns: repeat(2, 1fr); } }
@media (min-width: 992px) { .analysis-grid { grid-template-columns: 1fr; } }

.analysis-card { background: var(--color-surface); border:1px solid var(--color-border-strong); border-radius: var(--radius-m); overflow: hidden; display:flex; flex-direction: column; }
.analysis-card__media { position: relative; padding-top: 56%; background: var(--color-background-mute); }
.analysis-card__media img { position: absolute; top:0; left:0; width:100%; height:100%; object-fit: cover; }
.analysis-card__body { padding: 12px; display:flex; justify-content: space-between; align-items:center; gap: 8px; }
.analysis-card__title { font-weight: 600; color: var(--color-text-strong); }

.empty-state { border:1px dashed var(--color-border-strong); border-radius: var(--radius-m); padding: 28px; text-align: center; background: var(--color-background-mute); }
.empty-state__content h5 { margin: 0 0 4px; }
</style>


