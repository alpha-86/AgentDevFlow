# QA Case: Telegram Bot 部署说明

## Issue
#1: docs: 补充 Telegram Bot 部署说明到 README

## 测试范围

验证 README 中的 Telegram Bot 部署说明是否完整且准确。

## 验收测试用例

### TC-1: README 包含 Telegram Bot 章节

**步骤：**
1. 打开 README.md
2. 搜索"Telegram Bot"相关内容

**预期结果：**
- [x] README 包含"Telegram Bot"或"Telegram"章节
- [x] 章节包含 BotFather token 获取说明
- [x] 章节包含 systemd service 部署步骤

### TC-2: systemd service 文件引用正确

**步骤：**
1. 在 README 中找到 systemd service 相关说明
2. 验证 `scripts/telegram_bot.service` 文件存在

**预期结果：**
- [x] README 提到 `scripts/telegram_bot.service` 路径
- [x] 该文件在仓库中确实存在

### TC-3: 连接验证命令可用

**步骤：**
1. 在 README 中找到验证命令
2. 验证 `scripts/send_telegram.py` 存在

**预期结果：**
- [x] README 包含 `systemctl status telegram_bot` 命令
- [x] README 包含 `journalctl` 排查命令
- [x] README 包含 `send_telegram.py` 测试命令
- [x] `scripts/send_telegram.py` 文件存在

### TC-4: Telegram Bot 部署流程完整性

**步骤：**
1. 按照 README 中的步骤操作

**预期结果：**
- [x] 能获取 BotFather token
- [x] 能配置 systemd service
- [x] 能启动 Bot 服务
- [x] 能验证 Bot 连接状态

## 测试环境要求

- Linux 环境（支持 systemd）
- Python 3.x
- 有效的 Telegram Bot Token

## 已知限制

- 需要真实的 Telegram Bot Token 才能完整测试
- 生产环境高可用部署不在本次范围内
