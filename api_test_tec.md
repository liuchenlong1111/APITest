# API测试平台技术架构

## 1. 整体架构概述

### 1.1 架构模式
- **前后端分离架构**：Vue.js前端 + FastAPI后端
- **微服务架构**：模块化设计，支持独立部署和扩展
- **容器化部署**：Docker + Docker Compose
- **RESTful API**：标准化接口设计

### 1.2 技术栈选型

#### 前端技术栈
- **框架**：Vue 3 + Composition API
- **构建工具**：Vite
- **UI组件库**：Element Plus
- **状态管理**：Pinia
- **路由管理**：Vue Router 4
- **HTTP客户端**：Axios
- **代码编辑器**：Monaco Editor
- **图表库**：ECharts
- **样式预处理**：SCSS

#### 后端技术栈
- **框架**：FastAPI
- **异步支持**：asyncio + uvicorn
- **数据库**：MySQL 8.0 + Redis
- **认证授权**：JWT + OAuth2
- **API文档**：OpenAPI 3.0 (自动生成)
- **数据验证**：Pydantic
- **任务队列**：Celery + Redis
- **日志系统**：structlog

#### 基础设施
- **容器化**：Docker + Docker Compose
- **反向代理**：Nginx
- **数据库**：MySQL 8.0
- **缓存**：Redis 7
- **消息队列**：Redis (Celery Broker)
- **文件存储**：MinIO (S3兼容)

## 2. 系统架构设计

### 2.1 整体架构图

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web Browser   │    │   Mobile App    │    │   API Client    │
└─────────┬───────┘    └─────────┬───────┘    └─────────┬───────┘
          │                      │                      │
          └──────────────────────┼──────────────────────┘
                                 │
                    ┌─────────────┴─────────────┐
                    │       Nginx Proxy         │
                    └─────────────┬─────────────┘
                                 │
                    ┌─────────────┴─────────────┐
                    │      Vue.js Frontend      │
                    │   (Static Files Serve)    │
                    └─────────────┬─────────────┘
                                 │ HTTP/WebSocket
                    ┌─────────────┴─────────────┐
                    │     FastAPI Backend       │
                    │    (API Gateway)          │
                    └─────────────┬─────────────┘
                                 │
        ┌────────────────────────┼────────────────────────┐
        │                       │                        │
┌───────┴────────┐    ┌─────────┴─────────┐    ┌─────────┴─────────┐
│    MySQL 8.0   │    │      Redis        │    │      MinIO        │
│   (主数据库)    │    │   (缓存/队列)      │    │   (文件存储)       │
└────────────────┘    └───────────────────┘    └───────────────────┘
```

### 2.2 微服务模块划分

#### 核心服务模块
1. **用户认证服务** (auth-service)
2. **项目管理服务** (project-service)
3. **接口管理服务** (api-service)
4. **测试执行服务** (test-service)
5. **场景管理服务** (scenario-service)
6. **报告统计服务** (report-service)
7. **文件管理服务** (file-service)

## 3. 前端架构设计

### 3.1 项目结构

```
frontend/
├── public/
│   ├── index.html
│   └── favicon.ico
├── src/
│   ├── api/                    # API接口封装
│   │   ├── auth.js
│   │   ├── project.js
│   │   ├── api.js
│   │   ├── test.js
│   │   └── index.js
│   ├── assets/                 # 静态资源
│   │   ├── styles/
│   │   ├── images/
│   │   └── fonts/
│   ├── components/             # 公共组件
│   │   ├── common/
│   │   ├── layout/
│   │   └── business/
│   ├── composables/            # 组合式函数
│   │   ├── useAuth.js
│   │   ├── useApi.js
│   │   └── useTest.js
│   ├── directives/             # 自定义指令
│   ├── plugins/                # 插件配置
│   │   ├── element-plus.js
│   │   ├── axios.js
│   │   └── monaco.js
│   ├── router/                 # 路由配置
│   │   ├── index.js
│   │   └── modules/
│   ├── stores/                 # 状态管理
│   │   ├── auth.js
│   │   ├── project.js
│   │   ├── api.js
│   │   └── test.js
│   ├── utils/                  # 工具函数
│   │   ├── request.js
│   │   ├── storage.js
│   │   └── helpers.js
│   ├── views/                  # 页面组件
│   │   ├── auth/
│   │   ├── dashboard/
│   │   ├── project/
│   │   ├── api/
│   │   ├── test/
│   │   └── report/
│   ├── App.vue
│   └── main.js
├── package.json
├── vite.config.js
└── Dockerfile
```

### 3.2 核心技术实现

#### 状态管理 (Pinia)
```javascript
// stores/api.js
import { defineStore } from 'pinia'

export const useApiStore = defineStore('api', {
  state: () => ({
    currentModule: 'exam',
    apiList: [],
    categories: [],
    selectedApis: [],
    testResults: []
  }),
  
  getters: {
    categorizedApis: (state) => {
      // 按分类组织接口
    },
    testStatistics: (state) => {
      // 计算测试统计信息
    }
  },
  
  actions: {
    async fetchApiList(moduleId) {
      // 获取接口列表
    },
    async runTest(apiIds) {
      // 执行测试
    }
  }
})
```

#### HTTP请求封装
```javascript
// utils/request.js
import axios from 'axios'
import { useAuthStore } from '@/stores/auth'

const request = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  timeout: 30000
})

// 请求拦截器
request.interceptors.request.use(
  config => {
    const authStore = useAuthStore()
    if (authStore.token) {
      config.headers.Authorization = `Bearer ${authStore.token}`
    }
    return config
  },
  error => Promise.reject(error)
)

// 响应拦截器
request.interceptors.response.use(
  response => response.data,
  error => {
    // 错误处理
    return Promise.reject(error)
  }
)

export default request
```

## 4. 后端架构设计

### 4.1 项目结构

```
backend/
├── app/
│   ├── api/                    # API路由
│   │   ├── v1/
│   │   │   ├── auth.py
│   │   │   ├── projects.py
│   │   │   ├── apis.py
│   │   │   ├── tests.py
│   │   │   └── scenarios.py
│   │   └── deps.py            # 依赖注入
│   ├── core/                   # 核心配置
│   │   ├── config.py
│   │   ├── security.py
│   │   └── database.py
│   ├── crud/                   # 数据库操作
│   │   ├── base.py
│   │   ├── user.py
│   │   ├── project.py
│   │   └── api.py
│   ├── models/                 # 数据模型
│   │   ├── user.py
│   │   ├── project.py
│   │   ├── api.py
│   │   └── test.py
│   ├── schemas/                # Pydantic模型
│   │   ├── user.py
│   │   ├── project.py
│   │   ├── api.py
│   │   └── test.py
│   ├── services/               # 业务逻辑
│   │   ├── auth_service.py
│   │   ├── test_service.py
│   │   └── import_service.py
│   ├── tasks/                  # 异步任务
│   │   ├── test_tasks.py
│   │   └── import_tasks.py
│   ├── utils/                  # 工具函数
│   │   ├── security.py
│   │   ├── validators.py
│   │   └── helpers.py
│   └── main.py
├── tests/                      # 测试代码
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
```

### 4.2 核心技术实现

#### FastAPI应用配置
```python
# app/main.py
from fastapi import FastAPI, Middleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from app.api.v1 import auth, projects, apis, tests
from app.core.config import settings

app = FastAPI(
    title="API测试平台",
    description="企业级API测试管理平台",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 中间件配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(GZipMiddleware, minimum_size=1000)

# 路由注册
app.include_router(auth.router, prefix="/api/v1/auth", tags=["认证"])
app.include_router(projects.router, prefix="/api/v1/projects", tags=["项目"])
app.include_router(apis.router, prefix="/api/v1/apis", tags=["接口"])
app.include_router(tests.router, prefix="/api/v1/tests", tags=["测试"])
```

#### 数据库配置
```python
# app/core/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
import aiomysql
from databases import Database

# MySQL数据库配置
MYSQL_URL = "mysql+aiomysql://user:password@mysql:3306/api_test?charset=utf8mb4"
DATABASE_URL = "mysql://user:password@mysql:3306/api_test"

# 异步数据库连接
database = Database(MYSQL_URL)


#### 数据模型设计
```python
# app/models/api.py
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
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

class Module(Base):
    __tablename__ = "modules"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50), nullable=False, comment="模块名称")
    icon = Column(String(10), comment="模块图标")
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), comment="项目ID")
    created_at = Column(DateTime, default=func.now(), comment="创建时间")
    
    # 关联关系
    project = relationship("Project", back_populates="modules")
    categories = relationship("Category", back_populates="module", cascade="all, delete-orphan")

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
    apis = relationship("API", back_populates="category", cascade="all, delete-orphan")

class API(Base):
    __tablename__ = "apis"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(200), nullable=False, comment="接口名称")
    method = Column(String(10), nullable=False, comment="请求方法")
    url = Column(String(500), nullable=False, comment="接口URL")
    description = Column(Text, comment="接口描述")
    headers = Column(JSON, comment="请求头")
    params = Column(JSON, comment="请求参数")
    body = Column(JSON, comment="请求体")
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="SET NULL"), nullable=True, comment="分类ID")
    created_at = Column(DateTime, default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), comment="更新时间")
    
    # 关联关系
    category = relationship("Category", back_populates="apis")
    
    # 索引
    __table_args__ = (
        {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8mb4'},
    )
```

#### 业务服务层
```python
# app/services/test_service.py
from typing import List, Dict, Any
from app.models.api import API
from app.schemas.test import TestRequest, TestResult
import httpx
import asyncio

class TestService:
    def __init__(self):
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def run_single_test(self, api: API, config: Dict[str, Any]) -> TestResult:
        """执行单个接口测试"""
        try:
            start_time = time.time()
            
            # 构建请求
            request_data = self._build_request(api, config)
            
            # 发送请求
            response = await self.client.request(**request_data)
            
            end_time = time.time()
            duration = int((end_time - start_time) * 1000)
            
            # 构建结果
            return TestResult(
                api_id=api.id,
                status="success" if response.status_code < 400 else "failed",
                status_code=response.status_code,
                response_time=duration,
                response_data=response.json() if response.headers.get("content-type", "").startswith("application/json") else response.text,
                error_message=None
            )
            
        except Exception as e:
            return TestResult(
                api_id=api.id,
                status="failed",
                error_message=str(e)
            )
    
    async def run_parallel_tests(self, apis: List[API], config: Dict[str, Any]) -> List[TestResult]:
        """并行执行多个接口测试"""
        tasks = [self.run_single_test(api, config) for api in apis]
        return await asyncio.gather(*tasks)
    
    async def run_sequence_tests(self, apis: List[API], config: Dict[str, Any]) -> List[TestResult]:
        """顺序执行多个接口测试"""
        results = []
        context = {}  # 存储上下文数据
        
        for api in apis:
            # 使用上下文数据更新配置
            updated_config = self._update_config_with_context(config, context)
            
            result = await self.run_single_test(api, updated_config)
            results.append(result)
            
            # 更新上下文
            if result.status == "success":
                context[f"step_{len(results)}"] = result.response_data
        
        return results
```

## 5. 数据库设计

### 5.1 数据库表结构

#### 核心表设计
```sql
-- 创建数据库
CREATE DATABASE api_test CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE api_test;

-- 项目表
CREATE TABLE projects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL COMMENT '项目名称',
    description TEXT COMMENT '项目描述',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_name (name),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='项目表';

-- 模块表
CREATE TABLE modules (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL COMMENT '模块名称',
    icon VARCHAR(10) COMMENT '模块图标',
    project_id INT NOT NULL COMMENT '项目ID',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    INDEX idx_project_id (project_id),
    INDEX idx_name (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='模块表';

-- 分类表
CREATE TABLE categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL COMMENT '分类名称',
    description TEXT COMMENT '分类描述',
    color VARCHAR(7) DEFAULT '#00d4ff' COMMENT '分类颜色',
    module_id INT NOT NULL COMMENT '模块ID',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    FOREIGN KEY (module_id) REFERENCES modules(id) ON DELETE CASCADE,
    INDEX idx_module_id (module_id),
    INDEX idx_name (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='分类表';

-- 接口表
CREATE TABLE apis (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(200) NOT NULL COMMENT '接口名称',
    method VARCHAR(10) NOT NULL COMMENT '请求方法',
    url VARCHAR(500) NOT NULL COMMENT '接口URL',
    description TEXT COMMENT '接口描述',
    headers JSON COMMENT '请求头',
    params JSON COMMENT '请求参数',
    body JSON COMMENT '请求体',
    category_id INT NULL COMMENT '分类ID',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL,
    INDEX idx_category_id (category_id),
    INDEX idx_method (method),
    INDEX idx_name (name),
    INDEX idx_created_at (created_at),
    FULLTEXT idx_search (name, description)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='接口表';

-- 场景表
CREATE TABLE scenarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(200) NOT NULL COMMENT '场景名称',
    description TEXT COMMENT '场景描述',
    steps JSON NOT NULL COMMENT '场景步骤',
    module_id INT NOT NULL COMMENT '模块ID',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (module_id) REFERENCES modules(id) ON DELETE CASCADE,
    INDEX idx_module_id (module_id),
    INDEX idx_name (name),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='场景表';

-- 测试记录表
CREATE TABLE test_records (
    id INT AUTO_INCREMENT PRIMARY KEY,
    test_type VARCHAR(20) NOT NULL COMMENT '测试类型: normal, sequence, scenario',
    config JSON COMMENT '测试配置',
    status VARCHAR(20) DEFAULT 'running' COMMENT '测试状态',
    results JSON COMMENT '测试结果',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    completed_at TIMESTAMP NULL COMMENT '完成时间',
    INDEX idx_test_type (test_type),
    INDEX idx_status (status),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='测试记录表';

-- 用户表
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE COMMENT '用户名',
    email VARCHAR(100) NOT NULL UNIQUE COMMENT '邮箱',
    password_hash VARCHAR(255) NOT NULL COMMENT '密码哈希',
    full_name VARCHAR(100) COMMENT '全名',
    is_active BOOLEAN DEFAULT TRUE COMMENT '是否激活',
    is_superuser BOOLEAN DEFAULT FALSE COMMENT '是否超级用户',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_username (username),
    INDEX idx_email (email),
    INDEX idx_is_active (is_active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户表';

-- 用户项目关联表
CREATE TABLE user_projects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL COMMENT '用户ID',
    project_id INT NOT NULL COMMENT '项目ID',
    role VARCHAR(20) DEFAULT 'member' COMMENT '角色: owner, admin, member',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    UNIQUE KEY uk_user_project (user_id, project_id),
    INDEX idx_user_id (user_id),
    INDEX idx_project_id (project_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户项目关联表';
```

### 5.2 MySQL性能优化

#### MySQL配置优化
```ini
# my.cnf
[mysqld]
# 基础配置
default-authentication-plugin=mysql_native_password
character-set-server=utf8mb4
collation-server=utf8mb4_unicode_ci
default-time-zone='+08:00'

# 性能优化
innodb_buffer_pool_size=1G
innodb_log_file_size=256M
innodb_log_buffer_size=64M
innodb_flush_log_at_trx_commit=2
innodb_flush_method=O_DIRECT

# 连接配置
max_connections=1000
max_connect_errors=100000
wait_timeout=28800
interactive_timeout=28800

# 查询缓存
query_cache_type=1
query_cache_size=64M
query_cache_limit=2M

# 慢查询日志
slow_query_log=1
slow_query_log_file=/var/log/mysql/slow.log
long_query_time=2

# 二进制日志
log-bin=mysql-bin
binlog_format=ROW
expire_logs_days=7
```

#### 索引优化策略
```sql
-- 复合索引优化
CREATE INDEX idx_api_category_method ON apis(category_id, method);
CREATE INDEX idx_api_created_name ON apis(created_at, name);

-- 覆盖索引
CREATE INDEX idx_api_list_cover ON apis(category_id, method, name, url);

-- 分区表（大数据量时使用）
ALTER TABLE test_records PARTITION BY RANGE (YEAR(created_at)) (
    PARTITION p2023 VALUES LESS THAN (2024),
    PARTITION p2024 VALUES LESS THAN (2025),
    PARTITION p2025 VALUES LESS THAN (2026),
    PARTITION p_future VALUES LESS THAN MAXVALUE
);
```

### 5.3 Redis缓存设计

#### 缓存策略
```python
# 缓存键设计
CACHE_KEYS = {
    "api_list": "api:list:{module_id}",
    "category_list": "category:list:{module_id}",
    "test_result": "test:result:{test_id}",
    "user_session": "session:{user_id}",
    "api_stats": "stats:api:{api_id}:{date}"
}

# 缓存时间配置
CACHE_TTL = {
    "api_list": 3600,      # 1小时
    "category_list": 3600,  # 1小时
    "test_result": 86400,   # 24小时
    "user_session": 7200,   # 2小时
    "api_stats": 86400      # 24小时
}

# MySQL查询结果缓存
class MySQLCacheService:
    def __init__(self, redis_client):
        self.redis = redis_client
    
    async def get_cached_query(self, query_key: str, query_func, ttl: int = 3600):
        """缓存MySQL查询结果"""
        cached_result = await self.redis.get(query_key)
        if cached_result:
            return json.loads(cached_result)
        
        result = await query_func()
        await self.redis.setex(
            query_key, 
            ttl, 
            json.dumps(result, default=str)
        )
        return result
```

## 6. 容器化部署

### 6.1 Docker配置

#### 前端Dockerfile
```dockerfile
# frontend/Dockerfile
FROM node:18-alpine as builder

WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

#### 后端Dockerfile
```dockerfile
# backend/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# 安装Python依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 创建非root用户
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app
USER app

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### requirements.txt
```txt
# Web框架
fastapi==0.104.1
uvicorn[standard]==0.24.0

# 数据库相关
sqlalchemy==2.0.23
aiomysql==0.2.0
PyMySQL==1.1.0
databases[mysql]==0.8.0

# 异步HTTP客户端
httpx==0.25.2
aiofiles==23.2.1

# 认证和安全
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6

# 数据验证
pydantic==2.5.0
pydantic-settings==2.1.0

# 任务队列
celery==5.3.4
redis==5.0.1

# 日志
structlog==23.2.0

# 工具库
python-dotenv==1.0.0
```

### 6.2 Docker Compose配置

```yaml
# docker-compose.yml
version: '3.8'

services:
  # 前端服务
  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend
    networks:
      - api-test-network

  # 后端服务
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=mysql://apiuser:password@mysql:3306/api_test
      - REDIS_URL=redis://redis:6379/0
      - SECRET_KEY=your-secret-key
    depends_on:
      - mysql
      - redis
    networks:
      - api-test-network
    volumes:
      - ./backend/uploads:/app/uploads

  # 数据库服务
  mysql:
    image: mysql:8.0
    environment:
      - MYSQL_ROOT_PASSWORD=rootpassword
      - MYSQL_DATABASE=api_test
      - MYSQL_USER=apiuser
      - MYSQL_PASSWORD=password
    command: --default-authentication-plugin=mysql_native_password --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci
    volumes:
      - mysql_data:/var/lib/mysql
      - ./backend/init.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "3306:3306"
    networks:
      - api-test-network

  # Redis服务
  redis:
    image: redis:7-alpine
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data
    networks:
      - api-test-network

  # MinIO文件存储
  minio:
    image: minio/minio:latest
    command: server /data --console-address ":9001"
    environment:
      - MINIO_ROOT_USER=minioadmin
      - MINIO_ROOT_PASSWORD=minioadmin
    ports:
      - "9000:9000"
      - "9001:9001"
    volumes:
      - minio_data:/data
    networks:
      - api-test-network

  # Celery Worker
  celery-worker:
    build: ./backend
    command: celery -A app.tasks.celery worker --loglevel=info
    environment:
      - DATABASE_URL=mysql://apiuser:password@mysql:3306/api_test
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - mysql
      - redis
    networks:
      - api-test-network

volumes:
  mysql_data:
  redis_data:
  minio_data:

networks:
  api-test-network:
    driver: bridge
```

## 7. 部署和运维

### 7.1 生产环境部署

#### 环境配置
```bash
# .env.production
NODE_ENV=production
VITE_API_BASE_URL=https://api.yourdomain.com

# 后端环境变量
DATABASE_URL=mysql://user:pass@localhost:3306/api_test
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your-production-secret-key
ALLOWED_HOSTS=["https://yourdomain.com"]
```

#### 部署脚本
```bash
#!/bin/bash
# deploy.sh

# 拉取最新代码
git pull origin main

# 构建和部署
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up -d

# 等待MySQL启动
sleep 10


# 健康检查
sleep 30
curl -f http://localhost/health || exit 1

echo "部署完成！"

# MySQL数据库备份脚本
backup_mysql() {
    BACKUP_DIR="/backup/mysql"
    DATE=$(date +%Y%m%d_%H%M%S)
    BACKUP_FILE="api_test_backup_${DATE}.sql"
    
    mkdir -p $BACKUP_DIR
    
    docker-compose exec mysql mysqldump \
        -u root -prootpassword \
        --single-transaction \
        --routines \
        --triggers \
        api_test > $BACKUP_DIR/$BACKUP_FILE
    
    # 压缩备份文件
    gzip $BACKUP_DIR/$BACKUP_FILE
    
    # 删除7天前的备份
    find $BACKUP_DIR -name "*.gz" -mtime +7 -delete
    
    echo "MySQL备份完成: $BACKUP_FILE.gz"
}
```

### 7.2 监控和日志

#### MySQL监控
```python
# app/utils/mysql_monitor.py
import asyncio
import aiomysql
from typing import Dict, Any

class MySQLMonitor:
    def __init__(self, db_config: dict):
        self.db_config = db_config
    
    async def get_mysql_status(self) -> Dict[str, Any]:
        """获取MySQL状态信息"""
        try:
            conn = await aiomysql.connect(**self.db_config)
            cursor = await conn.cursor()
            
            # 获取连接数
            await cursor.execute("SHOW STATUS LIKE 'Threads_connected'")
            threads_connected = await cursor.fetchone()
            
            # 获取查询数
            await cursor.execute("SHOW STATUS LIKE 'Questions'")
            questions = await cursor.fetchone()
            
            # 获取慢查询数
            await cursor.execute("SHOW STATUS LIKE 'Slow_queries'")
            slow_queries = await cursor.fetchone()
            
            # 获取InnoDB缓冲池使用率
            await cursor.execute("""
                SELECT 
                    (SELECT VARIABLE_VALUE FROM information_schema.GLOBAL_STATUS 
                     WHERE VARIABLE_NAME = 'Innodb_buffer_pool_pages_data') /
                    (SELECT VARIABLE_VALUE FROM information_schema.GLOBAL_STATUS 
                     WHERE VARIABLE_NAME = 'Innodb_buffer_pool_pages_total') * 100 
                AS buffer_pool_usage
            """)
            buffer_pool_usage = await cursor.fetchone()
            
            await cursor.close()
            conn.close()
            
            return {
                "threads_connected": threads_connected[1] if threads_connected else 0,
                "total_questions": questions[1] if questions else 0,
                "slow_queries": slow_queries[1] if slow_queries else 0,
                "buffer_pool_usage": round(float(buffer_pool_usage[0]), 2) if buffer_pool_usage else 0
            }
            
        except Exception as e:
            return {"error": str(e)}
    
    async def check_mysql_health(self) -> bool:
        """检查MySQL健康状态"""
        try:
            conn = await aiomysql.connect(**self.db_config)
            await conn.ping()
            conn.close()
            return True
        except:
            return False
```

#### 日志配置
```python
# app/core/logging.py
import structlog
from structlog.stdlib import LoggerFactory

structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)
```

#### 健康检查
```python
# app/api/v1/health.py
from fastapi import APIRouter, Depends
from app.core.database import get_db
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/health")
async def health_check(db: Session = Depends(get_db)):
    """健康检查接口"""
    try:
        # 检查MySQL数据库连接
        db.execute(text("SELECT 1"))
        
        # 检查Redis连接
        import redis
        r = redis.Redis(host='redis', port=6379, db=0)
        r.ping()
        
        return {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "services": {
                "mysql": "ok",
                "redis": "ok"
            }
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }
```

## 8. 安全设计

### 8.1 认证授权

#### JWT认证
```python
# app/core/security.py
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
```

### 8.2 数据安全

#### 敏感数据加密
```python
# app/utils/encryption.py
from cryptography.fernet import Fernet
import base64

class DataEncryption:
    def __init__(self, key: str):
        self.fernet = Fernet(key.encode())
    
    def encrypt(self, data: str) -> str:
        """加密数据"""
        encrypted_data = self.fernet.encrypt(data.encode())
        return base64.b64encode(encrypted_data).decode()
    
    def decrypt(self, encrypted_data: str) -> str:
        """解密数据"""
        decoded_data = base64.b64decode(encrypted_data.encode())
        decrypted_data = self.fernet.decrypt(decoded_data)
        return decrypted_data.decode()
```

## 9. 性能优化

### 9.1 前端优化

#### 代码分割和懒加载
```javascript
// router/index.js
const routes = [
  {
    path: '/dashboard',
    component: () => import('@/views/dashboard/Index.vue')
  },
  {
    path: '/api',
    component: () => import('@/views/api/Index.vue')
  }
]
```

#### 缓存策略
```javascript
// utils/cache.js
class CacheManager {
  constructor() {
    this.cache = new Map()
    this.ttl = new Map()
  }
  
  set(key, value, ttl = 300000) { // 默认5分钟
    this.cache.set(key, value)
    this.ttl.set(key, Date.now() + ttl)
  }
  
  get(key) {
    if (this.ttl.get(key) < Date.now()) {
      this.cache.delete(key)
      this.ttl.delete(key)
      return null
    }
    return this.cache.get(key)
  }
}
```

### 9.2 后端优化

#### 数据库查询优化
```python
# app/crud/api.py
from sqlalchemy.orm import selectinload
from sqlalchemy import text

class APICrud:
    async def get_apis_with_categories(self, db: Session, module_id: int):
        """优化的接口查询，包含分类信息"""
        return db.query(API)\
            .options(selectinload(API.category))\
            .filter(API.category.has(module_id=module_id))\
            .all()
    
    async def search_apis(self, db: Session, keyword: str, limit: int = 20):
        """使用MySQL全文搜索"""
        return db.execute(
            text("""
                SELECT * FROM apis 
                WHERE MATCH(name, description) AGAINST(:keyword IN NATURAL LANGUAGE MODE)
                LIMIT :limit
            """),
            {"keyword": keyword, "limit": limit}
        ).fetchall()
    
    async def get_api_statistics(self, db: Session, category_id: int):
        """获取接口统计信息"""
        return db.execute(
            text("""
                SELECT 
                    method,
                    COUNT(*) as count,
                    AVG(CHAR_LENGTH(description)) as avg_desc_length
                FROM apis 
                WHERE category_id = :category_id 
                GROUP BY method
            """),
            {"category_id": category_id}
        ).fetchall()
```

#### 异步任务处理
```python
# app/tasks/test_tasks.py
from celery import Celery

celery_app = Celery("api_test")

@celery_app.task
def run_batch_tests(api_ids: List[int], config: dict):
    """批量测试异步任务"""
    # 执行批量测试逻辑
    pass
```

## 10. 扩展性设计

### 10.1 插件系统

#### 插件接口定义
```python
# app/plugins/base.py
from abc import ABC, abstractmethod

class BasePlugin(ABC):
    @abstractmethod
    def name(self) -> str:
        pass
    
    @abstractmethod
    def version(self) -> str:
        pass
    
    @abstractmethod
    def execute(self, context: dict) -> dict:
        pass

class ImportPlugin(BasePlugin):
    @abstractmethod
    def parse_document(self, content: str) -> List[dict]:
        pass

class TestPlugin(BasePlugin):
    @abstractmethod
    def run_test(self, api: dict, config: dict) -> dict:
        pass
```

### 10.2 API版本管理

#### 版本控制策略
```python
# app/api/versions.py
from fastapi import APIRouter

# v1 API
v1_router = APIRouter(prefix="/api/v1")

# v2 API (未来版本)
v2_router = APIRouter(prefix="/api/v2")

# 版本兼容性处理
@v1_router.get("/apis")
async def get_apis_v1():
    # v1版本的接口实现
    pass

@v2_router.get("/apis")
async def get_apis_v2():
    # v2版本的接口实现，保持向后兼容
    pass
```

## 11. 开发规范

### 11.1 代码规范

#### Python代码规范
```python
# 使用Black格式化
# 使用isort排序导入
# 使用flake8检查代码质量
# 使用mypy进行类型检查

# pyproject.toml
[tool.black]
line-length = 88
target-version = ['py311']

[tool.isort]
profile = "black"
multi_line_output = 3

[tool.mypy]
python_version = "3.11"
warn_return_any = true
warn_unused_configs = true
```

#### JavaScript代码规范
```javascript
// .eslintrc.js
module.exports = {
  extends: [
    '@vue/eslint-config-typescript',
    '@vue/eslint-config-prettier'
  ],
  rules: {
    'no-console': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
    'no-debugger': process.env.NODE_ENV === 'production' ? 'warn' : 'off'
  }
}
```

### 11.2 Git工作流

#### 分支策略
```
main          # 主分支，生产环境
├── develop   # 开发分支
├── feature/* # 功能分支
├── hotfix/*  # 热修复分支
└── release/* # 发布分支
```

#### 提交规范
```
feat: 新功能
fix: 修复bug
docs: 文档更新
style: 代码格式调整
refactor: 代码重构
test: 测试相关
chore: 构建过程或辅助工具的变动
```

## 12. 测试策略

### 12.1 前端测试

#### 单元测试
```javascript
// tests/unit/components/ApiItem.spec.js
import { mount } from '@vue/test-utils'
import ApiItem from '@/components/ApiItem.vue'

describe('ApiItem.vue', () => {
  it('renders api information correctly', () => {
    const api = {
      name: 'Test API',
      method: 'GET',
      url: '/api/test'
    }
    
    const wrapper = mount(ApiItem, {
      props: { api }
    })
    
    expect(wrapper.text()).toContain('Test API')
    expect(wrapper.find('.method-get').exists()).toBe(true)
  })
})
```

#### E2E测试
```javascript
// tests/e2e/api-management.spec.js
describe('API Management', () => {
  it('should create new API', () => {
    cy.visit('/api')
    cy.get('[data-cy=create-api-btn]').click()
    cy.get('[data-cy=api-name]').type('New API')
    cy.get('[data-cy=api-method]').select('POST')
    cy.get('[data-cy=api-url]').type('/api/new')
    cy.get('[data-cy=save-btn]').click()
    
    cy.contains('New API').should('be.visible')
  })
})
```

### 12.2 后端测试

#### 单元测试
```python
# tests/test_api_service.py
import pytest
from app.services.test_service import TestService
from app.models.api import API

@pytest.mark.asyncio
async def test_run_single_test():
    service = TestService()
    api = API(
        name="Test API",
        method="GET",
        url="https://httpbin.org/get"
    )
    
    result = await service.run_single_test(api, {})
    
    assert result.status == "success"
    assert result.status_code == 200
```

#### 集成测试
```python
# tests/test_api_endpoints.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_api():
    response = client.post(
        "/api/v1/apis/",
        json={
            "name": "Test API",
            "method": "GET",
            "url": "/test",
            "category_id": 1
        }
    )
    
    assert response.status_code == 201
    assert response.json()["name"] == "Test API"
```

这个技术架构文档提供了完整的API测试平台技术实现方案，涵盖了从前端Vue到后端FastAPI，再到容器化部署的所有技术细节。架构设计具有良好的可扩展性、安全性和性能优化，能够支持企业级的API测试需求。 