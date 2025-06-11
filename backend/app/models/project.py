from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base

class Project(Base):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False, comment="项目名称")
    description = Column(Text, comment="项目描述")
    created_at = Column(DateTime, default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), comment="更新时间")
    
    # 关联关系
    modules = relationship("Module", back_populates="project", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Project(id={self.id}, name='{self.name}')>"

class Module(Base):
    __tablename__ = "modules"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50), nullable=False, comment="模块名称")
    description = Column(Text, comment="模块描述")
    icon = Column(String(10), comment="模块图标")
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), comment="项目ID")
    created_at = Column(DateTime, default=func.now(), comment="创建时间")
    
    # 关联关系
    project = relationship("Project", back_populates="modules")
    categories = relationship("Category", back_populates="module", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Module(id={self.id}, name='{self.name}', project_id={self.project_id})>"

class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False, comment="分类名称")
    description = Column(Text, comment="分类描述")
    color = Column(String(7), default="#00d4ff", comment="分类颜色")
    module_id = Column(Integer, ForeignKey("modules.id", ondelete="CASCADE"), comment="模块ID")
    created_at = Column(DateTime, default=func.now(), comment="创建时间")
    
    # 关联关系
    module = relationship("Module", back_populates="categories")
    apis = relationship("API", back_populates="category")
    
    def __repr__(self):
        return f"<Category(id={self.id}, name='{self.name}', module_id={self.module_id})>" 