# Phase 3: Telegram 通道链路复核

**日期**: 2026-04-10
**任务**: Review Telegram 通道代码，判断用户→Team Lead→用户闭环是否实现
**原则**: 只基于代码实际实现判断，以代码链路是否闭环为准

---

## 一、当前入站消息链路图

```
用户发消息
    │
    ▼
bot_server.py (TelegramBotServer._process_update)
    │  update_id=xxx chat_id=xxx text=xxx
    │
    ├──→ 自动授权: authorized_chats.append(chat_id)
    ├──→ /start → "AgentDevFlow Bot 已启动"
    ├──→ /help  → 帮助信息
    ├──→ /status → _get_status_text()  【仅返回Bot自身状态】
    ├──→ /health → _health_check_text()【仅返回Bot健康状态】
    │
    ▼
on_message 回调 (如果已设置)
    │  signature: on_message(update, response)
    │
    ▼
【链路断点】❌ 无任何代码将消息路由到 Team Lead
```

**结论**: 入站链路在 `bot_server.py:212-213` 处断裂。`on_message` 回调存在但无人设置，无人将消息写入 task_queue 或触发 Team Lead。

---

## 二、当前出站消息链路图

```
Team Lead 回复
    │
    ▼
【链路断点】❌ 无任何代码知道用户的 chat_id
    │
    ▼
send_telegram.py::send_message(chat_id)  ← 需要 chat_id 参数
telegram_monitor.py::TelegramHealthChecker.send_test_message() ← 需要 chat_id 参数
bot_server.py::send_message(chat_id, text) ← 需要 chat_id 参数
```

**结论**: 出站链路完全断裂。没有任何模块维护 `session_id → chat_id` 映射，Team Lead 无法知道该回复到哪个 Telegram chat。

---

## 三、缺失能力清单

| # | 缺失能力 | 严重度 | 说明 |
|---|----------|--------|------|
| 1 | `on_message` 回调未连接 | 🔴 P0 | `TelegramBotServer.on_message` 存在但无任何地方设置 |
| 2 | 消息未写入 task_queue | 🔴 P0 | 用户 Telegram 消息从未写入 `.claude/task_queue/` |
| 3 | TaskQueuePoller 不存在 | 🔴 P0 | PRD 056 F1 要求的轮询服务完全不存在 |
| 4 | TeamLeadWakeupInterface 不存在 | 🔴 P0 | PRD 055 F3 要求的唤醒接口不存在 |
| 5 | UnifiedMessage 格式未定义 | 🔴 P0 | PRD 055 F2 要求的统一消息格式不存在 |
| 6 | `session_id → chat_id` 映射缺失 | 🔴 P0 | Team Lead 回复时无法确定目标 chat |
| 7 | task_router.py 与 Telegram 完全隔离 | 🔴 P0 | task_router.py 只处理 task 文件，不处理 Telegram 消息 |

---

## 四、最小补齐方案

### 4.1 入站补齐：让用户消息通知到 Team Lead

**核心思路**: Telegram Bot 收到消息后，写入 task_queue，由 task_router.py 已有能力进行路由。

**需修改文件**: `channels/telegram/bot_server.py`

**修改点**:

```python
# bot_server.py 第 78-79 行，添加 on_message 处理
self.on_message: Optional[Callable] = None

# 修改 _process_update 方法（第 212-213 行）
# 当前:
if self.on_message:
    self.on_message(update, response)

# 改为: 将消息写入 task_queue
if text and chat_id:
    self._write_to_task_queue(update)  # 新增方法

# 新增方法:
def _write_to_task_queue(self, update: Dict):
    """将收到的消息写入 task_queue"""
    import uuid
    from datetime import datetime

    message = update.get("message", {})
    chat_id = message.get("chat", {}).get("id")
    text = message.get("text", "")
    first_name = message.get("from", {}).get("first_name", "unknown")

    task_id = f"telegram_{uuid.uuid4().hex[:8]}"
    task_file = Path(AGENTDEVFLOW_ROOT) / ".claude" / "task_queue" / f"{task_id}.task"

    # 写入 task 文件（兼容 task_router.py 格式）
    task_file.parent.mkdir(parents=True, exist_ok=True)
    task_file.write_text(
        f"issue_id={task_id}\n"
        f"title=Telegram消息 from {first_name}\n"
        f"type=telegram\n"  # task_router.py ROLE_MAP 中无此 key，会默认路由到 Engineer
        f"source=telegram\n"
        f"chat_id={chat_id}\n"  # 用于回传
        f"content={text}\n"
        f"created_at={datetime.now().isoformat()}\n"
    )
```

**问题**: `task_router.py` 的 `ROLE_MAP` 中没有 `telegram` 类型，会默认路由到 `Engineer`。需要确认这是否符合预期，或新增路由规则。

### 4.2 出站补齐：让 Team Lead 回复回传到原用户 chat_id

**核心思路**: Team Lead 写回复到 task 结果文件或专用目录，前置 Agent（telegram_agent）轮询并发送。

**方案A（推荐）**: 创建 `telegram_response_queue`，由前置 Agent 轮询并发送

**新增文件**: `channels/telegram/response_forwarder.py`

```python
"""
Telegram 响应转发器
持续监控 response_queue，将 Team Lead 的回复发送回对应用户
"""
import time
import logging
from pathlib import Path
from typing import Dict
from channels.telegram.bot_server import get_bot_server

AGENTDEVFLOW_ROOT = Path(__file__).parent.parent.parent.resolve()
RESPONSE_QUEUE = AGENTDEVFLOW_ROOT / ".claude" / "telegram_response_queue"

logger = logging.getLogger(__name__)

def process_responses():
    """处理响应队列"""
    bot = get_bot_server()

    while True:
        for resp_file in RESPONSE_QUEUE.glob("*.response"):
            try:
                content = resp_file.read_text()
                resp_data = json.loads(content)

                chat_id = resp_data.get("chat_id")
                text = resp_data.get("text")

                if chat_id and text:
                    bot.send_message(int(chat_id), text)
                    resp_file.unlink()  # 删除已处理的响应文件
                    logger.info(f"响应已转发到 chat_id={chat_id}")
            except Exception as e:
                logger.error(f"处理响应失败: {e}")

        time.sleep(2)  # 每 2 秒检查一次
```

**Team Lead 端约定**: Team Lead 回复时，需要将响应写入:

```json
// .claude/telegram_response_queue/{msg_id}.response
{
  "chat_id": 123456789,
  "text": "这是 Team Lead 的回复"
}
```

### 4.3 需修改的文件清单

| 文件 | 修改内容 |
|------|----------|
| `channels/telegram/bot_server.py` | `_process_update()` 中新增 `_write_to_task_queue()` 调用 |
| `scripts/task_router.py` | 新增 `telegram` 类型的路由映射（可选，默认 Engineer 也可） |
| `channels/telegram/response_forwarder.py` | **新增** - 响应转发器 |
| `scripts/__init__.py` 或 systemd | 添加 response_forwarder 到启动脚本 |

---

## 五、与 hedge-ai PRD 055/056 的差距对比

| 能力项 | PRD 055/056 要求 | AgentDevFlow 现状 | 差距 |
|--------|------------------|-------------------|------|
| **F1 多源消息接收器** | `MessageReceiver` 抽象接口 + `TelegramReceiver.receive()` | `TelegramBotServer._process_update()` 存在但不连接 | 🔴 完全未对接 |
| **F2 统一消息格式** | `UnifiedMessage` dataclass | 无 | 🔴 不存在 |
| **F3 Team Lead 唤醒接口** | `TeamLeadWakeupInterface.wakeup()` | 无 | 🔴 不存在 |
| **F4 cclaude Alias** | `~/.bashrc` alias + session 持久化 | 无 | 🔴 不存在 |
| **F5 Session 管理** | `~/.cclaude/` 目录 | 无 | 🔴 不存在 |
| **F6 TaskQueuePoller** | PRD 056 F1: 轮询 task_queue 触发 Team Lead | 无 | 🔴 不存在 |
| **入站: Telegram → Team Lead** | 消息通过 UnifiedMessage 路由到 wakeup 接口 | `_process_update()` 仅返回本地响应 | 🔴 断裂 |
| **出站: Team Lead → 用户** | wakeup 接口返回 response 到原始 chat_id | 无任何回传机制 | 🔴 断裂 |

### 架构对比图

**PRD 055/056 期望架构**:
```
[Telegram] → [TelegramReceiver] → [UnifiedMessage] → [TeamLeadWakeupInterface] → [Team Lead]
                                                                       ↓
[Telegram] ← [ResponseQueue] ← [Team Lead Response]
```

**AgentDevFlow 现状**:
```
[Telegram] → [bot_server.py] → ❌ 断裂（不触发任何 wakeup）
                              ↓
[Telegram] ← ❌ 断裂（无 chat_id 映射，无回传机制）
```

---

## 六、总结

| 链路方向 | 状态 | 说明 |
|----------|------|------|
| 用户 → bot_server.py | ✅ 正常 | 消息接收正常 |
| bot_server.py → task_queue | ❌ 断裂 | 消息未写入 |
| task_queue → task_router.py | ✅ 正常 | task_router.py 已实现 |
| task_router.py → Team Lead | ❌ 断裂 | 无 TaskQueuePoller |
| Team Lead → 用户 | ❌ 断裂 | 无 chat_id 映射和回传机制 |

**最小补齐优先级**:
1. **P0**: `bot_server.py` 中 `_write_to_task_queue()` 方法，将消息写入 task_queue
2. **P0**: 创建 `response_forwarder.py`，将 Team Lead 响应回传到用户
3. **P0**: 创建 `TaskQueuePoller` 或等效机制，轮询 task_queue 并触发 Team Lead
