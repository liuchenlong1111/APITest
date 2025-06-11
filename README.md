# API测试平台

一个现代化的API测试管理平台，支持接口管理、场景测试、报告统计等功能。

## 技术栈

### 前端
- Vue 3 + Composition API
- Vite 构建工具
- Element Plus UI组件库
- Pinia 状态管理
- Vue Router 路由管理
- Axios HTTP客户端

### 后端
- FastAPI 异步Web框架
- MySQL 8.0 数据库
- Redis 缓存和任务队列
- SQLAlchemy ORM
- Pydantic 数据验证
- JWT 认证授权

### 基础设施
- Docker + Docker Compose
- Nginx 反向代理

## 功能特性

- 🚀 **接口管理**: 支持RESTful API的增删改查
- 📊 **分类管理**: 灵活的接口分类和标签系统
- 🔄 **批量测试**: 支持并行和顺序测试
- 🎯 **场景测试**: 复杂业务场景的自动化测试
- 📈 **统计报告**: 测试结果的可视化统计
- 📁 **导入导出**: 支持Swagger/Postman格式导入
- 🔐 **权限管理**: 用户认证和权限控制
- 🌐 **环境配置**: 多环境配置管理

## 快速开始

### 使用Docker Compose（推荐）

```bash
# 克隆项目
git clone <repository-url>
cd api-test-platform

# 启动服务
docker-compose up -d

# 访问应用
# 前端: http://localhost
# 后端API: http://localhost:8000
# API文档: http://localhost:8000/docs
```

### 手动部署

#### 前端开发

```bash
cd frontend
npm install
npm run dev
```

#### 后端开发

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## 项目结构

```
api-test-platform/
├── frontend/          # Vue前端项目
├── backend/           # FastAPI后端项目
├── docker-compose.yml # Docker编排文件
└── README.md         # 项目说明
```

## 环境要求

- Node.js >= 16
- Python >= 3.9
- MySQL >= 8.0
- Redis >= 6.0

## 开发指南

详细的开发文档请参考各子项目的README文件。

## 许可证

MIT License 