# Filebrowser 部署模式技能

## 部署步骤

### 1. 创建虚拟环境
```bash
cd /root/vps/game/filebrowser
python3 -m venv venv
source venv/bin/activate
pip install gunicorn flask
```

### 2. 启动 Filebrowser 容器
```bash
mkdir -p data config database
chmod 777 config database
docker run -d --name filebrowser \
  -p 8300:80 \
  -v $(pwd)/data:/srv \
  -v $(pwd)/config:/config \
  -v $(pwd)/database:/database \
  filebrowser/filebrowser:latest
```

### 3. 配置 nginx 反向代理
在 `/etc/nginx/sites-available/yangzhi01.lilexer.top` 添加：
```nginx
location /filebrowser/ {
    proxy_pass http://127.0.0.1:8300/filebrowser/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_buffering on;
    proxy_buffer_size 8k;
    proxy_buffers 16 8k;
    proxy_connect_timeout 10s;
    proxy_read_timeout 30s;
}
```

### 4. 更新 sites-enabled 并重启 nginx
```bash
cp /etc/nginx/sites-available/yangzhi01.lilexer.top /etc/nginx/sites-enabled/yangzhi01.lilexer.top
nginx -t && systemctl reload nginx
```

## 异常修复逻辑

### 问题1: Docker shim 错误
**症状**: `exec: "docker-containerd-shim": executable file not found in $PATH`
**修复**: 重启 Docker 服务或停止 containerd 进程

### 问题2: 权限不足
**症状**: `cp: can't create '/config/settings.json': Permission denied`
**修复**: `chmod 777 config database`

### 问题3: nginx 配置未生效
**症状**: 请求被转发到错误的服务（如 Django）
**原因**: `/etc/nginx/sites-enabled/` 是旧版本配置文件
**修复**: 
```bash
cp /etc/nginx/sites-available/yangzhi01.lilexer.top /etc/nginx/sites-enabled/yangzhi01.lilexer.top
```

### 问题4: nginx 服务无法启动
**症状**: `bind() to 0.0.0.0:443 failed (98: Address already in use)`
**原因**: 旧 nginx 进程未完全停止
**修复**: 
```bash
pkill nginx; sleep 1; nginx
```

### 问题5: 路径匹配错误
**症状**: 返回 404 或 Django 错误页面
**原因**: `proxy_pass` 路径配置不正确
**修复**: 使用 `proxy_pass http://127.0.0.1:8300/filebrowser/;`（带路径）

## 访问地址
`https://yangzhi01.lilexer.top/filebrowser`
