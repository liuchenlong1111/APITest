import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes: RouteRecordRaw[] = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/auth/Login.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/',
    redirect: '/dashboard',
    component: () => import('@/layouts/AppLayout.vue'),
    meta: { requiresAuth: true },
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('@/views/dashboard/Index.vue'),
        meta: { title: '仪表盘' }
      },
      {
        path: 'projects',
        name: 'Projects',
        component: () => import('@/views/project/Index.vue'),
        meta: { title: '项目管理' }
      },
      {
        path: 'projects/:id',
        name: 'ProjectDetail',
        component: () => import('@/views/project/Detail.vue'),
        meta: { title: '项目详情' }
      },
      {
        path: 'apis',
        name: 'APIs',
        component: () => import('@/views/api/Index.vue'),
        meta: { title: '接口管理', requiresAuth: false }
      },
      {
        path: 'apis/import',
        name: 'ImportAPI',
        component: () => import('@/views/api/ImportAPI.vue'),
        meta: { title: '接口导入' }
      },
      {
        path: 'scenarios',
        name: 'Scenarios',
        component: () => import('@/views/scenario/Index.vue'),
        meta: { title: '场景测试' }
      },
      {
        path: 'reports',
        name: 'Reports',
        component: () => import('@/views/report/Index.vue'),
        meta: { title: '测试报告' }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  console.log('路由守卫检查:', {
    从: from.path,
    到: to.path,
    目标路由名: to.name,
    需要认证: to.meta.requiresAuth,
    已认证: authStore.isAuthenticated,
    token: authStore.token ? '存在' : '不存在'
  })
  
  // 避免无限循环
  if (from.path === to.path) {
    console.log('路径相同，直接通过')
    next()
    return
  }
  
  // 检查是否需要认证
  const requiresAuth = to.meta.requiresAuth !== false
  
  if (requiresAuth && !authStore.isAuthenticated) {
    console.log('需要认证但未登录，跳转到登录页')
    if (to.path !== '/login') {
      next('/login')
    } else {
      next()
    }
  } else if (to.path === '/login' && authStore.isAuthenticated) {
    console.log('已认证用户访问登录页，重定向到仪表盘')
    next('/dashboard')
  } else {
    console.log('正常访问目标页面')
    next()
  }
})

export default router 