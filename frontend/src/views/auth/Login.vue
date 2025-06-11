<template>
  <div class="login-container">
    <!-- 调试组件 -->
    <DebugAuth />
    <!-- 动态背景粒子 -->
    <div class="particles"></div>
    
    <div class="login-wrapper">
      <div class="login-form-container cyber-container">
        <div class="login-header">
          <h1 class="login-title neon-text">⚡ CYBER API</h1>
          <p class="login-subtitle typewriter">下一代API测试控制中心</p>
          <div class="subtitle-glow"></div>
        </div>

        <el-form
          ref="loginFormRef"
          :model="loginForm"
          :rules="loginRules"
          class="login-form"
          @submit.prevent="handleLogin"
        >
          <el-form-item prop="username">
            <el-input
              v-model="loginForm.username"
              placeholder="用户名"
              size="large"
              prefix-icon="User"
              clearable
            />
          </el-form-item>

          <el-form-item prop="password">
            <el-input
              v-model="loginForm.password"
              type="password"
              placeholder="密码"
              size="large"
              prefix-icon="Lock"
              show-password
              @keyup.enter="handleLogin"
            />
          </el-form-item>

          <el-form-item>
            <el-button
              type="primary"
              size="large"
              class="login-button cyber-button pulse"
              :loading="loading"
              @click="handleLogin"
            >
              <span v-if="loading">
                <i class="loading-cyber"></i> 系统验证中...
              </span>
              <span v-else>
                🔐 启动系统
              </span>
            </el-button>
          </el-form-item>
        </el-form>

        <div class="login-footer">
          <p>
            需要访问权限？
            <el-button type="text" class="register-link neon-text-secondary" @click="showRegister = true">
              申请权限 →
            </el-button>
          </p>
          <div class="access-info">
            <p class="access-tip">🔒 安全连接已建立</p>
            <p class="access-tip">⚡ 量子加密传输</p>
          </div>
        </div>
      </div>
    </div>

    <!-- 注册对话框 -->
    <el-dialog
      v-model="showRegister"
      title="用户注册"
      width="400px"
      :before-close="handleCloseRegister"
    >
      <el-form
        ref="registerFormRef"
        :model="registerForm"
        :rules="registerRules"
        label-width="80px"
      >
        <el-form-item label="用户名" prop="username">
          <el-input v-model="registerForm.username" />
        </el-form-item>

        <el-form-item label="邮箱" prop="email">
          <el-input v-model="registerForm.email" type="email" />
        </el-form-item>

        <el-form-item label="姓名" prop="full_name">
          <el-input v-model="registerForm.full_name" />
        </el-form-item>

        <el-form-item label="密码" prop="password">
          <el-input v-model="registerForm.password" type="password" show-password />
        </el-form-item>
      </el-form>

      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showRegister = false">取消</el-button>
          <el-button type="primary" :loading="registerLoading" @click="handleRegister">
            注册
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { authApi } from '@/api/auth'
import type { FormInstance, FormRules } from 'element-plus'
import type { LoginForm, RegisterForm } from '@/types/auth'
import { ElMessage } from 'element-plus'
import DebugAuth from '@/components/DebugAuth.vue'

const router = useRouter()
const authStore = useAuthStore()

// 表单引用
const loginFormRef = ref<FormInstance>()
const registerFormRef = ref<FormInstance>()

// 登录表单
const loginForm = reactive<LoginForm>({
  username: 'admin123',
  password: 'admin123'
})

// 注册表单
const registerForm = reactive<RegisterForm>({
  username: '',
  email: '',
  full_name: '',
  password: ''
})

// 状态
const loading = ref(false)
const registerLoading = ref(false)
const showRegister = ref(false)

// 表单验证规则
const loginRules: FormRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度在 3 到 20 个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于 6 个字符', trigger: 'blur' }
  ]
}

const registerRules: FormRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度在 3 到 20 个字符', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于 6 个字符', trigger: 'blur' }
  ]
}

// 登录处理
const handleLogin = async () => {
  if (!loginFormRef.value) return

  try {
    await loginFormRef.value.validate()
    loading.value = true

    console.log('开始登录流程...')
    await authStore.login(loginForm)
    console.log('登录成功，认证状态:', authStore.isAuthenticated)
    console.log('Token:', authStore.token)
    
    ElMessage.success('登录成功')
    
    // 等待状态更新完成
    await new Promise(resolve => setTimeout(resolve, 200))
    
    console.log('准备跳转...')
    // 使用 replace 而不是 push，避免在历史记录中保留登录页
    await router.replace('/dashboard')
    console.log('跳转完成')
  } catch (error: any) {
    console.error('Login error:', error)
    ElMessage.error(error.response?.data?.detail || '登录失败')
  } finally {
    loading.value = false
  }
}

// 注册处理
const handleRegister = async () => {
  if (!registerFormRef.value) return

  try {
    await registerFormRef.value.validate()
    registerLoading.value = true

    await authApi.register(registerForm)
    ElMessage.success('注册成功，请登录')
    showRegister.value = false
    
    // 自动填充登录表单
    loginForm.username = registerForm.username
  } catch (error: any) {
    console.error('Register error:', error)
    ElMessage.error(error.response?.data?.detail || '注册失败')
  } finally {
    registerLoading.value = false
  }
}

// 关闭注册对话框
const handleCloseRegister = () => {
  showRegister.value = false
  registerFormRef.value?.resetFields()
}
</script>

<style lang="scss" scoped>
.login-container {
  height: 100vh;
  background: var(--gradient-cyber);
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;

  // 动态网格背景
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-image: 
      linear-gradient(var(--accent-primary) 1px, transparent 1px),
      linear-gradient(90deg, var(--accent-primary) 1px, transparent 1px);
    background-size: 50px 50px;
    background-position: 0 0, 0 0;
    opacity: 0.1;
    animation: grid-move 20s linear infinite;
  }

  // 动态光效
  &::after {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: conic-gradient(
      from 0deg,
      transparent 0deg,
      var(--accent-primary) 30deg,
      transparent 120deg,
      var(--accent-secondary) 180deg,
      transparent 240deg,
      var(--accent-tertiary) 300deg,
      transparent 360deg
    );
    opacity: 0.05;
    animation: rotate 30s linear infinite;
  }
}

@keyframes grid-move {
  0% { background-position: 0 0, 0 0; }
  100% { background-position: 50px 50px, 50px 50px; }
}

@keyframes rotate {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

// 粒子背景
.particles {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
  z-index: 1;

  &::before,
  &::after {
    content: '';
    position: absolute;
    width: 2px;
    height: 2px;
    background: var(--accent-primary);
    border-radius: 50%;
    box-shadow: 
      100px 200px var(--accent-primary),
      300px 100px var(--accent-secondary),
      500px 300px var(--accent-primary),
      700px 150px var(--accent-tertiary),
      900px 250px var(--accent-secondary),
      200px 400px var(--accent-primary),
      600px 350px var(--accent-secondary),
      800px 450px var(--accent-tertiary);
    animation: particles 25s linear infinite;
  }

  &::after {
    animation-delay: -12s;
  }
}

@keyframes particles {
  0% { transform: translateY(100vh) rotate(0deg); }
  100% { transform: translateY(-100vh) rotate(360deg); }
}

.login-wrapper {
  position: relative;
  z-index: 10;
}

.login-form-container {
  width: 420px;
  padding: 48px;
  position: relative;
  
  // 额外的科幻边框效果
  &::after {
    content: '';
    position: absolute;
    top: -2px;
    left: -2px;
    right: -2px;
    bottom: -2px;
    background: var(--gradient-neon);
    border-radius: 18px;
    z-index: -1;
    opacity: 0.3;
    animation: border-glow 3s ease-in-out infinite alternate;
  }
}

@keyframes border-glow {
  0% { opacity: 0.3; }
  100% { opacity: 0.8; }
}

.login-header {
  text-align: center;
  margin-bottom: 40px;
  position: relative;
}

.login-title {
  font-size: 36px;
  font-weight: 900;
  margin: 0 0 16px 0;
  font-family: 'Orbitron', monospace;
  letter-spacing: 2px;
}

.login-subtitle {
  color: var(--text-secondary);
  margin: 0 0 16px 0;
  font-size: 16px;
  font-weight: 300;
  letter-spacing: 1px;
}

.subtitle-glow {
  width: 100px;
  height: 2px;
  background: var(--gradient-neon);
  margin: 0 auto;
  border-radius: 1px;
  animation: pulse-glow 2s ease-in-out infinite;
}

@keyframes pulse-glow {
  0%, 100% { 
    opacity: 0.5;
    transform: scaleX(1);
  }
  50% { 
    opacity: 1;
    transform: scaleX(1.2);
  }
}

.login-form {
  .el-form-item {
    margin-bottom: 24px;
  }

  // 输入框科幻效果
  :deep(.el-input__wrapper) {
    height: 50px;
    
    &:hover,
    &.is-focus {
      box-shadow: 
        var(--shadow-neon),
        inset 0 0 10px rgba(0, 212, 255, 0.1) !important;
    }
  }

  :deep(.el-input__inner) {
    font-size: 16px;
    font-weight: 500;
    letter-spacing: 0.5px;
  }
}

.login-button {
  width: 100%;
  height: 56px;
  font-size: 18px;
  font-weight: 700;
  border-radius: 12px;
  letter-spacing: 1px;
  
  &:not(.is-loading) {
    animation: button-pulse 3s ease-in-out infinite;
  }
}

@keyframes button-pulse {
  0%, 100% { 
    box-shadow: 
      var(--shadow-neon),
      0 0 0 0 rgba(0, 212, 255, 0.7);
  }
  50% { 
    box-shadow: 
      var(--shadow-neon),
      0 0 0 8px rgba(0, 212, 255, 0);
  }
}

.login-footer {
  text-align: center;
  margin-top: 32px;
  color: var(--text-muted);
  font-size: 14px;

  .register-link {
    font-weight: 600;
    text-decoration: none;
    transition: all 0.3s ease;
    
    &:hover {
      transform: translateX(5px);
    }
  }
}

.access-info {
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  
  .access-tip {
    margin: 8px 0;
    font-size: 12px;
    color: var(--text-muted);
    opacity: 0.8;
  }
}

:deep(.el-input__wrapper) {
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

:deep(.el-input--large .el-input__wrapper) {
  padding: 12px 16px;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}
</style> 