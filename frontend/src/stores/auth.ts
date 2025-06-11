import { defineStore } from 'pinia'
import { ref, computed, readonly } from 'vue'
import type { User, LoginForm } from '@/types/auth'
import { authApi } from '@/api/auth'

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const token = ref<string | null>(localStorage.getItem('token'))
  const isAuthenticated = computed(() => !!token.value)

  const login = async (form: LoginForm) => {
    try {
      console.log('发送登录请求...')
      const response = await authApi.login(form)
      console.log('登录API响应:', response)
      
      token.value = response.access_token
      user.value = response.user
      localStorage.setItem('token', response.access_token)
      
      console.log('认证状态更新完成:', {
        token: token.value,
        user: user.value,
        isAuthenticated: isAuthenticated.value
      })
      
      return response
    } catch (error) {
      console.error('登录请求失败:', error)
      throw error
    }
  }

  const logout = () => {
    token.value = null
    user.value = null
    localStorage.removeItem('token')
  }

  const getCurrentUser = async () => {
    if (!token.value) return null
    
    try {
      const response = await authApi.getCurrentUser()
      user.value = response
      return response
    } catch (error) {
      logout()
      throw error
    }
  }

  return {
    user: readonly(user),
    token: readonly(token),
    isAuthenticated,
    login,
    logout,
    getCurrentUser
  }
}) 