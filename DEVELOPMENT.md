# API测试平台开发指南

## 项目概述

这是一个现代化的API测试管理平台，采用前后端分离架构，支持接口管理、场景测试、报告统计等功能。

## 技术栈

### 前端
- **Vue 3** - 渐进式JavaScript框架
- **TypeScript** - 类型安全的JavaScript超集
- **Vite** - 快速的前端构建工具
- **Element Plus** - Vue 3组件库
- **Pinia** - Vue状态管理库
- **Vue Router** - Vue路由管理
- **Axios** - HTTP客户端
- **ECharts** - 数据可视化图表库
- **SCSS** - CSS预处理器

### 后端
- **FastAPI** - 现代化的Python Web框架
- **SQLAlchemy** - Python ORM框架
- **MySQL** - 关系型数据库
- **Redis** - 内存数据库
- **Pydantic** - 数据验证库
- **JWT** - 身份认证
- **Uvicorn** - ASGI服务器

### 基础设施
- **Docker** - 容器化技术
- **Docker Compose** - 容器编排
- **Nginx** - Web服务器和反向代理

## 快速开始

### 使用Docker（推荐）

1. **克隆项目**
```bash
git clone <repository-url>
cd api-test-platform
```

2. **启动服务**
```bash
./start.sh
```

3. **访问应用**
- 前端: http://localhost
- 后端API: http://localhost:8000
- API文档: http://localhost:8000/docs

### 手动开发

#### 前端开发

1. **安装依赖**
```bash
cd frontend
npm install
```

2. **启动开发服务器**
```bash
npm run dev
```

3. **构建生产版本**
```bash
npm run build
```

#### 后端开发

1. **创建虚拟环境**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **配置环境变量**
```bash
cp env.example .env
# 编辑.env文件，配置数据库等信息
```

4. **启动开发服务器**
```bash
uvicorn app.main:app --reload
```

## 项目结构

```
api-test-platform/
├── frontend/                 # Vue前端项目
│   ├── src/
│   │   ├── api/             # API接口封装
│   │   ├── components/      # 公共组件
│   │   ├── layouts/         # 布局组件
│   │   ├── router/          # 路由配置
│   │   ├── stores/          # 状态管理
│   │   ├── styles/          # 样式文件
│   │   ├── types/           # TypeScript类型定义
│   │   ├── utils/           # 工具函数
│   │   └── views/           # 页面组件
│   ├── public/              # 静态资源
│   ├── package.json         # 依赖配置
│   ├── vite.config.ts       # Vite配置
│   └── Dockerfile           # Docker配置
├── backend/                  # FastAPI后端项目
│   ├── app/
│   │   ├── api/             # API路由
│   │   ├── core/            # 核心配置
│   │   ├── crud/            # 数据库操作
│   │   ├── models/          # 数据模型
│   │   ├── schemas/         # Pydantic模型
│   │   └── main.py          # 应用入口
│   ├── requirements.txt     # Python依赖
│   ├── Dockerfile           # Docker配置
│   └── init.sql             # 数据库初始化
├── docker-compose.yml       # Docker编排配置
├── start.sh                 # 启动脚本
└── README.md               # 项目说明
```

## 开发规范

### 代码规范

#### 前端
- 使用TypeScript进行类型检查
- 遵循Vue 3 Composition API规范
- 使用ESLint和Prettier进行代码格式化
- 组件命名使用PascalCase
- 文件命名使用kebab-case

#### 后端
- 遵循PEP 8 Python代码规范
- 使用Black进行代码格式化
- 使用isort进行导入排序
- 使用mypy进行类型检查
- API路由使用RESTful设计

### Git工作流

1. **分支命名规范**
```
feature/功能名称    # 新功能开发
bugfix/问题描述     # Bug修复
hotfix/紧急修复     # 紧急修复
```

2. **提交信息规范**
```
feat: 新功能
fix: Bug修复
docs: 文档更新
style: 代码格式调整
refactor: 代码重构
test: 测试相关
chore: 构建过程或辅助工具的变动
```

## 数据库设计

### 核心表结构

- **users** - 用户表
- **projects** - 项目表
- **modules** - 模块表
- **categories** - 分类表
- **apis** - 接口表
- **test_results** - 测试结果表
- **scenarios** - 场景表

### 数据库迁移

使用Alembic进行数据库迁移：

```bash
# 生成迁移文件
alembic revision --autogenerate -m "描述"

# 执行迁移
alembic upgrade head
```

## API文档

后端API遵循OpenAPI 3.0规范，启动服务后可访问：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 测试

### 前端测试

```bash
cd frontend
npm run test        # 单元测试
npm run test:e2e    # E2E测试
```

### 后端测试

```bash
cd backend
pytest              # 运行所有测试
pytest -v           # 详细输出
pytest --cov        # 测试覆盖率
```

## 部署

### 生产环境部署

1. **配置环境变量**
```bash
# 修改docker-compose.yml中的环境变量
# 设置安全的SECRET_KEY
# 配置生产数据库连接
```

2. **启动生产服务**
```bash
docker-compose -f docker-compose.prod.yml up -d
```

3. **配置Nginx**
```bash
# 配置SSL证书
# 设置域名和反向代理
```

### 监控和日志

- 使用Docker日志查看应用日志
- 配置日志轮转和持久化
- 设置应用监控和告警

## 常见问题

### 1. 数据库连接失败
检查MySQL服务是否启动，确认连接配置正确。

### 2. 前端代理失败
确认后端服务已启动，检查Vite代理配置。

### 3. Docker构建失败
检查Docker版本，清理Docker缓存后重试。

## 贡献指南

1. Fork项目
2. 创建功能分支
3. 提交代码
4. 创建Pull Request

## 许可证

MIT License 