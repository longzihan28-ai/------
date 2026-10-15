<template>
    <div class="knowledge-container">
        <div class="header-section">
            <div class="header-content">
                <el-image :src="iconUrl" style="width: 60px;height: 60px"></el-image>
                <h1>心理健康知识库</h1>
            </div>
        </div>
        <div class="content">
            <div class="recommend-section">
                <div class="section-title">推荐阅读</div>
                <div class="recommend-list">
                    <div v-for="item in recommendList" :key="item.id" class="recommend-item" @click="goToArticle(item.id)">
                        <h4>{{ item.title }}</h4>
                        <p class="read-count">
                            <el-icon><Histogram /></el-icon>
                            阅读量{{ item.readCount }}
                        </p>
                    </div>
                </div>
            </div>
            <div class="article-list">
                <div v-for="item in articleList" :key="item.id" class="article-item" @click="goToArticle(item.id)">
                    <el-image style="width: 240px;height: 150px" :src="getImage(item.coverImage)"></el-image>
                    <div class="info">
                        <div class="title">
                            <h3>{{ item.title }}</h3>
                            <el-tag Plain type="primary">{{ item.categoryName }}</el-tag>
                        </div>
                        <div :style="{marginTop: '10px'}">
                            <div class="flex-box">
                                <el-icon><Avatar /></el-icon>
                                <span>{{ item.authorName }}</span>
                            </div>
                            <div class="flex-box">
                                <el-icon><List /></el-icon>
                                <span>{{ dayjs(item.updateAt).format('YYYY-MM-DD') }}</span>
                            </div>
                        </div>
                        <div :style="{marginTop: '10px'}">
                            <div class="flex-box">
                                <el-icon><Platform /></el-icon>
                                <span>观看人数：{{ item.readCount }}</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="pagination-wrapper">
                <el-pagination
                style="margin-top: 25px;"
                :page-size="pagination.size"
                layout="prev, pager, next"
                :total="pagination.total"
                @change="handleChange"
                />
            </div>
    </div>
</template>

<script setup>
import { dayjs,ElMessage } from 'element-plus'
import { ref,reactive,onMounted } from 'vue'
import { getKnowledgeList } from '../api/frontend'
import { useRouter } from 'vue-router'

const router = useRouter()

const iconUrl = new URL(`../assets/images/book.png`,import.meta.url).href

const recommendList = ref([])

const articleList = ref([])

const pagination = reactive({
    currentPage: 1,
    size: 10,
    total: 0
})

const goToArticle = (id) => {
    router.push(`/knowledge/article/${id}`)
}

const getPageList = () => {
    const params = {
        sortField: 'publishedAt',
        sortDirection: 'desc',
        currentPage: pagination.currentPage,
        size: pagination.size
    }
    getKnowledgeList(params).then(res => {
        articleList.value = res.records
        pagination.total = res.total
    })
}

const handleChange = (page) => {
    pagination.currentPage = page
    getPageList()
}

const getImage = (url) => {
    //后端返回相对路径（如 /upload/xx.png），需拼接后端主机；注意主机与端口之间是冒号
    return url ? 'http://159.75.169.224:1235' + url : 'https://file.itndedu.com/psychology_ai.png'
}

onMounted (()=> {
    const params = {
        sortField: 'readCount',
        sortDirection: 'desc',
        currentPage: 1,
        size: 5
    }
    getKnowledgeList(params).then(res => {
        recommendList.value=res.records
    })
    //加载右侧文章列表（原代码未调用，导致 articleList 始终为空、图片不渲染）
    getPageList()
})

</script>

<style lang="scss" scoped>
.knowledge-container {
    background: linear-gradient(135deg, #fafbfc 0%, #f7f9fc 50%, #f2f6fa 100%);
    .flex-box {
        display: flex;
        align-items: center;
        span {
            margin-left: 10px;
        }
    }
    .header-section {
        background: linear-gradient(135deg, #f59e0b 0%, #8b5cf6 100%);
        color: white;
        padding: 48px;
        .header-content {
            display: flex;
            align-items: center;
            gap: 12px;
        }
    }
    .content {
        display: flex;
        //两列顶部对齐：推荐阅读卡片高度随自身内容自适应，不被右侧文章列表拉伸
        align-items: flex-start;
        gap: 20px;
        margin: 0 auto;
        width: 1200px;
        padding: 20px;
        .recommend-section {
            width: 280px;
            background: white;
            border-radius: 12px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
            padding: 15px;
            .section-title {
                font-size: 12px;
                font-weight: 600;
                color: #374151;
                margin-bottom: 10px;
                display: flex;
                align-items: center;
                gap: 5px;
            }
            .recommend-list {
                display: flex;
                flex-direction: column;
                gap: 1rem;
                .recommend-item {
                    border-left: 4px solid #f59e0b;
                    padding-left: 10px;
                    cursor: pointer;
                    .read-count {
                        margin-top: 15px;
                        font-size: 12px;
                        color: #6b7280;
                        display: flex;
                        align-items: center;
                        gap: 10px;
                    }
                }
            }
        }
        .article-list {
            flex: 1;
            .article-item {
                background: white;
                border-radius: 12px;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
                padding: 15px;
                margin-bottom: 20px;
                display: flex;
                .info {
                    margin-left: 20px;
                    .title {
                        display: flex;
                        align-items: center;
                        gap: 10px;
                    }
                }
            }
        }
    }
    .pagination-wrapper {
        display: flex;
        justify-content: center;
        padding-bottom: 30px;
    }
}

</style>