#!/bin/bash
# 预览自定义登录页面

echo "=========================================="
echo "Filebrowser 登录页面预览"
echo "=========================================="
echo ""

cd frontend/public

echo "启动HTTP服务器..."
echo ""
echo "访问地址: http://localhost:8080/custom-login.html"
echo ""
echo "按 Ctrl+C 停止服务器"
echo ""
echo "=========================================="

python3 -m http.server 8080
