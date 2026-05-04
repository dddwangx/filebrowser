# 🔄 Filebrowser 路由配置说明

**生成时间**: 2026-05-03  
**当前状态**: ⚠️ 路由配置需要调整

---

## 📌 当前路由架构

### 架构层次
```
用户浏览器
    ↓
外部 Nginx (yangzhi01.lilexer.top:8303)
    ↓
容器 Nginx (filebrowser-nginx1, 127.0.0.1:8302)
    ↓
Filebrowser 应用 (filebrowser-backend1, 容器内部)
```

---

## 🔍 问题分析

### 当前配置
1. **Filebrowser 应用配置** (`/config/settings.json`):
   ```json
   {
     "port": 80,
     "baseURL": "/filebrowser",
     "root": "/srv"
   }
   ```
   - 应用期望所有请求路径都以 `/filebrowser` 开头

2. **容器内 Nginx 配置** (filebrowser-nginx1):
   ```nginx
   location ~ ^/filebrowser(/.*)?$ {
       proxy_pass http://filebrowser_backend$1;
       proxy_set_header X-Script-Name /filebrowser;
   }
   ```
   - 匹配 `/filebrowser/files/` 
   - 代理到后端时变成 `/files/` (去掉了 `/filebrowser` 前缀)
   - 设置了 `X-Script-Name: /filebrowser` 头

3. **外部 Nginx 配置** (yangzhi01.lilexer.top:8303):
   ```nginx
   location /filebrowser/ {
       proxy_pass http://127.0.0.1:8302/filebrowser/;
   }
   ```
   - 转发到容器 nginx

### 问题根源
- 容器内 nginx 使用 `$1` 变量去掉了 `/filebrowser` 前缀
- Filebrowser 应用收到的是 `/files/` 而不是 `/filebrowser/files/`
- 虽然设置了 `X-Script-Name` 头，但应用仍然返回 404

---

## ✅ 解决方案

### 方案 1: 修改容器内 Nginx 配置（推荐）
保留完整路径传递给后端：

```nginx
location ~ ^/filebrowser(/.*)?$ {
    proxy_pass http://filebrowser_backend/filebrowser$1;
    # 保持其他配置不变
}
```

### 方案 2: 修改 Filebrowser baseURL
将 baseURL 改为空：

```json
{
  "port": 80,
  "baseURL": "",
  "root": "/srv"
}
```

然后容器内 nginx 配置：
```nginx
location /filebrowser/ {
    proxy_pass http://filebrowser_backend/;
}
```

### 方案 3: 使用不同的路由路径
外部访问使用 8301 端口（已经正常工作）：
- https://yangzhi01.lilexer.top:8301/
- https://yangzhi01.lilexer.top:8301/files/

---

## 🎯 推荐配置

### 当前可用的访问方式

#### 8301 端口（正常工作）
- **登录页**: https://yangzhi01.lilexer.top:8301/
- **文件浏览**: https://yangzhi01.lilexer.top:8301/files/
- **API**: https://yangzhi01.lilexer.top:8301/api/

配置说明：
- 外部 nginx 直接代理到 filebrowser 容器 (8300端口)
- 没有中间的容器 nginx 层
- 路径映射简单直接

#### 8303 端口（需要修复）
- **目标路径**: https://yangzhi01.lilexer.top:8303/filebrowser/files
- **当前状态**: 404 错误
- **原因**: 容器内 nginx 路径转换问题

---

## 🔧 修复步骤（方案 1）

### 1. 更新容器内 Nginx 配置

需要修改 `/root/vps/game/filebrowser/nginx-filebrowser.conf`:

```nginx
location ~ ^/filebrowser(/.*)?$ {
    proxy_pass http://filebrowser_backend/filebrowser$1;  # 保留完整路径
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_set_header X-Script-Name /filebrowser;
    proxy_set_header Connection "";
    # ... 其他配置
}
```

### 2. 重启容器

```bash
cd /root/vps/game/filebrowser
docker-compose -f docker-compose-with-nginx.yml restart nginx
```

### 3. 验证

```bash
curl -I https://yangzhi01.lilexer.top:8303/filebrowser/files/
```

---

## 📊 路由对比表

| 端口 | 外部路径 | 容器 Nginx | 后端应用收到 | 状态 |
|------|---------|-----------|------------|------|
| 8301 | /files/ | 无 | /filebrowser/files/ | ✅ 正常 |
| 8303 | /filebrowser/files/ | 有 | /files/ | ❌ 404 |
| 8303 (修复后) | /filebrowser/files/ | 有 | /filebrowser/files/ | ✅ 正常 |

---

## 💡 建议

### 短期方案
使用 8301 端口访问，该端口配置简单且工作正常：
- https://yangzhi01.lilexer.top:8301/

### 长期方案
如果需要使用 8303 端口和 `/filebrowser/files` 路径：
1. 修复容器内 nginx 配置
2. 重启容器
3. 更新文档

---

## 📝 配置文件位置

| 文件 | 路径 | 说明 |
|------|------|------|
| Filebrowser 配置 | /root/vps/game/filebrowser/config/settings.json | baseURL 设置 |
| 容器 Nginx 配置 | /root/vps/game/filebrowser/nginx-filebrowser.conf | 需要修改 |
| 外部 Nginx 配置 | /etc/nginx/sites-available/yangzhi01.lilexer.top | 8303 端口配置 |
| Docker Compose | /root/vps/game/filebrowser/docker-compose-with-nginx.yml | 容器编排 |

---

## ✅ 验证命令

```bash
# 测试 8301 端口（应该正常）
curl -I -k https://yangzhi01.lilexer.top:8301/files/

# 测试 8303 端口（当前 404）
curl -I -k https://yangzhi01.lilexer.top:8303/filebrowser/files/

# 测试容器内部
curl -I http://127.0.0.1:8302/filebrowser/files/

# 测试后端应用
docker exec filebrowser-backend1 wget -O- http://localhost/filebrowser/files/ 2>&1 | head -5
```

---

*文档生成时间: 2026-05-03*  
*状态: 问题已识别，等待修复*
