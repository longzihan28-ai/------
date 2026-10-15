import service from '../utils/request'

export const register = (data) => {
    return service.post('/user/add',data)
}

export const startSession = (data) => {
    //AI生成回复可能较慢，单独设置60秒超时（全局默认5秒会导致AI响应被误判为超时错误）
    return service.post('/psychological-chat/session/start',data,{ timeout: 60000 })
}

export const getSessionList = (params) => {
    return service.get('/psychological-chat/sessions',{params})
}

export const deleteSession = (sessionId) => {
    return service.delete(`/psychological-chat/sessions/${sessionId}`)
}

export const getSessionDetail = (sessionId) => {
    //历史消息包含完整对话内容（AI长篇回复），数据量大时全局5秒超时不够，单独设为30秒
    return service.get(`/psychological-chat/sessions/${sessionId}/messages`, { timeout: 30000 })
}

export const getSessionEmotion = (sessionId, config = {}) => {
    return service.get(`/psychological-chat/session/${sessionId}/emotion`, config)
}

export const addEmotionDiary = (data) => {
    return service.post('/emotion-diary',data)
}

export const getKnowledgeList = (params) => {
    return service.get('/knowledge/article/page',{params})
}

export const getKnowledgeDetail = (articleId) => {
    return service.get(`/knowledge/article/${articleId}`)
}