from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.models.api import API, TestResult, Scenario
from app.models.project import Category, Module
from app.schemas.api import (
    APICreate, APIUpdate, CategoryCreate, CategoryUpdate,
    TestResultCreate, ScenarioCreate, ScenarioUpdate
)

class CRUDCategory:
    def create(self, db: Session, *, obj_in: CategoryCreate) -> Category:
        """创建分类"""
        db_obj = Category(**obj_in.model_dump())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def get(self, db: Session, id: int) -> Optional[Category]:
        """根据ID获取分类"""
        return db.query(Category).filter(Category.id == id).first()
    
    def get_multi(self, db: Session, *, module_id: Optional[int] = None, skip: int = 0, limit: int = 100) -> List[Category]:
        """获取分类列表"""
        query = db.query(Category)
        if module_id is not None:
            query = query.filter(Category.module_id == module_id)
        return query.offset(skip).limit(limit).all()
    
    def get_by_project_id(self, db: Session, *, project_id: int, skip: int = 0, limit: int = 100) -> List[Category]:
        """根据项目ID获取分类列表"""
        return db.query(Category).join(Module).filter(
            Module.project_id == project_id
        ).offset(skip).limit(limit).all()
    
    def get_by_name(self, db: Session, *, name: str, module_id: int) -> Optional[Category]:
        """根据名称和模块ID获取分类"""
        return db.query(Category).filter(
            and_(Category.name == name, Category.module_id == module_id)
        ).first()
    
    def update(self, db: Session, *, db_obj: Category, obj_in: CategoryUpdate) -> Category:
        """更新分类"""
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def remove(self, db: Session, *, id: int) -> Category:
        """删除分类"""
        obj = db.query(Category).get(id)
        db.delete(obj)
        db.commit()
        return obj

class CRUDAPI:
    def create(self, db: Session, *, obj_in: APICreate) -> API:
        """创建接口"""
        db_obj = API(**obj_in.model_dump())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def get(self, db: Session, id: int) -> Optional[API]:
        """根据ID获取接口"""
        return db.query(API).filter(API.id == id).first()
    
    def get_multi(self, db: Session, *, category_id: Optional[int] = None, skip: int = 0, limit: int = 100) -> List[API]:
        """获取接口列表"""
        query = db.query(API)
        if category_id is not None:
            query = query.filter(API.category_id == category_id)
        return query.offset(skip).limit(limit).all()
    
    def get_by_project_id(self, db: Session, *, project_id: int, keyword: Optional[str] = None, skip: int = 0, limit: int = 100) -> List[API]:
        """根据项目ID获取接口列表"""
        # 使用左连接处理category_id为NULL的情况
        query = db.query(API).outerjoin(Category).outerjoin(Module).filter(
            Module.project_id == project_id
        )
        if keyword:
            query = query.filter(API.name.contains(keyword))
        return query.offset(skip).limit(limit).all()
    
    def get_by_project_and_category(self, db: Session, *, project_id: int, category_id: Optional[int] = None, keyword: Optional[str] = None, skip: int = 0, limit: int = 100) -> List[API]:
        """根据项目ID和分类ID获取接口列表"""
        query = db.query(API).outerjoin(Category).outerjoin(Module).filter(
            Module.project_id == project_id
        )
        if category_id is not None:
            query = query.filter(API.category_id == category_id)
        if keyword:
            query = query.filter(API.name.contains(keyword))
        return query.offset(skip).limit(limit).all()
    
    def get_by_project_module_category(self, db: Session, *, project_id: int, module_id: Optional[int] = None, category_id: Optional[int] = None, keyword: Optional[str] = None, skip: int = 0, limit: int = 100) -> List[API]:
        """根据项目ID、模块ID和分类ID获取接口列表"""
        query = db.query(API).outerjoin(Category).outerjoin(Module).filter(
            Module.project_id == project_id
        )
        if module_id is not None:
            query = query.filter(Category.module_id == module_id)
        if category_id is not None:
            query = query.filter(API.category_id == category_id)
        if keyword:
            query = query.filter(API.name.contains(keyword))
        return query.offset(skip).limit(limit).all()
    
    def get_by_name(self, db: Session, *, name: str) -> Optional[API]:
        """根据名称获取接口"""
        return db.query(API).filter(API.name == name).first()
    
    def search(self, db: Session, *, keyword: str, category_id: Optional[int] = None, skip: int = 0, limit: int = 100) -> List[API]:
        """搜索接口"""
        query = db.query(API).filter(API.name.contains(keyword))
        if category_id is not None:
            query = query.filter(API.category_id == category_id)
        return query.offset(skip).limit(limit).all()
    
    def update(self, db: Session, *, db_obj: API, obj_in: APIUpdate) -> API:
        """更新接口"""
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def remove(self, db: Session, *, id: int) -> API:
        """删除接口"""
        obj = db.query(API).get(id)
        db.delete(obj)
        db.commit()
        return obj

class CRUDTestResult:
    def create(self, db: Session, *, obj_in: TestResultCreate) -> TestResult:
        """创建测试结果"""
        db_obj = TestResult(**obj_in.model_dump())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def get_multi_by_api(self, db: Session, *, api_id: int, skip: int = 0, limit: int = 100) -> List[TestResult]:
        """根据API ID获取测试结果列表"""
        return db.query(TestResult).filter(TestResult.api_id == api_id).offset(skip).limit(limit).all()

class CRUDScenario:
    def create(self, db: Session, *, obj_in: ScenarioCreate) -> Scenario:
        """创建场景"""
        db_obj = Scenario(**obj_in.model_dump())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def get(self, db: Session, id: int) -> Optional[Scenario]:
        """根据ID获取场景"""
        return db.query(Scenario).filter(Scenario.id == id).first()
    
    def get_multi(self, db: Session, *, module_id: Optional[int] = None, skip: int = 0, limit: int = 100) -> List[Scenario]:
        """获取场景列表"""
        query = db.query(Scenario)
        if module_id is not None:
            query = query.filter(Scenario.module_id == module_id)
        return query.offset(skip).limit(limit).all()
    
    def update(self, db: Session, *, db_obj: Scenario, obj_in: ScenarioUpdate) -> Scenario:
        """更新场景"""
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def remove(self, db: Session, *, id: int) -> Scenario:
        """删除场景"""
        obj = db.query(Scenario).get(id)
        db.delete(obj)
        db.commit()
        return obj

# 创建CRUD实例
category = CRUDCategory()
api = CRUDAPI()
test_result = CRUDTestResult()
scenario = CRUDScenario() 