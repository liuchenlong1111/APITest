from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime

# Category schemas
class CategoryBase(BaseModel):
    name: str = Field(..., description="分类名称")
    description: Optional[str] = Field(None, description="分类描述")
    color: str = Field("#00d4ff", description="分类颜色")

class CategoryCreate(CategoryBase):
    module_id: int = Field(..., description="模块ID")

class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, description="分类名称")
    description: Optional[str] = Field(None, description="分类描述")
    color: Optional[str] = Field(None, description="分类颜色")

class CategoryInDBBase(CategoryBase):
    id: int
    module_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class Category(CategoryInDBBase):
    pass

class CategoryWithAPIs(CategoryInDBBase):
    apis: List["API"] = []

# API schemas
class APIBase(BaseModel):
    name: str = Field(..., description="接口名称")
    method: str = Field(..., description="请求方法")
    url: str = Field(..., description="接口URL")
    description: Optional[str] = Field(None, description="接口描述")
    headers: Optional[Dict[str, Any]] = Field(None, description="请求头")
    params: Optional[Dict[str, Any]] = Field(None, description="请求参数")
    body: Optional[Dict[str, Any]] = Field(None, description="请求体")

class APICreate(APIBase):
    category_id: Optional[int] = Field(None, description="分类ID")

class APIUpdate(BaseModel):
    name: Optional[str] = Field(None, description="接口名称")
    method: Optional[str] = Field(None, description="请求方法")
    url: Optional[str] = Field(None, description="接口URL")
    description: Optional[str] = Field(None, description="接口描述")
    headers: Optional[Dict[str, Any]] = Field(None, description="请求头")
    params: Optional[Dict[str, Any]] = Field(None, description="请求参数")
    body: Optional[Dict[str, Any]] = Field(None, description="请求体")
    category_id: Optional[int] = Field(None, description="分类ID")

class APIInDBBase(APIBase):
    id: int
    category_id: Optional[int]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class API(APIInDBBase):
    pass

class APIWithCategory(APIInDBBase):
    category: Optional[Category] = None

# 测试结果相关schemas
class TestResultBase(BaseModel):
    test_type: str = Field(..., description="测试类型")
    status: str = Field("pending", description="测试状态")
    status_code: Optional[int] = Field(None, description="HTTP状态码")
    response_time: Optional[int] = Field(None, description="响应时间(ms)")
    response_data: Optional[Dict[str, Any]] = Field(None, description="响应数据")
    error_message: Optional[str] = Field(None, description="错误信息")

class TestResultCreate(TestResultBase):
    api_id: int = Field(..., description="接口ID")

class TestResult(TestResultBase):
    id: int
    api_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# 场景相关schemas
class ScenarioBase(BaseModel):
    name: str = Field(..., description="场景名称")
    description: Optional[str] = Field(None, description="场景描述")
    steps: List[Dict[str, Any]] = Field(..., description="场景步骤")

class ScenarioCreate(ScenarioBase):
    module_id: int = Field(..., description="模块ID")

class ScenarioUpdate(BaseModel):
    name: Optional[str] = Field(None, description="场景名称")
    description: Optional[str] = Field(None, description="场景描述")
    steps: Optional[List[Dict[str, Any]]] = Field(None, description="场景步骤")

class Scenario(ScenarioBase):
    id: int
    module_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# 为了避免循环导入问题，在文件末尾更新forward references
CategoryWithAPIs.model_rebuild() 