<template>
  <el-container class="app-layout">
    <!-- 科幻背景效果 -->
    <div class="cyber-background"></div>
    
    <!-- 顶部导航 -->
    <el-header class="app-header cyber-container">
      <div class="header-left">
        <h1 class="app-title neon-text">⚡ CYBER API</h1>
        <div class="system-status">
          <span class="status-indicator pulse"></span>
          <span class="status-text">ONLINE</span>
        </div>
      </div>
      <div class="header-right">
        <div class="user-stats">
          <span class="stat-item">
            <span class="stat-label">连接:</span>
            <span class="stat-value neon-text-secondary">安全</span>
          </span>
        </div>
        <el-dropdown @command="handleCommand" class="user-dropdown">
          <span class="user-info cyber-card">
            <div class="user-avatar">
              <el-icon><User /></el-icon>
            </div>
            <span class="user-name">{{ authStore.user?.username || 'USER' }}</span>
            <el-icon class="dropdown-icon"><ArrowDown /></el-icon>
          </span>
          <template #dropdown>
            <el-dropdown-menu class="cyber-dropdown">
              <el-dropdown-item command="profile">
                <el-icon><User /></el-icon> 用户档案
              </el-dropdown-item>
              <el-dropdown-item command="settings">
                <el-icon><Setting /></el-icon> 系统设置
              </el-dropdown-item>
              <el-dropdown-item divided command="logout">
                <el-icon><SwitchButton /></el-icon> 断开连接
              </el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </el-header>

    <el-container>
      <!-- 侧边栏 -->
      <el-aside width="260px" class="app-aside cyber-container">
        <div class="sidebar-header">
          <div class="module-title">
            <span class="module-icon">🛠️</span>
            <span class="module-text">控制模块</span>
          </div>
        </div>
        
        <el-menu
          :default-active="currentRoute"
          class="sidebar-menu cyber-menu"
          router
        >
          <el-menu-item index="/dashboard" class="menu-item-cyber">
            <div class="menu-icon">
              <el-icon><Monitor /></el-icon>
            </div>
            <span class="menu-text">控制台</span>
            <div class="menu-effect"></div>
          </el-menu-item>
          <el-menu-item index="/projects" class="menu-item-cyber">
            <div class="menu-icon">
              <el-icon><Folder /></el-icon>
            </div>
            <span class="menu-text">项目中心</span>
            <div class="menu-effect"></div>
          </el-menu-item>
          <el-menu-item index="/apis" class="menu-item-cyber">
            <div class="menu-icon">
              <el-icon><Connection /></el-icon>
            </div>
            <span class="menu-text">接口矩阵</span>
            <div class="menu-effect"></div>
          </el-menu-item>
          <el-menu-item index="/scenarios" class="menu-item-cyber">
            <div class="menu-icon">
              <el-icon><Operation /></el-icon>
            </div>
            <span class="menu-text">场景引擎</span>
            <div class="menu-effect"></div>
          </el-menu-item>
          <el-menu-item index="/reports" class="menu-item-cyber">
            <div class="menu-icon">
              <el-icon><DataAnalysis /></el-icon>
            </div>
            <span class="menu-text">数据分析</span>
            <div class="menu-effect"></div>
          </el-menu-item>
        </el-menu>
      </el-aside>

      <!-- 主内容区 -->
      <el-main class="app-main">
        <router-view v-slot="{ Component, route }">
          <transition name="cyber-slide" mode="out-in">
            <component :is="Component" :key="route.path" />
          </transition>
        </router-view>
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import {
  User,
  ArrowDown,
  Monitor,
  Folder,
  Connection,
  Operation,
  DataAnalysis,
  Setting,
  SwitchButton
} from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const currentRoute = computed(() => route.path)

const handleCommand = (command: string) => {
  switch (command) {
    case 'profile':
      ElMessage.info('个人资料功能开发中...')
      break
    case 'settings':
      ElMessage.info('设置功能开发中...')
      break
    case 'logout':
      authStore.logout()
      router.push('/login')
      break
  }
}
</script>

<style lang="scss" scoped>
.app-layout {
  height: 100vh;
  position: relative;
}

// 科幻背景
.cyber-background {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: var(--gradient-cyber);
  z-index: -1;
  
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: 
      radial-gradient(circle at 25% 25%, rgba(0, 212, 255, 0.1) 0%, transparent 50%),
      radial-gradient(circle at 75% 75%, rgba(114, 9, 183, 0.1) 0%, transparent 50%);
    animation: bg-pulse 10s ease-in-out infinite alternate;
  }
}

@keyframes bg-pulse {
  0% { opacity: 0.3; }
  100% { opacity: 0.7; }
}

.app-header {
  height: 70px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 32px;
  position: relative;
  z-index: 100;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 24px;
}

.app-title {
  margin: 0;
  font-size: 24px;
  font-weight: 900;
  font-family: 'Orbitron', monospace;
  letter-spacing: 2px;
}

.system-status {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  color: var(--text-secondary);
  font-weight: 600;
  letter-spacing: 1px;
}

.status-indicator {
  width: 8px;
  height: 8px;
  background: var(--success);
  border-radius: 50%;
  box-shadow: 0 0 10px var(--success);
}

.header-right {
  display: flex;
  align-items: center;
  gap: 24px;
}

.user-stats {
  display: flex;
  gap: 16px;
  
  .stat-item {
    font-size: 12px;
    
    .stat-label {
      color: var(--text-muted);
    }
    
    .stat-value {
      font-weight: 600;
    }
  }
}

.user-info {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  padding: 8px 16px;
  border-radius: 8px;
  transition: all 0.3s ease;
  
  &:hover {
    transform: translateY(-1px);
  }
}

.user-avatar {
  width: 32px;
  height: 32px;
  background: var(--gradient-primary);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.user-name {
  font-weight: 600;
  font-family: 'Orbitron', monospace;
  letter-spacing: 1px;
}

.dropdown-icon {
  transition: transform 0.3s ease;
}

.user-dropdown:hover .dropdown-icon {
  transform: rotate(180deg);
}

.app-aside {
  background: none !important;
  border-right: none !important;
}

.sidebar-header {
  padding: 24px 20px 16px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.module-title {
  display: flex;
  align-items: center;
  gap: 12px;
  color: var(--text-primary);
  font-weight: 700;
  font-size: 16px;
  letter-spacing: 1px;
}

.module-icon {
  font-size: 18px;
}

.cyber-menu {
  background: transparent !important;
  border: none !important;
  padding: 16px 0;
  
  .menu-item-cyber {
    margin: 4px 16px;
    border-radius: 8px;
    height: 48px !important;
    position: relative;
    overflow: hidden;
    transition: all 0.3s ease;
    
    &:hover,
    &.is-active {
      background: var(--bg-glass-dark) !important;
      color: var(--accent-primary) !important;
      
      .menu-effect {
        opacity: 1;
        transform: translateX(0);
      }
      
      .menu-icon {
        color: var(--accent-primary);
        transform: scale(1.1);
      }
    }
    
    &.is-active {
      border-left: 3px solid var(--accent-primary);
    }
  }
}

// Element Plus 子菜单深度样式
:deep(.el-sub-menu) {
  .el-sub-menu__title {
    margin: 4px 16px !important;
    border-radius: 8px !important;
    height: 48px !important;
    position: relative;
    overflow: hidden;
    transition: all 0.3s ease;
    background: transparent !important;
    
    &:hover {
      background: var(--bg-glass-dark) !important;
      color: var(--accent-primary) !important;
      
      .menu-icon {
        color: var(--accent-primary);
        transform: scale(1.1);
      }
    }
  }
  
  .el-menu {
    background: transparent !important;
  }
  
  &.is-opened > .el-sub-menu__title {
    background: var(--bg-glass-dark) !important;
    color: var(--accent-primary) !important;
    border-left: 3px solid var(--accent-primary);
  }
}

.menu-icon {
  width: 24px;
  margin-right: 12px;
  transition: all 0.3s ease;
}

.menu-text {
  font-weight: 600;
  letter-spacing: 0.5px;
}

.menu-effect {
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  width: 3px;
  background: var(--gradient-neon);
  opacity: 0;
  transform: translateX(100%);
  transition: all 0.3s ease;
}

// 子菜单样式
:deep(.submenu-item-cyber) {
  margin: 2px 8px !important;
  border-radius: 6px !important;
  height: 40px !important;
  background: rgba(255, 255, 255, 0.03) !important;
  position: relative;
  transition: all 0.3s ease;
  
  &:hover,
  &.is-active {
    background: var(--bg-glass-dark) !important;
    color: var(--accent-secondary) !important;
    transform: translateX(4px);
    
    .submenu-icon {
      color: var(--accent-secondary);
      transform: scale(1.05);
    }
  }
  
  &.is-active {
    border-left: 2px solid var(--accent-secondary);
  }
}

.submenu-icon {
  width: 20px;
  margin-right: 10px;
  transition: all 0.3s ease;
  opacity: 0.8;
}

.submenu-text {
  font-weight: 500;
  letter-spacing: 0.3px;
  font-size: 14px;
}

.app-main {
  background: transparent !important;
  padding: 32px;
  overflow-y: auto;
  position: relative;
}

// 科幻路由过渡动画
.cyber-slide-enter-active,
.cyber-slide-leave-active {
  transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.cyber-slide-enter-from {
  opacity: 0;
  transform: translateX(30px) scale(0.95);
}

.cyber-slide-leave-to {
  opacity: 0;
  transform: translateX(-30px) scale(0.95);
}

// Element Plus 下拉菜单科幻样式
:deep(.cyber-dropdown) {
  background: var(--bg-glass) !important;
  backdrop-filter: blur(20px) !important;
  border: var(--border-glass) !important;
  border-radius: 12px !important;
  box-shadow: var(--shadow-cyber) !important;
  
  .el-dropdown-menu__item {
    color: var(--text-primary) !important;
    transition: all 0.3s ease;
    
    &:hover {
      background: var(--bg-glass-dark) !important;
      color: var(--accent-primary) !important;
    }
    
    .el-icon {
      margin-right: 8px;
    }
  }
}

// 响应式
@media (max-width: 768px) {
  .app-header {
    padding: 0 16px;
    
    .app-title {
      font-size: 18px;
    }
  }
  
  .app-aside {
    width: 220px !important;
  }
  
  .app-main {
    padding: 16px;
  }
}
</style> 