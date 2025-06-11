<template>
  <div v-if="showDebug" class="debug-auth">
    <el-card>
      <template #header>
        <div style="display: flex; justify-content: space-between; align-items: center">
          <span>认证状态调试</span>
          <el-button type="text" @click="showDebug = false">×</el-button>
        </div>
      </template>
      
      <div class="debug-info">
        <p><strong>当前路由:</strong> {{ $route.path }}</p>
        <p><strong>认证状态:</strong> {{ authStore.isAuthenticated ? '已认证' : '未认证' }}</p>
        <p><strong>Token存在:</strong> {{ authStore.token ? '是' : '否' }}</p>
        <p><strong>用户信息:</strong> {{ authStore.user ? authStore.user.username : '无' }}</p>
        <p><strong>LocalStorage Token:</strong> {{ localToken ? '存在' : '不存在' }}</p>
        
        <div class="debug-actions">
          <el-button size="small" @click="refreshAuth">刷新认证状态</el-button>
          <el-button size="small" @click="clearAuth">清除认证</el-button>
          <el-button size="small" @click="goDashboard">跳转仪表盘</el-button>
        </div>
      </div>
    </el-card>
  </div>
  
  <!-- 浮动按钮 -->
  <div v-if="!showDebug" class="debug-trigger">
    <el-button 
      type="primary" 
      size="small" 
      circle 
      @click="showDebug = true"
      title="显示调试信息"
    >
      🔍
    </el-button>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const showDebug = ref(false)

const localToken = computed(() => {
  return localStorage.getItem('token')
})

const refreshAuth = () => {
  location.reload()
}

const clearAuth = () => {
  authStore.logout()
  localStorage.removeItem('token')
  router.push('/login')
}

const goDashboard = () => {
  router.push('/dashboard')
}
</script>

<style scoped>
.debug-auth {
  position: fixed;
  top: 20px;
  right: 20px;
  width: 300px;
  z-index: 9999;
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.debug-info p {
  margin: 8px 0;
  font-size: 14px;
}

.debug-actions {
  margin-top: 16px;
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.debug-trigger {
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 9999;
}
</style> 