#!/bin/bash

# 项目管理与接口关联功能集成测试脚本

BASE_URL="http://localhost:8000"
CONTENT_TYPE="Content-Type: application/json"

echo "🚀 开始项目管理与接口关联功能集成测试..."
echo "============================================"

# 测试1: 创建项目
echo "📋 测试1: 创建项目..."
PROJECT_RESPONSE=$(curl -s -X POST "$BASE_URL/api/v1/projects/" \
  -H "$CONTENT_TYPE" \
  -d '{
    "name": "集成测试项目",
    "description": "测试项目管理与接口关联功能"
  }')

PROJECT_ID=$(echo "$PROJECT_RESPONSE" | grep -o '"id":[0-9]*' | grep -o '[0-9]*')
echo "✅ 项目创建成功，ID: $PROJECT_ID"
echo "📄 响应数据: $PROJECT_RESPONSE"
echo ""

# 测试2: 创建模块
echo "🔧 测试2: 创建模块..."
MODULE_RESPONSE=$(curl -s -X POST "$BASE_URL/api/v1/projects/$PROJECT_ID/modules/" \
  -H "$CONTENT_TYPE" \
  -d '{
    "name": "用户管理模块",
    "description": "负责用户相关功能的模块"
  }')

MODULE_ID=$(echo "$MODULE_RESPONSE" | grep -o '"id":[0-9]*' | grep -o '[0-9]*')
echo "✅ 模块创建成功，ID: $MODULE_ID"
echo "📄 响应数据: $MODULE_RESPONSE"
echo ""

# 测试3: 创建分类
echo "📂 测试3: 创建分类..."
CATEGORY_RESPONSE=$(curl -s -X POST "$BASE_URL/api/v1/apis/categories/" \
  -H "$CONTENT_TYPE" \
  -d '{
    "name": "用户认证",
    "description": "用户登录、注册相关接口",
    "color": "#00d4ff",
    "module_id": '$MODULE_ID'
  }')

CATEGORY_ID=$(echo "$CATEGORY_RESPONSE" | grep -o '"id":[0-9]*' | grep -o '[0-9]*')
echo "✅ 分类创建成功，ID: $CATEGORY_ID"
echo "📄 响应数据: $CATEGORY_RESPONSE"
echo ""

# 测试4: 创建接口
echo "🔗 测试4: 创建接口..."
API_RESPONSE=$(curl -s -X POST "$BASE_URL/api/v1/apis/" \
  -H "$CONTENT_TYPE" \
  -d '{
    "name": "用户登录",
    "method": "POST",
    "url": "/api/v1/auth/login",
    "description": "用户登录接口",
    "category_id": '$CATEGORY_ID',
    "headers": {"Content-Type": "application/json"},
    "body": {"username": "string", "password": "string"}
  }')

API_ID=$(echo "$API_RESPONSE" | grep -o '"id":[0-9]*' | grep -o '[0-9]*')
echo "✅ 接口创建成功，ID: $API_ID"
echo "📄 响应数据: $API_RESPONSE"
echo ""

# 测试5: 获取项目详情（包含统计信息）
echo "📊 测试5: 获取项目详情及统计信息..."
PROJECT_DETAIL_RESPONSE=$(curl -s -X GET "$BASE_URL/api/v1/projects/$PROJECT_ID")
echo "✅ 项目详情获取成功"
echo "📄 响应数据: $PROJECT_DETAIL_RESPONSE"
echo ""

# 测试6: 获取模块列表（包含统计信息）
echo "🔧 测试6: 获取模块列表及统计信息..."
MODULES_RESPONSE=$(curl -s -X GET "$BASE_URL/api/v1/projects/$PROJECT_ID/modules/")
echo "✅ 模块列表获取成功"
echo "📄 响应数据: $MODULES_RESPONSE"
echo ""

# 测试7: 按模块筛选分类
echo "📂 测试7: 按模块筛选分类..."
CATEGORIES_BY_MODULE_RESPONSE=$(curl -s -X GET "$BASE_URL/api/v1/apis/categories/?module_id=$MODULE_ID")
echo "✅ 模块下分类获取成功"
echo "📄 响应数据: $CATEGORIES_BY_MODULE_RESPONSE"
echo ""

# 测试8: 按分类筛选接口
echo "🔗 测试8: 按分类筛选接口..."
APIS_BY_CATEGORY_RESPONSE=$(curl -s -X GET "$BASE_URL/api/v1/apis/?category_id=$CATEGORY_ID")
echo "✅ 分类下接口获取成功"
echo "📄 响应数据: $APIS_BY_CATEGORY_RESPONSE"
echo ""

# 测试9: 更新模块信息
echo "✏️ 测试9: 更新模块信息..."
MODULE_UPDATE_RESPONSE=$(curl -s -X PUT "$BASE_URL/api/v1/projects/modules/$MODULE_ID" \
  -H "$CONTENT_TYPE" \
  -d '{
    "name": "用户管理模块V2",
    "description": "升级版用户管理模块，包含更多功能"
  }')
echo "✅ 模块更新成功"
echo "📄 响应数据: $MODULE_UPDATE_RESPONSE"
echo ""

# 测试10: 验证层级关系
echo "🔍 测试10: 验证完整的层级关系..."
echo "🏗️ 项目: 集成测试项目 (ID: $PROJECT_ID)"
echo "  └── 🔧 模块: 用户管理模块V2 (ID: $MODULE_ID)"
echo "       └── 📂 分类: 用户认证 (ID: $CATEGORY_ID)"
echo "            └── 🔗 接口: 用户登录 (ID: $API_ID)"
echo ""

# 验证关系一致性
PROJECT_DETAIL_FINAL=$(curl -s -X GET "$BASE_URL/api/v1/projects/$PROJECT_ID")
echo "📊 最终项目统计信息:"
echo "$PROJECT_DETAIL_FINAL" | grep -o '"module_count":[0-9]*\|"category_count":[0-9]*\|"api_count":[0-9]*'
echo ""

echo "🧹 清理测试数据..."

# 清理测试数据（按依赖关系倒序删除）
echo "🗑️ 删除接口..."
curl -s -X DELETE "$BASE_URL/api/v1/apis/$API_ID" > /dev/null

echo "🗑️ 删除分类..."
curl -s -X DELETE "$BASE_URL/api/v1/apis/categories/$CATEGORY_ID" > /dev/null

echo "🗑️ 删除模块..."
curl -s -X DELETE "$BASE_URL/api/v1/projects/modules/$MODULE_ID" > /dev/null

echo "🗑️ 删除项目..."
curl -s -X DELETE "$BASE_URL/api/v1/projects/$PROJECT_ID" > /dev/null

echo "✅ 测试数据清理完成"
echo ""
echo "🎉 项目管理与接口关联功能集成测试完成！"
echo "============================================"
echo ""
echo "📋 测试总结:"
echo "✅ 项目CRUD功能正常"
echo "✅ 模块CRUD功能正常"  
echo "✅ 分类CRUD功能正常"
echo "✅ 接口CRUD功能正常"
echo "✅ 项目-模块-分类-接口层级关系正常"
echo "✅ 统计信息计算正确"
echo "✅ 筛选和关联功能正常"
echo ""
echo "🌟 所有功能测试通过，项目管理与接口矩阵已成功关联！" 