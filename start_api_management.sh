#!/bin/bash

echo "🚀 启动API管理功能演示"
echo "================================"

# 检查端口是否被占用
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null ; then
        echo "⚠️  端口 $1 被占用"
        return 1
    else
        echo "✅ 端口 $1 可用"
        return 0
    fi
}

echo "检查端口状态..."
check_port 8000
BACKEND_PORT_FREE=$?
check_port 3000
FRONTEND_PORT_FREE=$?

echo ""
echo "启动后端服务..."
cd backend

# 检查Python环境
if ! command -v python &> /dev/null; then
    echo "❌ Python未安装"
    exit 1
fi

# 启动后端
if [ $BACKEND_PORT_FREE -eq 0 ]; then
    echo "🔥 启动后端服务在端口8000..."
    python -m app.main &
    BACKEND_PID=$!
    echo "后端进程ID: $BACKEND_PID"
else
    echo "⚠️  后端端口8000被占用，请先关闭占用进程"
fi

sleep 3

echo ""
echo "启动前端服务..."
cd ../frontend

# 检查npm
if ! command -v npm &> /dev/null; then
    echo "❌ npm未安装"
    exit 1
fi

# 安装依赖（如果需要）
if [ ! -d "node_modules" ]; then
    echo "📦 安装前端依赖..."
    npm install
fi

# 启动前端
if [ $FRONTEND_PORT_FREE -eq 0 ]; then
    echo "🔥 启动前端服务在端口3000..."
    npm run dev &
    FRONTEND_PID=$!
    echo "前端进程ID: $FRONTEND_PID"
else
    echo "⚠️  前端端口3000被占用，请先关闭占用进程"
fi

echo ""
echo "🎉 服务启动完成！"
echo "================================"
echo "📱 前端页面: http://localhost:3000/#/apis"
echo "📚 API文档: http://localhost:8000/docs"
echo "🧪 测试页面: 打开项目根目录的 api_test_standalone.html"
echo ""
echo "⚠️  注意：如果页面显示空白，请："
echo "1. 确保后端服务正常启动（访问 http://localhost:8000/docs）"
echo "2. 检查浏览器控制台错误信息"
echo "3. 使用独立测试页面 api_test_standalone.html"
echo ""
echo "按 Ctrl+C 停止所有服务"

# 等待用户中断
wait

# 清理进程
echo ""
echo "🛑 停止服务..."
if [ ! -z "$BACKEND_PID" ]; then
    kill $BACKEND_PID 2>/dev/null
    echo "✅ 后端服务已停止"
fi
if [ ! -z "$FRONTEND_PID" ]; then
    kill $FRONTEND_PID 2>/dev/null
    echo "✅ 前端服务已停止"
fi

echo "👋 再见！" 