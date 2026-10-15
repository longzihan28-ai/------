<template>
    <div class="frontend-layout">
        <div class="navbar-container">
            <div class="brand-section">
                <el-image style="width: 50px;height: 50px" :src="iconUrl" alt="品牌logo" class="brand-logo" />
                <h1 class="brand-name">心理健康AI助手</h1>
            </div>
            <div class="nav-section">
                <router-link to="/" class="nav-link">首页</router-link>
                <router-link to="/consultation" class="nav-link" v-if="isLoggedIn" >AI咨询</router-link>
                <router-link to="/emotion-diary" class="nav-link" v-if="isLoggedIn">情绪日志</router-link>
                <router-link to="/knowledge" class="nav-link" v-if="isLoggedIn">知识库</router-link>
                <el-button class="logout-btn" v-if="isLoggedIn" @click="handleLogout" >退出登录</el-button>
                <template v-else>
                    <router-link to="/auth/login" class="nav-link">登录</router-link>
                    <router-link to="auth/register" class="nav-link">
                        <el-button type="primary">注册</el-button>
                    </router-link>
                </template>
            </div>
        </div>
        <div class="main-content">
            <router-view></router-view>
        </div>
        <div class="footer-container">
            <div class="footer-bottom">
                <p>&copy; 2026 心理健康AI助手，All rights reserved.</p>
            </div>
        </div>
    </div>
</template>
<script setup>
import { ref, onMounted } from 'vue'
import { logout } from '../api/admin'
import { useRouter } from 'vue-router'
 
const iconUrl = new URL('../assets/images/机器人.png',import.meta.url).href

const isLoggedIn = ref(false)
const router = useRouter()

const handleLogout = () =>{
    logout().finally(()=>{
        //无论接口成功与否都清除本地登录状态
        localStorage.removeItem('token')
        localStorage.removeItem('userInfo')
        isLoggedIn.value = false
        router.push('/auth/login')
    })
}

onMounted(()=>{
    isLoggedIn.value = localStorage.getItem('token') !==null
})

</script>
<style lang="scss" scoped>
.frontend-layout {
        background-color: #fff;
        .navbar-container {
            max-width: 1200px;
            height: 100%;
            margin: 0 auto;
            padding: 10px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            .brand-section {
                display: flex;
                align-items: center;
                .brand-name {
                    margin-left: 10px;
                    font-size: 24px;
                    font-weight: 600;
                    color: #333;
                }
            }
            .nav-section {
                display: flex;
                align-items: center;
                gap: 40px;
                .nav-link {
                    color: #4b5563;
                    font-size: 16px;
                    font-weight: 500;
                    position: relative;
                    padding-bottom: 4px;
                    transition: color 0.2s ease;
                    &:hover {
                        color: #4A90E2;
                    }
                    //当前页面对应的导航项：主题色加深 + 底部指示条，便于识别所在页面
                    //用 exact-active 而非 active：子路由页面不会误点亮"首页"（/ 是所有子路由的父级）
                    &.router-link-exact-active {
                        color: #4A90E2;
                        font-weight: 600;
                        &::after {
                            content: '';
                            position: absolute;
                            left: 0;
                            right: 0;
                            bottom: 0;
                            height: 2px;
                            border-radius: 1px;
                            background: #4A90E2;
                        }
                    }
                }
            }
        }

        .footer-container {
            background: #1f2937;
            color: white;
            padding: 15px 0;
            margin-top: auto;
            .footer-bottom {
                max-width: 1200px;
                margin: 0 auto;
                padding: 0 10px;
                text-align: center;
            }
        }
    }

</style>