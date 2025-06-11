<template>
  <div class="project-page">
    <!-- 页面标题 -->
    <div class="page-header">
      <h1 class="page-title">
        <span class="icon">🏗️</span>
        项目中心
        <span class="subtitle">Project Control Center</span>
      </h1>
      <el-button 
        type="primary" 
        class="create-btn"
        @click="showCreateDialog = true"
      >
        <el-icon><Plus /></el-icon>
        新建项目
      </el-button>
    </div>

    <!-- 统计卡片 -->
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon">📊</div>
        <div class="stat-content">
          <div class="stat-value">{{ totalProjects }}</div>
          <div class="stat-label">总项目数</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">🔧</div>
        <div class="stat-content">
          <div class="stat-value">{{ totalModules }}</div>
          <div class="stat-label">总模块数</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">🔗</div>
        <div class="stat-content">
          <div class="stat-value">{{ totalAPIs }}</div>
          <div class="stat-label">总接口数</div>
        </div>
      </div>
    </div>

    <!-- 项目网格 -->
    <div class="projects-container">
      <div class="section-title">
        <span class="icon">📁</span>
        项目列表
        <span class="count">({{ projects?.length || 0 }})</span>
      </div>
      
      <div class="project-grid" v-loading="loading">
        <div
          v-for="project in projects"
          :key="project.id"
          class="project-card"
          @click="goToProject(project.id)"
        >
          <div class="project-header">
            <div class="project-info">
              <h3 class="project-name">{{ project.name }}</h3>
              <p class="project-desc">{{ project.description || '暂无描述' }}</p>
            </div>
            <el-dropdown 
              @command="handleCommand" 
              trigger="click"
              @click.stop
            >
              <el-icon class="more-icon"><MoreFilled /></el-icon>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item :command="`edit-${project.id}`">
                    <el-icon><Edit /></el-icon>
                    编辑项目
                  </el-dropdown-item>
                  <el-dropdown-item 
                    :command="`delete-${project.id}`" 
                    divided
                    class="danger-item"
                  >
                    <el-icon><Delete /></el-icon>
                    删除项目
                  </el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
          
          <div class="project-stats">
            <div class="stat-item">
              <span class="stat-icon">🔧</span>
              <span class="stat-text">{{ project.module_count }} 个模块</span>
            </div>
            <div class="stat-item">
              <span class="stat-icon">📂</span>
              <span class="stat-text">{{ project.category_count }} 个分类</span>
            </div>
            <div class="stat-item">
              <span class="stat-icon">🔗</span>
              <span class="stat-text">{{ project.api_count }} 个接口</span>
            </div>
          </div>
          
          <div class="project-footer">
            <span class="create-time">
              创建于 {{ formatDate(project.created_at) }}
            </span>
            <div class="project-status">
              <span class="status-dot"></span>
              活跃
            </div>
          </div>
        </div>
        
        <!-- 空状态 -->
        <div v-if="(projects?.length || 0) === 0 && !loading" class="empty-state">
          <div class="empty-icon">🚀</div>
          <div class="empty-title">还没有项目</div>
          <div class="empty-desc">创建您的第一个项目开始管理API</div>
          <el-button type="primary" @click="showCreateDialog = true">
            立即创建
          </el-button>
        </div>
      </div>
    </div>

    <!-- 创建项目对话框 -->
    <el-dialog 
      v-model="showCreateDialog" 
      title="🚀 新建项目" 
      width="500px"
      class="cyber-dialog"
    >
      <el-form 
        :model="projectForm" 
        :rules="formRules"
        ref="formRef"
        label-width="80px"
        class="cyber-form"
      >
        <el-form-item label="项目名称" prop="name">
          <el-input 
            v-model="projectForm.name" 
            placeholder="请输入项目名称"
            maxlength="100"
            show-word-limit
          />
        </el-form-item>
        <el-form-item label="项目描述" prop="description">
          <el-input
            v-model="projectForm.description"
            type="textarea"
            :rows="4"
            placeholder="请输入项目描述（可选）"
            maxlength="500"
            show-word-limit
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showCreateDialog = false">取消</el-button>
        <el-button 
          type="primary" 
          @click="createProject"
          :loading="creating"
        >
          创建项目
        </el-button>
      </template>
    </el-dialog>

    <!-- 编辑项目对话框 -->
    <el-dialog 
      v-model="showEditDialog" 
      title="✏️ 编辑项目" 
      width="500px"
      class="cyber-dialog"
    >
      <el-form 
        :model="editForm" 
        :rules="formRules"
        ref="editFormRef"
        label-width="80px"
        class="cyber-form"
      >
        <el-form-item label="项目名称" prop="name">
          <el-input 
            v-model="editForm.name" 
            placeholder="请输入项目名称"
            maxlength="100"
            show-word-limit
          />
        </el-form-item>
        <el-form-item label="项目描述" prop="description">
          <el-input
            v-model="editForm.description"
            type="textarea"
            :rows="4"
            placeholder="请输入项目描述（可选）"
            maxlength="500"
            show-word-limit
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showEditDialog = false">取消</el-button>
        <el-button 
          type="primary" 
          @click="updateProject"
          :loading="updating"
        >
          保存更改
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { Plus, MoreFilled, Edit, Delete } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox, type FormInstance } from 'element-plus'
import { projectApi, type ProjectStats, type ProjectCreate, type ProjectUpdate } from '@/api/api'

const router = useRouter()

// 响应式数据
const loading = ref(false)
const creating = ref(false)
const updating = ref(false)
const showCreateDialog = ref(false)
const showEditDialog = ref(false)
const projects = ref<ProjectStats[]>([])
const currentEditId = ref<number | null>(null)

// 表单引用
const formRef = ref<FormInstance>()
const editFormRef = ref<FormInstance>()

// 表单数据
const projectForm = reactive<ProjectCreate>({
  name: '',
  description: ''
})

const editForm = reactive<ProjectUpdate>({
  name: '',
  description: ''
})

// 表单验证规则
const formRules = {
  name: [
    { required: true, message: '请输入项目名称', trigger: 'blur' },
    { min: 1, max: 100, message: '项目名称长度在 1 到 100 个字符', trigger: 'blur' }
  ]
}

// 统计数据
const totalProjects = computed(() => projects.value?.length || 0)
const totalModules = computed(() => projects.value?.reduce((sum, p) => sum + p.module_count, 0) || 0)
const totalAPIs = computed(() => projects.value?.reduce((sum, p) => sum + p.api_count, 0) || 0)

// 获取项目列表
const fetchProjects = async () => {
  try {
    loading.value = true
    const response = await projectApi.getProjects()
    projects.value = response.data || response || []
    console.log('获取项目列表:', projects.value) // 调试日志
  } catch (error) {
    console.error('获取项目列表失败:', error)
    ElMessage.error('获取项目列表失败')
    projects.value = [] // 确保在错误时也有一个空数组
  } finally {
    loading.value = false
  }
}

// 创建项目
const createProject = async () => {
  if (!formRef.value) return
  
  const valid = await formRef.value.validate()
  if (!valid) return

  try {
    creating.value = true
    await projectApi.createProject(projectForm)
    ElMessage.success('项目创建成功')
    showCreateDialog.value = false
    
    // 重置表单
    Object.assign(projectForm, { name: '', description: '' })
    formRef.value?.resetFields()
    
    // 刷新列表
    await fetchProjects()
  } catch (error: any) {
    console.error('创建项目失败:', error)
    ElMessage.error(error.response?.data?.detail || '创建项目失败')
  } finally {
    creating.value = false
  }
}

// 更新项目
const updateProject = async () => {
  if (!editFormRef.value || !currentEditId.value) return
  
  const valid = await editFormRef.value.validate()
  if (!valid) return

  try {
    updating.value = true
    await projectApi.updateProject(currentEditId.value, editForm)
    ElMessage.success('项目更新成功')
    showEditDialog.value = false
    
    // 刷新列表
    await fetchProjects()
  } catch (error: any) {
    console.error('更新项目失败:', error)
    ElMessage.error(error.response?.data?.detail || '更新项目失败')
  } finally {
    updating.value = false
  }
}

// 删除项目
const deleteProject = async (projectId: number, projectName: string) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除项目"${projectName}"吗？删除后将无法恢复，包括其下的所有模块、分类和接口！`,
      '⚠️ 删除确认',
      {
        confirmButtonText: '确定删除',
        cancelButtonText: '取消',
        type: 'warning',
        confirmButtonClass: 'danger-confirm'
      }
    )
    
    await projectApi.deleteProject(projectId)
    ElMessage.success('项目删除成功')
    
    // 刷新列表
    await fetchProjects()
  } catch (error: any) {
    if (error !== 'cancel') {
      console.error('删除项目失败:', error)
      ElMessage.error(error.response?.data?.detail || '删除项目失败')
    }
  }
}

// 跳转到项目详情
const goToProject = (projectId: number) => {
  router.push(`/projects/${projectId}`)
}

// 处理下拉菜单命令
const handleCommand = (command: string) => {
  const [action, id] = command.split('-')
  const projectId = parseInt(id)
  const project = projects.value.find(p => p.id === projectId)
  
  if (!project) return
  
  if (action === 'edit') {
    currentEditId.value = projectId
    editForm.name = project.name
    editForm.description = project.description || ''
    showEditDialog.value = true
  } else if (action === 'delete') {
    deleteProject(projectId, project.name)
  }
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
onMounted(() => {
  fetchProjects()
})
</script>

<style scoped lang="scss">
.project-page {
  padding: 24px;
  min-height: calc(100vh - 60px);
  background: var(--cyber-bg-primary);
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  
  .page-title {
    display: flex;
    align-items: center;
    gap: 12px;
    font-size: 28px;
    font-weight: 600;
    color: var(--cyber-text-primary);
    margin: 0;
    
    .icon {
      font-size: 32px;
    }
    
    .subtitle {
      font-size: 14px;
      color: var(--cyber-text-secondary);
      font-weight: 400;
      margin-left: 8px;
    }
  }
  
  .create-btn {
    background: var(--cyber-gradient-primary);
    border: none;
    color: white;
    font-weight: 500;
    padding: 12px 24px;
    border-radius: 8px;
    transition: all 0.3s ease;
    
    &:hover {
      transform: translateY(-2px);
      box-shadow: 0 8px 20px rgba(0, 212, 255, 0.3);
    }
  }
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 32px;
  
  .stat-card {
    background: var(--cyber-bg-secondary);
    border: 1px solid var(--cyber-border-color);
    border-radius: 12px;
    padding: 20px;
    display: flex;
    align-items: center;
    gap: 16px;
    transition: all 0.3s ease;
    
    &:hover {
      transform: translateY(-3px);
      box-shadow: 0 8px 25px rgba(0, 212, 255, 0.1);
      border-color: var(--cyber-primary);
    }
    
    .stat-icon {
      font-size: 24px;
      padding: 12px;
      background: var(--cyber-gradient-primary);
      border-radius: 8px;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    
    .stat-content {
      .stat-value {
        font-size: 24px;
        font-weight: 600;
        color: var(--cyber-text-primary);
        line-height: 1;
      }
      
      .stat-label {
        font-size: 12px;
        color: var(--cyber-text-secondary);
        margin-top: 4px;
      }
    }
  }
}

.projects-container {
  .section-title {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 18px;
    font-weight: 600;
    color: var(--cyber-text-primary);
    margin-bottom: 20px;
    
    .icon {
      font-size: 20px;
    }
    
    .count {
      font-size: 14px;
      color: var(--cyber-text-secondary);
      font-weight: 400;
    }
  }
}

.project-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 24px;
  
  .project-card {
    background: var(--cyber-bg-secondary);
    border: 1px solid var(--cyber-border-color);
    border-radius: 16px;
    padding: 24px;
    cursor: pointer;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
    
    &::before {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 4px;
      background: var(--cyber-gradient-primary);
      transform: scaleX(0);
      transition: transform 0.3s ease;
    }
    
    &:hover {
      transform: translateY(-5px);
      box-shadow: 0 12px 30px rgba(0, 212, 255, 0.15);
      border-color: var(--cyber-primary);
      
      &::before {
        transform: scaleX(1);
      }
    }
    
    .project-header {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 16px;
      
      .project-info {
        flex: 1;
        min-width: 0;
        
        .project-name {
          font-size: 18px;
          font-weight: 600;
          color: var(--cyber-text-primary);
          margin: 0 0 8px 0;
          line-height: 1.3;
        }
        
        .project-desc {
          font-size: 14px;
          color: var(--cyber-text-secondary);
          margin: 0;
          line-height: 1.4;
          display: -webkit-box;
          -webkit-line-clamp: 2;
          -webkit-box-orient: vertical;
          overflow: hidden;
        }
      }
      
      .more-icon {
        color: var(--cyber-text-secondary);
        cursor: pointer;
        padding: 4px;
        border-radius: 4px;
        transition: all 0.2s ease;
        
        &:hover {
          background: var(--cyber-hover-bg);
          color: var(--cyber-primary);
        }
      }
    }
    
    .project-stats {
      display: flex;
      flex-direction: column;
      gap: 8px;
      margin-bottom: 16px;
      
      .stat-item {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 13px;
        color: var(--cyber-text-secondary);
        
        .stat-icon {
          font-size: 14px;
        }
      }
    }
    
    .project-footer {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-top: 16px;
      border-top: 1px solid var(--cyber-border-color);
      
      .create-time {
        font-size: 12px;
        color: var(--cyber-text-secondary);
      }
      
      .project-status {
        display: flex;
        align-items: center;
        gap: 6px;
        font-size: 12px;
        color: var(--cyber-success);
        
        .status-dot {
          width: 6px;
          height: 6px;
          border-radius: 50%;
          background: var(--cyber-success);
          animation: pulse 2s infinite;
        }
      }
    }
  }
}

.empty-state {
  grid-column: 1 / -1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  text-align: center;
  
  .empty-icon {
    font-size: 64px;
    margin-bottom: 16px;
    opacity: 0.5;
  }
  
  .empty-title {
    font-size: 20px;
    font-weight: 600;
    color: var(--cyber-text-primary);
    margin-bottom: 8px;
  }
  
  .empty-desc {
    font-size: 14px;
    color: var(--cyber-text-secondary);
    margin-bottom: 24px;
  }
}

// 对话框样式
:deep(.cyber-dialog) {
  .el-dialog {
    background: var(--cyber-bg-secondary);
    border: 1px solid var(--cyber-border-color);
    border-radius: 16px;
    
    .el-dialog__header {
      background: var(--cyber-gradient-primary);
      color: white;
      padding: 20px 24px;
      border-radius: 16px 16px 0 0;
      margin: 0;
    }
    
    .el-dialog__title {
      color: white;
      font-weight: 600;
    }
    
    .el-dialog__body {
      padding: 24px;
    }
    
    .el-dialog__footer {
      padding: 0 24px 24px;
    }
  }
}

// 表单样式
.cyber-form {
  :deep(.el-form-item__label) {
    color: var(--cyber-text-primary);
    font-weight: 500;
  }
  
  :deep(.el-input__inner) {
    background: var(--cyber-bg-primary);
    border-color: var(--cyber-border-color);
    color: var(--cyber-text-primary);
    
    &:focus {
      border-color: var(--cyber-primary);
      box-shadow: 0 0 0 2px rgba(0, 212, 255, 0.1);
    }
  }
  
  :deep(.el-textarea__inner) {
    background: var(--cyber-bg-primary);
    border-color: var(--cyber-border-color);
    color: var(--cyber-text-primary);
    
    &:focus {
      border-color: var(--cyber-primary);
      box-shadow: 0 0 0 2px rgba(0, 212, 255, 0.1);
    }
  }
}

// 下拉菜单样式
:deep(.el-dropdown-menu) {
  background: var(--cyber-bg-secondary);
  border: 1px solid var(--cyber-border-color);
  border-radius: 8px;
  padding: 8px;
  
  .el-dropdown-menu__item {
    color: var(--cyber-text-primary);
    border-radius: 6px;
    margin: 2px 0;
    
    &:hover {
      background: var(--cyber-hover-bg);
      color: var(--cyber-primary);
    }
    
    &.danger-item:hover {
      background: rgba(245, 108, 108, 0.1);
      color: var(--cyber-danger);
    }
  }
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

// 响应式设计
@media (max-width: 768px) {
  .project-page {
    padding: 16px;
  }
  
  .page-header {
    flex-direction: column;
    gap: 16px;
    align-items: stretch;
    
    .page-title {
      justify-content: center;
      text-align: center;
    }
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .project-grid {
    grid-template-columns: 1fr;
  }
}
</style> 