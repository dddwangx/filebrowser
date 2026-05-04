#!/bin/bash

# Claude Session-Env 同步脚本
# 用途: 每日同步 ~/.claude/session-env 到 filebrowser 数据目录

# 配置变量
SOURCE_DIR="/root/.claude/session-env"
TARGET_DIR="/root/vps/game/filebrowser/data/claude-sessions"
LOG_FILE="/root/vps/game/filebrowser/scripts/sync_claude_sessions.log"
MAX_LOG_SIZE=10485760  # 10MB

# 日志函数
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# 检查日志文件大小并轮转
rotate_log() {
    if [ -f "$LOG_FILE" ] && [ $(stat -f%z "$LOG_FILE" 2>/dev/null || stat -c%s "$LOG_FILE" 2>/dev/null) -gt $MAX_LOG_SIZE ]; then
        mv "$LOG_FILE" "$LOG_FILE.old"
        log "日志文件已轮转"
    fi
}

# 开始同步
log "========== 开始同步 Claude Session-Env =========="

# 检查源目录
if [ ! -d "$SOURCE_DIR" ]; then
    log "错误: 源目录不存在: $SOURCE_DIR"
    exit 1
fi

# 创建目标目录
if [ ! -d "$TARGET_DIR" ]; then
    log "创建目标目录: $TARGET_DIR"
    mkdir -p "$TARGET_DIR"
fi

# 统计源目录信息
SESSION_COUNT=$(find "$SOURCE_DIR" -mindepth 1 -maxdepth 1 -type d | wc -l)
SOURCE_SIZE=$(du -sh "$SOURCE_DIR" | cut -f1)
log "源目录: $SOURCE_DIR"
log "会话数量: $SESSION_COUNT"
log "源目录大小: $SOURCE_SIZE"

# 使用 rsync 同步
log "开始 rsync 同步..."
rsync -av --delete \
    --exclude='*.tmp' \
    --exclude='*.lock' \
    "$SOURCE_DIR/" "$TARGET_DIR/" >> "$LOG_FILE" 2>&1

RSYNC_EXIT=$?

if [ $RSYNC_EXIT -eq 0 ]; then
    # 统计目标目录信息
    TARGET_SIZE=$(du -sh "$TARGET_DIR" | cut -f1)
    log "同步成功!"
    log "目标目录: $TARGET_DIR"
    log "目标目录大小: $TARGET_SIZE"
    
    # 设置权限
    chmod -R 755 "$TARGET_DIR"
    log "权限已设置为 755"
    
    log "========== 同步完成 =========="
    rotate_log
    exit 0
else
    log "错误: rsync 同步失败，退出码: $RSYNC_EXIT"
    log "========== 同步失败 =========="
    exit 1
fi
