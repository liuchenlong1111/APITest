from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.crud.api import api as crud_api, category as crud_category
from app.crud.project import project as crud_project
from app.schemas.api import (
    API, APICreate, APIUpdate, APIWithCategory,
    Category, CategoryCreate, CategoryUpdate, CategoryWithAPIs
)

router = APIRouter()

# ================ 分类管理接口 ================

@router.get("/categories/", response_model=List[Category])
def get_categories(
    module_id: Optional[int] = Query(None, description="模块ID"),
    project_id: Optional[int] = Query(None, description="项目ID"),
    skip: int = Query(0, ge=0, description="跳过数量"),
    limit: int = Query(100, ge=1, le=1000, description="限制数量"),
    db: Session = Depends(get_db)
):
    """获取分类列表"""
    if project_id:
        # 按项目ID获取所有分类
        categories = crud_category.get_by_project_id(db, project_id=project_id, skip=skip, limit=limit)
    else:
        # 按模块ID获取分类
        categories = crud_category.get_multi(db, module_id=module_id, skip=skip, limit=limit)
    # 确保返回的对象可以被正确序列化
    return [Category.model_validate(category) for category in categories]

@router.post("/categories/", response_model=Category)
def create_category(
    category_in: CategoryCreate,
    db: Session = Depends(get_db)
):
    """创建分类"""
    # 检查同模块下分类名称是否重复
    existing = crud_category.get_by_name(db, name=category_in.name, module_id=category_in.module_id)
    if existing:
        raise HTTPException(status_code=400, detail="该模块下已存在同名分类")
    
    category = crud_category.create(db, obj_in=category_in)
    # 确保返回的对象可以被正确序列化
    return Category.model_validate(category)

@router.get("/categories/{category_id}", response_model=CategoryWithAPIs)
def get_category(
    category_id: int,
    db: Session = Depends(get_db)
):
    """获取分类详情"""
    category = crud_category.get(db, id=category_id)
    if not category:
        raise HTTPException(status_code=404, detail="分类不存在")
    # 确保返回的对象可以被正确序列化
    return CategoryWithAPIs.model_validate(category)

@router.put("/categories/{category_id}", response_model=Category)
def update_category(
    category_id: int,
    category_in: CategoryUpdate,
    db: Session = Depends(get_db)
):
    """更新分类"""
    category = crud_category.get(db, id=category_id)
    if not category:
        raise HTTPException(status_code=404, detail="分类不存在")
    
    # 如果要更新名称，检查同模块下是否重复
    if category_in.name and category_in.name != category.name:
        existing = crud_category.get_by_name(db, name=category_in.name, module_id=category.module_id)
        if existing:
            raise HTTPException(status_code=400, detail="该模块下已存在同名分类")
    
    category = crud_category.update(db, db_obj=category, obj_in=category_in)
    # 确保返回的对象可以被正确序列化
    return Category.model_validate(category)

@router.delete("/categories/{category_id}", response_model=Category)
def delete_category(
    category_id: int,
    db: Session = Depends(get_db)
):
    """删除分类"""
    category = crud_category.get(db, id=category_id)
    if not category:
        raise HTTPException(status_code=404, detail="分类不存在")
    
    category = crud_category.remove(db, id=category_id)
    # 确保返回的对象可以被正确序列化
    return Category.model_validate(category)

# ================ 接口管理接口 ================

@router.get("/", response_model=List[APIWithCategory])
def get_apis(
    category_id: Optional[int] = Query(None, description="分类ID"),
    project_id: Optional[int] = Query(None, description="项目ID"),
    module_id: Optional[int] = Query(None, description="模块ID"),
    keyword: Optional[str] = Query(None, description="搜索关键词"),
    skip: int = Query(0, ge=0, description="跳过数量"),
    limit: int = Query(100, ge=1, le=1000, description="限制数量"),
    db: Session = Depends(get_db)
):
    """获取接口列表"""
    if project_id:
        # 按项目ID获取接口，支持模块和分类过滤
        apis = crud_api.get_by_project_module_category(db, project_id=project_id, module_id=module_id, category_id=category_id, keyword=keyword, skip=skip, limit=limit)
    elif keyword:
        apis = crud_api.search(db, keyword=keyword, category_id=category_id, skip=skip, limit=limit)
    else:
        apis = crud_api.get_multi(db, category_id=category_id, skip=skip, limit=limit)
    # 确保返回的对象可以被正确序列化
    return [APIWithCategory.model_validate(api) for api in apis]

@router.post("/", response_model=API)
def create_api(
    api_in: APICreate,
    db: Session = Depends(get_db)
):
    """创建接口"""
    # 检查接口名称是否重复
    existing = crud_api.get_by_name(db, name=api_in.name)
    if existing:
        raise HTTPException(status_code=400, detail="接口名称已存在")
    
    # 如果指定了分类，检查分类是否存在
    if api_in.category_id:
        category = crud_category.get(db, id=api_in.category_id)
        if not category:
            raise HTTPException(status_code=404, detail="指定的分类不存在")
    
    api = crud_api.create(db, obj_in=api_in)
    # 确保返回的对象可以被正确序列化
    return API.model_validate(api)

@router.get("/{api_id}", response_model=APIWithCategory)
def get_api(
    api_id: int,
    db: Session = Depends(get_db)
):
    """获取接口详情"""
    api = crud_api.get(db, id=api_id)
    if not api:
        raise HTTPException(status_code=404, detail="接口不存在")
    # 确保返回的对象可以被正确序列化
    return APIWithCategory.model_validate(api)

@router.put("/{api_id}", response_model=API)
def update_api(
    api_id: int,
    api_in: APIUpdate,
    db: Session = Depends(get_db)
):
    """更新接口"""
    api = crud_api.get(db, id=api_id)
    if not api:
        raise HTTPException(status_code=404, detail="接口不存在")
    
    # 如果要更新名称，检查是否重复
    if api_in.name and api_in.name != api.name:
        existing = crud_api.get_by_name(db, name=api_in.name)
        if existing:
            raise HTTPException(status_code=400, detail="接口名称已存在")
    
    # 如果要更新分类，检查分类是否存在
    if api_in.category_id:
        category = crud_category.get(db, id=api_in.category_id)
        if not category:
            raise HTTPException(status_code=404, detail="指定的分类不存在")
    
    api = crud_api.update(db, db_obj=api, obj_in=api_in)
    # 确保返回的对象可以被正确序列化
    return API.model_validate(api)

@router.delete("/{api_id}", response_model=API)
def delete_api(
    api_id: int,
    db: Session = Depends(get_db)
):
    """删除接口"""
    api = crud_api.get(db, id=api_id)
    if not api:
        raise HTTPException(status_code=404, detail="接口不存在")
    
    api = crud_api.remove(db, id=api_id)
    # 确保返回的对象可以被正确序列化
    return API.model_validate(api) 