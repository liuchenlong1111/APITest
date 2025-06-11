# API管理功能说明

## 功能概述

本次更新为API测试平台添加了完整的接口分类和接口管理功能，包括：

### 1. 接口分类管理
- ✅ 创建分类
- ✅ 查看分类列表
- ✅ 编辑分类信息
- ✅ 删除分类
- ✅ 分类颜色标识

### 2. 接口管理
- ✅ 创建接口
- ✅ 查看接口列表
- ✅ 编辑接口信息
- ✅ 删除接口
- ✅ 接口搜索
- ✅ 按分类筛选
- ✅ 分页显示

## 技术实现

### 后端实现

#### 1. 数据模型 (backend/app/models/)
- **Category模型**: 接口分类信息
- **API模型**: 接口详细信息
- **TestResult模型**: 测试结果记录
- **Scenario模型**: 测试场景

#### 2. API接口 (backend/app/api/v1/apis.py)
```python
# 分类管理接口
GET    /api/v1/apis/categories/          # 获取分类列表
POST   /api/v1/apis/categories/          # 创建分类
GET    /api/v1/apis/categories/{id}      # 获取分类详情
PUT    /api/v1/apis/categories/{id}      # 更新分类
DELETE /api/v1/apis/categories/{id}      # 删除分类

# 接口管理接口
GET    /api/v1/apis/                     # 获取接口列表
POST   /api/v1/apis/                     # 创建接口
GET    /api/v1/apis/{id}                 # 获取接口详情
PUT    /api/v1/apis/{id}                 # 更新接口
DELETE /api/v1/apis/{id}                 # 删除接口
```

#### 3. 数据验证 (backend/app/schemas/api.py)
- Pydantic模型用于请求/响应数据验证
- 支持JSON格式的请求头、参数、请求体

#### 4. CRUD操作 (backend/app/crud/api.py)
- 封装数据库操作逻辑
- 支持搜索、分页、关联查询

### 前端实现

#### 1. API接口调用 (frontend/src/api/api.ts)
- TypeScript类型定义
- 统一的API调用封装
- 错误处理

#### 2. 页面组件 (frontend/src/views/api/Index.vue)
- Vue 3 Composition API
- Element Plus UI组件
- 响应式数据管理

## 使用方法

### 1. 启动服务

#### 后端服务
```bash
cd backend
python -m app.main
```
服务将在 http://localhost:8000 启动

#### 前端服务
```bash
cd frontend
npm install
npm run dev
```
服务将在 http://localhost:3000 启动

### 2. 访问页面

- 前端页面: http://localhost:3000/#/api
- API文档: http://localhost:8000/docs
- 测试页面: 打开项目根目录的 `test_api.html`

### 3. 功能操作

#### 分类管理
1. 点击"新增分类"按钮
2. 填写分类名称、描述、选择颜色
3. 点击确定保存
4. 可以点击分类标签进行筛选
5. 点击分类标签的×号删除分类

#### 接口管理
1. 点击"新增接口"按钮
2. 填写接口基本信息：
   - 接口名称（必填）
   - 请求方法（必填）
   - 接口地址（必填）
   - 接口描述（可选）
   - 所属分类（可选）
3. 填写请求详情（JSON格式）：
   - 请求头
   - 请求参数
   - 请求体
4. 点击确定保存

#### 搜索和筛选
- 在搜索框输入关键词搜索接口名称
- 选择分类进行筛选
- 支持分页浏览

## 数据库结构

### categories表
```sql
CREATE TABLE categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL COMMENT '分类名称',
    description TEXT COMMENT '分类描述',
    color VARCHAR(7) DEFAULT '#00d4ff' COMMENT '分类颜色',
    module_id INT NOT NULL COMMENT '模块ID',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### apis表
```sql
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
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

## 示例数据

系统已预置了一些示例数据：

### 分类示例
- 认证接口 (蓝色)
- 用户信息 (绿色)
- 项目操作 (橙色)
- 接口操作 (红色)

### 接口示例
- 用户登录 (POST /api/v1/auth/login)
- 用户注册 (POST /api/v1/auth/register)
- 获取用户信息 (GET /api/v1/auth/me)
- 更新用户信息 (PUT /api/v1/users/{id})
- 获取项目列表 (GET /api/v1/projects)
- 创建项目 (POST /api/v1/projects)
- 获取接口列表 (GET /api/v1/apis)
- 创建接口 (POST /api/v1/apis)

## 注意事项

1. **数据库连接**: 确保MySQL数据库正常运行，并执行了 `backend/init.sql` 初始化脚本
2. **CORS配置**: 后端已配置CORS允许前端跨域访问
3. **数据验证**: 前后端都有数据验证，确保数据完整性
4. **错误处理**: 统一的错误处理机制，用户友好的错误提示
5. **分页处理**: 当前分页总数计算需要优化，建议后端添加count接口

## 后续扩展

1. **接口测试**: 集成HTTP客户端，支持直接测试接口
2. **导入导出**: 支持Postman、Swagger等格式的导入导出
3. **版本管理**: 接口版本控制和变更历史
4. **权限控制**: 基于角色的接口访问权限
5. **批量操作**: 支持批量创建、编辑、删除接口
6. **接口文档**: 自动生成接口文档
7. **Mock服务**: 基于接口定义生成Mock数据

## 故障排除

### 常见问题

1. **前端页面空白**: 检查控制台错误，确保后端服务正常运行
2. **API调用失败**: 检查网络连接和后端服务状态
3. **数据不显示**: 检查数据库连接和数据是否正确初始化
4. **TypeScript错误**: 运行 `npm run type-check` 检查类型错误

### 调试方法

1. 查看浏览器开发者工具的Network标签
2. 查看后端日志输出
3. 使用 `test_api.html` 页面进行API测试
4. 访问 http://localhost:8000/docs 查看API文档 