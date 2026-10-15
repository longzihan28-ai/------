<template>
    <div class="consultation-container">
        <div class="sidebar">
            <div class="ai-assistant-info">
                <div class="breathing-circle">
                    <el-image :src="iconUrl" style="width: 25px;height:25px" alt="AI助手" />
                </div>
                <h3 class="assistant-name">宁渡AI助手</h3>
                <div class="online-status">
                    <div class="status-dot"></div>
                    在线服务中
                </div>
            </div>
            <div class="emotion-garden">
                <div class="garden-header">
                    <div class="garden-title">情绪花园</div>
                </div>
                <div class="emotion-info">
                    <div class="emotion-name">{{ currentEmotion.primaryEmotion }}</div>
                    <div class="emotion-score">{{ currentEmotion.emotionScore }} · {{ getEmotionStatusText(currentEmotion.emotionScore) }}</div>
                </div>
                <div class="warm-tips">
                    <div class="emotion-status-text">
                        <span class="status-label">今天感觉</span>
                        <span class="status-emotion">{{ currentEmotion.isNegative ? '需要关注' : '很不错' }}</span>
                    </div>
                    <div class="emotion-intensity">
                        <span class="intensity-dots">
                            <span v-for="dot in 3" :key="dot" class="dot" :class="{'active': getIntensityClass(currentEmotion.emotionScore) >= dot}"></span>
                        </span>
                        <span class="intensity-text">
                            {{ getRiskText(currentEmotion.riskLevel) }}
                        </span>
                    </div>
                    <div class="warm-suggestion" v-if="currentEmotion.suggestion">
                        <div class="suggestion-icon">💝</div>
                        <div class="suggestion-content">
                            <div class="suggestion-title">给你个建议</div>
                            <div class="suggestion-text">{{ currentEmotion.suggestion }}</div>
                        </div>
                    </div>
                    <div class="healing-actions" v-if="currentEmotion.improvementSuggestions.length > 0">
                        <div class="actions-title">治愈小行动</div>
                        <div class="actions-list">
                            <div v-for="action in currentEmotion.improvementSuggestions" :key="action" class="action-item">
                                <div class="action-icon">✨</div>
                                <div class="action-text">{{ action }}</div>
                            </div>
                        </div>
                    </div>
                    <div class="risk-notice" v-if="currentEmotion.isNegative && currentEmotion.riskLevel > 1">
                        <div class="notice-icon">🤗</div>
                        <div class="notice-content">
                            <div class="notice-title">温馨提示</div>
                            <div class="notice-text">{{ currentEmotion.riskDescription }}</div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="session-history">
                <h4 class="section-title">会话列表</h4>
                <div class="session-list">
                    <div v-for="session in sessionList" :key="session.id" @click="handleSessionClick(session)" :class="['session-item', { active: currentSession && currentSession.id === session.id }]">
                        <div class="session-info">
                            <div class="session-title">
                                <span>{{ session.sessionTitle }}</span>
                                <div class="session-meta">
                                    <span class="session-time">{{ session.startedAt }}</span>
                                </div>
                                <div class="session-preview">
                                    {{ session.lastMessageContent }}
                                </div>
                                <div class="session-stats">
                                    <span>
                                        <el-icon>
                                            <ChatRound />
                                        </el-icon>
                                        {{ session.messageCount || 0 }}
                                    </span>
                                    <span>
                                        <el-icon>
                                            <Clock />
                                        </el-icon>
                                        {{ session.durationMinutes || 0 }} 分钟
                                    </span>
                                </div>
                            </div>
                            <div class="session-actions">
                                <el-button text type="danger" size="small" @click.stop="handleDeleteSession(session.id)">
                                    <el-icon>
                                        <DeleteFilled />
                                    </el-icon>
                                </el-button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="chat-main">
            <div class="chat-header">
                <div class="header-left">
                    <div class="chat-avatar">
                        <el-image :src="iconUrl1" style="width: 30px;height: 30px" />
                    </div>
                    <div class="chat-info">
                        <h2>宁渡AI助手</h2>
                        <p>您的贴心AI心理健康助手</p>
                    </div>
                </div>
                <el-button circle @click="createNewFrontendSession" title="新建会话">
                    <el-icon>
                        <Plus />
                    </el-icon>
                </el-button>
            </div>
            <div class="chat-message" v-loading="messagesLoading" element-loading-text="正在加载历史消息...">
                <div class="message-item ai-message" v-if="message.length ===  0">
                    <div class="message-avatar">
                        <el-image :src="iconUrl" style="width: 18px;height: 18px" />
                    </div>
                    <div class="message-content">
                        <div class="message-bubble">
                            <p>您好，我是小暖，您的AI心理健康助手，很高兴陪伴您，为您提供温暖的心理健康支持，请告诉我，今天感觉怎么样，有什么要分享给我的吗？</p>
                        </div>
                        <div class="message-time">刚刚</div>
                    </div>
                </div>
                <div v-for="msg in message" :key="msg.id" class="message-item" :class="msg.senderType === 1 ? 'user-message' : 'ai-message'">
                    <div class="message-avatar">
                        <el-image v-if="msg.senderType === 1" style="width: 18px;height: 18px" :src="iconUrl2"></el-image>
                        <el-image v-if="msg.senderType === 2" style="width: 18px;height: 18px" :src="iconUrl"></el-image>
                    </div>
                    <div class="message-content">
                        <div class="message-bubble">
                            <div v-if="msg.senderType === 2 && isAiTyping && !msg.content" class="typing-indicator">
                                <div class="typing-dot"></div>
                                <div class="typing-dot"></div>
                                <div class="typing-dot"></div>
                            </div>
                            <div v-else-if="msg.isError" class="error-message">
                                <p>{{ msg.content }}</p>
                            </div>
                            <MarkdownRenderer v-else-if="msg.senderType === 2 && !msg.isError" :content="msg.content" :is-ai-message="true" />
                            <p v-else-if="msg.content" v-html="formatMessageContent(msg.content)"></p>
                        </div>
                        <div class="message-time">{{ msg.senderType === 2 && isAiTyping && !msg.content ? '正在输入中' : msg.createdAt }}</div>
                    </div>
                </div>
            </div>
            <div class="chat-input">
                <div class="input-container">
                    <el-input
                    v-model="userMessage"
                    placeholder="请输入您想要分享的内容..."
                    type="textarea"
                    :row="3"
                    :disabled="isAiTyping"
                    @keydown="handleKeyDown"
                    class="message-input"
                    clearable />
                    <div class="input-footer">
                        <span>按Enter发送，Shift+Enter换行</span>
                        <span>{{ userMessage.length }}/500</span>
                    </div>
                </div>
                <el-button :disabled="!userMessage.trim() || userMessage.length > 500" type="primary" class="send-btn" @click="sendMessage">
                    <el-icon>
                        <Promotion />
                    </el-icon>
                </el-button>
            </div>
        </div>
    </div>
</template>

<script setup>

import { Plus } from '@element-plus/icons-vue'
import { ref,onMounted,nextTick } from 'vue'
import { startSession,getSessionList,deleteSession,getSessionDetail,getSessionEmotion } from '../api/frontend'
import { ElMessage } from 'element-plus'
import MarkdownRenderer from '../components/MarkdownRenderer.vue'
import { fetchEventSource} from '@microsoft/fetch-event-source'

const iconUrl = new URL('../assets/images/robot-fill.png',import.meta.url).href
const iconUrl1 = new URL('../assets/images/like.png',import.meta.url).href
const iconUrl2 = new URL('../assets/images/users.png',import.meta.url).href

//新建会话
const createNewFrontendSession = () => {
    //AI正在回复时不允许新建，避免回复写入已废弃的会话
    if(isAiTyping.value) {
        ElMessage.warning('AI正在回复中，请稍候再新建会话')
        return
    }
    currentSession.value = {
        sessionId: `temp-${Date.now()}`,
        status: 'TEMP',
        sessionTitle: '新对话'
    }
    //重置聊天区，让点击立即产生可见反馈
    message.value = []
    userMessage.value = ''
    //重置情绪花园为默认状态
    currentEmotion.value = getDefaultEmotion()
    nextTick(() => {
        const box = document.querySelector('.chat-message')
        if(box) box.scrollTop = 0
    })
}

//定义当前会话
const currentSession = ref(null)
const sessionList = ref([])

//定义对话消息
const message = ref([])

//定义用户输入消息
const userMessage = ref('')

//定义AI助手是否正在输入
const isAiTyping = ref(false)

//情绪花园默认状态（新会话/分析未生成时展示）
const getDefaultEmotion = () => ({
    primaryEmotion: '中性',
    emotionScore: 50,
    isNegative: false,
    riskLevel: 0,
    suggestion: '情绪状态平稳',
    riskDescription: '',
    improvementSuggestions: []
})
const currentEmotion = ref(getDefaultEmotion())

//加载某个会话的情绪分析；后端分析结果可能在AI回复结束后延迟生成，失败时静默重试几次
const loadSessionEmotion = (sessionId, retry = 0) => {
    if(!sessionId || String(sessionId).startsWith('temp-')) return
    //后端要求 session_ 前缀的字符串id
    const id = String(sessionId).startsWith('session_') ? sessionId : `session_${sessionId}`
    getSessionEmotion(id, { silent: true }).then(res => {
        currentEmotion.value = {
            primaryEmotion: res.primaryEmotion ?? '中性',
            emotionScore: res.emotionScore ?? 50,
            isNegative: !!res.isNegative,
            riskLevel: res.riskLevel ?? 0,
            suggestion: res.suggestion || '情绪状态平稳',
            riskDescription: res.riskDescription || '',
            improvementSuggestions: Array.isArray(res.improvementSuggestions) ? res.improvementSuggestions : []
        }
    }).catch(() => {
        //分析结果尚未生成，2秒后重试，最多3次；仍失败则保持当前状态
        if(retry < 3 && currentSession.value?.sessionId === id) {
            setTimeout(() => loadSessionEmotion(id, retry + 1), 2000)
        }
    })
}

const getIntensityClass = (score) => {
    if(score >= 61) {
        return 3
    }
    if(score >=31) {
        return 2
    }
    return 1
}

//情绪评分对应的十级状态词：0-100分每10分一档（0-9绝望崩溃 … 90-100极致幸福）
const emotionStatus = ['绝望崩溃', '消沉抑郁', '焦虑烦躁', '低落不悦', '平静淡然', '轻松惬意', '愉悦舒心', '欢欣满足', '兴奋欣喜', '极致幸福']
const getEmotionStatusText = (score) => {
    const s = Number(score)
    if(Number.isNaN(s)) return emotionStatus[4]
    const index = Math.min(9, Math.max(0, Math.floor(s / 10)))
    return emotionStatus[index]
}

const getRiskText = (level) => {
    switch (level) {
        case 0:
            return '正常'
        case 1:
            return '关注'
        case 2:
            return '预警'
        case 3:
            return '危机'
        case 4:
            return '正常'
    }
}

//格式化消息内容：先转义HTML防止XSS，再把换行符转为<br>
const formatMessageContent = (content) => {
    const div = document.createElement('div')
    div.textContent = content
    return div.innerHTML.replace(/\n/g, '<br>')
}

//定义处理键盘事件
const handleKeyDown = (e) =>{
    if(e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault()
        sendMessage()
    }
}

const sendMessage = () =>{
    const content = userMessage.value.trim()
    if(!content) return

    //只有AI正在回复时才拦截发送
    if(isAiTyping.value) {
        ElMessage.error('AI助手正在回复中，请稍候')
        return
    }

    userMessage.value = ''

    //将用户消息显示在聊天窗口（senderType 1=用户 2=AI）
    message.value.push({
        id: `local-user-${Date.now()}`,
        senderType: 1,
        content: content,
        createdAt: new Date().toLocaleTimeString()
    })

    //新会话：先创建会话再发起流式回复；已有会话：直接发起流式回复
    if(currentSession.value && currentSession.value.status === 'TEMP') {
        startNewSession(content)
    } else if(currentSession.value && currentSession.value.sessionId) {
        startAIResponse(currentSession.value.sessionId, content)
    }
}

const startNewSession = (content) => {
    //构建会话参数
    const sessionParams = {
        initialMessage: content,
        sessionTitle: currentSession.value.sessionTitle === '新对话'
            ? `宁渡AI助手 - ${new Date().toLocaleString()}`
            : currentSession.value.sessionTitle
    }

    //先推送一条空的AI消息，用于显示"正在输入"动画
    const aiMsg = {
        id: `local-ai-${Date.now()}`,
        senderType: 2,
        content: '',
        createdAt: ''
    }
    message.value.push(aiMsg)

    isAiTyping.value = true
    //调用后端接口创建新的会话（后端会保存用户的首条消息）
    startSession(sessionParams).then(res => {
        //临时会话更新为正式会话
        Object.assign(currentSession.value, {
            sessionId: res.sessionId,
            status: res.status,
            sessionTitle: sessionParams.sessionTitle
        })
        //刷新左侧会话列表
        getSessionPage()
        //创建成功后发起流式AI回复（复用已推入的占位气泡）
        startAIResponse(res.sessionId, content, aiMsg)
    }).catch(() => {
        aiMsg.content = '会话创建失败，请重试'
        aiMsg.isError = true
        isAiTyping.value = false
    })
}

//发起流式AI回复；existingAiMsg 用于复用新会话时已推入的占位气泡
const startAIResponse = (sessionId, content, existingAiMsg) => {
    const aiMessage = existingAiMsg || {
        id: `ai_${Date.now()}_${Math.random().toString(36).slice(2,9)}`,
        senderType: 2,
        content: '',
        createdAt: ''
    }
    if(!existingAiMsg) message.value.push(aiMessage)
    //关键：必须通过数组返回的响应式代理对象修改内容，
    //直接改原始对象 aiMessage 会绕过 Vue 的 Proxy，流式过程中界面不会逐字更新
    const aiProxy = message.value.find(m => m.id === aiMessage.id) || aiMessage

    isAiTyping.value = true

    const ctrl = new AbortController() //用来终止fetch请求
    let finished = false

    //正常结束/异常都只收尾一次
    const finish = () => {
        if(finished) return
        finished = true
        if(!aiProxy.content) {
            aiProxy.content = 'AI暂时没有回复内容，请重试'
            aiProxy.isError = true
        }
        aiProxy.createdAt = new Date().toLocaleTimeString()
        isAiTyping.value = false
        //刷新左侧会话列表（最后一条消息、消息数等）
        getSessionPage()
        //本轮对话结束，刷新当前会话的情绪分析
        if(currentSession.value?.sessionId) {
            loadSessionEmotion(currentSession.value.sessionId)
        }
        ctrl.abort()
    }

    fetchEventSource('/api/psychological-chat/stream',{
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'text/event-stream',
            'token': localStorage.getItem('token') || ''
        },
        body: JSON.stringify({
            sessionId,
            userMessage: content
        }),
        signal: ctrl.signal,
        //连接建立时校验响应类型，非流式响应直接抛错走onerror
        async onopen(response) {
            if(!response.ok) {
                throw new Error(`连接失败(${response.status})`)
            }
            const contentType = response.headers.get('Content-Type') || ''
            if(!contentType.includes('text/event-stream')) {
                const text = await response.text().catch(() => '')
                throw new Error(text || '服务器返回非流式数据')
            }
        },
        onmessage: (event) => {
            //结束信号
            if(event.event === 'done') {
                finish()
                return
            }
            const raw = (event.data || '').trim()
            //心跳空块直接忽略
            if(!raw || raw === '{}') return
            let payload
            try {
                payload = JSON.parse(raw)
            } catch(e) {
                return
            }
            if(String(payload.code) === '200') {
                //逐字累积AI回复（通过响应式代理修改才能触发界面实时更新）
                if(payload.data && payload.data.content) {
                    aiProxy.content += payload.data.content
                }
            } else {
                //业务错误交给onerror统一收尾
                throw new Error(payload.msg || payload.message || 'AI回复失败')
            }
        },
        onerror: (err) => {
            //已有部分回复时保留内容，不覆盖成错误提示
            if(!aiProxy.content) {
                aiProxy.content = 'AI回复失败，请重试'
                aiProxy.isError = true
            }
            finish()
            ElMessage.error('AI回复失败，请重试')
            //抛出错误以阻止 fetch-event-source 自动重连
            throw err
        },
        onclose: () => {
            finish()
        }
    })
}

const getSessionPage = () => {
    getSessionList({
        pageNum: 1,
        pageSize: 10
    }).then(res => {
        console.log(res)
        sessionList.value = res.records
    })
}

//历史消息请求序号，防止快速切换会话时旧响应覆盖新会话
let sessionReqSeq = 0

//历史消息加载中状态（网络慢时给用户明确反馈）
const messagesLoading = ref(false)

//获取会话数据
const handleSessionClick = (session) => {
    //列表项使用数字id，后端sessionId为 session_ + id
    const sessionId = session.sessionId || `session_${session.id}`

    //更新当前会话数据对象（供继续对话时调用流式接口）
    currentSession.value = {
        sessionId,
        id: session.id,
        status: 'ACTIVE',
        sessionTitle: session.sessionTitle
    }

    //加载该会话的情绪分析（情绪花园）
    loadSessionEmotion(sessionId)

    //每次点击递增序号，只有最后一次点击的响应才会渲染
    const reqSeq = ++sessionReqSeq
    //加载超过5秒才显示加载动画，快速加载时不打扰用户
    const loadingTimer = setTimeout(() => {
        if(reqSeq === sessionReqSeq) {
            messagesLoading.value = true
        }
    }, 5000)
    getSessionDetail(session.sessionId || session.id).then(res => {
        if(reqSeq !== sessionReqSeq) return
        message.value = Array.isArray(res) ? res : []
        //切换后滚动到最新消息
        nextTick(() => {
            const box = document.querySelector('.chat-message')
            if(box) box.scrollTop = box.scrollHeight
        })
    }).catch((err) => {
        if(reqSeq !== sessionReqSeq) return
        //打印真实失败原因，便于定位（HTTP状态/业务错误/超时）
        console.error('加载历史消息失败:', err)
        ElMessage.error('历史消息加载失败')
    }).finally(() => {
        clearTimeout(loadingTimer)
        //只有最后一次点击的请求才复位loading，避免快速切换时闪烁
        if(reqSeq === sessionReqSeq) {
            messagesLoading.value = false
        }
    })
}

//删除历史会话
const handleDeleteSession = (sessionId) =>{
    deleteSession(sessionId).then(res =>{
        ElMessage.success('删除成功')
        //如果删除的是当前正在查看的会话，清空聊天区
        if(currentSession.value && (currentSession.value.id === sessionId
            || currentSession.value.sessionId === `session_${sessionId}`)) {
            message.value = []
            createNewFrontendSession()
        }
        getSessionPage()
    }).catch(() => {
        //错误提示已由请求拦截器统一弹出（如"会话不存在"），这里只需兜底刷新列表
        getSessionPage()
    })
}

onMounted(()=>{
    //初始化时获取会话列表
    getSessionPage()
    //初始化时创建一个新会话
    createNewFrontendSession()
})

</script>

<style lang="scss" scoped>
.consultation-container {
    margin: 0 auto;
    max-width: 1200px;
    width: 100%;
    box-sizing: border-box;
    display: flex;
    gap: 20px;
    padding: 20px;
    .sidebar {
        width: 320px;
        .ai-assistant-info {
            margin-bottom: 20px;
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.9) 0%, rgba(255, 252, 248, 0.95) 100%);
            border-radius: 16px;
            padding: 16px;
            box-shadow: 0 8px 32px rgba(251, 146, 60, 0.06), 0 2px 8px rgba(0, 0, 0, 0.04);
            border: 1px solid rgba(251, 146, 60, 0.08);
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
            .breathing-circle {
                width: 60px;
                height: 60px;
                background: linear-gradient(135deg, #fb923c 0%, #f59e0b 100%);
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                margin: 0 auto 12px;
                animation: breathing 4s ease-in-out infinite;
                box-shadow: 0 6px 24px rgba(251, 146, 60, 0.25);
                position: relative;
            }
            .assistant-name {
                font-size: 16px;
                font-weight: 700;
                background: linear-gradient(135deg, #fb923c, #f59e0b);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                text-align: center;
                background-clip: text;
                margin: 0 0 12px;
            }
            .online-status {
                display: flex;
                align-items: center;
                justify-content: center;
                color: #059669;
                font-size: 12px;
                font-weight: 600;
                .status-dot {
                    width: 8px;
                    height: 8px;
                    background: #059669;
                    border-radius: 50%;
                    margin-right: 8px;
                    animation: pulse 2s infinite;
                    box-shadow: 0 0 8px rgba(5, 150, 105, 0.4);
                }
            }
        }
        .session-history {
            background: white;
            border-radius: 16px;
            padding: 16px;
            box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
            min-height: 250px;
            display: flex;
            flex-direction: column;
            .section-title {
                font-size: 16px;
                font-weight: 600;
                color: #333;
                margin: 0 0 16px;
                display: flex;
                align-items: center;
                justify-content: space-between;
                
            }
            .session-list {
                overflow-y: auto;
                max-height: 200px;
                scrollbar-width: thin;
                scrollbar-color: rgba(64, 150, 255, 0.3) transparent;
                .session-item {
                    position: relative;
                    display: flex;
                    align-items: flex-start;
                    gap: 12px;
                    padding: 12px;
                    margin-bottom: 8px;
                    border-radius: 12px;
                    cursor: pointer;
                    transition: all 0.3s ease;
                    border: 2px solid transparent;
                    &:hover {
                        background: #f8f9ff;
                        border-color: #e6f0ff;
                    }
                    &.active {
                        background: #e6f0ff;
                        border-color: #4096ff;
                    }
                    .session-info {
                        flex: 1;
                        .session-title {
                            font-weight: 500;
                            font-size: 14px;
                            color: #333;
                            margin-bottom: 4px;
                            white-space: nowrap;
                            overflow: hidden;
                            text-overflow: ellipsis;
                            .session-meta {
                                display: flex;
                                align-items: center;
                                gap: 8px;
                                margin-bottom: 6px;
                                .session-time {
                                    font-size: 12px;
                                    color: #999;
                                }
                            }
                            .session-preview {
                                width: 200px;
                                font-size: 12px;
                                color: #666;
                                margin-bottom: 6px;
                                white-space: nowrap;
                                overflow: hidden;
                                text-overflow: ellipsis;
                            }
                            .session-stats {
                                display: flex;
                                align-items: center;
                                gap: 12px;
                                span {
                                    font-size: 12px;
                                    color: #999;
                                    display: flex;
                                    align-items: center;
                                    gap: 4px;
                                }
                            }
                        }
                        .session-actions {
                            position: absolute;
                            top: 10px;
                            right: 12px;
                        }
                    }
                }
                .no-sessions-text {
                    text-align: center;
                    font-size: 14px;
                    color: #999;
                }
            }
        }
        .emotion-garden {
            background: linear-gradient(135deg, #fef9e7 0%, #fcf4e6 50%, #f6f0e8 100%);
            border-radius: 20px;
            padding: 16px;
            margin-bottom: 20px;
            box-shadow: 0 8px 32px rgba(252, 244, 230, 0.8);
            border: 1px solid rgba(255, 255, 255, 0.2);
            position: relative;
            overflow: hidden;
            min-height: 300px;
            
            .garden-header {
                display: flex;
                align-items: center;
                justify-content: space-between;
                margin-bottom: 20px;
                position: relative;
                z-index: 2;
                .garden-title {
                    display: flex;
                    align-items: center;
                    gap: 8px;
                    font-size: 16px;
                    font-weight: 600;
                    color: #8b4513;
                }
            }
            .emotion-info {
                margin: 0 auto;
                width: 80px;
                height: 80px;
                border-radius: 50%;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                z-index: 10;
                box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
                border: 2px solid rgba(255, 255, 255, 0.8);
                background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 50%, #fecfef 100%);
                color: #fff;
                .emotion-name {
                    font-size: 15px;
                    font-weight: 600;
                    line-height: 1;
                    margin-bottom: 2px;
                }
                .emotion-score {
                    font-size: 14px;
                    font-weight: 700;
                    opacity: 0.9;
                }
            }
            .warm-tips {
                text-align: center;
                margin-bottom: 16px;
                .emotion-status-text {
                    margin-bottom: 12px;
                    .status-label {
                        font-size: 14px;
                        color: #8b7355;
                        margin-right: 8px;
                    }
                    .status-emotion {
                        font-size: 16px;
                        font-weight: 600;
                        padding: 4px 12px;
                        border-radius: 16px;
                        display: inline-block;
                    }
                }
                .emotion-intensity {
                    margin-bottom: 16px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    gap: 8px;
                    .intensity-dots {
                        display: flex;
                        gap: 4px;
                        .dot {
                            width: 8px;
                            height: 8px;
                            border-radius: 50%;
                            background: #e0e0e0;
                            transition: all 0.3s ease;
                            &.active {
                                background: linear-gradient(135deg, #ff9a9e, #fecfef);
                                transform: scale(1.2);
                                box-shadow: 0 2px 8px rgba(255, 154, 158, 0.4);
                            }
                        }
                    }
                    .intensity-text {
                        font-size: 12px;
                        color: #8b7355;
                        font-weight: 500;
                    }
                }
                .warm-suggestion {
                    background: linear-gradient(135deg, rgba(255, 255, 255, 0.95), rgba(255, 255, 255, 0.8));
                    border-radius: 16px;
                    padding: 12px;
                    margin-bottom: 16px;
                    display: flex;
                    align-items: flex-start;
                    gap: 10px;
                    border: 1px solid rgba(255, 255, 255, 0.6);
                    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08);
                    .suggestion-icon {
                        font-size: 20px;
                        flex-shrink: 0;
                        margin-top: 2px;
                    }
                    .suggestion-content {
                        text-align: left;
                        flex: 1;
                        .suggestion-title {
                            font-size: 14px;
                            font-weight: 600;
                            color: #8b7355;
                            margin-bottom: 6px;
                        }
                        .suggestion-text {
                            font-size: 13px;
                            color: #6b5b47;
                            line-height: 1.5;
                        }
                    }
                }
                .healing-actions {
                    margin-bottom: 16px;
                    .actions-title {
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        gap: 8px;
                        font-size: 14px;
                        font-weight: 600;
                        color: #8b7355;
                        margin-bottom: 16px;
                    }
                    .actions-list {
                        display: flex;
                        flex-direction: column;
                        gap: 10px;
                        .action-item {
                            background: linear-gradient(135deg, rgba(255, 255, 255, 0.9), rgba(255, 255, 255, 0.7));
                            border-radius: 12px;
                            padding: 12px;
                            display: flex;
                            align-items: center;
                            gap: 10px;
                            border: 1px solid rgba(255, 255, 255, 0.5);
                            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
                            text-align: left;
                            .action-icon {
                                font-size: 14px;
                                color: #ffd700;
                                flex-shrink: 0;
                            }
                            .action-text {
                                font-size: 12px;
                                color: #6b5b47;
                                line-height: 1.4;
                                flex: 1;
                            }
                        }
                    }
                }
                .risk-notice {
                    background: linear-gradient(135deg, #fff9e6, #ffeaa7);
                    border-radius: 16px;
                    padding: 16px;
                    display: flex;
                    align-items: flex-start;
                    gap: 12px;
                    border: 1px solid rgba(255, 234, 167, 0.6);
                    box-shadow: 0 6px 20px rgba(255, 234, 167, 0.3);
                    .notice-icon {
                        font-size: 20px;
                        flex-shrink: 0;
                        margin-top: 2px;
                    }
                    .notice-content {
                        flex: 1;
                        .notice-title {
                            font-size: 14px;
                            font-weight: 600;
                            color: #d4840f;
                            margin-bottom: 6px;
                        }
                        .notice-text {
                            font-size: 13px;
                            color: #b8740c;
                            line-height: 1.5;
                        }
                    }
                }
            }
        }
    }
    .chat-main {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(255, 252, 250, 0.98) 100%);
        border-radius: 20px;
        box-shadow: 0 12px 40px rgba(251, 146, 60, 0.08), 0 4px 16px rgba(0, 0, 0, 0.04);
        border: 1px solid rgba(251, 146, 60, 0.1);
        backdrop-filter: blur(10px);
        display: flex;
        flex-direction: column;
        overflow: hidden;
        flex: 1;
        .chat-header {
            background: linear-gradient(135deg, #fb923c 0%, #f59e0b 100%);
            color: white;
            padding: 20px 24px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            position: relative;
            flex-shrink: 0;
            .header-left {
                display: flex;
                align-items: center;
                .chat-avatar {
                    width: 48px;
                    height: 48px;
                    background: rgba(255, 255, 255, 0.25);
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    margin-right: 16px;
                    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
                    position: relative;
                    z-index: 1;
                }
                .chat-info {
                    h2 {
                        font-size: 20px;
                        font-weight: 700;
                        margin-bottom: 4px;
                    }
                    p {
                        font-size: 14px;
                    }
                }
            }
        }
        .chat-message {
            flex: 1;
            overflow-y: auto;
            padding: 24px;
            display: flex;
            flex-direction: column;
            gap: 16px;
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.02) 0%, rgba(255, 252, 248, 0.05) 100%);
            min-height: 0;
            max-height: calc(100vh - 200px);
            scrollbar-width: thin;
            scrollbar-color: rgba(251, 146, 60, 0.3) transparent;
            .message-item {
                display: flex;
                align-items: flex-start;
                gap: 12px;
                .message-avatar {
                    width: 32px;
                    height: 32px;
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 14px;
                    color: white;
                    flex-shrink: 0;
                }
                &.ai-message {
                    .message-avatar {
                        background: linear-gradient(135deg, #fb923c, #f59e0b);
                        box-shadow: 0 4px 12px rgba(251, 146, 60, 0.3);
                    }
                }
                &.user-message {
                    .message-avatar {
                        background: linear-gradient(135deg, #6b7280, #4b5563);
                        box-shadow: 0 4px 12px rgba(107, 114, 128, 0.3);
                    }
                }
                .message-content {
                    max-width: 70%;
                    .message-bubble {
                        background: linear-gradient(135deg, rgba(255, 255, 255, 0.9) 0%, rgba(255, 252, 248, 0.95) 100%);
                        border-radius: 16px;
                        padding: 12px 16px;
                        position: relative;
                        animation: fadeInUp 0.4s ease-out;
                        border: 1px solid rgba(251, 146, 60, 0.1);
                        box-shadow: 0 4px 16px rgba(251, 146, 60, 0.05);
                        .typing-indicator {
                            display: flex;
                            gap: 4px;
                            padding: 8px 0;
                            .typing-dot {
                                width: 8px;
                                height: 8px;
                                background: #ccc;
                                border-radius: 50%;
                                animation: typing 1.5s ease-in-out infinite;
                                &:nth-child(2) {
                                    animation-delay: 0.2s;
                                }
                                &:nth-child(3) {
                                    animation-delay: 0.4s;
                                }   
                            }
                        }
                        /* 错误消息样式 */
                        .error-message {
                            background: linear-gradient(135deg, #FEF2F2 0%, #FECACA 100%);
                            border: 1px solid #F87171;
                            border-radius: 12px;
                            padding: 12px 16px;
                            color: #991B1B;
                            font-weight: 500;
                            display: flex;
                            align-items: center;
                            gap: 8px;
                        }
                    }
                    .message-time {
                        font-size: 12px;
                        color: #999;
                        margin-top: 4px;
                    }
                }
            }
        }
        .chat-input {
            border-top: 1px solid rgba(251, 146, 60, 0.1);
            padding: 20px 24px;
            display: flex;
            gap: 12px;
            align-items: flex-end;
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.5) 0%, rgba(255, 252, 248, 0.7) 100%);
            backdrop-filter: blur(10px);
            flex-shrink: 0;
            .input-container {
                flex: 1;
            }
            .input-footer {
                display: flex;
                justify-content: space-between;
                align-items: center;
                font-size: 12px;
                color: #78716c;
                font-weight: 500;
            }
            .send-btn {
                height: 60px;
                width: 60px;
                border-radius: 16px;
                background: linear-gradient(135deg, #fb923c 0%, #f59e0b 100%) !important;
                border: none !important;
                box-shadow: 0 6px 20px rgba(251, 146, 60, 0.25);
                transition: all 0.3s ease;
            }

        }

    }
}

</style>