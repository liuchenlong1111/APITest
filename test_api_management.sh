#!/bin/bash

# API管理功能测试脚本
# 使用curl测试接口分类和接口的增删改查功能

BASE_URL="http://localhost:8000"

echo "🚀 开始测试API管理功能..."

# 1. 测试获取分类列表
echo -e "\n1. 测试获取分类列表"
response=$(curl -s "$BASE_URL/api/v1/apis/categories/")
if [[ $? -eq 0 ]]; then
    count=$(echo "$response" | jq length)
    echo "✅ 获取分类列表成功，共 $count 个分类"
else
    echo "❌ 获取分类列表失败"
    exit 1
fi

# 2. 测试创建分类
echo -e "\n2. 测试创建分类"
new_category='{"name": "Shell测试分类", "description": "这是一个Shell脚本创建的分类", "color": "#42b883", "module_id": 1}'
response=$(curl -s -X POST "$BASE_URL/api/v1/apis/categories/" \
    -H "Content-Type: application/json" \
    -d "$new_category")

if [[ $? -eq 0 ]]; then
    category_id=$(echo "$response" | jq -r '.id')
    echo "✅ 创建分类成功，ID: $category_id"
else
    echo "❌ 创建分类失败"
    exit 1
fi

# 3. 测试获取接口列表
echo -e "\n3. 测试获取接口列表"
response=$(curl -s "$BASE_URL/api/v1/apis/")
if [[ $? -eq 0 ]]; then
    count=$(echo "$response" | jq length)
    echo "✅ 获取接口列表成功，共 $count 个接口"
else
    echo "❌ 获取接口列表失败"
    exit 1
fi

# 4. 测试创建接口
echo -e "\n4. 测试创建接口"
new_api="{\"name\": \"Shell测试接口\", \"method\": \"POST\", \"url\": \"/api/v1/test/shell\", \"description\": \"这是一个Shell脚本创建的接口\", \"category_id\": $category_id}"
response=$(curl -s -X POST "$BASE_URL/api/v1/apis/" \
    -H "Content-Type: application/json" \
    -d "$new_api")

if [[ $? -eq 0 ]]; then
    api_id=$(echo "$response" | jq -r '.id')
    echo "✅ 创建接口成功，ID: $api_id"
else
    echo "❌ 创建接口失败"
    exit 1
fi

# 5. 测试获取接口详情
echo -e "\n5. 测试获取接口详情"
response=$(curl -s "$BASE_URL/api/v1/apis/$api_id")
if [[ $? -eq 0 ]]; then
    name=$(echo "$response" | jq -r '.name')
    method=$(echo "$response" | jq -r '.method')
    url=$(echo "$response" | jq -r '.url')
    category_name=$(echo "$response" | jq -r '.category.name')
    echo "✅ 获取接口详情成功"
    echo "   - 名称: $name"
    echo "   - 方法: $method"
    echo "   - URL: $url"
    echo "   - 分类: $category_name"
else
    echo "❌ 获取接口详情失败"
    exit 1
fi

# 6. 测试更新接口
echo -e "\n6. 测试更新接口"
update_data='{"description": "这是一个更新后的Shell测试接口", "method": "PUT"}'
response=$(curl -s -X PUT "$BASE_URL/api/v1/apis/$api_id" \
    -H "Content-Type: application/json" \
    -d "$update_data")

if [[ $? -eq 0 ]]; then
    new_description=$(echo "$response" | jq -r '.description')
    new_method=$(echo "$response" | jq -r '.method')
    echo "✅ 更新接口成功"
    echo "   - 新描述: $new_description"
    echo "   - 新方法: $new_method"
else
    echo "❌ 更新接口失败"
    exit 1
fi

# 7. 测试搜索接口
echo -e "\n7. 测试搜索接口"
response=$(curl -s "$BASE_URL/api/v1/apis/?keyword=Shell")
if [[ $? -eq 0 ]]; then
    count=$(echo "$response" | jq length)
    echo "✅ 搜索接口成功，找到 $count 个结果"
else
    echo "❌ 搜索接口失败"
    exit 1
fi

# 8. 测试按分类筛选接口
echo -e "\n8. 测试按分类筛选接口"
response=$(curl -s "$BASE_URL/api/v1/apis/?category_id=$category_id")
if [[ $? -eq 0 ]]; then
    count=$(echo "$response" | jq length)
    echo "✅ 按分类筛选成功，找到 $count 个接口"
else
    echo "❌ 按分类筛选失败"
    exit 1
fi

# 9. 测试更新分类
echo -e "\n9. 测试更新分类"
update_category='{"description": "这是一个更新后的Shell测试分类", "color": "#ff6b6b"}'
response=$(curl -s -X PUT "$BASE_URL/api/v1/apis/categories/$category_id" \
    -H "Content-Type: application/json" \
    -d "$update_category")

if [[ $? -eq 0 ]]; then
    new_description=$(echo "$response" | jq -r '.description')
    new_color=$(echo "$response" | jq -r '.color')
    echo "✅ 更新分类成功"
    echo "   - 新描述: $new_description"
    echo "   - 新颜色: $new_color"
else
    echo "❌ 更新分类失败"
    exit 1
fi

# 10. 清理测试数据 - 删除接口
echo -e "\n10. 清理测试数据 - 删除接口"
response=$(curl -s -X DELETE "$BASE_URL/api/v1/apis/$api_id")
if [[ $? -eq 0 ]]; then
    echo "✅ 删除接口成功"
else
    echo "❌ 删除接口失败"
    exit 1
fi

# 11. 清理测试数据 - 删除分类
echo -e "\n11. 清理测试数据 - 删除分类"
response=$(curl -s -X DELETE "$BASE_URL/api/v1/apis/categories/$category_id")
if [[ $? -eq 0 ]]; then
    echo "✅ 删除分类成功"
else
    echo "❌ 删除分类失败"
    exit 1
fi

echo -e "\n🎉 所有测试通过！API管理功能正常工作。"

# 测试错误情况
echo -e "\n🔍 测试错误情况..."

# 测试创建重复名称的分类
echo -e "\n1. 测试创建重复名称的分类"
duplicate_category='{"name": "认证接口", "description": "重复的分类", "module_id": 1}'
response=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/api/v1/apis/categories/" \
    -H "Content-Type: application/json" \
    -d "$duplicate_category")

http_code=$(echo "$response" | tail -n1)
if [[ "$http_code" == "400" ]]; then
    echo "✅ 正确拒绝了重复的分类名称"
else
    echo "❌ 应该拒绝重复的分类名称，但返回了: $http_code"
fi

# 测试获取不存在的接口
echo -e "\n2. 测试获取不存在的接口"
response=$(curl -s -w "\n%{http_code}" "$BASE_URL/api/v1/apis/99999")
http_code=$(echo "$response" | tail -n1)
if [[ "$http_code" == "404" ]]; then
    echo "✅ 正确返回了404错误"
else
    echo "❌ 应该返回404错误，但返回了: $http_code"
fi

# 测试删除不存在的分类
echo -e "\n3. 测试删除不存在的分类"
response=$(curl -s -w "\n%{http_code}" -X DELETE "$BASE_URL/api/v1/apis/categories/99999")
http_code=$(echo "$response" | tail -n1)
if [[ "$http_code" == "404" ]]; then
    echo "✅ 正确返回了404错误"
else
    echo "❌ 应该返回404错误，但返回了: $http_code"
fi

echo -e "\n✨ 所有测试完成！" 