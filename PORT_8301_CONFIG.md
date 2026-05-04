# Filebrowser 端口 8301 配置说明

## 配置完成时间
2026-05-02

## 访问地址

**主访问地址**: `https://yangzhi01.lilexer.top:8301/`

这个端口专门用于 filebrowser 自定义登录页面，避免与默认端口冲突。

## 配置详情

### 端口监听
- **端口**: 8301 (HTTPS)
- **协议**: SSL/TLS
- **证书**: 使用与主域名相同的 SSL 证书

### 路由配置

1. **根路径 `/`**
   - 直接显示自定义登录页面
   - 后端: `http://127.0.0.1:8080/filebrowser-customer`

2. **Logo 资源 `/logos/`**
   - 提供 logo 图片资源
   - 后端: `http://127.0.0.1:8080/logos/`
   - 缓存: 7 天

3. **API 请求 `/api/`**
   - 转发到 filebrowser 应用
   - 后端: `http://127.0.0.1:8300/filebrowser/api/`

## 架构图

```
用户访问 https://yangzhi01.lilexer.top:8301/
    ↓
主机 Nginx (端口 8301)
    ↓
    ├─→ / → Docker Nginx (127.0.0.1:8080) → 自定义登录页面
    ├─→ /logos/ → Docker Nginx (127.0.0.1:8080) → Logo 图片
    └─→ /api/ → Filebrowser 容器 (127.0.0.1:8300) → API 处理
```

## Nginx 配置

配置文件位置: `/etc/nginx/sites-available/yangzhi01.lilexer.top`

```nginx
# Filebrowser Custom on port 8301
server {
    listen 8301 ssl;
    listen [::]:8301 ssl;
    server_name yangzhi01.lilexer.top;

    ssl_certificate /root/.acme.sh/yangzhi01.lilexer.top_ecc/fullchain.cer;
    ssl_certificate_key /root/.acme.sh/yangzhi01.lilexer.top_ecc/yangzhi01.lilexer.top.key;

    # 直接显示自定义登录页面
    location / {
        proxy_pass http://127.0.0.1:8080/filebrowser-customer;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # 静态资源
    location /logos/ {
        proxy_pass http://127.0.0.1:8080/logos/;
        expires 7d;
        add_header Cache-Control "public, immutable";
    }

    # API 请求转发到 filebrowser
    location /api/ {
        proxy_pass http://127.0.0.1:8300/filebrowser/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 验证测试

```bash
# 测试端口监听
ss -tlnp | grep 8301

# 测试 HTTPS 访问
curl -I https://yangzhi01.lilexer.top:8301/

# 测试页面内容
curl -s https://yangzhi01.lilexer.top:8301/ | head -30

# 测试 logo 资源
curl -I https://yangzhi01.lilexer.top:8301/logos/logo_01.jpg
```

## 所有访问方式对比

| 访问方式 | URL | 说明 |
|---------|-----|------|
| **端口 8301** | `https://yangzhi01.lilexer.top:8301/` | ✅ 推荐：独立端口，自定义登录页 |
| 路径方式 | `https://yangzhi01.lilexer.top/filebrowser-custom` | ✅ 可用：通过路径访问 |
| 原版 | `https://yangzhi01.lilexer.top/filebrowser/` | ✅ 可用：原版 filebrowser |

## 优势

1. **独立端口**: 避免与其他服务路径冲突
2. **简洁 URL**: 直接访问根路径即可，无需记忆复杂路径
3. **易于管理**: 独立的 server 块，配置清晰
4. **灵活扩展**: 可以在此端口下添加更多自定义功能

## 防火墙配置

如果服务器有防火墙，需要开放 8301 端口：

```bash
# UFW
sudo ufw allow 8301/tcp

# iptables
sudo iptables -A INPUT -p tcp --dport 8301 -j ACCEPT

# firewalld
sudo firewall-cmd --permanent --add-port=8301/tcp
sudo firewall-cmd --reload
```

## 重新加载配置

```bash
# 测试配置
nginx -t

# 重新加载
nginx -s reload

# 或使用 systemctl
systemctl reload nginx
```

## 故障排查

### 无法访问
1. 检查 nginx 是否监听端口: `ss -tlnp | grep 8301`
2. 检查防火墙规则
3. 检查 SSL 证书是否有效
4. 查看 nginx 错误日志: `tail -f /var/log/nginx/error.log`

### 页面显示异常
1. 检查 Docker nginx 容器是否运行: `docker ps | grep filebrowser-nginx`
2. 检查后端服务: `curl -I http://127.0.0.1:8080/filebrowser-customer`
3. 检查 filebrowser 容器: `docker ps | grep filebrowser`

## 相关文档

- [NGINX_ROUTING.md](./NGINX_ROUTING.md) - 完整的 nginx 路由配置说明
- [DEPLOYMENT_COMPLETE.md](./DEPLOYMENT_COMPLETE.md) - 部署完整文档
