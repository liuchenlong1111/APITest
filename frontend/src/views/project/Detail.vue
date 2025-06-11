<template>
  <div class="project-detail-page">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="header-left">
        <el-button 
          type="text" 
          class="back-btn"
          @click="$router.go(-1)"
        >
          <el-icon><ArrowLeft /></el-icon>
          返回
        </el-button>
        <div class="project-title">
          <h1>{{ projectData?.name || '项目详情' }}</h1>
          <p class="project-desc">{{ projectData?.description || '暂无描述' }}</p>
        </div>
      </div>
      <div class="header-actions">
        <el-button 
          type="primary" 
          @click="showModuleDialog = true"
        >
          <el-icon><Plus /></el-icon>
          新建模块
        </el-button>
        <el-dropdown @command="handleProjectAction">
          <el-button type="default">
            项目操作
            <el-icon class="ml-1"><ArrowDown /></el-icon>
          </el-button>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="edit">
                <el-icon><Edit /></el-icon>
                编辑项目
              </el-dropdown-item>
              <el-dropdown-item command="delete" divided class="danger-item">
                <el-icon><Delete /></el-icon>
                删除项目
              </el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </div>

    <!-- 项目统计 -->
    <div class="stats-grid" v-if="projectData">
      <div class="stat-card">
        <div class="stat-icon">🔧</div>
        <div class="stat-content">
          <div class="stat-value">{{ projectData.module_count }}</div>
          <div class="stat-label">模块数量</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">📂</div>
        <div class="stat-content">
          <div class="stat-value">{{ projectData.category_count }}</div>
          <div class="stat-label">分类数量</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">🔗</div>
        <div class="stat-content">
          <div class="stat-value">{{ projectData.api_count }}</div>
          <div class="stat-label">接口数量</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">📅</div>
        <div class="stat-content">
          <div class="stat-value">{{ formatDate(projectData.created_at) }}</div>
          <div class="stat-label">创建时间</div>
        </div>
      </div>
    </div>

    <!-- 模块列表 -->
    <div class="modules-section">
      <div class="section-title">
        <span class="icon">🔧</span>
        项目模块
        <span class="count" v-if="projectData">({{ projectData.modules?.length || 0 }})</span>
      </div>
      
      <div class="modules-grid" v-loading="loading">
        <div
          v-for="module in projectData?.modules"
          :key="module.id"
          class="module-card"
          @click="goToModule(module.id)"
        >
          <div class="module-header">
            <div class="module-info">
              <h3 class="module-name">{{ module.name }}</h3>
              <p class="module-desc">{{ module.description || '暂无描述' }}</p>
            </div>
            <el-dropdown @command="handleModuleAction" @click.stop>
              <el-icon class="more-icon"><MoreFilled /></el-icon>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item :command="`edit-${module.id}`">
                    <el-icon><Edit /></el-icon>
                    编辑模块
                  </el-dropdown-item>
                  <el-dropdown-item :command="`apis-${module.id}`">
                    <el-icon><Connection /></el-icon>
                    管理接口
                  </el-dropdown-item>
                  <el-dropdown-item 
                    :command="`delete-${module.id}`" 
                    divided
                    class="danger-item"
                  >
                    <el-icon><Delete /></el-icon>
                    删除模块
                  </el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
          
          <div class="module-stats">
            <div class="stat-item">
              <span class="stat-icon">📂</span>
              <span class="stat-text">{{ module.category_count }} 个分类</span>
            </div>
            <div class="stat-item">
              <span class="stat-icon">🔗</span>
              <span class="stat-text">{{ module.api_count }} 个接口</span>
            </div>
          </div>
        </div>
        
        <!-- 空状态 -->
        <div v-if="projectData?.modules?.length === 0 && !loading" class="empty-state">
          <div class="empty-icon">🔧</div>
          <div class="empty-title">还没有模块</div>
          <div class="empty-desc">创建模块来组织您的API接口</div>
          <el-button type="primary" @click="showModuleDialog = true">
            创建模块
          </el-button>
        </div>
      </div>
    </div>

    <!-- 接口概览 -->
    <div class="apis-section">
      <div class="section-title">
        <span class="icon">🔗</span>
        接口概览
        <el-button 
          type="text" 
          @click="$router.push({ path: '/apis', query: { project_id: projectId } })"
          class="view-all-btn"
        >
          查看全部 →
        </el-button>
      </div>
      
      <div class="apis-preview" v-loading="apisLoading">
        <div class="api-summary-cards">
          <div class="summary-card">
            <div class="summary-title">HTTP 方法分布</div>
            <div class="method-stats">
              <div class="method-item" v-for="(count, method) in methodStats" :key="method">
                <span class="method-tag" :class="`method-${method.toLowerCase()}`">{{ method }}</span>
                <span class="method-count">{{ count }}</span>
              </div>
            </div>
          </div>
          
          <div class="summary-card">
            <div class="summary-title">接口状态分布</div>
            <div class="status-stats">
              <div class="status-item">
                <span class="status-dot active"></span>
                <span class="status-text">活跃接口：{{ activeApiCount }}</span>
              </div>
              <div class="status-item">
                <span class="status-dot inactive"></span>
                <span class="status-text">待开发：{{ inactiveApiCount }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 新建模块对话框 -->
    <el-dialog 
      v-model="showModuleDialog" 
      title="🔧 新建模块" 
      width="500px"
    >
      <el-form 
        :model="moduleForm" 
        :rules="moduleRules"
        ref="moduleFormRef"
        label-width="80px"
      >
        <el-form-item label="模块名称" prop="name">
          <el-input 
            v-model="moduleForm.name" 
            placeholder="请输入模块名称"
            maxlength="100"
            show-word-limit
          />
        </el-form-item>
        <el-form-item label="模块描述" prop="description">
          <el-input
            v-model="moduleForm.description"
            type="textarea"
            :rows="4"
            placeholder="请输入模块描述（可选）"
            maxlength="500"
            show-word-limit
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showModuleDialog = false">取消</el-button>
        <el-button 
          type="primary" 
          @click="createModule"
          :loading="creatingModule"
        >
          创建模块
        </el-button>
      </template>
    </el-dialog>

    <!-- 编辑模块对话框 -->
    <el-dialog 
      v-model="showEditModuleDialog" 
      title="✏️ 编辑模块" 
      width="500px"
    >
      <el-form 
        :model="editModuleForm" 
        :rules="moduleRules"
        ref="editModuleFormRef"
        label-width="80px"
      >
        <el-form-item label="模块名称" prop="name">
          <el-input 
            v-model="editModuleForm.name" 
            placeholder="请输入模块名称"
            maxlength="100"
            show-word-limit
          />
        </el-form-item>
        <el-form-item label="模块描述" prop="description">
          <el-input
            v-model="editModuleForm.description"
            type="textarea"
            :rows="4"
            placeholder="请输入模块描述（可选）"
            maxlength="500"
            show-word-limit
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showEditModuleDialog = false">取消</el-button>
        <el-button 
          type="primary" 
          @click="updateModule"
          :loading="updatingModule"
        >
          保存更改
        </el-button>
      </template>
    </el-dialog>

    <!-- 编辑项目对话框 -->
    <el-dialog 
      v-model="showEditProjectDialog" 
      title="✏️ 编辑项目" 
      width="500px"
    >
      <el-form 
        :model="editProjectForm" 
        :rules="projectRules"
        ref="editProjectFormRef"
        label-width="80px"
      >
        <el-form-item label="项目名称" prop="name">
          <el-input 
            v-model="editProjectForm.name" 
            placeholder="请输入项目名称"
            maxlength="100"
            show-word-limit
          />
        </el-form-item>
        <el-form-item label="项目描述" prop="description">
          <el-input
            v-model="editProjectForm.description"
            type="textarea"
            :rows="4"
            placeholder="请输入项目描述（可选）"
            maxlength="500"
            show-word-limit
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showEditProjectDialog = false">取消</el-button>
        <el-button 
          type="primary" 
          @click="updateProject"
          :loading="updatingProject"
        >
          保存更改
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { 
  ArrowLeft, ArrowDown, Plus, Edit, Delete, MoreFilled, Connection 
} from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox, type FormInstance } from 'element-plus'
import { projectApi, apiApi, moduleApi } from '@/api/api'
import type { 
  ModuleCreate, ModuleUpdate, ProjectUpdate 
} from '@/api/api'

const route = useRoute()
const router = useRouter()

// 获取项目ID
const projectId = computed(() => parseInt(route.params.id as string))

// 响应式数据
const loading = ref(false)
const apisLoading = ref(false)
const creatingModule = ref(false)
const updatingModule = ref(false)
const updatingProject = ref(false)
const projectData = ref<any>(null)
const showModuleDialog = ref(false)
const showEditModuleDialog = ref(false)
const showEditProjectDialog = ref(false)
const currentEditModuleId = ref<number | null>(null)

// 接口统计数据
const methodStats = ref<Record<string, number>>({})
const activeApiCount = ref(0)
const inactiveApiCount = ref(0)

// 表单引用
const moduleFormRef = ref<FormInstance>()
const editModuleFormRef = ref<FormInstance>()
const editProjectFormRef = ref<FormInstance>()

// 表单数据
const moduleForm = reactive<ModuleCreate>({
  name: '',
  description: '',
  project_id: 0
})

const editModuleForm = reactive<ModuleUpdate>({
  name: '',
  description: ''
})

const editProjectForm = reactive<ProjectUpdate>({
  name: '',
  description: ''
})

// 表单验证规则
const moduleRules = {
  name: [
    { required: true, message: '请输入模块名称', trigger: 'blur' },
    { min: 1, max: 100, message: '模块名称长度在 1 到 100 个字符', trigger: 'blur' }
  ]
}

const projectRules = {
  name: [
    { required: true, message: '请输入项目名称', trigger: 'blur' },
    { min: 1, max: 100, message: '项目名称长度在 1 到 100 个字符', trigger: 'blur' }
  ]
}

// 获取项目详情
const fetchProjectDetail = async () => {
  try {
    loading.value = true
    const response = await projectApi.getProject(projectId.value)
    projectData.value = response.data
  } catch (error) {
    console.error('获取项目详情失败:', error)
    ElMessage.error('获取项目详情失败')
  } finally {
    loading.value = false
  }
}

// 获取接口统计数据
const fetchApiStats = async () => {
  try {
    apisLoading.value = true
    const response = await apiApi.getAPIs({
      limit: 1000
    })
    
    const apis = response.data
    
    // 统计HTTP方法
    const methods: Record<string, number> = {}
    let active = 0
    let inactive = 0
    
    apis.forEach((api: any) => {
      // 统计方法
      const method = api.method.toUpperCase()
      methods[method] = (methods[method] || 0) + 1
      
      // 统计状态（这里假设有status字段，或者根据实际情况调整）
      if (api.is_active !== false) {
        active++
      } else {
        inactive++
      }
    })
    
    methodStats.value = methods
    activeApiCount.value = active
    inactiveApiCount.value = inactive
  } catch (error) {
    console.error('获取接口统计失败:', error)
  } finally {
    apisLoading.value = false
  }
}

// 创建模块
const createModule = async () => {
  if (!moduleFormRef.value) return
  
  const valid = await moduleFormRef.value.validate()
  if (!valid) return

  try {
    creatingModule.value = true
    moduleForm.project_id = projectId.value
    await projectApi.createModule(projectId.value, moduleForm)
    ElMessage.success('模块创建成功')
    showModuleDialog.value = false
    
    // 重置表单
    Object.assign(moduleForm, { name: '', description: '', project_id: 0 })
    moduleFormRef.value?.resetFields()
    
    // 刷新项目详情
    await fetchProjectDetail()
  } catch (error: any) {
    console.error('创建模块失败:', error)
    ElMessage.error(error.response?.data?.detail || '创建模块失败')
  } finally {
    creatingModule.value = false
  }
}

// 更新模块
const updateModule = async () => {
  if (!editModuleFormRef.value || !currentEditModuleId.value) return
  
  const valid = await editModuleFormRef.value.validate()
  if (!valid) return

  try {
    updatingModule.value = true
    await moduleApi.updateModule(currentEditModuleId.value, editModuleForm)
    ElMessage.success('模块更新成功')
    showEditModuleDialog.value = false
    
    // 刷新项目详情
    await fetchProjectDetail()
  } catch (error: any) {
    console.error('更新模块失败:', error)
    ElMessage.error(error.response?.data?.detail || '更新模块失败')
  } finally {
    updatingModule.value = false
  }
}

// 删除模块
const deleteModule = async (moduleId: number, moduleName: string) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除模块"${moduleName}"吗？删除后将无法恢复，包括其下的所有分类和接口！`,
      '⚠️ 删除确认',
      {
        confirmButtonText: '确定删除',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    await moduleApi.deleteModule(moduleId)
    ElMessage.success('模块删除成功')
    
    // 刷新项目详情
    await fetchProjectDetail()
  } catch (error: any) {
    if (error !== 'cancel') {
      console.error('删除模块失败:', error)
      ElMessage.error(error.response?.data?.detail || '删除模块失败')
    }
  }
}

// 更新项目
const updateProject = async () => {
  if (!editProjectFormRef.value) return
  
  const valid = await editProjectFormRef.value.validate()
  if (!valid) return

  try {
    updatingProject.value = true
    await projectApi.updateProject(projectId.value, editProjectForm)
    ElMessage.success('项目更新成功')
    showEditProjectDialog.value = false
    
    // 刷新项目详情
    await fetchProjectDetail()
  } catch (error: any) {
    console.error('更新项目失败:', error)
    ElMessage.error(error.response?.data?.detail || '更新项目失败')
  } finally {
    updatingProject.value = false
  }
}

// 删除项目
const deleteProject = async () => {
  try {
    await ElMessageBox.confirm(
      `确定要删除项目"${projectData.value?.name}"吗？删除后将无法恢复，包括其下的所有模块、分类和接口！`,
      '⚠️ 删除确认',
      {
        confirmButtonText: '确定删除',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    await projectApi.deleteProject(projectId.value)
    ElMessage.success('项目删除成功')
    
    // 返回项目列表
    router.push('/projects')
  } catch (error: any) {
    if (error !== 'cancel') {
      console.error('删除项目失败:', error)
      ElMessage.error(error.response?.data?.detail || '删除项目失败')
    }
  }
}

// 处理项目操作
const handleProjectAction = (command: string) => {
  if (command === 'edit') {
    editProjectForm.name = projectData.value?.name || ''
    editProjectForm.description = projectData.value?.description || ''
    showEditProjectDialog.value = true
  } else if (command === 'delete') {
    deleteProject()
  }
}

// 处理模块操作
const handleModuleAction = (command: string) => {
  const [action, id] = command.split('-')
  const moduleId = parseInt(id)
  const module = projectData.value?.modules?.find((m: any) => m.id === moduleId)
  
  if (!module) return
  
  if (action === 'edit') {
    currentEditModuleId.value = moduleId
    editModuleForm.name = module.name
    editModuleForm.description = module.description || ''
    showEditModuleDialog.value = true
  } else if (action === 'delete') {
    deleteModule(moduleId, module.name)
  } else if (action === 'apis') {
    // 跳转到接口管理页面，并筛选当前模块的接口
    router.push({ 
      path: '/apis', 
      query: { 
        project_id: projectId.value,
        module_id: moduleId 
      } 
    })
  }
}

// 跳转到模块详情（如果有的话）
const goToModule = (moduleId: number) => {
  // 可以跳转到接口管理页面并筛选该模块
  router.push({ 
    path: '/apis', 
    query: { 
      project_id: projectId.value,
      module_id: moduleId 
    } 
  })
}

// 格式化日期
const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'numeric',
    day: 'numeric'
  })
}

// 组件挂载时获取数据
onMounted(async () => {
  await fetchProjectDetail()
  await fetchApiStats()
})
</script>

<style scoped lang="scss">
.project-detail-page {
  padding: 24px;
  min-height: calc(100vh - 60px);
  background: var(--cyber-bg-primary);
}

.page-header {
  display: flex;
  justify-content: between;
  align-items: flex-start;
  margin-bottom: 24px;
  
  .header-left {
    flex: 1;
    
    .back-btn {
      color: var(--cyber-primary);
      margin-bottom: 12px;
      
      &:hover {
        color: var(--cyber-primary-light);
      }
    }
    
    .project-title {
      h1 {
        font-size: 28px;
        font-weight: 600;
        color: var(--cyber-text-primary);
        margin-bottom: 8px;
      }
      
      .project-desc {
        color: var(--cyber-text-secondary);
        font-size: 16px;
        margin: 0;
      }
    }
  }
  
  .header-actions {
    display: flex;
    gap: 12px;
    
    .ml-1 {
      margin-left: 4px;
    }
  }
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
  margin-bottom: 32px;
}

.stat-card {
  background: var(--cyber-surface);
  border: 1px solid var(--cyber-border);
  border-radius: 8px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 16px;
  
  .stat-icon {
    font-size: 24px;
    opacity: 0.8;
  }
  
  .stat-content {
    .stat-value {
      font-size: 24px;
      font-weight: 600;
      color: var(--cyber-text-primary);
      margin-bottom: 4px;
    }
    
    .stat-label {
      font-size: 14px;
      color: var(--cyber-text-secondary);
    }
  }
}

.section-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 18px;
  font-weight: 600;
  color: var(--cyber-text-primary);
  margin-bottom: 16px;
  
  .icon {
    font-size: 20px;
  }
  
  .count {
    color: var(--cyber-text-secondary);
    font-weight: normal;
    font-size: 16px;
  }
  
  .view-all-btn {
    margin-left: auto;
    color: var(--cyber-primary);
    
    &:hover {
      color: var(--cyber-primary-light);
    }
  }
}

.modules-section {
  margin-bottom: 32px;
}

.modules-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 16px;
}

.module-card {
  background: var(--cyber-surface);
  border: 1px solid var(--cyber-border);
  border-radius: 8px;
  padding: 20px;
  cursor: pointer;
  transition: all 0.3s ease;
  
  &:hover {
    border-color: var(--cyber-primary);
    box-shadow: 0 4px 12px rgba(0, 191, 255, 0.15);
  }
  
  .module-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 16px;
    
    .module-info {
      flex: 1;
      
      .module-name {
        font-size: 16px;
        font-weight: 600;
        color: var(--cyber-text-primary);
        margin-bottom: 4px;
      }
      
      .module-desc {
        font-size: 14px;
        color: var(--cyber-text-secondary);
        margin: 0;
        line-height: 1.4;
      }
    }
    
    .more-icon {
      color: var(--cyber-text-secondary);
      cursor: pointer;
      
      &:hover {
        color: var(--cyber-primary);
      }
    }
  }
  
  .module-stats {
    display: flex;
    gap: 16px;
    
    .stat-item {
      display: flex;
      align-items: center;
      gap: 4px;
      font-size: 14px;
      color: var(--cyber-text-secondary);
      
      .stat-icon {
        opacity: 0.7;
      }
    }
  }
}

.apis-section {
  .apis-preview {
    .api-summary-cards {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
      gap: 16px;
      
      .summary-card {
        background: var(--cyber-surface);
        border: 1px solid var(--cyber-border);
        border-radius: 8px;
        padding: 20px;
        
        .summary-title {
          font-size: 16px;
          font-weight: 600;
          color: var(--cyber-text-primary);
          margin-bottom: 16px;
        }
        
        .method-stats {
          display: flex;
          flex-wrap: wrap;
          gap: 8px;
          
          .method-item {
            display: flex;
            align-items: center;
            gap: 8px;
            
            .method-tag {
              padding: 2px 8px;
              border-radius: 4px;
              font-size: 12px;
              font-weight: 500;
              
              &.method-get {
                background: rgba(34, 197, 94, 0.1);
                color: #22c55e;
              }
              
              &.method-post {
                background: rgba(59, 130, 246, 0.1);
                color: #3b82f6;
              }
              
              &.method-put {
                background: rgba(251, 191, 36, 0.1);
                color: #fbbf24;
              }
              
              &.method-delete {
                background: rgba(239, 68, 68, 0.1);
                color: #ef4444;
              }
            }
            
            .method-count {
              font-size: 14px;
              color: var(--cyber-text-secondary);
            }
          }
        }
        
        .status-stats {
          .status-item {
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 8px;
            
            .status-dot {
              width: 8px;
              height: 8px;
              border-radius: 50%;
              
              &.active {
                background: #22c55e;
              }
              
              &.inactive {
                background: #6b7280;
              }
            }
            
            .status-text {
              font-size: 14px;
              color: var(--cyber-text-secondary);
            }
          }
        }
      }
    }
  }
}

.empty-state {
  text-align: center;
  padding: 40px;
  color: var(--cyber-text-secondary);
  
  .empty-icon {
    font-size: 48px;
    margin-bottom: 16px;
    opacity: 0.6;
  }
  
  .empty-title {
    font-size: 18px;
    font-weight: 600;
    margin-bottom: 8px;
    color: var(--cyber-text-primary);
  }
  
  .empty-desc {
    margin-bottom: 24px;
    font-size: 14px;
  }
}

:deep(.danger-item) {
  color: #ef4444;
  
  &:hover {
    background-color: rgba(239, 68, 68, 0.1);
  }
}
</style> 