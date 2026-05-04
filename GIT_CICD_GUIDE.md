# Git 版本控制与 CI/CD 配置指南

## 当前状态

### Git 配置
- **远程仓库**: `https://github.com/dddwangx/filebrowser.git`
- **分支**: `master`
- **用户配置**: `Kiro <kiro@example.com>`

### 已提交内容
- 部署配置文件 (nginx, docker-compose)
- 自定义登录页面
- 同步脚本 (Claude sessions)
- 部署文档

## Git 基础操作

### 查看状态
```bash
git status
git log --oneline -5
git branch -a
```

### 提交更改
```bash
git add <files>
git commit -m "描述"
git push origin master
```

### 回滚
```bash
git reset --hard HEAD~1
git push origin master --force
```

## CI/CD 流程

### 1. 本地开发
```bash
# 创建新分支
git checkout -b feature/your-feature

# 开发并提交
git add .
git commit -m "Add feature"

# 推送到远程
git push origin feature/your-feature
```

### 2. 创建 Pull Request
- 访问 GitHub 创建 PR
- 代码审查通过后合并

### 3. 自动部署
- 合并到 `master` 或打标签 `v*`
- GitHub Actions 自动触发部署
- SSH 连接到 VPS
- 拉取最新代码并重启服务

## 部署配置

### 环境变量 (GitHub Secrets)
- `VPS_HOST`: 服务器 IP
- `VPS_USER`: 用户名
- `VPS_SSH_KEY`: SSH 私钥
- `VPS_PORT`: SSH 端口

### 部署脚本位置
- `/root/vps/game/filebrowser/scripts/`
- `sync_claude_sessions.sh`: 同步脚本
- `integrate_custom_login.sh`: 登录集成

## 权限修复

已修复文件权限:
- 目录: `755`
- 文件: `644`

## 下一步

1. 配置 GitHub Secrets
2. 测试 CI/CD 流程
3. 设置标签自动部署
