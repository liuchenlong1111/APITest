import request from '@/utils/request'
import type { LoginForm, LoginResponse, RegisterForm, User } from '@/types/auth'

export const authApi = {
  // 登录
  login: (data: LoginForm): Promise<LoginResponse> => {
    return request.post('/api/v1/auth/login', data)
  },

  // 注册
  register: (data: RegisterForm): Promise<User> => {
    return request.post('/api/v1/auth/register', data)
  },

  // 获取当前用户信息
  getCurrentUser: (): Promise<User> => {
    return request.get('/api/v1/auth/me')
  },

  // 刷新Token
  refreshToken: (): Promise<LoginResponse> => {
    return request.post('/api/v1/auth/refresh')
  },

  // 登出
  logout: (): Promise<void> => {
    return request.post('/api/v1/auth/logout')
  }
} 