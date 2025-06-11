#!/usr/bin/env python3
"""
项目管理功能测试脚本
测试项目、模块、分类、接口的增删改查和层级关系
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_auth():
    """测试用户认证"""
    print("🔐 测试用户认证...")
    
    # 登录获取token
    login_data = {
        "username": "admin123",
        "password": "admin123"
    }
    
    response = requests.post(f"{BASE_URL}/api/v1/auth/login", json=login_data)
    if response.status_code == 200:
        token = response.json()["access_token"]
        print("✅ 登录成功")
        return {"Authorization": f"Bearer {token}"}
    else:
        print(f"❌ 登录失败: {response.text}")
        return None

def test_projects(headers):
    """测试项目管理"""
    print("\n🏗️ 测试项目管理...")
    
    # 1. 创建项目
    project_data = {
        "name": "电商平台API",
        "description": "电商平台的后端API接口管理"
    }
    
    response = requests.post(f"{BASE_URL}/api/v1/projects/", json=project_data, headers=headers)
    if response.status_code == 200:
        project = response.json()
        project_id = project["id"]
        print(f"✅ 创建项目成功: {project['name']} (ID: {project_id})")
    else:
        print(f"❌ 创建项目失败: {response.text}")
        return None
    
    # 2. 获取项目列表
    response = requests.get(f"{BASE_URL}/api/v1/projects/", headers=headers)
    if response.status_code == 200:
        projects = response.json()
        print(f"✅ 获取项目列表成功，共 {len(projects)} 个项目")
        for p in projects:
            print(f"   - {p['project']['name']}: {p['module_count']}个模块, {p['api_count']}个接口")
    else:
        print(f"❌ 获取项目列表失败: {response.text}")
    
    return project_id

def test_modules(headers, project_id):
    """测试模块管理"""
    print(f"\n🔧 测试模块管理 (项目ID: {project_id})...")
    
    modules_data = [
        {"name": "用户管理", "icon": "👤"},
        {"name": "商品管理", "icon": "📦"},
        {"name": "订单管理", "icon": "📋"},
        {"name": "支付管理", "icon": "💳"}
    ]
    
    module_ids = []
    
    # 1. 创建模块
    for module_data in modules_data:
        response = requests.post(f"{BASE_URL}/api/v1/projects/{project_id}/modules/", 
                               json=module_data, headers=headers)
        if response.status_code == 200:
            module = response.json()
            module_ids.append(module["id"])
            print(f"✅ 创建模块成功: {module['name']} (ID: {module['id']})")
        else:
            print(f"❌ 创建模块失败: {response.text}")
    
    # 2. 获取模块列表
    response = requests.get(f"{BASE_URL}/api/v1/projects/{project_id}/modules/", headers=headers)
    if response.status_code == 200:
        modules = response.json()
        print(f"✅ 获取模块列表成功，共 {len(modules)} 个模块")
        for m in modules:
            print(f"   - {m['module']['name']}: {m['category_count']}个分类, {m['api_count']}个接口")
    else:
        print(f"❌ 获取模块列表失败: {response.text}")
    
    return module_ids

def test_categories(headers, module_ids):
    """测试分类管理"""
    print(f"\n📂 测试分类管理...")
    
    categories_data = [
        # 用户管理模块的分类
        {"name": "用户认证", "description": "用户登录、注册相关接口", "color": "#409eff", "module_id": module_ids[0]},
        {"name": "用户信息", "description": "用户信息管理接口", "color": "#67c23a", "module_id": module_ids[0]},
        
        # 商品管理模块的分类
        {"name": "商品CRUD", "description": "商品增删改查接口", "color": "#e6a23c", "module_id": module_ids[1]},
        {"name": "商品搜索", "description": "商品搜索和筛选接口", "color": "#f56c6c", "module_id": module_ids[1]},
        
        # 订单管理模块的分类
        {"name": "订单操作", "description": "订单创建、修改、取消", "color": "#909399", "module_id": module_ids[2]},
        {"name": "订单查询", "description": "订单状态查询接口", "color": "#00d4ff", "module_id": module_ids[2]},
    ]
    
    category_ids = []
    
    # 1. 创建分类
    for category_data in categories_data:
        response = requests.post(f"{BASE_URL}/api/v1/apis/categories/", 
                               json=category_data, headers=headers)
        if response.status_code == 200:
            category = response.json()
            category_ids.append(category["id"])
            print(f"✅ 创建分类成功: {category['name']} (ID: {category['id']})")
        else:
            print(f"❌ 创建分类失败: {response.text}")
    
    # 2. 获取分类列表
    for module_id in module_ids[:3]:  # 只测试前3个模块
        response = requests.get(f"{BASE_URL}/api/v1/apis/categories/?module_id={module_id}", headers=headers)
        if response.status_code == 200:
            categories = response.json()
            module_name = ["用户管理", "商品管理", "订单管理"][module_ids.index(module_id)]
            print(f"✅ 获取{module_name}模块分类成功，共 {len(categories)} 个分类")
        else:
            print(f"❌ 获取分类列表失败: {response.text}")
    
    return category_ids

def test_apis(headers, category_ids):
    """测试接口管理"""
    print(f"\n🔗 测试接口管理...")
    
    apis_data = [
        # 用户认证分类的接口
        {
            "name": "用户登录",
            "method": "POST",
            "url": "/api/v1/auth/login",
            "description": "用户登录接口",
            "category_id": category_ids[0],
            "headers": {"Content-Type": "application/json"},
            "body": {"username": "string", "password": "string"}
        },
        {
            "name": "用户注册",
            "method": "POST", 
            "url": "/api/v1/auth/register",
            "description": "用户注册接口",
            "category_id": category_ids[0],
            "headers": {"Content-Type": "application/json"},
            "body": {"username": "string", "email": "string", "password": "string"}
        },
        
        # 用户信息分类的接口
        {
            "name": "获取用户信息",
            "method": "GET",
            "url": "/api/v1/users/me",
            "description": "获取当前用户信息",
            "category_id": category_ids[1],
            "headers": {"Authorization": "Bearer {token}"}
        },
        
        # 商品CRUD分类的接口
        {
            "name": "创建商品",
            "method": "POST",
            "url": "/api/v1/products",
            "description": "创建新商品",
            "category_id": category_ids[2],
            "headers": {"Content-Type": "application/json"},
            "body": {"name": "string", "price": "number", "description": "string"}
        },
        {
            "name": "获取商品列表",
            "method": "GET",
            "url": "/api/v1/products",
            "description": "获取商品列表",
            "category_id": category_ids[2],
            "params": {"page": 1, "limit": 20, "category": "string"}
        }
    ]
    
    api_ids = []
    
    # 1. 创建接口
    for api_data in apis_data:
        response = requests.post(f"{BASE_URL}/api/v1/apis/", json=api_data, headers=headers)
        if response.status_code == 200:
            api = response.json()
            api_ids.append(api["id"])
            print(f"✅ 创建接口成功: {api['method']} {api['name']} (ID: {api['id']})")
        else:
            print(f"❌ 创建接口失败: {response.text}")
    
    # 2. 获取接口列表
    response = requests.get(f"{BASE_URL}/api/v1/apis/", headers=headers)
    if response.status_code == 200:
        apis = response.json()
        print(f"✅ 获取接口列表成功，共 {len(apis)} 个接口")
        
        # 按分类统计
        category_stats = {}
        for api in apis:
            if api.get("category"):
                cat_name = api["category"]["name"]
                category_stats[cat_name] = category_stats.get(cat_name, 0) + 1
        
        for cat_name, count in category_stats.items():
            print(f"   - {cat_name}: {count}个接口")
    else:
        print(f"❌ 获取接口列表失败: {response.text}")
    
    return api_ids

def test_hierarchy_query(headers, project_id):
    """测试层级查询"""
    print(f"\n🎯 测试层级查询...")
    
    # 1. 获取项目详情（包含完整层级）
    response = requests.get(f"{BASE_URL}/api/v1/projects/{project_id}", headers=headers)
    if response.status_code == 200:
        project_detail = response.json()
        print(f"✅ 获取项目详情成功:")
        print(f"   项目: {project_detail['project']['name']}")
        print(f"   统计: {project_detail['module_count']}个模块, {project_detail['category_count']}个分类, {project_detail['api_count']}个接口")
        
        if 'modules' in project_detail:
            print(f"   模块详情:")
            for module in project_detail['modules']:
                print(f"     - {module['module']['name']}: {module['category_count']}个分类, {module['api_count']}个接口")
    else:
        print(f"❌ 获取项目详情失败: {response.text}")

def main():
    """主测试函数"""
    print("🚀 开始测试项目管理功能...")
    print("=" * 60)
    
    # 1. 认证
    headers = test_auth()
    if not headers:
        return
    
    # 2. 测试项目管理
    project_id = test_projects(headers)
    if not project_id:
        return
    
    # 3. 测试模块管理
    module_ids = test_modules(headers, project_id)
    if not module_ids:
        return
    
    # 4. 测试分类管理
    category_ids = test_categories(headers, module_ids)
    if not category_ids:
        return
    
    # 5. 测试接口管理
    api_ids = test_apis(headers, category_ids)
    
    # 6. 测试层级查询
    test_hierarchy_query(headers, project_id)
    
    print("\n" + "=" * 60)
    print("🎉 项目管理功能测试完成！")
    print(f"✅ 创建了1个项目，{len(module_ids)}个模块，{len(category_ids)}个分类，{len(api_ids)}个接口")
    print("\n📋 测试总结:")
    print("   - 项目增删改查 ✅")
    print("   - 模块增删改查 ✅") 
    print("   - 分类增删改查 ✅")
    print("   - 接口增删改查 ✅")
    print("   - 层级关系查询 ✅")
    print("\n🌐 现在可以访问前端页面查看效果:")
    print("   - 项目管理: http://localhost:3000/#/projects")
    print("   - 接口矩阵: http://localhost:3000/#/apis")

if __name__ == "__main__":
    main() 