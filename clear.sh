#!/bin/sh

# 检查是否传入目录参数
if [ "$#" -ne 1 ]; then
    echo "用法: $0 目录名"
    exit 1
fi

TARGET_DIR="$1"

# 检查参数是否为有效目录
if [ ! -d "$TARGET_DIR" ]; then
    echo "$TARGET_DIR 不是一个有效的目录"
    exit 1
fi

# 查找目标目录下最新的 log_*.txt 文件
LOG_FILE=$(ls -t "$TARGET_DIR"/log_*.txt 2>/dev/null | head -n 1)

# 如果没有找到 log 文件，则退出
if [ -z "$LOG_FILE" ]; then
    echo "未在 $TARGET_DIR 中找到 log_*.txt 文件"
    exit 1
fi

# 提取 log 文件的时间戳
TIMESTAMP=$(echo "$LOG_FILE" | grep -oE '[0-9]{14}')
if [ -z "$TIMESTAMP" ]; then
    echo "无法从 $LOG_FILE 提取时间戳"
    exit 1
fi

# 创建新文件夹
BACKUP_DIR="$TARGET_DIR/backup_$TIMESTAMP"
mkdir -p "$BACKUP_DIR"

# 移动除新文件夹和已有 backup_* 目录之外的所有文件和目录
for item in "$TARGET_DIR"/*; do
    if [ "$item" != "$BACKUP_DIR" ] && [[ ! "$item" =~ backup_.* ]]; then
        mv "$item" "$BACKUP_DIR"/
    fi
done

echo "所有非 backup_ 目录的文件已移动到 $BACKUP_DIR"
