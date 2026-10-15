import axios from 'axios'
import { ElMessage } from 'element-plus'

const service = axios.create({
    baseURL: '/api',
    timeout: 5000,
})


//请求拦截器
service.interceptors.request.use(
    (config) =>{
        //在发送请求前做些什么
        const token = localStorage.getItem('token')
        if(token) {
            config.headers['token'] = token
        }
        return config
    },
        (error) => {
            return Promise.reject(error)
        }
)

//响应拦截器
service.interceptors.response.use(
    (response) =>{
        const {data, config} = response
        if(data.code ==='200' || data.code ==='2000') {
            return data.data
        }
        else {
            //code -1/500 等是后端业务错误码，只提示并拒绝Promise；
            //真正的登录过期由 HTTP 401/403 处理，不能在这里强制退出
            //config.silent 用于轮询类请求（如情绪分析），失败时由调用方自行处理，不弹全局提示
            if(!config.silent) {
                ElMessage.error(data.msg || '请求失败')
            }
            return Promise.reject(data.msg || '请求失败')
        }
        return response
    },
    (error) =>{
        const cfg = error.config || {}
        if(error.response) {
            const { status, data } = error.response
            if(status === 401 || status === 403) {
                ElMessage.error(data?.msg || '登录已过期，请重新登录')
                localStorage.removeItem('token')
                localStorage.removeItem('userInfo')
                window.location.href = '/auth/login'
            } else if(!cfg.silent) {
                ElMessage.error(data?.msg || `请求失败(${status})`)
            }
        } else if(!cfg.silent) {
            ElMessage.error(error.message || '网络错误')
        }
        return Promise.reject(error)
    }
)

export default service