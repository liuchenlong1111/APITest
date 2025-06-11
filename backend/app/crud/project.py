from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func, and_

from app.models.project import Project, Module, Category
from app.models.api import API
from app.schemas.project import (
    ProjectCreate, ProjectUpdate, ModuleCreate, ModuleUpdate
)

class CRUDProject:
    def create(self, db: Session, *, obj_in: ProjectCreate) -> Project:
        """创建项目"""
        db_obj = Project(**obj_in.model_dump())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def get(self, db: Session, id: int) -> Optional[Project]:
        """根据ID获取项目"""
        return db.query(Project).filter(Project.id == id).first()
    
    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[Project]:
        """获取项目列表"""
        return db.query(Project).offset(skip).limit(limit).all()
    
    def get_by_name(self, db: Session, *, name: str) -> Optional[Project]:
        """根据名称获取项目"""
        return db.query(Project).filter(Project.name == name).first()
    
    def get_with_stats(self, db: Session, *, project_id: int) -> dict:
        """获取项目及其统计信息"""
        project = self.get(db, id=project_id)
        if not project:
            return None
        
        # 统计模块数量
        module_count = db.query(func.count(Module.id)).filter(Module.project_id == project_id).scalar()
        
        # 统计分类数量
        category_count = db.query(func.count(Category.id)).join(Module).filter(Module.project_id == project_id).scalar()
        
        # 统计接口数量
        api_count = db.query(func.count(API.id)).join(Category).join(Module).filter(Module.project_id == project_id).scalar()
        
        return {
            "id": project.id,
            "name": project.name,
            "description": project.description,
            "created_at": project.created_at.isoformat() if project.created_at else None,
            "updated_at": project.updated_at.isoformat() if project.updated_at else None,
            "module_count": module_count,
            "category_count": category_count,
            "api_count": api_count
        }
    
    def get_all_with_stats(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[dict]:
        """获取所有项目及其统计信息"""
        projects = self.get_multi(db, skip=skip, limit=limit)
        result = []
        
        for project in projects:
            stats = self.get_with_stats(db, project_id=project.id)
            result.append(stats)
        
        return result
    
    def update(self, db: Session, *, db_obj: Project, obj_in: ProjectUpdate) -> Project:
        """更新项目"""
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def remove(self, db: Session, *, id: int) -> Project:
        """删除项目"""
        obj = db.query(Project).get(id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj

class CRUDModule:
    def create(self, db: Session, *, obj_in: ModuleCreate) -> Module:
        """创建模块"""
        db_obj = Module(**obj_in.model_dump())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def get(self, db: Session, id: int) -> Optional[Module]:
        """根据ID获取模块"""
        return db.query(Module).filter(Module.id == id).first()
    
    def get_multi(self, db: Session, *, project_id: Optional[int] = None, skip: int = 0, limit: int = 100) -> List[Module]:
        """获取模块列表"""
        query = db.query(Module)
        if project_id is not None:
            query = query.filter(Module.project_id == project_id)
        return query.offset(skip).limit(limit).all()
    
    def get_by_name(self, db: Session, *, name: str, project_id: int) -> Optional[Module]:
        """根据名称和项目ID获取模块"""
        return db.query(Module).filter(
            and_(Module.name == name, Module.project_id == project_id)
        ).first()
    
    def get_with_stats(self, db: Session, *, module_id: int) -> dict:
        """获取模块及其统计信息"""
        module = self.get(db, id=module_id)
        if not module:
            return None
        
        # 统计分类数量
        category_count = db.query(func.count(Category.id)).filter(Category.module_id == module_id).scalar()
        
        # 统计接口数量
        api_count = db.query(func.count(API.id)).join(Category).filter(Category.module_id == module_id).scalar()
        
        return {
            "id": module.id,
            "name": module.name,
            "description": module.description,
            "icon": module.icon,
            "project_id": module.project_id,
            "created_at": module.created_at.isoformat() if module.created_at else None,
            "category_count": category_count,
            "api_count": api_count
        }
    
    def get_modules_with_stats(self, db: Session, *, project_id: int) -> List[dict]:
        """获取项目下所有模块及其统计信息"""
        modules = self.get_multi(db, project_id=project_id)
        result = []
        
        for module in modules:
            stats = self.get_with_stats(db, module_id=module.id)
            result.append(stats)
        
        return result
    
    def update(self, db: Session, *, db_obj: Module, obj_in: ModuleUpdate) -> Module:
        """更新模块"""
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def remove(self, db: Session, *, id: int) -> Module:
        """删除模块"""
        obj = db.query(Module).get(id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj

# 创建CRUD实例
project = CRUDProject()
module = CRUDModule() 