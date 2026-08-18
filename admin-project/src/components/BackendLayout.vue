<script setup lang="ts">
import Sidebar from './Sidebar.vue';
import Navbar from './Navbar.vue';
</script>

<template>
    <div class="backend-layout">
    <el-container>
      <Sidebar />
      <el-container>
        <el-header>
            <Navbar />
        </el-header>
        <el-main>
            <router-view></router-view>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>
<style lang="scss" scoped>
.backend-layout {
    height: 100vh;
}
</style>