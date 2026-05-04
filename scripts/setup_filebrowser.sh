#!/bin/bash
# Filebrowser完整部署脚本

set -e

echo "=========================================="
echo "Filebrowser 定制化部署脚本"
echo "=========================================="
echo ""

# 颜色定义
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 1. 创建必要的目录
echo -e "${BLUE}[1/6] 创建目录结构...${NC}"
mkdir -p config
mkdir -p data/users
mkdir -p database
mkdir -p frontend/public/logos
mkdir -p scripts

echo -e "${GREEN}✓ 目录创建完成${NC}"
echo ""

# 2. 生成用户凭据
echo -e "${BLUE}[2/6] 生成用户凭据...${NC}"
if [ -f "scripts/generate_users.py" ]; then
    python3 scripts/generate_users.py
    echo -e "${GREEN}✓ 用户凭据生成完成${NC}"
else
    echo -e "${YELLOW}⚠ 用户生成脚本不存在，跳过${NC}"
fi
echo ""

# 3. 下载Logo图片
echo -e "${BLUE}[3/6] 下载Logo图片...${NC}"
if [ -f "scripts/download_images.py" ]; then
    # 检查是否已安装requests
    if ! python3 -c "import requests" 2>/dev/null; then
        echo "安装Python依赖..."
        pip3 install requests -q
    fi
    python3 scripts/download_images.py
    echo -e "${GREEN}✓ Logo图片下载完成${NC}"
else
    echo -e "${YELLOW}⚠ 图片下载脚本不存在，创建占位图片${NC}"
    # 创建占位图片（使用ImageMagick或简单的方式）
    for i in {1..15}; do
        touch "frontend/public/logos/logo_$(printf '%02d' $i).jpg"
    done
fi
echo ""

# 4. 设置权限
echo -e "${BLUE}[4/6] 设置目录权限...${NC}"
chmod -R 755 config
chmod -R 755 data
chmod -R 777 database
chmod +x scripts/*.py 2>/dev/null || true
chmod +x scripts/*.sh 2>/dev/null || true
echo -e "${GREEN}✓ 权限设置完成${NC}"
echo ""

# 5. 检查Docker
echo -e "${BLUE}[5/6] 检查Docker环境...${NC}"
if ! command -v docker &> /dev/null; then
    echo -e "${YELLOW}⚠ Docker未安装，请先安装Docker${NC}"
    exit 1
fi

if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo -e "${YELLOW}⚠ Docker Compose未安装，请先安装Docker Compose${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Docker环境检查通过${NC}"
echo ""

# 6. 启动服务
echo -e "${BLUE}[6/6] 启动Filebrowser服务...${NC}"
if [ -f "docker-compose.yml" ]; then
    docker-compose down 2>/dev/null || true
    docker-compose up -d
    echo -e "${GREEN}✓ Filebrowser服务已启动${NC}"
else
    echo -e "${YELLOW}⚠ docker-compose.yml不存在${NC}"
fi
echo ""

# 显示摘要信息
echo "=========================================="
echo -e "${GREEN}部署完成！${NC}"
echo "=========================================="
echo ""
echo "访问地址: http://localhost:8000/filebrowser"
echo ""
echo "管理员凭据已保存在: config/login_credentials.txt"
echo "查看凭据: cat config/login_credentials.txt | head -n 10"
echo ""
echo "查看服务状态: docker-compose ps"
echo "查看日志: docker-compose logs -f"
echo "停止服务: docker-compose down"
echo ""
echo "=========================================="
