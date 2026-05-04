# 🚀 快速启动指南

## 当前状态

✅ **已完成**:
- 用户凭据生成（21个用户）
- Logo图片下载（15张）
- 自定义登录页面
- 所有脚本和文档

## 立即预览登录页面

### 方法1: 使用预览脚本（推荐）

```bash
./scripts/preview_login.sh
```

然后在浏览器中访问: **http://localhost:8080/custom-login.html**

### 方法2: 手动启动

```bash
cd frontend/public
python3 -m http.server 8080
```

访问: http://localhost:8080/custom-login.html

## 查看管理员凭据

```bash
cat config/login_credentials.txt | head -n 10
```

**管理员账户**:
- 用户名: `admin`
- 密码: `oWEz6M6sy7g#*jUC`

## 查看所有用户

```bash
cat config/login_credentials.txt
```

## 查看Logo图片

```bash
ls -lh frontend/public/logos/
```

## 登录页面特性

### 🎨 视觉效果
- ✅ 彩色渐变背景（5色渐变）
- ✅ 呼吸动画（8秒循环）
- ✅ Logo轮播（15张图片，每5秒切换）
- ✅ 毛玻璃登录框
- ✅ 彩色渐变文字（加粗）
- ✅ 悬浮按钮效果

### 🖼️ Logo轮播
- 15张自然风景和动物特写
- 圆形展示 + 彩色边框
- 淡入淡出过渡动画
- 自动循环播放

### 📱 响应式设计
- 适配桌面、平板、手机
- 流畅的动画效果
- 现代化UI设计

## 部署到生产环境

### 安装Docker Compose

```bash
# Debian/Ubuntu
sudo apt-get update
sudo apt-get install docker-compose

# 或使用pip
pip3 install docker-compose
```

### 启动Filebrowser服务

```bash
# 方法1: 使用部署脚本
./scripts/setup_filebrowser.sh

# 方法2: 手动启动
docker-compose up -d

# 方法3: 使用Docker命令
docker run -d \
  --name filebrowser \
  -p 8000:80 \
  -v $(pwd)/data:/srv \
  -v $(pwd)/config:/config \
  -v $(pwd)/database:/database \
  -e FB_BASEURL=/filebrowser \
  filebrowser/filebrowser:latest
```

### 访问应用

- **URL**: http://localhost:8000/filebrowser
- **用户名**: admin
- **密码**: oWEz6M6ys7g#*jUC

## 文件位置

```
项目根目录: /root/vps/game/filebrowser/

重要文件:
├── config/login_credentials.txt       # 所有用户凭据
├── frontend/public/custom-login.html  # 自定义登录页
├── frontend/public/logos/             # 15张Logo图片
├── scripts/preview_login.sh           # 预览脚本
├── QUICK_START.md                     # 本文档
├── CUSTOM_SETUP.md                    # 详细文档
└── DEPLOYMENT_SUMMARY.md              # 完成总结
```

## 常用命令

```bash
# 预览登录页面
./scripts/preview_login.sh

# 查看管理员密码
cat config/login_credentials.txt | head -n 10

# 重新生成用户
python3 scripts/generate_users.py

# 重新下载图片
python3 scripts/download_images_improved.py

# 查看图片列表
ls -lh frontend/public/logos/

# 启动Filebrowser
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

## 自定义配置

### 修改Logo切换时间

编辑 `frontend/public/custom-login.html`，找到:

```javascript
setInterval(changeLogo, 5000); // 改为你想要的毫秒数
```

### 修改背景颜色

编辑 `frontend/public/custom-login.html`，找到:

```css
.animated-background {
    background: linear-gradient(135deg, 
        #667eea 0%,   /* 改为你的颜色 */
        #764ba2 25%, 
        #f093fb 50%, 
        #4facfe 75%, 
        #00f2fe 100%
    );
}
```

### 修改动画速度

```css
/* 渐变移动速度 */
animation: gradientShift 15s ease infinite;

/* 呼吸动画速度 */
animation: breathe 8s ease-in-out infinite;
```

## 故障排除

### 问题: 图片不显示

```bash
# 检查图片是否存在
ls frontend/public/logos/*.jpg

# 重新下载
python3 scripts/download_images_improved.py
```

### 问题: 端口被占用

```bash
# 查看端口占用
ss -lntp | grep 8080

# 使用其他端口
python3 -m http.server 8888
```

### 问题: Docker无法启动

```bash
# 检查Docker状态
systemctl status docker

# 启动Docker
sudo systemctl start docker
```

## 下一步

1. ✅ 预览登录页面效果
2. ⏳ 安装Docker Compose
3. ⏳ 启动Filebrowser服务
4. ⏳ 集成自定义登录页到Filebrowser
5. ⏳ 配置HTTPS和域名

## 技术支持

- 详细文档: `CUSTOM_SETUP.md`
- 完成总结: `DEPLOYMENT_SUMMARY.md`
- Filebrowser官网: https://filebrowser.org/

---

**享受你的定制化Filebrowser！** 🎨✨
