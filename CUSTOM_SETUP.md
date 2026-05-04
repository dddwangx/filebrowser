# Filebrowser 定制化部署指南

## 功能特性

### 1. 用户管理系统
- ✅ 自动生成1个管理员账户
- ✅ 自动生成20个随机用户账户
- ✅ 随机生成安全密码
- ✅ 凭据保存到配置文件

### 2. 动态Logo轮播
- ✅ 15张自然风景和动物特写图片
- ✅ 每5秒自动切换
- ✅ 平滑淡入淡出动画
- ✅ 圆形边框 + 彩色渐变边框

### 3. 登录页面美化
- ✅ 彩色渐变背景（紫蓝粉渐变）
- ✅ 呼吸动画效果
- ✅ 字体加粗 + 彩色渐变文字
- ✅ 毛玻璃效果登录框
- ✅ 响应式设计

## 快速开始

### 方式一：一键部署（推荐）

```bash
# 1. 进入项目目录
cd /root/vps/game/filebrowser

# 2. 给脚本添加执行权限
chmod +x scripts/setup_filebrowser.sh

# 3. 运行部署脚本
./scripts/setup_filebrowser.sh
```

### 方式二：手动部署

#### 步骤1: 生成用户凭据

```bash
python3 scripts/generate_users.py
```

生成的文件：
- `config/user_credentials.json` - 完整用户信息（含密码）
- `config/login_credentials.txt` - 登录凭据列表（易读格式）

#### 步骤2: 下载Logo图片

```bash
# 安装依赖
pip3 install requests pillow

# 下载图片
python3 scripts/download_images_improved.py
```

图片保存位置：`frontend/public/logos/`

#### 步骤3: 启动服务

```bash
# 启动Docker容器
docker-compose up -d

# 查看运行状态
docker-compose ps

# 查看日志
docker-compose logs -f
```

## 访问应用

- **访问地址**: http://localhost:8000/filebrowser
- **管理员账户**: 查看 `config/login_credentials.txt` 文件的第一个账户

```bash
# 查看管理员凭据
cat config/login_credentials.txt | head -n 10
```

## 目录结构

```
/root/vps/game/filebrowser/
├── scripts/
│   ├── generate_users.py              # 用户生成脚本
│   ├── download_images_improved.py    # 图片下载脚本
│   └── setup_filebrowser.sh           # 一键部署脚本
├── frontend/
│   └── public/
│       ├── custom-login.html          # 自定义登录页面
│       └── logos/                     # Logo图片目录
│           ├── logo_01.jpg
│           ├── logo_02.jpg
│           └── ...
├── config/
│   ├── user_credentials.json          # 用户凭据（JSON）
│   └── login_credentials.txt          # 登录信息（文本）
├── data/                              # 文件存储目录
├── database/                          # 数据库目录
└── docker-compose.yml                 # Docker配置

```

## 配置说明

### Docker Compose 配置

```yaml
version: '3'
services:
  filebrowser:
    image: filebrowser/filebrowser:latest
    container_name: filebrowser
    restart: unless-stopped
    ports:
      - "8000:80"
    volumes:
      - ./data:/srv
      - ./config:/config
      - ./database:/database
    environment:
      - FB_BASEURL=/filebrowser
```

### 自定义登录页面特性

#### 背景动画
- 5色渐变：紫蓝 → 深紫 → 粉紫 → 天蓝 → 青色
- 15秒完整渐变循环
- 8秒呼吸动画（透明度 + 缩放）

#### Logo轮播
- 15张图片循环播放
- 5秒切换间隔
- 淡入淡出过渡效果
- 圆形裁剪 + 彩色边框

#### 文字样式
- 标题：900字重 + 彩色渐变
- 标签：700字重 + 彩色渐变
- 按钮：800字重 + 大写 + 字母间距

## 常用命令

### 服务管理

```bash
# 启动服务
docker-compose up -d

# 停止服务
docker-compose down

# 重启服务
docker-compose restart

# 查看日志
docker-compose logs -f

# 查看状态
docker-compose ps
```

### 用户管理

```bash
# 重新生成用户
python3 scripts/generate_users.py

# 查看所有用户凭据
cat config/login_credentials.txt

# 查看管理员凭据
cat config/login_credentials.txt | head -n 10

# 查看用户数量
cat config/user_credentials.json | grep '"username"' | wc -l
```

### 图片管理

```bash
# 重新下载图片
python3 scripts/download_images_improved.py

# 查看图片列表
ls -lh frontend/public/logos/

# 查看图片清单
cat frontend/public/logos/manifest.json
```

## 自定义配置

### 修改用户数量

编辑 `scripts/generate_users.py`：

```python
# 修改这一行的数字
users = generate_users(20)  # 改为你想要的数量
```

### 修改Logo切换时间

编辑 `frontend/public/custom-login.html`：

```javascript
// 修改这一行的毫秒数（5000 = 5秒）
setInterval(changeLogo, 5000);
```

### 修改背景渐变颜色

编辑 `frontend/public/custom-login.html` 的CSS部分：

```css
.animated-background {
    background: linear-gradient(135deg, 
        #667eea 0%,    /* 改为你的颜色 */
        #764ba2 25%,   /* 改为你的颜色 */
        #f093fb 50%,   /* 改为你的颜色 */
        #4facfe 75%,   /* 改为你的颜色 */
        #00f2fe 100%   /* 改为你的颜色 */
    );
}
```

### 修改动画速度

```css
/* 渐变移动速度 */
animation: gradientShift 15s ease infinite;  /* 改为你想要的秒数 */

/* 呼吸动画速度 */
animation: breathe 8s ease-in-out infinite;  /* 改为你想要的秒数 */
```

## 图片来源

Logo图片通过以下方式获取：

1. **Unsplash Source API** (主要)
   - 免费、高质量
   - 无需API密钥
   - 随机自然风景和动物图片

2. **Picsum Photos** (备选)
   - 免费占位图服务
   - 稳定可靠

3. **本地生成** (最后备选)
   - 使用PIL生成彩色渐变占位图
   - 确保始终有可用图片

## 故障排除

### 问题1: 图片无法下载

```bash
# 检查网络连接
ping source.unsplash.com

# 手动安装依赖
pip3 install requests pillow

# 使用备选脚本
python3 scripts/download_images_improved.py
```

### 问题2: Docker容器无法启动

```bash
# 检查端口占用
ss -lntp | grep 8000

# 查看详细日志
docker-compose logs

# 重新构建
docker-compose down
docker-compose up -d --force-recreate
```

### 问题3: 无法访问登录页面

```bash
# 检查容器状态
docker-compose ps

# 检查文件权限
ls -la frontend/public/custom-login.html

# 检查Nginx配置（如果使用）
nginx -t
```

### 问题4: Logo不显示

```bash
# 检查图片文件
ls -lh frontend/public/logos/

# 检查图片数量
ls frontend/public/logos/*.jpg | wc -l

# 重新下载
python3 scripts/download_images_improved.py
```

## 安全建议

1. **修改默认密码**
   - 首次登录后立即修改管理员密码
   - 定期更新用户密码

2. **限制访问**
   - 使用防火墙限制访问IP
   - 配置Nginx反向代理
   - 启用HTTPS

3. **备份数据**
   ```bash
   # 备份数据库
   cp -r database database.backup
   
   # 备份配置
   cp -r config config.backup
   ```

4. **日志监控**
   ```bash
   # 定期查看日志
   docker-compose logs --tail=100
   ```

## 性能优化

1. **图片优化**
   - 压缩Logo图片大小
   - 使用WebP格式（如果浏览器支持）

2. **缓存配置**
   - 配置浏览器缓存
   - 使用CDN加速静态资源

3. **数据库优化**
   - 定期清理旧数据
   - 优化数据库索引

## 更新日志

- **2026-05-02**: 初始版本
  - 用户管理系统
  - Logo轮播功能
  - 登录页面美化
  - 一键部署脚本

## 技术栈

- **后端**: Filebrowser (Go)
- **前端**: HTML5 + CSS3 + JavaScript
- **容器**: Docker + Docker Compose
- **脚本**: Python 3
- **图片源**: Unsplash API

## 许可证

本定制化方案基于Filebrowser开源项目，遵循Apache 2.0许可证。

## 支持

如有问题，请查看：
- Filebrowser官方文档: https://filebrowser.org/
- GitHub Issues: https://github.com/filebrowser/filebrowser/issues

---

**享受你的定制化Filebrowser体验！** 🎨✨
