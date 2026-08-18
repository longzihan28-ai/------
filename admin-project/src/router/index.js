import { createRouter , createWebHistory } from "vue-router";
import BackendLayout from "../components/BackendLayout.vue";

const backendRoutes = [
    {
        path: '/back',
        component: BackendLayout,
        children: [
                {
                    path: 'dashboard',
                    component: ()=>import('../views/dashboard.vue')
                }
        ]
    }
]

const router = createRouter ({
    history: createWebHistory(),
    routes: backendRoutes
})

export default router