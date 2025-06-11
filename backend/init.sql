-- 创建数据库
CREATE DATABASE IF NOT EXISTS api_test CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE api_test;

-- 用户表
CREATE TABLE IF NOT EXISTS users (
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

-- 项目表
CREATE TABLE IF NOT EXISTS projects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL COMMENT '项目名称',
    description TEXT COMMENT '项目描述',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_name (name),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='项目表';

-- 模块表
CREATE TABLE IF NOT EXISTS modules (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL COMMENT '模块名称',
    description TEXT COMMENT '模块描述',
    icon VARCHAR(10) COMMENT '模块图标',
    project_id INT NOT NULL COMMENT '项目ID',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    INDEX idx_project_id (project_id),
    INDEX idx_name (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='模块表';

-- 分类表
CREATE TABLE IF NOT EXISTS categories (
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
CREATE TABLE IF NOT EXISTS apis (
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

-- 测试结果表
CREATE TABLE IF NOT EXISTS test_results (
    id INT AUTO_INCREMENT PRIMARY KEY,
    api_id INT NOT NULL COMMENT '接口ID',
    test_type VARCHAR(20) NOT NULL COMMENT '测试类型: normal, sequence, scenario',
    status VARCHAR(20) DEFAULT 'pending' COMMENT '测试状态: pending, running, success, failed',
    status_code INT COMMENT 'HTTP状态码',
    response_time INT COMMENT '响应时间(ms)',
    response_data JSON COMMENT '响应数据',
    error_message TEXT COMMENT '错误信息',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    FOREIGN KEY (api_id) REFERENCES apis(id) ON DELETE CASCADE,
    INDEX idx_api_id (api_id),
    INDEX idx_test_type (test_type),
    INDEX idx_status (status),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='测试结果表';

-- 场景表
CREATE TABLE IF NOT EXISTS scenarios (
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

-- 插入默认管理员用户
INSERT IGNORE INTO users (username, email, password_hash, full_name, is_superuser) VALUES 
('admin', 'admin@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj6QJw/2Oy6e', '系统管理员', TRUE);

-- 插入示例项目
INSERT IGNORE INTO projects (id, name, description) VALUES 
(1, 'API测试平台', '用于演示的API测试项目');

-- 插入示例模块
INSERT IGNORE INTO modules (id, name, icon, project_id) VALUES 
(1, '用户管理', '👤', 1),
(2, '项目管理', '📁', 1),
(3, '接口管理', '🔗', 1),
(4, '测试管理', '🧪', 1);

-- 插入示例分类
INSERT IGNORE INTO categories (id, name, description, color, module_id) VALUES 
(1, '认证接口', '用户认证相关接口', '#409eff', 1),
(2, '用户信息', '用户信息管理接口', '#67c23a', 1),
(3, '项目操作', '项目CRUD操作接口', '#e6a23c', 2),
(4, '接口操作', '接口CRUD操作接口', '#f56c6c', 3);

-- 插入示例接口
INSERT IGNORE INTO apis (id, name, method, url, description, category_id) VALUES 
(1, '用户登录', 'POST', '/api/v1/auth/login', '用户登录接口', 1),
(2, '用户注册', 'POST', '/api/v1/auth/register', '用户注册接口', 1),
(3, '获取用户信息', 'GET', '/api/v1/auth/me', '获取当前用户信息', 2),
(4, '更新用户信息', 'PUT', '/api/v1/users/{id}', '更新用户信息', 2),
(5, '获取项目列表', 'GET', '/api/v1/projects', '获取项目列表', 3),
(6, '创建项目', 'POST', '/api/v1/projects', '创建新项目', 3),
(7, '获取接口列表', 'GET', '/api/v1/apis', '获取接口列表', 4),
(8, '创建接口', 'POST', '/api/v1/apis', '创建新接口', 4); 