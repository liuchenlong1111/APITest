#!/bin/bash

echo "🚀 启动API测试平台..."

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose未安装，请先安装Docker Compose"
    exit 1
fi

# 创建环境变量文件
if [ ! -f "backend/.env" ]; then
    echo "📝 创建后端环境变量文件..."
    cp backend/env.example backend/.env
fi

# 构建并启动服务
echo "🔨 构建并启动服务..."
docker-compose up --build -d

# 等待服务启动
echo "⏳ 等待服务启动..."
sleep 30

# 检查服务状态
echo "🔍 检查服务状态..."
docker-compose ps

echo ""
echo "✅ 服务启动完成！"
echo ""
echo "📱 前端地址: http://localhost"
echo "🔧 后端API: http://localhost:8000"
echo "📚 API文档: http://localhost:8000/docs"
echo "🗄️  MySQL: localhost:3306"
echo "🔴 Redis: localhost:6379"
echo ""
echo "默认管理员账号:"
echo "用户名: admin"
echo "密码: admin123"
echo ""
echo "使用 'docker-compose logs -f' 查看日志"
echo "使用 'docker-compose down' 停止服务" 