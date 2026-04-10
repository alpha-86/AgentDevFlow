# Telegram 通道接入

## 作用

Telegram 在 AgentDevFlow 中承担的是移动端实时沟通与状态跟进通道，不是正式交付主线。

正式流程主线仍然是：

- GitHub Issue
- 文档交付物
- PR / Human Review

## 最小配置

```bash
export TELEGRAM_BOT_TOKEN=<your-bot-token>
export TELEGRAM_CHAT_ID=<your-chat-id>
```

## 当前相关实现

- `scripts/telegram_bot.service`
- `scripts/send_telegram.py`
- `channels/telegram/`
- `channels/core/telegram_monitor.py`

## 使用边界

- Telegram 负责移动端实时通知、进展查看和人与 Agent 的即时沟通。
- Telegram 不能替代 GitHub Issue、文档交付物和正式评审结论。
- 关键结论仍必须回写到 GitHub Issue 和对应文件交付物。
