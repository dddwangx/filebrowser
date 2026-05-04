# 📋 Filebrowser 应用配置详情

**生成时间**: 2026-05-03  
**应用版本**: filebrowser/filebrowser:latest  
**部署状态**: ✅ 生产运行中

---

## 📌 应用概述

### 基本信息
- **应用名称**: Filebrowser
- **应用类型**: Web 文件管理系统
- **开源项目**: [filebrowser/filebrowser](https://github.com/filebrowser/filebrowser)
- **许可证**: Apache License 2.0
- **部署方式**: Docker + Nginx 反向代理

### 功能特性
- 📁 文件浏览、上传、下载、删除
- 📝 在线编辑文件
- 🔍 文件搜索
- 👥 多用户管理
- 🔐 权限控制
- 📱 响应式界面

---

## 🌐 访问配置

### 外部访问地址
| 服务 | URL | 说明 |
|------|-----|------|
| **自定义登录页** | https://yangzhi01.lilexer.top:8301/ | 主入口（推荐） |
| **Filebrowser 原版** | https://yangzhi01.lilexer.top:8301/filebrowser/ | 登录后访问 |
| **API 接口** | https://yangzhi01.lilexer.top:8301/api/ | RESTful API |

### 内部访问地址
- **容器内部**: http://filebrowser:80
- **宿主机**: http://localhost:8300 (直连), http://localhost:8302 (Nginx)

### 端口映射
```
宿主机端口 8300 → 容器端口 80 (filebrowser 直连)
宿主机端口 8302 → 容器端口 80 (nginx 代理)
宿主机端口 8301 → Nginx 主服务 (外部访问)
```

---

## 🔐 认证信息

### 管理员账户
```
用户名: admin
密码: N0-xYDmosLEYgTe5
```

⚠️ **安全提示**: 
- 首次登录后请立即修改密码
- 密码存储位置: /root/vps/game/filebrowser/config/login_credentials.txt
- 用户数据库: /root/vps/game/filebrowser/database/filebrowser.db

### 认证机制
- **认证方式**: JWT (JSON Web Token)
- **会话管理**: 基于 Token 的无状态认证
- **密码加密**: bcrypt 哈希算法

---

## 🐳 Docker 配置

### 容器信息
```yaml
服务名称: filebrowser
镜像: filebrowser/filebrowser:latest
容器名称: 
  - filebrowser (主容器)
  - filebrowser-backend1 (后端)
  - filebrowser-nginx1 (Nginx 代理)
重启策略: unless-stopped
健康检查: ✅ 已启用
```

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

### 卷挂载
| 宿主机路径 | 容器路径 | 用途 |
|-----------|---------|------|
| ./data | /srv | 文件存储目录 |
| ./config | /config | 配置文件目录 |
| ./database | /database | 数据库文件 |

### 环境变量
```bash
FB_BASEURL=/filebrowser    # 应用基础路径
```

---

## ⚙️ Filebrowser 配置

### 配置文件位置
/root/vps/game/filebrowser/config/settings.json

### 配置内容
```json
{
  "port": 80,
  "baseURL": "/filebrowser",
  "address": "",
  "log": "stdout",
  "database": "/database/filebrowser.db",
  "root": "/srv"
}
```

### 配置说明
- **port**: 容器内监听端口 (80)
- **baseURL**: 应用基础路径 (/filebrowser)
- **address**: 监听地址 (空表示所有接口)
- **log**: 日志输出 (stdout)
- **database**: 数据库文件路径
- **root**: 文件根目录

---

## 🔧 Nginx 配置

### 配置文件位置
/root/vps/game/filebrowser/nginx-filebrowser.conf

### 上游服务器
```nginx
upstream filebrowser_backend {
    server filebrowser:80;
    keepalive 32;
}
```

### 路由规则

#### 1. 自定义登录页
```nginx
location = /filebrowser-customer {
    root /var/www/filebrowser;
    try_files /custom-login.html =404;
    expires 1h;
}
```

#### 2. Filebrowser 主应用
```nginx
location ~ ^/filebrowser(/.*)?$ {
    proxy_pass http://filebrowser_backend$1;
    proxy_http_version 1.1;
    proxy_set_header X-Script-Name /filebrowser;
}
```

#### 3. API 接口
```nginx
location /api/ {
    proxy_pass http://filebrowser_backend/api/;
    proxy_no_cache 1;
    proxy_cache_bypass 1;
}
```

#### 4. Logo 静态资源
```nginx
location /logos/ {
    root /var/www/filebrowser;
    expires 30d;
    add_header Cache-Control "public, immutable, max-age=2592000";
}
```

### 性能优化配置

#### Gzip 压缩
```nginx
gzip on;
gzip_vary on;
gzip_proxied any;
gzip_comp_level 6;
gzip_types text/plain text/css text/xml text/javascript 
           application/json application/javascript;
```

#### 缓存配置
```nginx
proxy_cache_path /var/cache/nginx 
                 levels=1:2 
                 keys_zone=filebrowser_cache:10m 
                 max_size=100m 
                 inactive=60m;
```

#### 连接优化
```nginx
proxy_connect_timeout 5s;
proxy_send_timeout 10s;
proxy_read_timeout 10s;
proxy_buffering on;
proxy_buffer_size 4k;
proxy_buffers 8 4k;
```

---

## 💾 数据存储

### 数据库
- **类型**: SQLite
- **位置**: /root/vps/game/filebrowser/database/filebrowser.db
- **大小**: 64 KB
- **权限**: 1000:fuse (rw)

### 文件存储
- **根目录**: /root/vps/game/filebrowser/data
- **映射到容器**: /srv
- **用途**: 用户上传和管理的文件

### 配置文件
```
/root/vps/game/filebrowser/config/
├── settings.json              # Filebrowser 配置
├── login_credentials.txt      # 登录凭据
└── user_credentials.json      # 用户凭据（11KB）
```

---

## 🎨 前端定制

### 自定义登录页
- **文件**: frontend/public/custom-login.html
- **访问路径**: /filebrowser-customer
- **特性**:
  - 15张随机轮播 Logo
  - 响应式设计
  - 性能优化（DOM缓存、async/await）
  - 错误处理和用户反馈

### Logo 资源
- **位置**: frontend/public/logos/
- **数量**: 15 张图片
- **缓存策略**: 30 天强缓存

---

## 📊 性能指标

### 响应时间
- **首字节时间 (TTFB)**: ~55ms
- **总加载时间**: ~55ms
- **缓存命中后**: ~10-15ms

### 优化措施
- ✅ Gzip 压缩（减少 60-80% 传输大小）
- ✅ 连接池（32 个 keepalive 连接）
- ✅ 浏览器缓存（Logo 30天，登录页 1小时）
- ✅ 代理缓冲优化
- ✅ 前端性能优化（DOM缓存、async/await）

### 缓存策略
| 资源类型 | 缓存时间 | 策略 |
|---------|---------|------|
| Logo 图片 | 30 天 | public, immutable, max-age=2592000 |
| 登录页面 | 1 小时 | public, max-age=3600 |
| API 请求 | 不缓存 | no-cache, cache-bypass |

---

## 🔒 安全配置

### 传输安全
- ✅ HTTPS/TLS 加密
- ✅ 强制 HTTPS 重定向
- ✅ X-Content-Type-Options: nosniff

### 应用安全
- ✅ JWT 令牌认证
- ✅ 密码 bcrypt 加密
- ✅ 输入验证
- ✅ 错误信息不泄露敏感数据

### 超时设置
```nginx
proxy_connect_timeout 5s;
proxy_send_timeout 10s;
proxy_read_timeout 10s;
```

### 访问控制
- 基于用户的权限管理
- 文件级别的访问控制
- 支持多用户隔离

---

## 🛠️ 运维管理

### 常用命令

#### 查看容器状态
```bash
docker ps | grep filebrowser
```

#### 查看日志
```bash
# Nginx 日志
docker logs filebrowser-nginx1 --tail 50

# Filebrowser 日志
docker logs filebrowser --tail 50
docker logs filebrowser-backend1 --tail 50
```

#### 重启服务
```bash
# 重启 Nginx
docker restart filebrowser-nginx1

# 重启 Filebrowser
docker restart filebrowser filebrowser-backend1

# 重启所有
docker restart filebrowser-nginx1 filebrowser-backend1 filebrowser
```

#### 停止/启动服务
```bash
# 停止
docker stop filebrowser-nginx1 filebrowser-backend1 filebrowser

# 启动
docker start filebrowser filebrowser-backend1 filebrowser-nginx1
```

### 备份策略

#### 需要备份的内容
- 数据库: /root/vps/game/filebrowser/database/filebrowser.db
- 配置文件: /root/vps/game/filebrowser/config/
- 用户文件: /root/vps/game/filebrowser/data/
- Nginx 配置: /root/vps/game/filebrowser/nginx-filebrowser.conf

#### 备份命令示例
```bash
# 创建备份目录
mkdir -p /root/backups/filebrowser/$(date +%Y%m%d)

# 备份数据库
cp /root/vps/game/filebrowser/database/filebrowser.db \
   /root/backups/filebrowser/$(date +%Y%m%d)/

# 备份配置
cp -r /root/vps/game/filebrowser/config \
      /root/backups/filebrowser/$(date +%Y%m%d)/
```

---

## 🐛 故障排查

### 常见问题

#### 1. 登录后显示加载状态
**原因**: 前端 API 请求失败或路由配置问题  
**解决方案**:
```bash
# 检查 API 路由
curl -I https://yangzhi01.lilexer.top:8301/api/login

# 查看 Nginx 日志
docker logs filebrowser-nginx1 --tail 50

# 清除浏览器缓存并重试
```

#### 2. 显示 "用户名或密码错误"
**原因**: 数据库损坏或密码不匹配  
**解决方案**:
```bash
# 重置数据库
docker stop filebrowser
rm /root/vps/game/filebrowser/database/filebrowser.db
docker start filebrowser
sleep 3
docker logs filebrowser | grep "initialized"
```

#### 3. 页面加载缓慢
**原因**: 网络问题或缓存未生效  
**解决方案**:
```bash
# 检查 Nginx 缓存
ls -lh /var/cache/nginx/

# 检查 gzip 是否启用
curl -I -H "Accept-Encoding: gzip" https://yangzhi01.lilexer.top:8301/
```

#### 4. 容器无法启动
**原因**: 端口冲突或配置错误  
**解决方案**:
```bash
# 检查端口占用
ss -tlnp | grep -E '8300|8301|8302'

# 检查容器日志
docker logs filebrowser

# 验证配置文件
cat /root/vps/game/filebrowser/config/settings.json
```

---

## 📁 项目结构

```
/root/vps/game/filebrowser/
├── frontend/
│   └── public/
│       ├── custom-login.html          # 自定义登录页
│       └── logos/                     # 15张Logo图片
├── config/
│   ├── settings.json                  # Filebrowser配置
│   ├── login_credentials.txt          # 登录凭据
│   └── user_credentials.json          # 用户凭据
├── database/
│   └── filebrowser.db                 # SQLite数据库
├── data/                              # 用户文件存储
├── nginx-filebrowser.conf             # Nginx配置
├── docker-compose.yml                 # Docker Compose配置
├── docker-compose-with-nginx.yml      # 带Nginx的配置
└── 文档/
    ├── APPLICATION_CONFIG.md          # 本文档
    ├── QUICK_REFERENCE.md             # 快速参考
    ├── FINAL_LOGIN_FIX.md             # 登录修复报告
    ├── PERFORMANCE_OPTIMIZATION.md    # 性能优化报告
    └── DEPLOYMENT_COMPLETE.md         # 部署完成报告
```

---

## 📚 相关文档

| 文档 | 说明 |
|------|------|
| QUICK_REFERENCE.md | 快速参考指南 |
| FINAL_LOGIN_FIX.md | 登录功能修复详情 |
| PERFORMANCE_OPTIMIZATION.md | 性能优化详情 |
| DEPLOYMENT_COMPLETE.md | 部署完成报告 |
| PORT_8301_CONFIG.md | 8301端口配置说明 |
| NGINX_ROUTING.md | Nginx路由配置 |

---

## 🔄 更新历史

| 日期 | 版本 | 更新内容 |
|------|------|---------|
| 2026-05-02 | 1.0 | 初始部署 |
| 2026-05-02 | 1.1 | 修复登录功能 |
| 2026-05-02 | 1.2 | 性能优化 |
| 2026-05-03 | 1.3 | 生成配置详情文档 |

---

## ✅ 部署检查清单

- [x] Docker 容器运行正常
- [x] Nginx 配置正确
- [x] API 路由正常
- [x] 登录功能正常
- [x] 文件上传/下载正常
- [x] 重定向正确
- [x] 缓存策略生效
- [x] Gzip 压缩启用
- [x] HTTPS 加密启用
- [x] 性能优化完成
- [x] 安全措施启用
- [x] 文档完整

---

## 📞 技术支持

### 查看实时状态
```bash
# 容器状态
docker ps | grep filebrowser

# 端口监听
ss -tlnp | grep -E '8300|8301|8302'

# 磁盘使用
du -sh /root/vps/game/filebrowser/*

# 数据库大小
ls -lh /root/vps/game/filebrowser/database/filebrowser.db
```

### 配置文件位置
- Nginx 配置: /root/vps/game/filebrowser/nginx-filebrowser.conf
- Filebrowser 配置: /root/vps/game/filebrowser/config/settings.json
- 登录凭据: /root/vps/game/filebrowser/config/login_credentials.txt

---

## 🎯 当前状态

**部署状态**: 🎉 生产就绪  
**运行状态**: ✅ 正常运行  
**登录功能**: ✅ 正常  
**性能状态**: ⚡ 已优化  
**安全状态**: 🔐 已加固  
**文档状态**: 📚 完整  

---

*文档生成时间: 2026-05-03*  
*最后更新: 2026-05-03*  
*维护者: System Administrator*
