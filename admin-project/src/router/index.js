import { createRouter , createWebHistory } from "vue-router";
import BackendLayout from "../components/BackendLayout.vue";
import AuthLayout from "../components/AuthLayout.vue";
import FrontendLayout from "../components/FrontendLayout.vue";

const backendRoutes = [
    {
        path: '/back',
        redirect: '/back/dashboard',
        component: BackendLayout,
        children: [
                {
                    path: 'dashboard',
                    component: ()=>import('../views/dashboard.vue'),
                    meta: {
                        title: '数据分析',
                        icon: 'PieChart'
                    }
                },
                {
                    path: 'knowledge',
                    component: ()=>import('../views/knowledge.vue'),
                    meta: {
                        title: '知识文章',
                        icon: 'ChatLineSquare'
                    }
                },
                {
                    path: 'emotional',
                    component: ()=>import('../views/emotional.vue'),
                    meta: {
                        title: '情绪日志',
                        icon: 'User'
                    }
                },
                {
                    path: 'consultations',
                    component: ()=>import('../views/consultations.vue'),
                    meta: {
                        title: '咨询记录',
                        icon: 'Message'
                    }
                }
        ]
    },
    {
        path: '/auth',
        component: AuthLayout,
        children: [
            {
                path: 'login',
                component: ()=>import('../views/login.vue'),
                meta: {
                    title: '登录'
                }
            },
            {
                path: 'register',
                component: ()=>import('../views/register.vue'),
                meta: {
                    title: '注册'
                }
            }
        ]
    }
]


const frontendRoutes = [
    {
        path: '/',
        component: FrontendLayout,
        children: [
            {
                path: '',
                component: ()=> import('../views/home.vue'),
                
            },
            {
                path: 'consultation',
                component: ()=> import('../views/consultation.vue')
            },
            {
                path: 'emotion-diary',
                component: ()=> import('../views/emotionDiary.vue')
            },
            {
                path: 'knowledge',
                component: ()=> import('../views/frontendKnowledge.vue')
            },
            {
                path: 'knowledge/article/:id',
                component: ()=> import('../views/articleDetail.vue'),
                props: true
            }
        ]
    }
]


const router = createRouter ({
    history: createWebHistory(),
    routes: [...backendRoutes,...frontendRoutes]
})

router.beforeEach((to, from, next) => {
    const token = localStorage.getItem('token')
    let userInfo = null
    try {
        userInfo = JSON.parse(localStorage.getItem('userInfo'))
    } catch (e) {
        userInfo = null
    }
    //未登录（无 token 或用户信息损坏）：仅首页和登录/注册页可访问，其余页面一律跳登录页
    if(!token || !userInfo) {
        if(to.path.startsWith('/auth') || to.path === '/') {
            next()
        } else {
            next('/auth/login')
        }
        return
    }

    if(userInfo.userType == 2){
        //管理员：只能进后台，其他地址统一跳到后台首页
        if(to.path.startsWith('/back')) {
            next()
        } else {
            next('/back/dashboard')
        }
    } else if(userInfo.userType == 1){
        //普通用户：可以访问前台页面，但不能进后台
        if(to.path.startsWith('/back') || to.path.startsWith('/auth')) {
            next('/')
        } else {
            next()
        }
    } else {
        //userType 缺失或异常（如测试数据）时视为未登录，跳登录页，保证 next() 必被调用
        next('/auth/login')
    }
})

export default router