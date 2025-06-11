import request from '@/utils/request'

// 接口相关类型定义
export interface API {
  id: number
  name: string
  method: string
  url: string
  description?: string
  headers?: Record<string, any>
  params?: Record<string, any>
  body?: Record<string, any>
  category_id?: number
  created_at: string
  updated_at: string
  category?: Category
}

export interface APICreate {
  name: string
  method: string
  url: string
  description?: string
  headers?: Record<string, any>
  params?: Record<string, any>
  body?: Record<string, any>
  category_id?: number
}

export interface APIUpdate {
  name?: string
  method?: string
  url?: string
  description?: string
  headers?: Record<string, any>
  params?: Record<string, any>
  body?: Record<string, any>
  category_id?: number
}

// 分类相关类型定义
export interface Category {
  id: number
  name: string
  description?: string
  color: string
  module_id: number
  created_at: string
  apis?: API[]
}

export interface CategoryCreate {
  name: string
  description?: string
  color?: string
  module_id: number
}

export interface CategoryUpdate {
  name?: string
  description?: string
  color?: string
}

// 项目相关类型定义
export interface Project {
  id: number
  name: string
  description?: string
  created_at: string
  updated_at: string
}

export interface ProjectCreate {
  name: string
  description?: string
}

export interface ProjectUpdate {
  name?: string
  description?: string
}

export interface ProjectStats {
  id: number
  name: string
  description?: string
  created_at: string
  updated_at: string
  module_count: number
  category_count: number
  api_count: number
  modules?: ModuleStats[]
}

// 模块相关类型定义
export interface Module {
  id: number
  name: string
  description?: string
  icon?: string
  project_id: number
  created_at: string
}

export interface ModuleCreate {
  name: string
  description?: string
  icon?: string
  project_id: number
}

export interface ModuleUpdate {
  name?: string
  description?: string
  icon?: string
  project_id?: number
}

export interface ModuleStats {
  id: number
  name: string
  description?: string
  icon?: string
  project_id: number
  created_at: string
  category_count: number
  api_count: number
}

// 分类API
export const categoryApi = {
  // 获取分类列表
  getCategories: (params?: { module_id?: number; project_id?: number; skip?: number; limit?: number }) => {
    return request.get<Category[]>('/api/v1/apis/categories/', { params })
  },

  // 创建分类
  createCategory: (data: CategoryCreate) => {
    return request.post<Category>('/api/v1/apis/categories/', data)
  },

  // 获取分类详情
  getCategory: (id: number) => {
    return request.get<Category>(`/api/v1/apis/categories/${id}`)
  },

  // 更新分类
  updateCategory: (id: number, data: CategoryUpdate) => {
    return request.put<Category>(`/api/v1/apis/categories/${id}`, data)
  },

  // 删除分类
  deleteCategory: (id: number) => {
    return request.delete<Category>(`/api/v1/apis/categories/${id}`)
  }
}

// 接口API
export const apiApi = {
  // 获取接口列表
  getAPIs: (params?: { 
    project_id?: number
    module_id?: number
    category_id?: number
    keyword?: string
    skip?: number
    limit?: number 
  }) => {
    return request.get<API[]>('/api/v1/apis/', { params })
  },

  // 创建接口
  createAPI: (data: APICreate) => {
    return request.post<API>('/api/v1/apis/', data)
  },

  // 获取接口详情
  getAPI: (id: number) => {
    return request.get<API>(`/api/v1/apis/${id}`)
  },

  // 更新接口
  updateAPI: (id: number, data: APIUpdate) => {
    return request.put<API>(`/api/v1/apis/${id}`, data)
  },

  // 删除接口
  deleteAPI: (id: number) => {
    return request.delete<API>(`/api/v1/apis/${id}`)
  }
}

// 项目API
export const projectApi = {
  // 获取项目列表
  getProjects: (params?: { skip?: number; limit?: number }) => {
    return request.get<ProjectStats[]>('/api/v1/projects/', { params })
  },

  // 创建项目
  createProject: (data: ProjectCreate) => {
    return request.post<Project>('/api/v1/projects/', data)
  },

  // 获取项目详情
  getProject: (id: number) => {
    return request.get<ProjectStats>(`/api/v1/projects/${id}`)
  },

  // 更新项目
  updateProject: (id: number, data: ProjectUpdate) => {
    return request.put<Project>(`/api/v1/projects/${id}`, data)
  },

  // 删除项目
  deleteProject: (id: number) => {
    return request.delete<{ message: string }>(`/api/v1/projects/${id}`)
  },

  // 获取项目下的模块列表
  getModules: (projectId: number, params?: { skip?: number; limit?: number }) => {
    return request.get<ModuleStats[]>(`/api/v1/projects/${projectId}/modules/`, { params })
  },

  // 创建模块
  createModule: (projectId: number, data: Omit<ModuleCreate, 'project_id'>) => {
    return request.post<Module>(`/api/v1/projects/${projectId}/modules/`, data)
  }
}

// 模块API
export const moduleApi = {
  // 获取模块详情
  getModule: (id: number) => {
    return request.get<ModuleStats>(`/api/v1/projects/modules/${id}`)
  },

  // 更新模块
  updateModule: (id: number, data: ModuleUpdate) => {
    return request.put<Module>(`/api/v1/projects/modules/${id}`, data)
  },

  // 删除模块
  deleteModule: (id: number) => {
    return request.delete<{ message: string }>(`/api/v1/projects/modules/${id}`)
  }
} 