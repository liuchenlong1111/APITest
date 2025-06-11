# 导入所有模型以确保正确的关系映射
from .user import User
from .project import Project, Module, Category
from .api import API, TestResult, Scenario

# 导出所有模型
__all__ = [
    "User",
    "Project", 
    "Module",
    "Category",
    "API",
    "TestResult", 
    "Scenario"
] 