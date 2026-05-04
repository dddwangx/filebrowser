# 📋 Claude Session-Env 自动同步配置

**配置时间**: 2026-05-03  
**状态**: ✅ 已启用并运行  
**同步频率**: 每日凌晨 2:00

---

## 📌 功能概述

自动将 Claude 的会话环境数据同步到 Filebrowser 数据目录，方便通过 Web 界面访问和管理。

### 同步内容
- **源目录**: `~/.claude/session-env`
- **目标目录**: `/root/vps/game/filebrowser/data/claude-sessions`
- **会话数量**: 44 个会话目录
- **数据大小**: ~180KB

---

## 🔧 配置文件

### 1. 同步脚本
**位置**: `/root/vps/game/filebrowser/scripts/sync_claude_sessions.sh`

**功能特性**:
- ✅ 使用 rsync 增量同步
- ✅ 自动创建目标目录
- ✅ 排除临时文件 (*.tmp, *.lock)
- ✅ 详细日志记录
- ✅ 日志文件自动轮转 (10MB)
- ✅ 同步前后统计信息
- ✅ 自动设置权限 (755)

**关键配置**:
```bash
SOURCE_DIR="/root/.claude/session-env"
TARGET_DIR="/root/vps/game/filebrowser/data/claude-sessions"
LOG_FILE="/root/vps/game/filebrowser/scripts/sync_claude_sessions.log"
MAX_LOG_SIZE=10485760  # 10MB
```

### 2. Systemd Service
**位置**: `/etc/systemd/system/claude-session-sync.service`

```ini
[Unit]
Description=Sync Claude Session-Env to Filebrowser
After=network.target

[Service]
Type=oneshot
ExecStart=/root/vps/game/filebrowser/scripts/sync_claude_sessions.sh
User=root
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

### 3. Systemd Timer
**位置**: `/etc/systemd/system/claude-session-sync.timer`

```ini
[Unit]
Description=Daily sync of Claude Session-Env to Filebrowser
Requires=claude-session-sync.service

[Timer]
# 每天凌晨 2:00 执行
OnCalendar=daily
OnCalendar=*-*-* 02:00:00
# 如果错过了执行时间，立即执行
Persistent=true
# 首次启动后 5 分钟执行一次
OnBootSec=5min

[Install]
WantedBy=timers.target
```

---

## 📊 同步状态

### 当前状态
```
定时器状态: active (waiting)
下次执行: Mon 2026-05-04 00:00:00 EDT
上次执行: Sun 2026-05-03 09:12:14 EDT
执行结果: ✅ 成功
```

### 同步统计
- **会话数量**: 44 个
- **源目录大小**: 180KB
- **目标目录大小**: 180KB
- **同步方式**: rsync 增量同步
- **传输数据**: 2.6KB (首次), 2.4KB (增量)

---

## 🛠️ 管理命令

### 查看定时器状态
```bash
# 查看所有定时器
systemctl list-timers

# 查看 Claude 同步定时器
systemctl list-timers | grep claude

# 查看详细状态
systemctl status claude-session-sync.timer
```

### 查看服务状态
```bash
# 查看服务状态
systemctl status claude-session-sync.service

# 查看服务日志
journalctl -u claude-session-sync.service -n 50
```

### 手动执行同步
```bash
# 直接运行脚本
/root/vps/game/filebrowser/scripts/sync_claude_sessions.sh

# 通过 systemd 执行
systemctl start claude-session-sync.service
```

### 启动/停止定时器
```bash
# 启动定时器
systemctl start claude-session-sync.timer

# 停止定时器
systemctl stop claude-session-sync.timer

# 重启定时器
systemctl restart claude-session-sync.timer

# 启用开机自启
systemctl enable claude-session-sync.timer

# 禁用开机自启
systemctl disable claude-session-sync.timer
```

---

## 📝 日志管理

### 日志文件位置
```
/root/vps/game/filebrowser/scripts/sync_claude_sessions.log
```

### 查看日志
```bash
# 查看完整日志
cat /root/vps/game/filebrowser/scripts/sync_claude_sessions.log

# 查看最近 20 行
tail -20 /root/vps/game/filebrowser/scripts/sync_claude_sessions.log

# 实时监控日志
tail -f /root/vps/game/filebrowser/scripts/sync_claude_sessions.log
```

### 日志格式
```
[2026-05-03 09:12:14] ========== 开始同步 Claude Session-Env ==========
[2026-05-03 09:12:14] 源目录: /root/.claude/session-env
[2026-05-03 09:12:14] 会话数量: 44
[2026-05-03 09:12:14] 源目录大小: 180K
[2026-05-03 09:12:14] 开始 rsync 同步...
[2026-05-03 09:12:14] 同步成功!
[2026-05-03 09:12:14] 目标目录: /root/vps/game/filebrowser/data/claude-sessions
[2026-05-03 09:12:14] 目标目录大小: 180K
[2026-05-03 09:12:14] 权限已设置为 755
[2026-05-03 09:12:14] ========== 同步完成 ==========
```

### 日志轮转
- 当日志文件超过 10MB 时自动轮转
- 旧日志保存为 `sync_claude_sessions.log.old`
- 新日志从头开始记录

---

## 🌐 Web 访问

### 通过 Filebrowser 访问
1. 访问: https://yangzhi01.lilexer.top:8301/
2. 登录账户: admin / N0-xYDmosLEYgTe5
3. 导航到: `/claude-sessions/`
4. 浏览 44 个会话目录

### 目录结构
```
/root/vps/game/filebrowser/data/claude-sessions/
├── 0842e806-2afe-4183-bc5d-23f4f7a3840a/
├── 107d3d17-23c4-45ff-b5b5-4927d060659f/
├── 115baff6-de3a-4149-b43e-add7f28e0a29/
├── ... (共 44 个会话目录)
└── e694c47f-5065-47fb-a849-b4e2ef1ae54a/
```

---

## 🔍 故障排查

### 问题 1: 同步失败
**检查步骤**:
```bash
# 1. 检查源目录是否存在
ls -la /root/.claude/session-env

# 2. 检查目标目录权限
ls -la /root/vps/game/filebrowser/data/

# 3. 查看错误日志
tail -50 /root/vps/game/filebrowser/scripts/sync_claude_sessions.log

# 4. 手动执行测试
/root/vps/game/filebrowser/scripts/sync_claude_sessions.sh
```

### 问题 2: 定时器未执行
**检查步骤**:
```bash
# 1. 检查定时器状态
systemctl status claude-session-sync.timer

# 2. 检查定时器是否启用
systemctl is-enabled claude-session-sync.timer

# 3. 查看 systemd 日志
journalctl -u claude-session-sync.timer -n 50

# 4. 重新加载配置
systemctl daemon-reload
systemctl restart claude-session-sync.timer
```

### 问题 3: 权限问题
**解决方案**:
```bash
# 确保脚本可执行
chmod +x /root/vps/game/filebrowser/scripts/sync_claude_sessions.sh

# 确保目标目录可写
chmod 755 /root/vps/game/filebrowser/data/

# 手动设置同步目录权限
chmod -R 755 /root/vps/game/filebrowser/data/claude-sessions/
```

### 问题 4: rsync 未安装
**解决方案**:
```bash
# 检查 rsync 是否安装
which rsync

# 安装 rsync (如果未安装)
apt-get update && apt-get install -y rsync
```

---

## 📈 性能优化

### 当前优化措施
- ✅ 使用 rsync 增量同步（只传输变化的文件）
- ✅ 排除临时文件减少传输量
- ✅ 使用 --delete 选项保持目标目录干净
- ✅ 日志文件自动轮转避免占用过多空间

### 同步性能
- **首次同步**: ~2.6KB 传输，<1秒完成
- **增量同步**: ~2.4KB 传输，<1秒完成
- **网络带宽**: 5.6KB/s (本地同步)

---

## 🔐 安全考虑

### 权限设置
- 脚本权限: 755 (可执行)
- 目标目录权限: 755 (可读可执行)
- 日志文件权限: 644 (可读)

### 数据保护
- 源目录保持不变（只读操作）
- 使用 rsync 的 --delete 选项保持同步一致性
- 排除临时和锁文件避免冲突

### 访问控制
- 通过 Filebrowser 的用户认证访问
- HTTPS 加密传输
- 仅 root 用户可执行同步脚本

---

## 📅 执行计划

### 定时执行
- **每日执行**: 凌晨 2:00
- **首次启动**: 系统启动后 5 分钟
- **错过补偿**: 如果错过执行时间，立即执行

### 执行时间表
```
下次执行: Mon 2026-05-04 00:00:00 EDT
之后执行: Tue 2026-05-05 00:00:00 EDT
...
```

---

## 🔄 维护建议

### 定期检查
```bash
# 每周检查一次同步状态
systemctl status claude-session-sync.timer

# 每月检查一次日志大小
ls -lh /root/vps/game/filebrowser/scripts/sync_claude_sessions.log

# 每季度检查一次磁盘空间
du -sh /root/vps/game/filebrowser/data/claude-sessions/
```

### 备份建议
- 源目录已由 Claude 管理，无需额外备份
- 目标目录可通过 Filebrowser 定期导出
- 日志文件定期归档（可选）

---

## 📚 相关文档

| 文档 | 说明 |
|------|------|
| `APPLICATION_CONFIG.md` | Filebrowser 应用配置详情 |
| `QUICK_REFERENCE.md` | 快速参考指南 |
| `sync_claude_sessions.sh` | 同步脚本源码 |
| `sync_claude_sessions.log` | 同步日志文件 |

---

## ✅ 配置检查清单

- [x] 同步脚本已创建并可执行
- [x] Systemd service 已配置
- [x] Systemd timer 已配置并启用
- [x] 首次同步已成功执行
- [x] 日志记录正常
- [x] 定时器已启动并等待下次执行
- [x] 目标目录权限正确
- [x] 可通过 Filebrowser Web 访问

---

## 🎯 当前状态

**同步脚本**: ✅ 已部署  
**定时任务**: ✅ 已启用  
**首次同步**: ✅ 成功 (44 个会话, 180KB)  
**下次执行**: 🕐 2026-05-04 00:00:00  
**日志记录**: ✅ 正常  
**Web 访问**: ✅ 可用  

---

*文档生成时间: 2026-05-03*  
*最后更新: 2026-05-03*  
*维护者: System Administrator*
