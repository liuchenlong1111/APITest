from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# Project schemas
class ProjectBase(BaseModel):
    name: str = Field(..., description="项目名称", max_length=100)
    description: Optional[str] = Field(None, description="项目描述")

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, description="项目名称", max_length=100)
    description: Optional[str] = Field(None, description="项目描述")

class Project(ProjectBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Module schemas
class ModuleBase(BaseModel):
    name: str = Field(..., description="模块名称", max_length=50)
    description: Optional[str] = Field(None, description="模块描述")
    icon: Optional[str] = Field(None, description="模块图标", max_length=10)

class ModuleCreateRequest(ModuleBase):
    """用于API请求的模块创建模式（不包含project_id）"""
    pass

class ModuleCreate(ModuleBase):
    """用于数据库操作的模块创建模式（包含project_id）"""
    project_id: int = Field(..., description="项目ID")

class ModuleUpdate(BaseModel):
    name: Optional[str] = Field(None, description="模块名称", max_length=50)
    description: Optional[str] = Field(None, description="模块描述")
    icon: Optional[str] = Field(None, description="模块图标", max_length=10)
    project_id: Optional[int] = Field(None, description="项目ID")

class Module(ModuleBase):
    id: int
    project_id: int
    created_at: datetime

    class Config:
        from_attributes = True

# 关联模型
class ProjectWithModules(Project):
    modules: List[Module] = []

class ModuleWithStats(Module):
    category_count: int = 0
    api_count: int = 0

class ProjectWithStats(Project):
    module_count: int = 0
    category_count: int = 0
    api_count: int = 0
    modules: List[ModuleWithStats] = [] 