# Nginx 路由配置说明

## 配置完成时间
2026-05-02

## 路由配置

已成功配置 nginx 将 `/filebrowser-custom` 路由到 filebrowser 自定义登录页面。

### 路由列表

1. **自定义登录页面**
   - URL: `https://yangzhi01.lilexer.top/filebrowser-custom`
   - 后端: `http://127.0.0.1:8080/filebrowser-customer`
   - 说明: 显示自定义的彩色渐变登录页面

2. **自定义登录页面静态资源**
   - URL: `https://yangzhi01.lilexer.top/filebrowser-custom/*`
   - 后端: `http://127.0.0.1:8080/filebrowser-customer/*`
   - 说明: 支持自定义登录页面的静态资源

3. **Logo 图片资源**
   - URL: `https://yangzhi01.lilexer.top/logos/*`
   - 后端: `http://127.0.0.1:8080/logos/*`
   - 说明: 提供 logo 图片，带 7 天缓存

4. **原版 Filebrowser**
   - URL: `https://yangzhi01.lilexer.top/filebrowser/`
   - 后端: `http://127.0.0.1:8300/filebrowser/`
   - 说明: 原版 filebrowser 应用

## 架构说明

```
用户请求 (HTTPS)
    ↓
主机 Nginx (yangzhi01.lilexer.top:443)
    ↓
    ├─→ /filebrowser-custom → Docker Nginx (127.0.0.1:8080)
    │                              ↓
    │                         自定义登录页面 (custom-login.html)
    │
    ├─→ /logos/* → Docker Nginx (127.0.0.1:8080)
    │                   ↓
    │              Logo 图片资源
    │
    └─→ /filebrowser/ → Filebrowser 容器 (127.0.0.1:8300)
                            ↓
                       原版 Filebrowser 应用
```

## 配置文件位置

- **主机 Nginx 配置**: `/etc/nginx/sites-available/yangzhi01.lilexer.top`
- **启用的配置**: `/etc/nginx/sites-enabled/yangzhi01.lilexer.top`
- **Docker Nginx 配置**: `/root/vps/game/filebrowser/nginx-filebrowser.conf`
- **自定义登录页面**: `/root/vps/game/filebrowser/frontend/public/custom-login.html`

## 配置详情

在 `/etc/nginx/sites-available/yangzhi01.lilexer.top` 的 HTTPS server 块中添加：

```nginx
# Filebrowser 自定义登录页面
location = /filebrowser-custom {
    proxy_pass http://127.0.0.1:8080/filebrowser-customer;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}

# Filebrowser 自定义登录页面的静态资源（logos等）
location /filebrowser-custom/ {
    proxy_pass http://127.0.0.1:8080/filebrowser-customer/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}

# Filebrowser logos 静态资源
location /logos/ {
    proxy_pass http://127.0.0.1:8080/logos/;
    expires 7d;
    add_header Cache-Control "public, immutable";
}
```

## 重新加载配置

```bash
# 测试配置
nginx -t

# 重新加载
nginx -s reload

# 或者如果 PID 文件不存在
kill -HUP $(pgrep -f "nginx: master")
```

## 验证测试

```bash
# 测试自定义登录页
curl -I https://yangzhi01.lilexer.top/filebrowser-custom

# 测试 logo 资源
curl -I https://yangzhi01.lilexer.top/logos/logo_01.jpg

# 测试原版 filebrowser
curl -I https://yangzhi01.lilexer.top/filebrowser/
```

## 注意事项

1. 主机 nginx 配置文件在 `sites-enabled` 中是独立文件，不是符号链接
2. 修改配置后需要同时更新 `sites-available` 和 `sites-enabled` 中的文件
3. Docker nginx 容器运行在 8080 端口，提供自定义登录页面
4. Filebrowser 容器运行在 8300 端口，提供原版应用

## 备份

配置备份位置: `/etc/nginx/sites-available/yangzhi01.lilexer.top.backup`
