<template>
  <div class="api-page">
    <!-- 页面标题区域 -->
    <div class="page-header cyber-container">
      <div class="header-content">
        <div class="title-section">
          <h1 class="page-title neon-text">🔗 接口矩阵</h1>
          <p class="page-subtitle">API MANAGEMENT CONSOLE</p>
          <div class="title-glow"></div>
        </div>
        <div class="header-actions">
          <el-button type="primary" class="cyber-button pulse" @click="goToImportAPI">
            <el-icon><Upload /></el-icon>
            <span>接口导入</span>
          </el-button>
          <el-button type="primary" class="cyber-button pulse" @click="showCreateCategoryDialog">
            <el-icon><Plus /></el-icon>
            <span>创建分类</span>
          </el-button>
          <el-button type="primary" class="cyber-button pulse" @click="showCreateAPIDialog">
            <el-icon><Plus /></el-icon>
            <span>部署接口</span>
          </el-button>
        </div>
      </div>
    </div>

    <!-- 主内容区域 -->
    <div class="content-container cyber-container">

      <!-- 项目层级控制台 -->
      <div class="project-hierarchy-console cyber-card">
        <div class="console-header">
          <h3 class="console-title">🏗️ 项目层级控制台</h3>
          <div class="console-status">
            <span class="status-dot pulse"></span>
            <span>ACTIVE</span>
          </div>
        </div>
                <el-row :gutter="16">
          <el-col :span="5">
            <div class="input-group">
              <label class="input-label">项目选择</label>
              <el-select
                v-model="selectedProjectId"
                placeholder="选择项目"
                clearable
                size="large"
                @change="handleProjectChange"
              >
                <el-option
                  v-for="project in projects"
                  :key="project.id"
                  :label="project.name"
                  :value="project.id"
                >
                  🏗️ {{ project.name }}
                </el-option>
              </el-select>
            </div>
          </el-col>
          <el-col :span="5">
            <div class="input-group">
              <label class="input-label">模块选择</label>
              <el-select
                v-model="selectedModuleId"
                placeholder="选择模块"
                clearable
                size="large"
                @change="(val) => { console.log('🔄 Select @change:', val); selectedModuleId = val; selectedCategoryId = undefined; handleSearch(); }"
                :disabled="!selectedProjectId"
              >
                <el-option
                  v-for="module in currentModules"
                  :key="module.id"
                  :label="module.name"
                  :value="module.id"
                  @click="() => { console.log('点击模块选项:', module.id, module.name); selectedModuleId = module.id; handleSearch(); }"
                >
                  🔧 {{ module.name }}
                </el-option>
              </el-select>
            </div>
          </el-col>
          <el-col :span="5">
            <div class="input-group">
              <label class="input-label">分类过滤</label>
              <el-select
                v-model="selectedCategoryId"
                placeholder="选择分类"
                clearable
                size="large"
                @change="handleSearch"
                :disabled="!selectedProjectId || currentCategories.length === 0"
              >
                <el-option
                  v-for="category in currentCategories"
                  :key="category.id"
                  :label="category.name"
                  :value="category.id"
                >
                  <span class="category-dot" :style="{ color: category.color }">●</span>
                  {{ category.name }}
                </el-option>
              </el-select>
            </div>
          </el-col>
          <el-col :span="5">
            <div class="input-group">
              <label class="input-label">目标检索</label>
              <el-input
                v-model="searchKeyword"
                placeholder="输入接口标识符..."
                clearable
                size="large"
                @keyup.enter="handleSearch"
              >
                <template #prefix>
                  <el-icon><Search /></el-icon>
                </template>
              </el-input>
            </div>
          </el-col>
          <el-col :span="4">
            <div class="input-group">
              <label class="input-label">操作指令</label>
              <div class="button-group">
                <el-button type="primary" class="cyber-button" @click="handleSearch">
                  执行扫描
                </el-button>
                <el-button class="cyber-button" @click="handleReset">
                  重置参数
                </el-button>
              </div>
            </div>
          </el-col>
        </el-row>
        
        <!-- 层级面包屑 -->
        <div class="hierarchy-breadcrumb" v-if="selectedProjectId">
          <div class="breadcrumb-item">
            <span class="breadcrumb-icon">🏗️</span>
            <span class="breadcrumb-text">{{ getCurrentProjectName() }}</span>
          </div>
          <div class="breadcrumb-arrow" v-if="selectedModuleId">→</div>
          <div class="breadcrumb-item" v-if="selectedModuleId">
            <span class="breadcrumb-icon">🔧</span>
            <span class="breadcrumb-text">{{ getCurrentModuleName() }}</span>
          </div>
          <div class="breadcrumb-arrow" v-if="selectedCategoryId">→</div>
          <div class="breadcrumb-item" v-if="selectedCategoryId">
            <span class="breadcrumb-icon">📂</span>
            <span class="breadcrumb-text">{{ getCurrentCategoryName() }}</span>
          </div>
        </div>
        
        <!-- 项目统计信息 -->
        <div class="project-stats" v-if="selectedProjectId">
          <div class="stats-grid">
            <div class="stat-card">
              <div class="stat-icon">🔧</div>
              <div class="stat-content">
                <div class="stat-value">{{ currentModules.length }}</div>
                <div class="stat-label">模块数量</div>
              </div>
            </div>
            <div class="stat-card">
              <div class="stat-icon">📂</div>
              <div class="stat-content">
                <div class="stat-value">{{ currentCategories.length }}</div>
                <div class="stat-label">分类数量</div>
              </div>
            </div>
            <div class="stat-card">
              <div class="stat-icon">🔗</div>
              <div class="stat-content">
                <div class="stat-value">{{ apis.length }}</div>
                <div class="stat-label">接口数量</div>
              </div>
            </div>
            <div class="stat-card">
              <div class="stat-icon">✅</div>
              <div class="stat-content">
                <div class="stat-value">{{ apis.filter(api => api.category_id).length }}</div>
                <div class="stat-label">已分类接口</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 分类管理终端 -->
      <div class="category-terminal cyber-card" v-if="selectedProjectId">
        <div class="terminal-header">
          <h3 class="terminal-title">📂 分类管理终端</h3>
          <div class="terminal-info">
            <span class="info-item">
              <span class="info-label">当前分类:</span>
              <span class="info-value neon-text-secondary">{{ currentCategories.length }}</span>
            </span>
            <el-button 
              type="primary" 
              class="cyber-button-small"
              @click="showCreateCategoryDialog"
            >
              <el-icon><Plus /></el-icon>
              新增分类
            </el-button>
          </div>
        </div>
        <div class="category-grid">
          <div
            v-for="category in currentCategories"
            :key="category.id"
            class="category-module cyber-card"
            @click="handleCategoryClick(category)"
          >
            <div class="module-header">
              <div class="module-indicator" :style="{ backgroundColor: category.color }"></div>
              <span class="module-name">{{ category.name }}</span>
              <div class="module-actions">
                <el-button 
                  type="primary" 
                  text 
                  size="small" 
                  class="edit-btn"
                  @click.stop="showEditCategoryDialog(category)"
                >
                  <el-icon><Edit /></el-icon>
                </el-button>
                <el-button 
                  type="danger" 
                  text 
                  size="small" 
                  class="delete-btn"
                  @click.stop="handleDeleteCategory(category.id)"
                >
                  <el-icon><Close /></el-icon>
                </el-button>
              </div>
            </div>
            <div class="module-stats">
              <span class="stat-label">接口数量:</span>
              <span class="stat-value">{{ category.apis?.length || 0 }}</span>
              <span class="stat-label" style="margin-left: 10px;">模块:</span>
              <span class="stat-value">{{ getModuleName(category.module_id) }}</span>
            </div>
            <div class="module-description">
              {{ category.description || '暂无描述' }}
            </div>
          </div>
        </div>
      </div>
      
      <!-- 项目选择提示 -->
      <div class="empty-state cyber-card" v-else>
        <div class="empty-content">
          <div class="empty-icon">🎯</div>
          <div class="empty-title">请选择项目和模块</div>
          <div class="empty-desc">
            选择一个项目和模块来查看和管理其中的接口分类
          </div>
          <el-button type="primary" @click="$router.push('/projects')">
            前往项目管理
          </el-button>
        </div>
      </div>

      <!-- 接口数据库 -->
      <div class="api-database cyber-card">
        <div class="database-header">
          <h3 class="database-title">💾 接口数据库</h3>
          <div class="database-stats">
            <span class="stat-item">
              <span class="stat-label">总接口:</span>
              <span class="stat-value neon-text">{{ total }}</span>
            </span>
            <span class="stat-item">
              <span class="stat-label">当前页:</span>
              <span class="stat-value">{{ currentPage }}/{{ Math.ceil(total / pageSize) }}</span>
            </span>
          </div>
        </div>
        <el-table 
          :data="apis" 
          v-loading="loading"
          row-key="id"
          class="cyber-table"
        >
          <el-table-column prop="name" label="接口名称" min-width="150">
            <template #default="{ row }">
              <el-link type="primary" @click="handleViewAPI(row)">
                {{ row.name }}
              </el-link>
            </template>
          </el-table-column>
          
          <el-table-column prop="method" label="请求方法" width="100">
            <template #default="{ row }">
              <el-tag :type="getMethodType(row.method)" size="small">
                {{ row.method.toUpperCase() }}
              </el-tag>
            </template>
          </el-table-column>
          
          <el-table-column prop="url" label="接口地址" min-width="200" show-overflow-tooltip>
            <template #default="{ row }">
              <div v-if="row.url && row.url.trim()" class="url-display">
                <el-tooltip :content="row.url" placement="top">
                  <code class="url-text">{{ row.url }}</code>
                </el-tooltip>
              </div>
              <div v-else class="url-debug">
                <span class="text-gray url-fallback">未设置</span>
                <small class="debug-info">{{ row.url || 'null' }}</small>
              </div>
            </template>
          </el-table-column>
          
          <el-table-column label="请求参数" min-width="180" show-overflow-tooltip>
            <template #default="{ row }">
              <div v-if="row.params && Object.keys(row.params).length > 0" class="params-display">
                <el-tooltip :content="JSON.stringify(row.params, null, 2)" placement="top">
                  <span class="params-preview">
                    {{ Object.keys(row.params).slice(0, 3).join(', ') }}
                    <span v-if="Object.keys(row.params).length > 3">...</span>
                  </span>
                </el-tooltip>
              </div>
              <span v-else class="text-gray">无参数</span>
            </template>
          </el-table-column>
          
          <el-table-column label="请求头" min-width="150" show-overflow-tooltip>
            <template #default="{ row }">
              <div v-if="row.headers && Object.keys(row.headers).length > 0" class="headers-display">
                <el-tooltip :content="JSON.stringify(row.headers, null, 2)" placement="top">
                  <span class="headers-preview">
                    <el-tag size="small" type="success">{{ Object.keys(row.headers).length }}个</el-tag>
                  </span>
                </el-tooltip>
              </div>
              <span v-else class="text-gray">无头部</span>
            </template>
          </el-table-column>
          
          <el-table-column label="请求体" min-width="150" show-overflow-tooltip>
            <template #default="{ row }">
              <div v-if="row.body" class="body-display">
                <el-tooltip :content="JSON.stringify(row.body, null, 2)" placement="top">
                  <span class="body-preview">
                    <el-tag size="small" type="info">{{ getBodyType(row.body) }}</el-tag>
                  </span>
                </el-tooltip>
              </div>
              <span v-else class="text-gray">无数据</span>
            </template>
          </el-table-column>
          
          <el-table-column prop="category" label="分类" width="120">
            <template #default="{ row }">
              <el-tag v-if="row.category" :color="row.category.color" size="small">
                {{ row.category.name }}
              </el-tag>
              <span v-else class="text-gray">未分类</span>
            </template>
          </el-table-column>
          
          <el-table-column prop="description" label="描述" min-width="150" show-overflow-tooltip />
          
          <el-table-column prop="updated_at" label="更新时间" width="180">
            <template #default="{ row }">
              {{ formatDateTime(row.updated_at) }}
            </template>
          </el-table-column>
          
          <el-table-column label="操作指令" width="240" fixed="right">
            <template #default="{ row }">
              <div class="action-buttons">
                <el-button type="primary" text class="action-btn edit-btn" @click="handleEditAPI(row)">
                  <el-icon><Edit /></el-icon>
                  <span>编辑</span>
                </el-button>
                <el-button type="success" text class="action-btn test-btn" @click="handleTestAPI(row)">
                  <el-icon><VideoPlay /></el-icon>
                  <span>测试</span>
                </el-button>
                <el-button type="danger" text class="action-btn delete-btn" @click="handleDeleteAPI(row.id)">
                  <el-icon><Delete /></el-icon>
                  <span>删除</span>
                </el-button>
              </div>
            </template>
          </el-table-column>
        </el-table>

        <!-- 数据分页控制器 -->
        <div class="pagination-controller">
          <div class="controller-info">
            <span class="info-text">数据分页控制器</span>
            <span class="status-indicator pulse"></span>
          </div>
          <el-pagination
            v-model:current-page="currentPage"
            v-model:page-size="pageSize"
            :total="total"
            :page-sizes="[10, 20, 50, 100]"
            layout="total, sizes, prev, pager, next, jumper"
            class="cyber-pagination"
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
          />
        </div>
      </div>
    </div>

    <!-- 创建分类对话框 -->
    <el-dialog
      v-model="categoryDialogVisible"
      :title="categoryForm.id ? '编辑分类' : '新增分类'"
      width="500px"
    >
      <el-form
        ref="categoryFormRef"
        :model="categoryForm"
        :rules="categoryRules"
        label-width="80px"
      >
        <el-form-item label="分类名称" prop="name">
          <el-input v-model="categoryForm.name" placeholder="请输入分类名称" />
        </el-form-item>
        
        <el-form-item label="所属模块" prop="module_id">
          <el-select v-model="categoryForm.module_id" placeholder="选择模块" :disabled="!selectedProjectId">
            <el-option
              v-for="module in currentModules"
              :key="module.id"
              :label="module.name"
              :value="module.id"
            >
              🔧 {{ module.name }}
            </el-option>
          </el-select>
          <div v-if="currentModules.length === 0" style="color: #f56c6c; font-size: 12px; margin-top: 5px;">
            当前项目暂无模块，请先创建模块
          </div>
        </el-form-item>
        
        <el-form-item label="分类描述" prop="description">
          <el-input
            v-model="categoryForm.description"
            type="textarea"
            placeholder="请输入分类描述"
            :rows="3"
          />
        </el-form-item>
        
        <el-form-item label="分类颜色" prop="color">
          <el-color-picker v-model="categoryForm.color" />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="categoryDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSaveCategory" :loading="categoryLoading">
          确定
        </el-button>
      </template>
    </el-dialog>

    <!-- 创建/编辑接口对话框 -->
    <el-dialog
      v-model="apiDialogVisible"
      :title="apiForm.id ? '编辑接口' : '新增接口'"
      width="800px"
    >
      <el-form
        ref="apiFormRef"
        :model="apiForm"
        :rules="apiRules"
        label-width="100px"
      >
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="接口名称" prop="name">
              <el-input v-model="apiForm.name" placeholder="请输入接口名称" />
            </el-form-item>
          </el-col>
          
          <el-col :span="12">
            <el-form-item label="请求方法" prop="method">
              <el-select v-model="apiForm.method" placeholder="选择请求方法">
                <el-option label="GET" value="GET" />
                <el-option label="POST" value="POST" />
                <el-option label="PUT" value="PUT" />
                <el-option label="DELETE" value="DELETE" />
                <el-option label="PATCH" value="PATCH" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-form-item label="接口地址" prop="url">
          <el-input v-model="apiForm.url" placeholder="请输入接口地址" />
        </el-form-item>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="所属分类">
              <el-select v-model="apiForm.category_id" placeholder="选择分类" clearable>
                <el-option
                  v-for="category in categories"
                  :key="category.id"
                  :label="category.name"
                  :value="category.id"
                >
                  <span :style="{ color: category.color }">● </span>
                  {{ category.name }}
                </el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-form-item label="接口描述">
          <el-input
            v-model="apiForm.description"
            type="textarea"
            placeholder="请输入接口描述"
            :rows="3"
          />
        </el-form-item>
        
        <el-form-item label="请求头">
          <el-input
            v-model="apiForm.headersText"
            type="textarea"
            placeholder="请输入JSON格式的请求头"
            :rows="4"
          />
        </el-form-item>
        
        <el-form-item label="请求参数">
          <el-input
            v-model="apiForm.paramsText"
            type="textarea"
            placeholder="请输入JSON格式的请求参数"
            :rows="4"
          />
        </el-form-item>
        
        <el-form-item label="请求体">
          <el-input
            v-model="apiForm.bodyText"
            type="textarea"
            placeholder="请输入JSON格式的请求体"
            :rows="4"
          />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="apiDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSaveAPI" :loading="apiLoading">
          确定
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed, watch, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox, ElButton, ElCard, ElInput, ElSelect, ElOption, ElRow, ElCol, ElTable, ElTableColumn, ElTag, ElLink, ElPagination, ElDialog, ElForm, ElFormItem, ElColorPicker, ElIcon } from 'element-plus'
import { Plus, Search, Close, Edit, VideoPlay, Delete, Upload } from '@element-plus/icons-vue'
import { apiApi, categoryApi, projectApi, type API, type Category, type APICreate, type APIUpdate, type CategoryCreate, type CategoryUpdate, type ProjectStats, type ModuleStats } from '@/api/api'

const route = useRoute()
const router = useRouter()

// 响应式数据
const loading = ref(false)
const categoryLoading = ref(false)
const apiLoading = ref(false)

// 项目层级相关
const selectedProjectId = ref<number | undefined>()
const selectedModuleId = ref<number | undefined>()
const projects = ref<ProjectStats[]>([])
const currentModules = ref<ModuleStats[]>([])

// 搜索相关
const searchKeyword = ref('')
const selectedCategoryId = ref<number | undefined>()

// 分页相关
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)

// 数据列表
const categories = ref<Category[]>([])
const apis = ref<API[]>([])

// 计算属性
const currentCategories = computed(() => {
  if (selectedModuleId.value) {
    // 如果选择了模块，只显示该模块下的分类
    return categories.value.filter(cat => cat.module_id === selectedModuleId.value)
  } else if (selectedProjectId.value) {
    // 如果只选择了项目，显示项目下的所有分类
    return categories.value
  }
  return []
})

// 层级名称获取方法
const getCurrentProjectName = () => {
  const project = projects.value.find(p => p.id === selectedProjectId.value)
  return project?.name || ''
}

const getCurrentModuleName = () => {
  const module = currentModules.value.find(m => m.id === selectedModuleId.value)
  return module?.name || ''
}

const getCurrentCategoryName = () => {
  const category = currentCategories.value.find(c => c.id === selectedCategoryId.value)
  return category?.name || ''
}

const getModuleName = (moduleId: number) => {
  const module = currentModules.value.find(m => m.id === moduleId)
  return module?.name || '未知模块'
}

// 分类对话框
const categoryDialogVisible = ref(false)
const categoryFormRef = ref()
const categoryForm = reactive({
  id: undefined as number | undefined,
  name: '',
  description: '',
  color: '#00d4ff',
  module_id: undefined as number | undefined
})

const categoryRules = {
  name: [
    { required: true, message: '请输入分类名称', trigger: 'blur' },
    { min: 1, max: 100, message: '分类名称长度在 1 到 100 个字符', trigger: 'blur' }
  ],
  module_id: [
    { required: true, message: '请选择所属模块', trigger: 'change' }
  ]
}

// 接口对话框
const apiDialogVisible = ref(false)
const apiFormRef = ref()
const apiForm = reactive({
  id: undefined as number | undefined,
  name: '',
  method: 'GET',
  url: '',
  description: '',
  category_id: undefined as number | undefined,
  headersText: '',
  paramsText: '',
  bodyText: ''
})

const apiRules = {
  name: [
    { required: true, message: '请输入接口名称', trigger: 'blur' },
    { min: 1, max: 200, message: '接口名称长度在 1 到 200 个字符', trigger: 'blur' }
  ],
  method: [
    { required: true, message: '请选择请求方法', trigger: 'change' }
  ],
  url: [
    { required: true, message: '请输入接口地址', trigger: 'blur' },
    { min: 1, max: 500, message: '接口地址长度在 1 到 500 个字符', trigger: 'blur' }
  ]
}

// 方法
const loadProjects = async () => {
  try {
    const response = await projectApi.getProjects()
    projects.value = response.data || response || []
    console.log('加载项目列表:', projects.value)
  } catch (error) {
    console.error('Failed to load projects:', error)
    ElMessage.error('加载项目列表失败')
  }
}

const loadModules = async (projectId: number) => {
  try {
    const response = await projectApi.getModules(projectId)
    currentModules.value = response.data || response
  } catch (error) {
    console.error('Failed to load modules:', error)
  }
}

const loadCategories = async (moduleId?: number, projectId?: number) => {
  try {
    const params: any = {}
    if (moduleId) params.module_id = moduleId
    if (projectId) params.project_id = projectId
    
    const response = await categoryApi.getCategories(params)
    categories.value = response.data || response || []
    console.log('加载分类:', { moduleId, projectId, count: categories.value.length })
  } catch (error) {
    console.error('Failed to load categories:', error)
    ElMessage.error('加载分类列表失败')
  }
}

const handleProjectChange = async (projectId: number | undefined) => {
  selectedModuleId.value = undefined
  selectedCategoryId.value = undefined
  categories.value = []
  
  if (projectId) {
    // 加载项目的模块
    await loadModules(projectId)
    // 加载项目下的所有分类
    await loadCategories(undefined, projectId)
    console.log('项目变更 - 项目ID:', projectId, '分类数量:', categories.value.length)
  } else {
    currentModules.value = []
  }
  
  handleSearch()
}

const handleModuleChange = async (moduleId: number | undefined) => {
  console.log('=== 模块选择变更 (@change) ===')
  console.log('handleModuleChange 参数:', moduleId)
  console.log('变更前 selectedModuleId.value:', selectedModuleId.value)
  
  // 🔥 强制设置模块ID，确保设置成功
  selectedModuleId.value = moduleId
  
  console.log('强制设置后 selectedModuleId.value:', selectedModuleId.value)
  
  // 重置分类选择
  selectedCategoryId.value = undefined
  
  console.log('==================')
  
  handleSearch()
}

const handleModuleDirectChange = async (moduleId: number | undefined) => {
  console.log('=== 模块直接变更 (@update:modelValue) ===')
  console.log('handleModuleDirectChange 参数:', moduleId)
  console.log('当前 selectedModuleId.value:', selectedModuleId.value)
  
  // 确保值被设置
  selectedModuleId.value = moduleId
  
  // 重置分类选择
  selectedCategoryId.value = undefined
  
  console.log('设置后 selectedModuleId.value:', selectedModuleId.value)
  console.log('==================')
  
  // 延迟一下再搜索，确保所有值都更新了
  setTimeout(() => {
    handleSearch()
  }, 100)
}

const loadAPIs = async () => {
  console.log('🚀 loadAPIs 开始执行 - 这是最新版本的代码!')
  console.log('🔍 当前状态检查:')
  console.log('  - selectedProjectId.value:', selectedProjectId.value)
  console.log('  - selectedModuleId.value:', selectedModuleId.value)
  console.log('  - selectedCategoryId.value:', selectedCategoryId.value)
  console.log('  - searchKeyword.value:', searchKeyword.value)
  console.log('  - searchKeyword 类型:', typeof searchKeyword.value)
  console.log('  - searchKeyword 长度:', searchKeyword.value.length)
  console.log('  - selectedModuleId 类型:', typeof selectedModuleId.value)
  console.log('  - selectedModuleId 是否为 null:', selectedModuleId.value === null)
  console.log('  - selectedModuleId 是否为 undefined:', selectedModuleId.value === undefined)
  console.log('  - currentModules.length:', currentModules.value.length)
  console.log('  - currentModules:', currentModules.value.map(m => ({ id: m.id, name: m.name })))
  
  loading.value = true
  try {
    const params: any = {
      skip: (currentPage.value - 1) * pageSize.value,
      limit: pageSize.value
    }
    
    // 支持项目ID、模块ID和分类ID的组合过滤
    if (selectedProjectId.value) {
      params.project_id = selectedProjectId.value
      console.log('✅ 添加项目ID到参数:', selectedProjectId.value)
    }
    
    if (selectedModuleId.value) {
      params.module_id = selectedModuleId.value
      console.log('✅ 添加模块ID到参数:', selectedModuleId.value)
    } else {
      console.log('❌ 模块ID为空，值为:', selectedModuleId.value)
    }
    
    if (selectedCategoryId.value) {
      params.category_id = selectedCategoryId.value
    }
    
    if (searchKeyword.value) {
      params.keyword = searchKeyword.value
      console.log('✅ 添加搜索关键词到参数:', searchKeyword.value)
    } else {
      console.log('❌ 搜索关键词为空，值为:', searchKeyword.value)
    }
    
    console.log('=== 加载接口调试信息 ===')
    console.log('selectedProjectId:', selectedProjectId.value)
    console.log('selectedModuleId:', selectedModuleId.value)
    console.log('selectedCategoryId:', selectedCategoryId.value)
    console.log('API参数:', params)
    console.log('========================')
    
    const response = await apiApi.getAPIs(params)
    const data = response.data || response || []
    apis.value = Array.isArray(data) ? data : []
    total.value = Array.isArray(data) ? data.length : 0
    
    console.log('🔍 API响应数据调试:')
    console.log('  - response:', response)
    console.log('  - data:', data)
    console.log('  - apis.value:', apis.value)
    console.log('  - 第一个API数据:', apis.value[0])
    if (apis.value[0]) {
      console.log('  - 第一个API的url字段:', apis.value[0].url)
      console.log('  - 第一个API的params字段:', apis.value[0].params)
      console.log('  - 第一个API的headers字段:', apis.value[0].headers)
    }
    
    console.log('加载接口:', { 
      projectId: selectedProjectId.value,
      moduleId: selectedModuleId.value, 
      categoryId: selectedCategoryId.value, 
      keyword: searchKeyword.value,
      count: apis.value.length 
    })
  } catch (error) {
    console.error('Failed to load APIs:', error)
    ElMessage.error('加载接口列表失败')
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  console.log('🔍 handleSearch 被调用')
  console.log('  - 调用前 selectedModuleId.value:', selectedModuleId.value)
  currentPage.value = 1
  console.log('  - 即将调用 loadAPIs()')
  loadAPIs()
}

const handleReset = () => {
  searchKeyword.value = ''
  selectedModuleId.value = undefined
  selectedCategoryId.value = undefined
  currentPage.value = 1
  // 保持项目选择，只重置搜索条件
  loadAPIs()
}

const goToImportAPI = () => {
  router.push('/apis/import')
}

const handleSizeChange = (size: number) => {
  pageSize.value = size
  loadAPIs()
}

const handleCurrentChange = (page: number) => {
  currentPage.value = page
  loadAPIs()
}

// 分类相关方法
const showCreateCategoryDialog = () => {
  // 检查是否已选择项目
  if (!selectedProjectId.value) {
    ElMessage.error('请先选择项目')
    return
  }
  
  // 检查模块数据是否已加载
  if (currentModules.value.length === 0) {
    ElMessage.error('该项目暂无模块，请先创建模块')
    return
  }
  
  resetCategoryForm()
  // 新建分类时，如果选择了模块则使用当前模块，否则选择第一个模块
  categoryForm.module_id = selectedModuleId.value || currentModules.value[0]?.id
  categoryDialogVisible.value = true
}

const showEditCategoryDialog = (category: Category) => {
  resetCategoryForm()
  categoryForm.id = category.id
  categoryForm.name = category.name
  categoryForm.description = category.description || ''
  categoryForm.color = category.color
  categoryForm.module_id = category.module_id
  categoryDialogVisible.value = true
}

const resetCategoryForm = () => {
  categoryForm.id = undefined
  categoryForm.name = ''
  categoryForm.description = ''
  categoryForm.color = '#00d4ff'
  categoryForm.module_id = undefined
}

const handleSaveCategory = async () => {
  try {
    await categoryFormRef.value.validate()
    categoryLoading.value = true
    
    const data: CategoryCreate | CategoryUpdate = {
      name: categoryForm.name,
      description: categoryForm.description,
      color: categoryForm.color
    }
    
    if (categoryForm.id) {
      await categoryApi.updateCategory(categoryForm.id, data as CategoryUpdate)
      ElMessage.success('分类更新成功')
    } else {
      // 确保选择了模块
      if (!categoryForm.module_id) {
        ElMessage.error('请选择模块')
        return
      }
      await categoryApi.createCategory({ ...data, module_id: categoryForm.module_id } as CategoryCreate)
      ElMessage.success('分类创建成功')
    }
    
    categoryDialogVisible.value = false
    await loadCategories(undefined, selectedProjectId.value)
  } catch (error) {
    console.error('Failed to save category:', error)
  } finally {
    categoryLoading.value = false
  }
}

const handleDeleteCategory = async (id: number) => {
  try {
    await ElMessageBox.confirm('确认删除此分类吗？删除后分类下的接口将变为未分类状态。', '警告', {
      confirmButtonText: '确认',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    await categoryApi.deleteCategory(id)
    ElMessage.success('分类删除成功')
    await loadCategories(undefined, selectedProjectId.value)
    await loadAPIs()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('Failed to delete category:', error)
    }
  }
}

const handleCategoryClick = (category: Category) => {
  console.log('=== 分类卡片点击 ===')
  console.log('点击的分类:', category.name, 'ID:', category.id)
  console.log('点击前 selectedCategoryId:', selectedCategoryId.value)
  selectedCategoryId.value = category.id
  console.log('点击后 selectedCategoryId:', selectedCategoryId.value)
  console.log('==================')
  handleSearch()
}

// 接口相关方法
const showCreateAPIDialog = () => {
  resetAPIForm()
  apiDialogVisible.value = true
}

const resetAPIForm = () => {
  apiForm.id = undefined
  apiForm.name = ''
  apiForm.method = 'GET'
  apiForm.url = ''
  apiForm.description = ''
  apiForm.category_id = undefined
  apiForm.headersText = ''
  apiForm.paramsText = ''
  apiForm.bodyText = ''
}

const parseJsonText = (text: string) => {
  if (!text.trim()) return undefined
  try {
    return JSON.parse(text)
  } catch (error) {
    console.warn('JSON解析失败:', text, error)
    // 如果解析失败，返回原文本而不是undefined
    return text
  }
}

const handleSaveAPI = async () => {
  try {
    await apiFormRef.value.validate()
    apiLoading.value = true
    
    // 验证JSON格式的字段
    const headers = parseJsonText(apiForm.headersText)
    const params = parseJsonText(apiForm.paramsText) 
    const body = parseJsonText(apiForm.bodyText)
    
    const data: APICreate | APIUpdate = {
      name: apiForm.name,
      method: apiForm.method,
      url: apiForm.url,
      description: apiForm.description,
      category_id: apiForm.category_id,
      headers: headers,
      params: params,
      body: body
    }
    
    console.log('准备提交的API数据:', data)
    
    if (apiForm.id) {
      await apiApi.updateAPI(apiForm.id, data as APIUpdate)
      ElMessage.success('接口更新成功')
    } else {
      await apiApi.createAPI(data as APICreate)
      ElMessage.success('接口创建成功')
    }
    
    apiDialogVisible.value = false
    await loadAPIs()
  } catch (error: any) {
    console.error('保存接口失败:', error)
    
    // 详细的错误信息处理
    if (error?.response?.data?.detail) {
      ElMessage.error(`保存失败: ${error.response.data.detail}`)
    } else if (error?.message) {
      ElMessage.error(`保存失败: ${error.message}`)
    } else {
      ElMessage.error('保存接口失败，请检查输入的数据格式')
    }
  } finally {
    apiLoading.value = false
  }
}

const handleEditAPI = (api: API) => {
  apiForm.id = api.id
  apiForm.name = api.name
  apiForm.method = api.method
  apiForm.url = api.url
  apiForm.description = api.description || ''
  apiForm.category_id = api.category_id
  apiForm.headersText = api.headers ? JSON.stringify(api.headers, null, 2) : ''
  apiForm.paramsText = api.params ? JSON.stringify(api.params, null, 2) : ''
  apiForm.bodyText = api.body ? JSON.stringify(api.body, null, 2) : ''
  apiDialogVisible.value = true
}

const handleViewAPI = (api: API) => {
  // 这里可以实现查看接口详情的逻辑
  ElMessage.info('查看接口详情功能待实现')
}

const handleTestAPI = (api: API) => {
  // 这里可以实现测试接口的逻辑
  ElMessage.info('测试接口功能待实现')
}

const handleDeleteAPI = async (id: number) => {
  try {
    await ElMessageBox.confirm('确认删除此接口吗？', '警告', {
      confirmButtonText: '确认',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    await apiApi.deleteAPI(id)
    ElMessage.success('接口删除成功')
    await loadAPIs()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('Failed to delete API:', error)
    }
  }
}

// 工具方法
const getMethodType = (method: string): 'success' | 'primary' | 'warning' | 'danger' | 'info' => {
  const types: Record<string, 'success' | 'primary' | 'warning' | 'danger' | 'info'> = {
    GET: 'success',
    POST: 'primary',
    PUT: 'warning',
    DELETE: 'danger',
    PATCH: 'info'
  }
  return types[method.toUpperCase()] || 'info'
}

const getBodyType = (body: any): string => {
  if (!body) return '无数据'
  if (typeof body === 'string') {
    try {
      JSON.parse(body)
      return 'JSON'
    } catch {
      return 'Text'
    }
  }
  if (typeof body === 'object') return 'JSON'
  return 'Unknown'
}

const formatDateTime = (dateTime: string) => {
  return new Date(dateTime).toLocaleString()
}

// 初始化URL参数
const initializeFromQuery = async () => {
  const projectId = route.query.project_id ? parseInt(route.query.project_id as string) : undefined
  const moduleId = route.query.module_id ? parseInt(route.query.module_id as string) : undefined
  
  if (projectId) {
    selectedProjectId.value = projectId
    await loadModules(projectId)
    
    if (moduleId && currentModules.value.some(m => m.id === moduleId)) {
      selectedModuleId.value = moduleId
      await loadCategories(moduleId)
    }
  }
}

// 监听路由查询参数变化
watch(() => route.query, async (newQuery) => {
  const projectId = newQuery.project_id ? parseInt(newQuery.project_id as string) : undefined
  const moduleId = newQuery.module_id ? parseInt(newQuery.module_id as string) : undefined
  
  if (projectId !== selectedProjectId.value) {
    selectedProjectId.value = projectId
    selectedModuleId.value = undefined
    selectedCategoryId.value = undefined
    currentModules.value = []
    
    if (projectId) {
      await loadModules(projectId)
    }
  }
  
  if (moduleId !== selectedModuleId.value && moduleId && currentModules.value.some(m => m.id === moduleId)) {
    selectedModuleId.value = moduleId
    selectedCategoryId.value = undefined
    await loadCategories(moduleId)
  }
  
  handleSearch()
}, { immediate: false })

// 生命周期
onMounted(async () => {
  await loadProjects()
  await initializeFromQuery()
  await loadCategories()
  await loadAPIs()
})
</script>

<style lang="scss" scoped>
.api-page {
  padding: 0;
  min-height: 100vh;
}

// 页面标题区域
.page-header {
  margin-bottom: 32px;
  padding: 32px;
  position: relative;
  
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 2px;
    background: var(--gradient-neon);
    opacity: 0.8;
  }
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.title-section {
  flex: 1;
}

.page-title {
  margin: 0 0 8px 0;
  font-size: 32px;
  font-weight: 900;
  font-family: 'Orbitron', monospace;
  letter-spacing: 2px;
}

.page-subtitle {
  margin: 0 0 16px 0;
  font-size: 14px;
  color: var(--text-secondary);
  font-weight: 300;
  letter-spacing: 3px;
  text-transform: uppercase;
}

.title-glow {
  width: 80px;
  height: 2px;
  background: var(--gradient-neon);
  border-radius: 1px;
  animation: pulse-glow 2s ease-in-out infinite;
}

.header-actions {
  display: flex;
  gap: 16px;
}

// 主内容容器
.content-container {
  padding: 32px;
  margin-bottom: 32px;
}

// 搜索控制台
.search-console {
  margin-bottom: 32px;
  padding: 24px;
}

.console-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.console-title {
  margin: 0;
  font-size: 18px;
  font-weight: 700;
  color: var(--text-primary);
  font-family: 'Orbitron', monospace;
}

.console-status {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  color: var(--text-secondary);
  font-weight: 600;
}

.status-dot {
  width: 6px;
  height: 6px;
  background: var(--success);
  border-radius: 50%;
  box-shadow: 0 0 8px var(--success);
}

.input-group {
  margin-bottom: 16px;
}

.input-label {
  display: block;
  margin-bottom: 8px;
  font-size: 12px;
  color: var(--text-secondary);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.category-dot {
  margin-right: 8px;
  font-size: 12px;
}

.button-group {
  display: flex;
  gap: 12px;
}

// 项目统计信息
.project-stats {
  margin-top: 24px;
  padding-top: 24px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
}

.stat-card {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(0, 212, 255, 0.2);
  border-radius: 8px;
  padding: 16px;
  display: flex;
  align-items: center;
  gap: 12px;
  transition: all 0.3s ease;
  
  &:hover {
    border-color: rgba(0, 212, 255, 0.5);
    background: rgba(0, 212, 255, 0.05);
    transform: translateY(-2px);
  }
}

.stat-icon {
  font-size: 24px;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 212, 255, 0.1);
  border-radius: 8px;
}

.stat-content {
  flex: 1;
}

.stat-value {
  font-size: 20px;
  font-weight: 700;
  color: var(--primary);
  font-family: 'Orbitron', monospace;
  line-height: 1;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 12px;
  color: var(--text-secondary);
  font-weight: 400;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.module-tag {
  font-size: 11px;
  color: var(--text-secondary);
  margin-left: 8px;
  padding: 2px 6px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 10px;
}

.breadcrumb-module {
  font-size: 11px;
  color: var(--text-secondary);
  margin-left: 8px;
}

// 分类管理终端
.category-terminal {
  margin-bottom: 32px;
  padding: 24px;
}

.terminal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.terminal-title {
  margin: 0;
  font-size: 18px;
  font-weight: 700;
  color: var(--text-primary);
  font-family: 'Orbitron', monospace;
}

.terminal-info {
  display: flex;
  gap: 16px;
}

.info-item {
  font-size: 12px;
  
  .info-label {
    color: var(--text-muted);
  }
  
  .info-value {
    font-weight: 600;
  }
}

.category-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 16px;
}

.category-module {
  padding: 20px;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  
  &:hover {
    transform: translateY(-4px);
    border-color: var(--accent-primary);
  }
}

.module-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}

.module-indicator {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  box-shadow: 0 0 8px currentColor;
}

.module-name {
  flex: 1;
  font-weight: 700;
  font-size: 16px;
  color: var(--text-primary);
}

.module-actions {
  display: flex;
  gap: 4px;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.category-module:hover .module-actions {
  opacity: 1;
}

.delete-btn {
  opacity: 0;
  transition: opacity 0.3s ease;
}

.category-module:hover .delete-btn {
  opacity: 1;
}

.module-stats {
  margin-bottom: 8px;
  font-size: 12px;
  
  .stat-label {
    color: var(--text-muted);
  }
  
  .stat-value {
    color: var(--accent-primary);
    font-weight: 600;
  }
}

.module-description {
  font-size: 12px;
  color: var(--text-secondary);
  line-height: 1.4;
}

// 接口数据库
.api-database {
  padding: 24px;
}

.database-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.database-title {
  margin: 0;
  font-size: 18px;
  font-weight: 700;
  color: var(--text-primary);
  font-family: 'Orbitron', monospace;
}

.database-stats {
  display: flex;
  gap: 24px;
}

.stat-item {
  font-size: 12px;
  
  .stat-label {
    color: var(--text-muted);
  }
  
  .stat-value {
    font-weight: 600;
    margin-left: 4px;
  }
}

// 表格样式
.cyber-table {
  :deep(.el-table__header) {
    background: var(--bg-secondary);
    
    th {
      background: var(--bg-secondary) !important;
      color: var(--text-primary) !important;
      border-bottom: 2px solid var(--accent-primary) !important;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 1px;
      font-size: 12px;
    }
  }
  
  :deep(.el-table__body) {
    tr {
      transition: all 0.3s ease;
      
      &:hover {
        background: var(--bg-glass-dark) !important;
      }
    }
    
    td {
      border-bottom: 1px solid rgba(255, 255, 255, 0.05) !important;
      color: var(--text-primary) !important;
      
      // 确保所有文本内容都可见
      .cell {
        color: var(--text-primary) !important;
      }
      
      // 链接样式
      a {
        color: var(--accent-primary) !important;
        text-decoration: none;
        
        &:hover {
          color: var(--accent-secondary) !important;
        }
      }
    }
  }
}

// 操作按钮
.action-buttons {
  display: flex;
  gap: 8px;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 6px 12px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
  transition: all 0.3s ease;
  
  &.edit-btn:hover {
    background: rgba(0, 212, 255, 0.1);
    color: var(--accent-primary);
  }
  
  &.test-btn:hover {
    background: rgba(0, 255, 159, 0.1);
    color: var(--success);
  }
  
  &.delete-btn:hover {
    background: rgba(255, 107, 107, 0.1);
    color: var(--error);
  }
}

// 分页控制器
.pagination-controller {
  margin-top: 32px;
  padding-top: 24px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.controller-info {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}

.info-text {
  font-size: 12px;
  color: var(--text-secondary);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.status-indicator {
  width: 6px;
  height: 6px;
  background: var(--accent-primary);
  border-radius: 50%;
  box-shadow: 0 0 8px var(--accent-primary);
}

.cyber-pagination {
  display: flex;
  justify-content: center;
}

// 层级面包屑
.hierarchy-breadcrumb {
  margin-top: 20px;
  padding: 16px;
  background: var(--bg-glass-dark);
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: 12px;
  border: 1px solid rgba(0, 212, 255, 0.2);
}

.breadcrumb-item {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  background: var(--bg-secondary);
  border-radius: 6px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.breadcrumb-icon {
  font-size: 14px;
}

.breadcrumb-text {
  font-size: 12px;
  color: var(--text-primary);
  font-weight: 600;
}

.breadcrumb-arrow {
  color: var(--accent-primary);
  font-size: 16px;
  font-weight: bold;
}

// 空状态
.empty-state {
  margin-bottom: 32px;
  padding: 60px 24px;
  text-align: center;
}

.empty-content {
  max-width: 400px;
  margin: 0 auto;
}

.empty-icon {
  font-size: 64px;
  margin-bottom: 16px;
  opacity: 0.5;
}

.empty-title {
  font-size: 20px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 8px;
}

.empty-desc {
  font-size: 14px;
  color: var(--text-secondary);
  margin-bottom: 24px;
  line-height: 1.5;
}

// 工具类
.text-gray {
  color: var(--text-muted) !important;
  font-size: 12px;
  font-weight: 500;
}

.url-fallback {
  color: var(--text-muted) !important;
  font-style: italic;
  background: rgba(255, 255, 255, 0.05);
  padding: 2px 6px;
  border-radius: 3px;
}

.url-debug {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.debug-info {
  font-size: 9px !important;
  color: var(--warning) !important;
  font-family: monospace;
  opacity: 0.7;
}

.cyber-button-small {
  padding: 8px 16px;
  font-size: 12px;
  border-radius: 6px;
}

// 参数显示
.params-display, .body-display, .headers-display, .url-display {
  max-width: 100%;
}

.url-text {
  background: rgba(0, 255, 159, 0.15) !important;
  border: 1px solid rgba(0, 255, 159, 0.4) !important;
  border-radius: 4px;
  padding: 4px 8px;
  font-size: 11px !important;
  color: var(--success) !important;
  font-family: 'Courier New', monospace;
  display: inline-block;
  max-width: 100%;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-weight: 600 !important;
}

.params-preview {
  display: inline-block;
  padding: 4px 8px;
  background: rgba(0, 212, 255, 0.15) !important;
  border: 1px solid rgba(0, 212, 255, 0.4) !important;
  border-radius: 4px;
  font-size: 11px !important;
  color: var(--accent-primary) !important;
  font-family: 'Courier New', monospace;
  max-width: 100%;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-weight: 600 !important;
}

.headers-preview {
  .el-tag {
    font-size: 10px;
    border-radius: 4px;
  }
}

.body-preview {
  .el-tag {
    font-size: 10px;
    border-radius: 4px;
  }
}

// 响应式
@media (max-width: 768px) {
  .page-header {
    padding: 24px 16px;
  }
  
  .header-content {
    flex-direction: column;
    gap: 24px;
    align-items: flex-start;
  }
  
  .content-container {
    padding: 16px;
  }
  
  .category-grid {
    grid-template-columns: 1fr;
  }
  
  .database-stats {
    flex-direction: column;
    gap: 8px;
  }
  
  .action-buttons {
    flex-direction: column;
    gap: 4px;
  }
}
</style> 