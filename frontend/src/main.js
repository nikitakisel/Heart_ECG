import './assets/main.css'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap'

import { createApp } from 'vue'
import axios from 'axios'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import Login from './components/Auth/Login.vue'
import Logout from './components/Auth/Logout.vue'
import Register from './components/Auth/Register.vue'
import ImageUploader from './components/Analysis/ImageUploader.vue'
import Analysis from './components/Analysis/Analysis.vue'
import AnalysisList from './components/Analysis/AnalysisList.vue'
import UserProfile from './components/User/Profile.vue'

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
            path: '/profile',
            component: UserProfile,
            meta: {
                title: 'Профиль пользователя',
                requiresAuth: true,
            },
        },
        {
            path: '/analysis',
            component: AnalysisList,
            meta: { requiresAuth: true },
        },
        {
            path: '/analysis/:slug',
            component: Analysis,
            meta: { requiresAuth: true },
        },
    ],
    history: createWebHistory()
})

router.beforeEach(async (to, from) => {
    if (to.meta && to.meta.title) {
        document.title = to.meta.title
    }

    if (!to.meta?.requiresAuth) {
        return true
    }

    const tokensRaw = localStorage.getItem('tokens')
    if (!tokensRaw) {
        return { path: '/login', query: { redirect: to.fullPath } }
    }

    const tokens = JSON.parse(tokensRaw)
    // Try verify access token first
    try {
        await axios.post('http://localhost:8000/api/auth/token/verify/', { token: tokens.access })
        return true
    } catch (e) {
        // Try to refresh
        try {
            const resp = await axios.post('http://localhost:8000/api/auth/token/refresh/', { refresh: tokens.refresh })
            const newTokens = {
                refresh: resp.data.refresh,
                access: resp.data.access,
            }
            localStorage.setItem('tokens', JSON.stringify(newTokens))
            return true
        } catch (e2) {
            localStorage.removeItem('tokens')
            return { path: '/login', query: { redirect: to.fullPath } }
        }
    }
})

const app = createApp(App);
app.use(router);
app.mount('#app')
