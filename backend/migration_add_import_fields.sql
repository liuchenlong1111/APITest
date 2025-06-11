-- 为API表添加导入功能所需的字段
-- 添加路径字段
ALTER TABLE apis ADD COLUMN path VARCHAR(500) COMMENT '接口路径';

-- 添加参数列表字段
ALTER TABLE apis ADD COLUMN parameters JSON COMMENT '参数列表';

-- 添加响应定义字段
ALTER TABLE apis ADD COLUMN responses JSON COMMENT '响应定义';

-- 添加标签字段
ALTER TABLE apis ADD COLUMN tags JSON COMMENT '标签';

-- 添加安全配置字段
ALTER TABLE apis ADD COLUMN security JSON COMMENT '安全配置';

-- 添加备注字段
ALTER TABLE apis ADD COLUMN notes TEXT COMMENT '备注';

-- 添加项目ID字段
ALTER TABLE apis ADD COLUMN project_id INT COMMENT '项目ID';

-- 添加外键约束
ALTER TABLE apis ADD CONSTRAINT fk_apis_project_id 
FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE;

-- 修改url字段为可空（兼容性）
ALTER TABLE apis MODIFY COLUMN url VARCHAR(500) COMMENT '接口URL';

-- 为新字段添加索引
CREATE INDEX idx_apis_project_id ON apis(project_id);
CREATE INDEX idx_apis_path ON apis(path);

-- 更新现有数据，将url字段复制到path字段
UPDATE apis SET path = url WHERE path IS NULL AND url IS NOT NULL; 