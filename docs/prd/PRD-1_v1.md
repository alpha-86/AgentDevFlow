# PRD: Telegram Bot 部署说明

## Issue
#1: docs: 补充 Telegram Bot 部署说明到 README

## 背景
当前 AgentDevFlow README 缺少 Telegram Bot 部署相关说明，用户无法了解如何配置和启动 Telegram Bot 与 AgentDevFlow 的连接。

## 目标
在 README 中补充完整的 Telegram Bot 部署说明，使新用户能够：
1. 了解 Telegram Bot 的作用
2. 配置 Bot 与 AgentDevFlow 的连接
3. 使用 systemd 部署 Bot 服务
4. 验证 Bot 连接状态

## 验收标准

### 必须包含内容
- [x] Telegram Bot 配置说明（BotFather token 获取方式）
- [x] systemd service 文件位置说明（`scripts/telegram_bot.service`）
- [x] Bot 连接状态验证方法
- [x] 依赖说明（Python, python-telegram-bot 库）

### 放置位置
- 主 README.md 的"部署"或"快速启动"章节
- 或新建 `docs/deployment/telegram-bot.md` 并在 README 中链接

## 用户故事

### 场景 1: 新用户首次部署
作为新用户，我希望在 README 中找到 Telegram Bot 部署说明，这样我可以快速将 Bot 连接到我自己的 Telegram 账号。

**验收条件：**
- README 包含"Telegram Bot"章节
- 章节包含 BotFather token 获取步骤
- 章节包含 systemd service 部署步骤
- 章节包含连接验证命令

## 非目标
- 不包含 Telegram Bot 的 Python API 二次开发说明
- 不包含生产环境高可用部署方案

## 依赖项
- python-telegram-bot 库
- systemd
-有效的 Telegram Bot Token

## 优先级
P1 - 文档补充

---
* Phase 4 演练 - doc PR for issue #1
