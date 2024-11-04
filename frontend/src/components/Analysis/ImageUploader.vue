<template>
  <Header />
  <h1 style="text-align: center; margin-bottom: 20px;">Начало анализа</h1>
  <form class="form-container" @submit.prevent="submitData" >
    <div class="form-group">
      <label for="dataname">Название анализа</label>
      <input type="text" v-model="formData.name" class="form-control" id="dataname" name="fname" >    
    </div>
    <div class="input-group mb-3">
      <div class="custom-file">
        <input type="file" @change="handleFileSelect" class="custom-file-input" id="inputGroupFile02" name="file2">
        <label class="custom-file-label" for="inputGroupFile02" aria-describedby="inputGroupFileAddon02">Нажмите на кнопку либо перетащите файл</label>
      </div>
    </div>
    <button type="submit" class="btn btn-danger">Отправить</button>
  </form>
</template>

<script>
import Header from '../Includes/Header.vue';
import apiClient from '@/apiClient';

export default {
  data() {
    return {
        formData : {
          name: null,
          image: null,
        },
        show_password: null,
      }
  },
  components: {
    Header
  },
  methods: {
    handleFileSelect(event) {
      this.formData.image = event.target.files[0];
    },
    submitData() {
      apiClient.post('http://localhost:8000/api/analysis/', this.formData, {
        headers: {
            'Content-Type': 'multipart/form-data'
          }
      })
      .then(response => {
        this.$router.push(`/analysis/${response.data.slug}`);
      })
      .catch(error => {
        console.error('Ошибка отправки изображения:', error);
      })
    }
  }
}
</script>

<style>
.form-container {
  background: #fff;
  padding: 30px;
  width: 400px;
  height: 400px;
  border-radius: 10px;
  box-shadow: 1px 1px 5px rgba(0,0,0,0.1);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  margin: auto;
}
</style>