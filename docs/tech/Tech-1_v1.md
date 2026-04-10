# Tech Doc: Telegram Bot 部署说明

## Issue
#1: docs: 补充 Telegram Bot 部署说明到 README

## 技术方案

### 方案选择
在 README.md 中新增"Telegram Bot 部署"章节，直接说明配置和启动方式。

### 文件修改清单

| 文件 | 操作 | 说明 |
|------|------|------|
| `README.md` | 修改 | 新增 Telegram Bot 章节 |
| `scripts/telegram_bot.service` | 参考 | systemd service 模板 |
| `scripts/send_telegram.py` | 参考 | Bot 发送消息脚本 |

### Telegram Bot 配置参数

```bash
# 环境变量
TELEGRAM_BOT_TOKEN=<your-bot-token>
TELEGRAM_CHAT_ID=<your-chat-id>
```

### systemd service 部署步骤

1. 复制 service 文件：
```bash
sudo cp scripts/telegram_bot.service /etc/systemd/system/
```

2. 编辑 token：
```bash
sudo vim /etc/systemd/system/telegram_bot.service
# Environment="TELEGRAM_BOT_TOKEN=<your-token>"
```

3. 启用并启动：
```bash
sudo systemctl daemon-reload
sudo systemctl enable telegram_bot
sudo systemctl start telegram_bot
```

### 连接验证

```bash
# 检查服务状态
sudo systemctl status telegram_bot

# 查看日志
journalctl -u telegram_bot -f

# 发送测试消息
python scripts/send_telegram.py --test
```

## 风险项

| 风险 | 级别 | 缓解 |
|------|------|------|
| Bot Token 泄露 | 高 | 只在 systemd 环境变量中设置，不提交到 git |
| 服务启动失败 | 中 | 提供 journalctl 排查命令 |

## 已在仓库中的相关文件

- `scripts/telegram_bot.service` - systemd service 文件
- `scripts/send_telegram.py` - 发送消息 CLI 工具
- `hedge_ai/telegram/bot_server.py` - Bot 服务端实现
