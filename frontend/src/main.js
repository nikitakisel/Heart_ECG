import './assets/main.css'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap'

import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import Login from './components/Auth/Login.vue'
import Register from './components/Auth/Register.vue'
import ImageUploader from './components/Analysis/ImageUploader.vue'
import Analysis from './components/Analysis/Analysis.vue'
import AnalysisList from './components/Analysis/AnalysisList.vue'

const router = createRouter({
    routes: [
        {
            path: '/login',
            component: Login,
        },
        {
            path: '/register',
            component: Register,
        },
        {
            path: '/',
            component: ImageUploader,
        },
        {
            path: '/analysis',
            component: AnalysisList,
        },
        {
            path: '/analysis/:slug',
            component: Analysis,
        },
    ],
    history: createWebHistory()
})

const app = createApp(App);
app.use(router);
app.mount('#app')