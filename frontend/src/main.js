import './assets/main.css'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap'

import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import Login from './components/Auth/Login.vue'
import Logout from './components/Auth/Logout.vue'
import Register from './components/Auth/Register.vue'
import ImageUploader from './components/Analysis/ImageUploader.vue'
import Analysis from './components/Analysis/Analysis.vue'
import AnalysisList from './components/Analysis/AnalysisList.vue'

const router = createRouter({
    routes: [
        {
            path: '/login',
            component: Login,
            meta: {
                title: 'Вход',
            },
        },
        {
            path: '/register',
            component: Register,
            meta: {
                title: 'Регистрация',
            },
        },
        {
            path: '/logout',
            component: Logout,
            meta: {
                title: 'Выход',
            },
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

router.beforeEach((to, from) => {
    document.title = to.meta?.title
})

const app = createApp(App);
app.use(router);
app.mount('#app')
