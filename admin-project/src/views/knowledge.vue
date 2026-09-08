<script setup>
import {onMounted ,ref,reactive} from 'vue'
import PageHead from '../components/PageHead.vue';
import TableSearch from '../components/tableSearch.vue';
import { categoryTree ,articlePage} from '../api/admin.js';

const formItem=[
    {comp:'input',prop:'title',label:'文章标题',placeholder:'请输入文章标题'},
    {comp:'select',prop:'categoryId',label: '分类',placeholder:'请选择分类'},
    {comp:'select',prop:'status',label: '状态',placeholder: '请输入文章内容', options:[{
        label: '草稿',
        value: '0'
    },{
        label: '已发布',
        value: '1'
    },{
        label: '已下线',
        value: '2'
    }
]}
]

//分页参数
const pagination = reactive({
    currentPage: 1,
    size: 10,
    total: 0
})

const handleSearch = async(formData)=>{
    console.log(formData,'查询参数')

    const params = {
        ...pagination,
        ...formData
    }

    const { records,total } = await articlePage(params)
    tableData.value=records
}

const categoryMap = reactive({})

const categories = ref ([])

//列表数据
const tableData = ref([])

onMounted (async()=>{
    const data = await categoryTree()

    categories.value = data.map(item =>{
        categoryMap[item.id] = item.categoryName
        return {
            label: item.categoryName,
            value: item.id
        }
    })

    formItem[1].options=categories.value

    //获取列表
    handleSearch()
})

</script>

<template>
    <div>
        <PageHead title="知识文章">
            <template #buttons>
                <el-button type="primary">新增</el-button>
            </template>
        </PageHead>
        <TableSearch  :formItem="formItem" @search="handleSearch"/>
        <el-table :data="tableData" style="width: 100%;margin-top: 25px">
            <el-table-column width="450" label="文章标题" fixed="left">
                <template #default="scope">
                    <div style="display: flex; align-items: center;">
                        <el-icon><timer /></el-icon>
                        <span>{{ scope.row.title }}</span>
                    </div>
                </template>
            </el-table-column>

            <el-table-column label="分类" width="200">
                <template #default="scope">
                    <div style="display: flex;align-items: center">
                        <el-icon><timer /></el-icon>
                        <span>{{ categories[scope.row.categories] }}</span>
                    </div>
                </template>
            </el-table-column>

            <el-table-column prop="authorName" label="作者"  width="150" />
            <el-table-column prop="readCount" label="阅读量" width="150"/>
            <el-table-column prop="publishedAt" label="发布时间" width="150"/>

            <el-table-column label="操作" width="240" fixed="right">
                <template #default="scope">
                    <el-button text type="primary">编辑</el-button>
                    <el-button v-if="scope.row.status === 0 || scope.row.status === 2" text type="success">发布</el-button>
                    <el-button v-if="scope.row.status === 1" text type="warning">下线</el-button>
                    <el-button text type="danger">删除</el-button>
                </template>
            </el-table-column>

        </el-table>
    </div>
</template>
