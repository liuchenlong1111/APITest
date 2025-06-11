import request from '@/utils/request'

export interface LLMProvider {
  id: string
  name: string
  description: string
  models: string[]
  default_model: string
  api_key_placeholder: string
  base_url: string
}

export interface LLMConfig {
  provider: string
  api_key: string
  model?: string
  base_url?: string
}

export interface FileUploadResponse {
  file_id: string
  filename: string
  file_type: string
  file_size: number
  parsed_info: {
    type: string
    metadata: Record<string, any>
    error?: string
  }
  message: string
  status: string
}

export interface APIInfo {
  name: string
  description: string
  method: string
  path: string
  tags: string[]
  parameters: Record<string, any>[]
  responses: Record<string, any>[]
  security: string[]
  notes: string
}

export interface AnalysisResult {
  type: string
  message?: string
  data?: APIInfo
  status: string
}

/**
 * 获取支持的大模型提供商列表
 */
export const getLLMProviders = (): Promise<LLMProvider[]> => {
  return request.get('/api/v1/import/providers')
}

/**
 * 配置大模型
 */
export const configureLLM = (config: LLMConfig): Promise<{ config_id: string; message: string; status: string }> => {
  return request.post('/api/v1/import/configure-llm', config)
}

/**
 * 上传文档文件
 */
export const uploadDocument = (file: File): Promise<FileUploadResponse> => {
  const formData = new FormData()
  formData.append('file', file)
  
  return request.post('/api/v1/import/upload-document', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

/**
 * 分析文档 - 流式接口
 */
export const analyzeDocument = (
  configId: string,
  fileId: string,
  fileType: string,
  onMessage: (result: AnalysisResult) => void,
  onError?: (error: string) => void,
  onComplete?: () => void
): EventSource => {
  const eventSource = new EventSource(
    `/api/v1/import/analyze-document?config_id=${configId}&file_id=${fileId}&file_type=${fileType}`,
    { withCredentials: true }
  )

  eventSource.onmessage = (event) => {
    try {
      const result: AnalysisResult = JSON.parse(event.data)
      onMessage(result)
      
      if (result.type === 'complete') {
        onComplete?.()
        eventSource.close()
      }
    } catch (error) {
      console.error('解析SSE消息失败:', error)
      onError?.('解析服务器消息失败')
    }
  }

  eventSource.onerror = (error) => {
    console.error('SSE连接出错:', error)
    onError?.('连接服务器失败')
    eventSource.close()
  }

  return eventSource
}

/**
 * 保存API接口到数据库
 */
export const saveAPIs = (projectId: number, apis: APIInfo[]): Promise<{ message: string; count: number; status: string }> => {
  const formData = new FormData()
  formData.append('project_id', projectId.toString())
  formData.append('apis_data', JSON.stringify(apis))
  
  return request.post('/api/v1/import/save-apis', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

/**
 * 清理上传的文件
 */
export const cleanupFile = (fileId: string): Promise<{ message: string; status: string }> => {
  return request.delete(`/api/v1/import/cleanup-file/${fileId}`)
} 