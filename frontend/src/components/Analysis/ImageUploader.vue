<template>
  <Header />
  <h1 style="text-align: center; margin-bottom: 20px;">Начало анализа</h1>
  <form class="form-container card" @submit.prevent="submitData">
    <div class="form-group">
      <label for="dataname">Название анализа</label>
      <input type="text" v-model="name" class="form-control" id="dataname" name="fname" placeholder="Например: ЭКГ от 12.11" autocomplete="off">
    </div>

    <div
      class="dropzone"
      :class="{ 'dropzone--active': isDragging }"
      @dragover.prevent="onDragOver"
      @dragleave.prevent="onDragLeave"
      @drop.prevent="onDrop"
      role="button"
      tabindex="0"
      @keydown.enter.prevent="openFileDialog"
      @click="openFileDialog"
      aria-label="Загрузить изображение"
    >
      <template v-if="!image">
        <p class="dropzone__title">Перетащите сюда изображение</p>
        <p class="p-muted">или нажмите, чтобы выбрать файл</p>
      </template>
      <template v-else>
        <p class="dropzone__title">Выбран файл: <strong>{{ image.name }}</strong></p>
        <div v-if="previewUrl" class="preview">
          <img :src="previewUrl" alt="Предпросмотр изображения">
        </div>
      </template>
      <input ref="fileInput" type="file" accept="image/*" class="visually-hidden" @change="handleFileSelect">
    </div>

    <div v-if="uploadProgress > 0" class="progress">
      <div class="progress__bar" :style="{ width: uploadProgress + '%' }"></div>
    </div>

    <div style="display: flex; gap: 8px; align-items: center;">
      <button type="submit" class="btn btn-danger" :disabled="!image || isUploading">
        {{ isUploading ? 'Загрузка...' : 'Отправить' }}
      </button>
      <button type="button" class="btn" @click="resetSelection" :disabled="isUploading && uploadProgress > 0">
        Сбросить
      </button>
    </div>
  </form>
</template>

<script>
import Header from '../Includes/Header.vue';
import apiClient from '@/apiClient';

export default {
  data() {
    return {
        name: null,
        image: null,
        previewUrl: null,
        isDragging: false,
        isUploading: false,
        uploadProgress: 0,
      }
  },
  components: {
    Header
  },
  methods: {
    openFileDialog() {
      this.$refs.fileInput && this.$refs.fileInput.click();
    },
    onDragOver() {
      this.isDragging = true;
    },
    onDragLeave() {
      this.isDragging = false;
    },
    onDrop(event) {
      this.isDragging = false;
      const files = event.dataTransfer.files;
      if (files && files[0]) {
        this.setImage(files[0]);
      }
    },
    handleFileSelect(event) {
      const file = event.target.files && event.target.files[0];
      if (file) this.setImage(file);
    },
    setImage(file) {
      this.image = file;
      if (this.previewUrl) URL.revokeObjectURL(this.previewUrl);
      this.previewUrl = URL.createObjectURL(file);
    },
    submitData() {
      if (!this.image) return;
      const form = new FormData();
      if (this.name) form.append('name', this.name);
      form.append('image', this.image);
      this.isUploading = true;
      this.uploadProgress = 0;
      apiClient.post('http://localhost:8000/api/analysis/', form, {
        headers: { 'Content-Type': 'multipart/form-data' },
        onUploadProgress: (e) => {
          if (e.total) this.uploadProgress = Math.round((e.loaded / e.total) * 100);
        }
      })
        .then(response => {
          this.$router.push(`/analysis/${response.data.slug}`);
        })
        .catch(error => {
          console.error('Ошибка отправки изображения:', error);
        })
        .finally(() => {
          this.isUploading = false;
          setTimeout(() => (this.uploadProgress = 0), 600);
        });
    },
    resetSelection() {
      if (this.previewUrl) {
        URL.revokeObjectURL(this.previewUrl);
      }
      this.previewUrl = null;
      this.image = null;
      this.uploadProgress = 0;
      this.isDragging = false;
      if (this.$refs.fileInput) {
        this.$refs.fileInput.value = '';
      }
    }
  }
}
</script>

<style>
.form-container {
  padding: 24px;
  width: 100%;
  max-width: 560px;
  min-height: 300px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  justify-content: flex-start;
  margin: 20px auto;
}
.dropzone {
  border: 2px dashed var(--color-border-strong);
  border-radius: var(--radius-m);
  padding: 20px;
  text-align: center;
  background: var(--color-surface);
  transition: border-color .15s ease, background-color .15s ease, box-shadow .15s ease;
  cursor: pointer;
}
.dropzone--active {
  border-color: var(--color-primary);
  background: rgba(215,38,61,.06);
  box-shadow: 0 0 0 3px rgba(225,29,72,.10);
}
.dropzone__title { font-weight: 600; color: var(--color-text-strong); }
.preview { margin-top: 12px; display: flex; justify-content: center; }
.preview img { max-width: 100%; height: auto; border-radius: var(--radius-s); box-shadow: var(--shadow-1); }

.progress { width: 100%; height: 8px; background: var(--color-background-mute); border-radius: 999px; overflow: hidden; border: 1px solid var(--color-border-strong); }
.progress__bar { height: 100%; background: var(--color-primary); width: 0%; transition: width .2s ease; }

@media (max-width: 480px) {
  .form-container { padding: 16px; margin: 12px auto; }
}
</style>
