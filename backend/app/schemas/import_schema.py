from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from enum import Enum


class LLMProviderInfo(BaseModel):
    """大模型提供商信息"""
    id: str = Field(..., description="提供商ID")
    name: str = Field(..., description="提供商名称")
    description: str = Field(..., description="提供商描述")
    models: List[str] = Field(..., description="支持的模型列表")
    default_model: str = Field(..., description="默认模型")
    api_key_placeholder: str = Field(..., description="API Key占位符")
    base_url: str = Field(..., description="API基础地址")


class LLMConfigRequest(BaseModel):
    """大模型配置请求"""
    provider: str = Field(..., description="大模型提供商")
    api_key: str = Field(..., description="API密钥")
    model: Optional[str] = Field(None, description="模型名称")
    base_url: Optional[str] = Field(None, description="API基础地址")


class ImportRequest(BaseModel):
    """导入请求"""
    config_id: str = Field(..., description="大模型配置ID")
    file_id: str = Field(..., description="文件ID")
    file_type: str = Field(..., description="文件类型")


class ImportResponse(BaseModel):
    """导入响应"""
    message: str = Field(..., description="响应消息")
    status: str = Field(..., description="状态")
    data: Optional[Dict[str, Any]] = Field(None, description="响应数据")


class APIInfo(BaseModel):
    """API信息"""
    name: str = Field(..., description="接口名称")
    description: str = Field("", description="接口描述")
    method: str = Field(..., description="HTTP方法")
    path: str = Field(..., description="接口路径")
    tags: List[str] = Field(default_factory=list, description="标签")
    parameters: List[Dict[str, Any]] = Field(default_factory=list, description="参数")
    responses: List[Dict[str, Any]] = Field(default_factory=list, description="响应")
    security: List[str] = Field(default_factory=list, description="安全认证")
    notes: str = Field("", description="备注")


class SaveAPIsRequest(BaseModel):
    """保存API请求"""
    project_id: int = Field(..., description="项目ID")
    apis: List[APIInfo] = Field(..., description="API列表")


class FileUploadResponse(BaseModel):
    """文件上传响应"""
    file_id: str = Field(..., description="文件ID")
    filename: str = Field(..., description="原始文件名")
    file_type: str = Field(..., description="文件类型")
    file_size: int = Field(..., description="文件大小")
    parsed_info: Dict[str, Any] = Field(..., description="解析信息")
    message: str = Field(..., description="响应消息")
    status: str = Field(..., description="状态")


class AnalysisResult(BaseModel):
    """分析结果"""
    type: str = Field(..., description="结果类型")
    message: Optional[str] = Field(None, description="消息")
    data: Optional[Dict[str, Any]] = Field(None, description="数据")
    status: str = Field(..., description="状态") 