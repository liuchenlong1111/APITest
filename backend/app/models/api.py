from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base

class API(Base):
    __tablename__ = "apis"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(200), nullable=False, comment="接口名称")
    method = Column(String(10), nullable=False, comment="请求方法")
    url = Column(String(500), comment="接口URL")  # 兼容旧字段
    path = Column(String(500), comment="接口路径")  # 新增路径字段
    description = Column(Text, comment="接口描述")
    headers = Column(JSON, comment="请求头")
    params = Column(JSON, comment="请求参数")
    parameters = Column(JSON, comment="参数列表")  # 导入时使用
    body = Column(JSON, comment="请求体")
    responses = Column(JSON, comment="响应定义")  # 导入时使用
    tags = Column(JSON, comment="标签")  # 导入时使用
    security = Column(JSON, comment="安全配置")  # 导入时使用
    notes = Column(Text, comment="备注")  # 导入时使用
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=True, comment="项目ID")
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="SET NULL"), nullable=True, comment="分类ID")
    created_at = Column(DateTime, default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), comment="更新时间")
    
    # 关联关系
    category = relationship("Category", back_populates="apis")
    test_results = relationship("TestResult", back_populates="api")
    
    def __repr__(self):
        return f"<API(id={self.id}, name='{self.name}', method='{self.method}', url='{self.url}')>"

class TestResult(Base):
    __tablename__ = "test_results"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    api_id = Column(Integer, ForeignKey("apis.id", ondelete="CASCADE"), comment="接口ID")
    test_type = Column(String(20), nullable=False, comment="测试类型: normal, sequence, scenario")
    status = Column(String(20), default="pending", comment="测试状态: pending, running, success, failed")
    status_code = Column(Integer, comment="HTTP状态码")
    response_time = Column(Integer, comment="响应时间(ms)")
    response_data = Column(JSON, comment="响应数据")
    error_message = Column(Text, comment="错误信息")
    created_at = Column(DateTime, default=func.now(), comment="创建时间")
    
    # 关联关系
    api = relationship("API", back_populates="test_results")
    
    def __repr__(self):
        return f"<TestResult(id={self.id}, api_id={self.api_id}, status='{self.status}')>"

class Scenario(Base):
    __tablename__ = "scenarios"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(200), nullable=False, comment="场景名称")
    description = Column(Text, comment="场景描述")
    steps = Column(JSON, nullable=False, comment="场景步骤")
    module_id = Column(Integer, ForeignKey("modules.id", ondelete="CASCADE"), comment="模块ID")
    created_at = Column(DateTime, default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), comment="更新时间")
    
    def __repr__(self):
        return f"<Scenario(id={self.id}, name='{self.name}', module_id={self.module_id})>" 