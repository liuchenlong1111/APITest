<template>
  <div class="import-api-container">
    <el-card class="page-card">
      <template #header>
        <div class="card-header">
          <span class="title">接口文档导入</span>
          <span class="subtitle">通过大模型分析整理接口文档，自动录入API接口</span>
        </div>
      </template>

      <!-- 步骤条 -->
      <el-steps :active="currentStep" align-center class="steps">
        <el-step title="配置大模型" description="选择并配置大模型"></el-step>
        <el-step title="上传文档" description="上传接口文档文件"></el-step>
        <el-step title="智能分析" description="大模型分析整理接口"></el-step>
        <el-step title="确认保存" description="确认并保存到项目"></el-step>
      </el-steps>

      <!-- 步骤1: 配置大模型 -->
      <div v-if="currentStep === 0" class="step-content">
        <el-form :model="llmForm" :rules="llmRules" ref="llmFormRef" label-width="120px">
          <el-form-item label="大模型提供商" prop="provider">
            <el-select v-model="llmForm.provider" placeholder="请选择大模型提供商" style="width: 100%" @change="onProviderChange">
              <el-option
                v-for="provider in providers"
                :key="provider.id"
                :label="provider.name"
                :value="provider.id"
              >
                <div class="provider-option">
                  <span>{{ provider.name }}</span>
                  <span class="provider-desc">{{ provider.description }}</span>
                </div>
              </el-option>
            </el-select>
          </el-form-item>

          <el-form-item label="模型" prop="model">
            <el-select v-model="llmForm.model" placeholder="请选择模型" style="width: 100%">
              <el-option
                v-for="model in currentProviderModels"
                :key="model"
                :label="model"
                :value="model"
              >
              </el-option>
            </el-select>
          </el-form-item>

          <el-form-item label="API Key" prop="api_key">
            <el-input
              v-model="llmForm.api_key"
              type="password"
              :placeholder="currentProvider?.api_key_placeholder || 'sk-xxx'"
              show-password
              style="width: 100%"
            />
          </el-form-item>

          <el-form-item label="API地址" prop="base_url">
            <el-input
              v-model="llmForm.base_url"
              placeholder="API基础地址"
              style="width: 100%"
            />
            <div class="form-tip">如使用默认地址可不填</div>
          </el-form-item>

          <el-form-item>
            <el-button type="primary" @click="configureLLMHandler" :loading="configuring">
              配置并测试连接
            </el-button>
          </el-form-item>

          <div v-if="configResult.message" class="config-result" :class="configResult.status">
            <el-icon><SuccessFilled v-if="configResult.status === 'success'" /><CircleCloseFilled v-else /></el-icon>
            {{ configResult.message }}
          </div>
        </el-form>
      </div>

      <!-- 步骤2: 上传文档 -->
      <div v-if="currentStep === 1" class="step-content">
        <el-upload
          ref="uploadRef"
          class="upload-demo"
          drag
          :auto-upload="false"
          :on-change="handleFileChange"
          :before-upload="beforeUpload"
          accept=".txt,.md,.docx,.xlsx,.html,.json"
          :limit="1"
        >
          <el-icon class="el-icon--upload"><upload-filled /></el-icon>
          <div class="el-upload__text">
            将文件拖拽到此处，或<em>点击上传</em>
          </div>
          <template #tip>
            <div class="el-upload__tip">
              支持的文件格式：.txt, .md, .docx, .xlsx, .html, .json (OpenAPI/Swagger, Postman集合)
              <br>
              文件大小不超过10MB
            </div>
          </template>
        </el-upload>

        <div v-if="uploadedFile" class="file-info">
          <h4>已上传文件信息</h4>
          <el-descriptions :column="2" border>
            <el-descriptions-item label="文件名">{{ uploadedFile.filename }}</el-descriptions-item>
            <el-descriptions-item label="文件类型">{{ uploadedFile.file_type }}</el-descriptions-item>
            <el-descriptions-item label="文件大小">{{ formatFileSize(uploadedFile.file_size) }}</el-descriptions-item>
            <el-descriptions-item label="解析状态">
              <el-tag :type="uploadedFile.parsed_info.error ? 'danger' : 'success'">
                {{ uploadedFile.parsed_info.error ? '解析失败' : '解析成功' }}
              </el-tag>
            </el-descriptions-item>
          </el-descriptions>
          
          <div class="file-actions">
            <el-button type="primary" @click="startAnalysis" :disabled="!!uploadedFile.parsed_info.error">
              开始分析
            </el-button>
            <el-button @click="clearFile">重新上传</el-button>
          </div>
        </div>
      </div>

      <!-- 步骤3: 智能分析 -->
      <div v-if="currentStep === 2" class="step-content">
        <div class="analysis-section">
          <div class="analysis-header">
            <h4>正在使用 {{ currentProvider?.name }} 分析文档...</h4>
            <el-progress :percentage="analysisProgress" :status="analysisStatus"></el-progress>
          </div>

          <div class="analysis-log">
            <div v-for="(log, index) in analysisLogs" :key="index" class="log-item" :class="log.type">
              <el-icon>
                <Loading v-if="log.type === 'processing'" />
                <SuccessFilled v-else-if="log.type === 'success'" />
                <WarningFilled v-else-if="log.type === 'warning'" />
                <CircleCloseFilled v-else-if="log.type === 'error'" />
                <InfoFilled v-else />
              </el-icon>
              <span>{{ log.message }}</span>
              <span class="timestamp">{{ log.timestamp }}</span>
            </div>
          </div>

          <div v-if="analyzedAPIs.length > 0" class="api-preview">
            <h4>分析到的API接口 ({{ analyzedAPIs.length }}个)</h4>
            <div class="api-list">
              <div v-for="(api, index) in analyzedAPIs" :key="index" class="api-item">
                <div class="api-header">
                  <el-tag :type="getMethodType(api.method) as any" size="small">{{ api.method }}</el-tag>
                  <span class="api-path">{{ api.path }}</span>
                  <span class="api-name">{{ api.name }}</span>
                </div>
                <div class="api-description">{{ api.description }}</div>
                <div class="api-meta">
                  <el-tag v-for="tag in api.tags" :key="tag" size="small" effect="plain">{{ tag }}</el-tag>
                  <span class="param-count">参数: {{ api.parameters.length }}个</span>
                </div>
              </div>
            </div>
          </div>

          <div v-if="analysisComplete" class="analysis-actions">
            <el-button type="primary" @click="currentStep = 3" :disabled="analyzedAPIs.length === 0">
              确认接口信息
            </el-button>
            <el-button @click="retryAnalysis">重新分析</el-button>
          </div>
        </div>
      </div>

      <!-- 步骤4: 确认保存 -->
      <div v-if="currentStep === 3" class="step-content">
        <el-form :model="saveForm" :rules="saveRules" ref="saveFormRef" label-width="120px">
          <el-form-item label="目标项目" prop="project_id">
            <el-select v-model="saveForm.project_id" placeholder="请选择项目" style="width: 100%" clearable>
              <el-option
                v-for="project in projects"
                :key="project.id"
                :label="project.name"
                :value="project.id"
              >
              </el-option>
            </el-select>
          </el-form-item>
        </el-form>

        <div class="api-confirm">
          <h4>确认要导入的API接口 ({{ selectedAPIs.length }}/{{ analyzedAPIs.length }}个)</h4>
          
          <div class="api-table">
            <el-table :data="analyzedAPIs" @selection-change="handleSelectionChange" max-height="400">
              <el-table-column type="selection" width="55"></el-table-column>
              <el-table-column label="方法" width="100">
                <template #default="scope">
                  <el-tag :type="getMethodType(scope.row.method) as any" size="small">
                    {{ scope.row.method }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="path" label="路径" min-width="200"></el-table-column>
              <el-table-column prop="name" label="名称" min-width="150"></el-table-column>
              <el-table-column prop="description" label="描述" min-width="200" show-overflow-tooltip></el-table-column>
              <el-table-column label="参数" width="80">
                <template #default="scope">
                  {{ scope.row.parameters.length }}
                </template>
              </el-table-column>
            </el-table>
          </div>

          <div class="save-actions">
            <el-button type="primary" @click="saveAPIsHandler" :loading="saving" :disabled="selectedAPIs.length === 0 || !saveForm.project_id">
              导入选中的API ({{ selectedAPIs.length }}个)
            </el-button>
            <el-button @click="currentStep = 2">返回上一步</el-button>
          </div>
        </div>
      </div>

      <!-- 底部导航 -->
      <div class="step-navigation">
        <el-button v-if="currentStep > 0" @click="prevStep">上一步</el-button>
        <el-button v-if="currentStep < 3 && currentStep !== 2" type="primary" @click="nextStep" :disabled="!canProceed">
          下一步
        </el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import {
  SuccessFilled,
  CircleCloseFilled,
  UploadFilled,
  Loading,
  WarningFilled,
  InfoFilled
} from '@element-plus/icons-vue'
import {
  getLLMProviders,
  configureLLM,
  uploadDocument,
  analyzeDocument,
  saveAPIs as saveAPIsAPI,
  cleanupFile,
  type LLMProvider,
  type LLMConfig,
  type FileUploadResponse,
  type APIInfo,
  type AnalysisResult
} from '@/api/import'
import { projectApi } from '@/api/api'

// 响应式数据
const currentStep = ref(0)
const providers = ref<LLMProvider[]>([])
const projects = ref<any[]>([])
const configuring = ref(false)
const uploadedFile = ref<FileUploadResponse | null>(null)
const analyzedAPIs = ref<APIInfo[]>([])
const selectedAPIs = ref<APIInfo[]>([])
const analysisProgress = ref(0)
const analysisStatus = ref<'' | 'success' | 'exception' | 'warning'>('')
const analysisComplete = ref(false)
const analysisLogs = ref<Array<{
  type: 'info' | 'success' | 'warning' | 'error' | 'processing'
  message: string
  timestamp: string
}>>([])
const saving = ref(false)
const configId = ref('')

// 表单数据
const llmForm = reactive<LLMConfig>({
  provider: '',
  api_key: '',
  model: '',
  base_url: ''
})

const saveForm = reactive({
  project_id: undefined as number | undefined
})

const configResult = reactive({
  message: '',
  status: '' as 'success' | 'error' | ''
})

// 表单验证规则
const llmRules = {
  provider: [{ required: true, message: '请选择大模型提供商', trigger: 'change' }],
  api_key: [{ required: true, message: '请输入API Key', trigger: 'blur' }],
  model: [{ required: true, message: '请选择模型', trigger: 'change' }]
}

const saveRules = {
  project_id: [{ required: true, message: '请选择目标项目', trigger: 'change' }]
}

// refs
const llmFormRef = ref()
const saveFormRef = ref()
const uploadRef = ref()

// 计算属性
const currentProvider = computed(() => {
  return providers.value.find(p => p.id === llmForm.provider)
})

const currentProviderModels = computed(() => {
  return currentProvider.value?.models || []
})

const canProceed = computed(() => {
  switch (currentStep.value) {
    case 0:
      return configResult.status === 'success'
    case 1:
      return uploadedFile.value && !uploadedFile.value.parsed_info.error
    case 2:
      return analysisComplete.value && analyzedAPIs.value.length > 0
    case 3:
      return selectedAPIs.value.length > 0 && saveForm.project_id
    default:
      return false
  }
})

// 生命周期
onMounted(async () => {
  await loadProviders()
  await loadProjects()
})

// 方法
const loadProviders = async () => {
  try {
    providers.value = await getLLMProviders()
  } catch (error) {
    ElMessage.error('加载大模型提供商失败')
  }
}

const loadProjects = async () => {
  try {
    const response = await projectApi.getProjects()
    projects.value = response.data || response
  } catch (error) {
    ElMessage.error('加载项目列表失败')
  }
}

const onProviderChange = () => {
  const provider = currentProvider.value
  if (provider) {
    llmForm.model = provider.default_model
    llmForm.base_url = provider.base_url
  }
  configResult.message = ''
  configResult.status = ''
}

const configureLLMHandler = async () => {
  if (!llmFormRef.value) return
  
  try {
    await llmFormRef.value.validate()
    configuring.value = true
    
    const response = await configureLLM(llmForm)
    configId.value = response.config_id
    configResult.message = response.message
    configResult.status = 'success'
    
    ElMessage.success('大模型配置成功')
  } catch (error: any) {
    configResult.message = error.response?.data?.detail || '配置失败'
    configResult.status = 'error'
    ElMessage.error(configResult.message)
  } finally {
    configuring.value = false
  }
}

const handleFileChange = (file: any) => {
  uploadFile(file.raw)
}

const beforeUpload = (file: File) => {
  const isValidSize = file.size / 1024 / 1024 < 10
  if (!isValidSize) {
    ElMessage.error('文件大小不能超过10MB')
    return false
  }
  return true
}

const uploadFile = async (file: File) => {
  try {
    const response = await uploadDocument(file)
    uploadedFile.value = response
    ElMessage.success('文件上传成功')
  } catch (error: any) {
    ElMessage.error(error.response?.data?.detail || '文件上传失败')
  }
}

const clearFile = () => {
  if (uploadedFile.value) {
    cleanupFile(uploadedFile.value.file_id)
  }
  uploadedFile.value = null
  uploadRef.value?.clearFiles()
}

const startAnalysis = () => {
  if (!uploadedFile.value || !configId.value) return
  
  currentStep.value = 2
  analyzedAPIs.value = []
  analysisLogs.value = []
  analysisProgress.value = 0
  analysisStatus.value = ''
  analysisComplete.value = false
  
  addLog('info', '开始分析文档...')
  
  analyzeDocument(
    configId.value,
    uploadedFile.value.file_id,
    uploadedFile.value.file_type,
    (result: AnalysisResult) => {
      handleAnalysisResult(result)
    },
    (error: string) => {
      addLog('error', `分析出错: ${error}`)
      analysisStatus.value = 'exception'
      analysisComplete.value = true
    },
    () => {
      addLog('success', '文档分析完成')
      analysisProgress.value = 100
      analysisStatus.value = 'success'
      analysisComplete.value = true
    }
  )
}

const handleAnalysisResult = (result: AnalysisResult) => {
  switch (result.type) {
    case 'start':
      addLog('processing', result.message || '开始分析...')
      analysisProgress.value = 10
      break
    
    case 'api':
      if (result.data) {
        analyzedAPIs.value.push(result.data)
        addLog('success', `发现API: ${result.data.method} ${result.data.path}`)
        analysisProgress.value = Math.min(90, 10 + analyzedAPIs.value.length * 5)
      }
      break
    
    case 'error':
      addLog('error', result.message || '分析出错')
      analysisStatus.value = 'exception'
      break
    
    case 'complete':
      addLog('success', `分析完成，共发现 ${analyzedAPIs.value.length} 个API接口`)
      analysisProgress.value = 100
      analysisStatus.value = 'success'
      analysisComplete.value = true
      break
  }
}

const addLog = (type: 'info' | 'success' | 'warning' | 'error' | 'processing', message: string) => {
  analysisLogs.value.push({
    type,
    message,
    timestamp: new Date().toLocaleTimeString()
  })
}

const retryAnalysis = () => {
  startAnalysis()
}

const handleSelectionChange = (selection: APIInfo[]) => {
  selectedAPIs.value = selection
}

const saveAPIsHandler = async () => {
  if (!saveFormRef.value || !saveForm.project_id) return
  
  try {
    await saveFormRef.value.validate()
    saving.value = true
    
    const response = await saveAPIsAPI(saveForm.project_id, selectedAPIs.value)
    
    ElMessage.success(response.message)
    
    if (uploadedFile.value) {
      await cleanupFile(uploadedFile.value.file_id)
    }
    
    resetForm()
    
  } catch (error: any) {
    ElMessage.error(error.response?.data?.detail || '保存API失败')
  } finally {
    saving.value = false
  }
}

const resetForm = () => {
  currentStep.value = 0
  uploadedFile.value = null
  analyzedAPIs.value = []
  selectedAPIs.value = []
  analysisLogs.value = []
  configResult.message = ''
  configResult.status = ''
  configId.value = ''
  Object.assign(llmForm, { provider: '', api_key: '', model: '', base_url: '' })
  Object.assign(saveForm, { project_id: null })
}

const nextStep = () => {
  if (canProceed.value && currentStep.value < 3) {
    currentStep.value++
  }
}

const prevStep = () => {
  if (currentStep.value > 0) {
    currentStep.value--
  }
}

const getMethodType = (method: string) => {
  const types: Record<string, string> = {
    'GET': 'success',
    'POST': 'primary',
    'PUT': 'warning',
    'DELETE': 'danger',
    'PATCH': 'info'
  }
  return types[method.toUpperCase()] || 'info'
}

const formatFileSize = (size: number) => {
  if (size < 1024) return `${size} B`
  if (size < 1024 * 1024) return `${(size / 1024).toFixed(1)} KB`
  return `${(size / 1024 / 1024).toFixed(1)} MB`
}
</script>

<style scoped lang="scss">
.import-api-container {
  padding: 20px;
  min-height: calc(100vh - 120px);
}

.page-card {
  max-width: 1200px;
  margin: 0 auto;
}

.card-header {
  .title {
    font-size: 20px;
    font-weight: 600;
    color: #303133;
  }
  
  .subtitle {
    display: block;
    font-size: 14px;
    color: #909399;
    margin-top: 8px;
  }
}

.steps {
  margin: 30px 0;
}

.step-content {
  margin: 40px 0;
  min-height: 400px;
}

.provider-option {
  display: flex;
  flex-direction: column;
  
  .provider-desc {
    font-size: 12px;
    color: #909399;
  }
}

.form-tip {
  font-size: 12px;
  color: #909399;
  margin-top: 5px;
}

.config-result {
  display: flex;
  align-items: center;
  padding: 12px;
  border-radius: 4px;
  margin-top: 16px;
  
  .el-icon {
    margin-right: 8px;
  }
  
  &.success {
    background-color: #f0f9ff;
    color: #67c23a;
    border: 1px solid #e1f3d8;
  }
  
  &.error {
    background-color: #fef0f0;
    color: #f56c6c;
    border: 1px solid #fbc4c4;
  }
}

.upload-demo {
  margin: 20px 0;
}

.file-info {
  margin-top: 20px;
  padding: 20px;
  background-color: #f8f9fa;
  border-radius: 8px;
  
  h4 {
    margin-bottom: 16px;
    color: #303133;
  }
}

.file-actions {
  margin-top: 20px;
  display: flex;
  gap: 12px;
}

.analysis-section {
  .analysis-header {
    margin-bottom: 20px;
    
    h4 {
      margin-bottom: 16px;
      color: #303133;
    }
  }
}

.analysis-log {
  max-height: 300px;
  overflow-y: auto;
  border: 1px solid #e4e7ed;
  border-radius: 4px;
  padding: 16px;
  background-color: #fafafa;
  
  .log-item {
    display: flex;
    align-items: center;
    margin-bottom: 8px;
    font-size: 14px;
    
    .el-icon {
      margin-right: 8px;
      flex-shrink: 0;
    }
    
    .timestamp {
      margin-left: auto;
      font-size: 12px;
      color: #909399;
    }
    
    &.success {
      color: #67c23a;
    }
    
    &.error {
      color: #f56c6c;
    }
    
    &.warning {
      color: #e6a23c;
    }
    
    &.processing {
      color: #409eff;
    }
  }
}

.api-preview {
  margin-top: 20px;
  
  h4 {
    margin-bottom: 16px;
    color: #303133;
  }
}

.api-list {
  max-height: 400px;
  overflow-y: auto;
  border: 1px solid #e4e7ed;
  border-radius: 4px;
}

.api-item {
  padding: 16px;
  border-bottom: 1px solid #f5f7fa;
  
  &:last-child {
    border-bottom: none;
  }
  
  .api-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 8px;
    
    .api-path {
      font-family: monospace;
      color: #606266;
    }
    
    .api-name {
      font-weight: 500;
      color: #303133;
    }
  }
  
  .api-description {
    color: #606266;
    margin-bottom: 8px;
    font-size: 14px;
  }
  
  .api-meta {
    display: flex;
    align-items: center;
    gap: 8px;
    
    .param-count {
      font-size: 12px;
      color: #909399;
    }
  }
}

.analysis-actions {
  margin-top: 20px;
  display: flex;
  gap: 12px;
}

.api-confirm {
  h4 {
    margin-bottom: 16px;
    color: #303133;
  }
}

.api-table {
  margin: 20px 0;
}

.save-actions {
  margin-top: 20px;
  display: flex;
  gap: 12px;
}

.step-navigation {
  margin-top: 40px;
  padding-top: 20px;
  border-top: 1px solid #e4e7ed;
  display: flex;
  justify-content: space-between;
}
</style> 