import {createRouter, createWebHistory} from 'vue-router'

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            component: () => import('../layouts/AuthLayout.vue'),
            children: [
                {
                    path: '',
                    name: 'home',
                    component: () => import('../views/HomeView.vue'),
                    meta: { title: 'Mi Aplicación', auth: true }
                },
                {
                    path: 'users',
                    name: 'users',
                    component: () => import('../views/UsersView.vue'),
                    meta: { title: 'Usuarios', auth: true }
                }
            ]
        },
        {
            path: '/login',
            component: () => import('../layouts/GuestLayout.vue'),
            children: [
                {
                    path: '',
                    name: 'login',
                    component: () => import('../views/LoginView.vue'),
                    meta: { title: 'Iniciar sesión', auth: false }
                }
            ]
        }
    ]
})

router.beforeEach((to, from, next) => {
    document.title = to.meta.title || 'Mi Aplicación';
    const requiresAuth = to.meta.auth;
    const token = localStorage.getItem('token');

    if (requiresAuth && !token) {
        return next('/login');
    }

    next();
})

export default router