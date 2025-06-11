from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.crud.project import project as crud_project, module as crud_module
from app.schemas.project import (
    Project, ProjectCreate, ProjectUpdate, ProjectWithStats,
    Module, ModuleCreate, ModuleCreateRequest, ModuleUpdate, ModuleWithStats
)

router = APIRouter()

# ================ 项目管理接口 ================

@router.get("/", response_model=List[dict])
def get_projects(
    skip: int = Query(0, ge=0, description="跳过数量"),
    limit: int = Query(100, ge=1, le=1000, description="限制数量"),
    db: Session = Depends(get_db)
):
    """获取项目列表（包含统计信息）"""
    projects = crud_project.get_all_with_stats(db, skip=skip, limit=limit)
    return projects

@router.post("/", response_model=Project)
def create_project(
    project_in: ProjectCreate,
    db: Session = Depends(get_db)
):
    """创建项目"""
    # 检查项目名称是否重复
    existing = crud_project.get_by_name(db, name=project_in.name)
    if existing:
        raise HTTPException(status_code=400, detail="项目名称已存在")
    
    project = crud_project.create(db, obj_in=project_in)
    # 确保返回的对象可以被正确序列化
    return Project.model_validate(project)

@router.get("/{project_id}", response_model=dict)
def get_project(
    project_id: int,
    db: Session = Depends(get_db)
):
    """获取项目详情（包含统计信息和模块列表）"""
    project_stats = crud_project.get_with_stats(db, project_id=project_id)
    if not project_stats:
        raise HTTPException(status_code=404, detail="项目不存在")
    
    # 获取项目下的模块及其统计信息
    modules_stats = crud_module.get_modules_with_stats(db, project_id=project_id)
    project_stats["modules"] = modules_stats
    
    return project_stats

@router.put("/{project_id}", response_model=Project)
def update_project(
    project_id: int,
    project_in: ProjectUpdate,
    db: Session = Depends(get_db)
):
    """更新项目"""
    project = crud_project.get(db, id=project_id)
    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")
    
    # 如果要更新名称，检查是否重复
    if project_in.name and project_in.name != project.name:
        existing = crud_project.get_by_name(db, name=project_in.name)
        if existing:
            raise HTTPException(status_code=400, detail="项目名称已存在")
    
    project = crud_project.update(db, db_obj=project, obj_in=project_in)
    # 确保返回的对象可以被正确序列化
    return Project.model_validate(project)

@router.delete("/{project_id}", response_model=dict)
def delete_project(
    project_id: int,
    db: Session = Depends(get_db)
):
    """删除项目"""
    project = crud_project.get(db, id=project_id)
    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")
    
    crud_project.remove(db, id=project_id)
    return {"message": "项目删除成功"}

# ================ 模块管理接口 ================

@router.get("/{project_id}/modules/", response_model=List[dict])
def get_modules(
    project_id: int,
    skip: int = Query(0, ge=0, description="跳过数量"),
    limit: int = Query(100, ge=1, le=1000, description="限制数量"),
    db: Session = Depends(get_db)
):
    """获取项目下的模块列表（包含统计信息）"""
    # 先检查项目是否存在
    project = crud_project.get(db, id=project_id)
    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")
    
    modules = crud_module.get_modules_with_stats(db, project_id=project_id)
    return modules

@router.post("/{project_id}/modules/", response_model=Module)
def create_module(
    project_id: int,
    module_in: ModuleCreateRequest,
    db: Session = Depends(get_db)
):
    """创建模块"""
    # 检查项目是否存在
    project = crud_project.get(db, id=project_id)
    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")
    
    # 检查同项目下模块名称是否重复
    existing = crud_module.get_by_name(db, name=module_in.name, project_id=project_id)
    if existing:
        raise HTTPException(status_code=400, detail="该项目下已存在同名模块")
    
    # 创建一个包含project_id的模块数据
    module_data = ModuleCreate(
        name=module_in.name,
        description=module_in.description,
        icon=module_in.icon,
        project_id=project_id
    )
    module = crud_module.create(db, obj_in=module_data)
    # 确保返回的对象可以被正确序列化
    return Module.model_validate(module)

@router.get("/modules/{module_id}", response_model=dict)
def get_module(
    module_id: int,
    db: Session = Depends(get_db)
):
    """获取模块详情（包含统计信息）"""
    module_stats = crud_module.get_with_stats(db, module_id=module_id)
    if not module_stats:
        raise HTTPException(status_code=404, detail="模块不存在")
    
    return module_stats

@router.put("/modules/{module_id}", response_model=Module)
def update_module(
    module_id: int,
    module_in: ModuleUpdate,
    db: Session = Depends(get_db)
):
    """更新模块"""
    module = crud_module.get(db, id=module_id)
    if not module:
        raise HTTPException(status_code=404, detail="模块不存在")
    
    # 如果要更新名称，检查是否重复
    if module_in.name and module_in.name != module.name:
        project_id = module_in.project_id if module_in.project_id else module.project_id
        existing = crud_module.get_by_name(db, name=module_in.name, project_id=project_id)
        if existing:
            raise HTTPException(status_code=400, detail="该项目下已存在同名模块")
    
    module = crud_module.update(db, db_obj=module, obj_in=module_in)
    # 确保返回的对象可以被正确序列化
    return Module.model_validate(module)

@router.delete("/modules/{module_id}", response_model=dict)
def delete_module(
    module_id: int,
    db: Session = Depends(get_db)
):
    """删除模块"""
    module = crud_module.get(db, id=module_id)
    if not module:
        raise HTTPException(status_code=404, detail="模块不存在")
    
    crud_module.remove(db, id=module_id)
    return {"message": "模块删除成功"} 