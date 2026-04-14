"""
Telegram 消息监控模块

从 hedge-ai/channels/core/telegram_monitor.py 迁移
保留：TelegramMonitor、TelegramHealthChecker、消息状态跟踪、重试机制
剥离：业务相关的特定消息类型
"""

import os
import json
import uuid
import logging
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field, asdict
from enum import Enum
from threading import Lock

import requests


AGENTDEVFLOW_ROOT = os.environ.get(
    "AGENTDEVFLOW_ROOT",
    str(__file__.rsplit("/channels/", 1)[0] if "/channels/" in __file__ else os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
)

logger = logging.getLogger(__name__)


# ================== 数据模型 ==================

class MessageStatus(Enum):
    """消息状态"""
    PENDING = "pending"
    SENT = "sent"
    DELIVERED = "delivered"
    FAILED = "failed"
    RETRYING = "retrying"


@dataclass
class TelegramMessageRecord:
    """Telegram 消息记录"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    message_type: str = ""          # 消息类型（自定义，如 status/alert/info）
    content_preview: str = ""       # 消息内容预览（前100字符）
    recipient_chat_id: str = ""     # 接收者 chat_id
    sent_at: Optional[str] = None   # 发送时间（ISO格式）
    status: str = "pending"         # pending/sent/delivered/failed/retrying
    message_id: Optional[str] = None  # Telegram 返回的 message_id
    error_message: Optional[str] = None  # 错误信息
    retry_count: int = 0            # 重试次数
    sent_duration_ms: Optional[int] = None  # 发送耗时（毫秒）
    delivery_confirmed_at: Optional[str] = None  # 送达确认时间

    def to_dict(self) -> Dict:
        return {k: v for k, v in asdict(self).items() if v is not None}

    @classmethod
    def from_dict(cls, data: Dict) -> "TelegramMessageRecord":
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})


@dataclass
class TelegramStats:
    """Telegram 统计信息"""
    total_sent: int = 0
    total_failed: int = 0
    last_24h_sent: int = 0
    last_24h_failed: int = 0
    last_message_at: Optional[str] = None
    avg_duration_ms: float = 0.0
    consecutive_failures: int = 0
    success_rate: float = 100.0


# ================== 监控类 ==================

class TelegramMonitor:
    """Telegram 消息监控器"""

    def __init__(self, storage_path: str = None):
        if storage_path is None:
            storage_path = os.path.join(AGENTDEVFLOW_ROOT, ".claude", "results", "telegram_monitor.json")
        self.storage_path = storage_path
        self._records: List[TelegramMessageRecord] = []
        self._lock = Lock()
        self._load_records()

    def _load_records(self):
        """从文件加载记录"""
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self._records = [TelegramMessageRecord.from_dict(r) for r in data]
                logger.info(f"加载了 {len(self._records)} 条 Telegram 消息记录")
            except Exception as e:
                logger.warning(f"加载消息记录失败: {e}")
                self._records = []

    def _save_records(self):
        """保存记录到文件"""
        try:
            os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
            with open(self.storage_path, 'w', encoding='utf-8') as f:
                json.dump([r.to_dict() for r in self._records], f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"保存消息记录失败: {e}")

    def add_record(self, record: TelegramMessageRecord):
        """添加消息记录"""
        with self._lock:
            self._records.append(record)
            if len(self._records) > 1000:
                self._records = self._records[-1000:]
            self._save_records()

    def update_record(self, record_id: str, **kwargs):
        """更新消息记录"""
        with self._lock:
            for record in self._records:
                if record.id == record_id:
                    for key, value in kwargs.items():
                        if hasattr(record, key):
                            setattr(record, key, value)
                    self._save_records()
                    return True
        return False

    def get_record(self, record_id: str) -> Optional[TelegramMessageRecord]:
        """获取消息记录"""
        with self._lock:
            for record in self._records:
                if record.id == record_id:
                    return record
        return None

    def get_recent_records(self, limit: int = 50, status: str = None) -> List[TelegramMessageRecord]:
        """获取最近的消息记录"""
        with self._lock:
            records = sorted(self._records, key=lambda x: x.sent_at or "", reverse=True)
            if status:
                records = [r for r in records if r.status == status]
            return records[:limit]

    def get_failed_records(self, hours: int = 24) -> List[TelegramMessageRecord]:
        """获取失败的消息记录"""
        with self._lock:
            cutoff = (datetime.now() - timedelta(hours=hours)).isoformat()
            return [r for r in self._records if r.status == "failed" and r.sent_at and r.sent_at > cutoff]

    def get_stats(self) -> TelegramStats:
        """获取统计信息"""
        with self._lock:
            stats = TelegramStats()
            now = datetime.now()
            cutoff_24h = (now - timedelta(hours=24)).isoformat()
            total_count = 0
            total_duration = 0

            for record in self._records:
                if record.status == "sent":
                    total_count += 1
                    if record.sent_duration_ms:
                        total_duration += record.sent_duration_ms
                    stats.total_sent += 1
                    if record.sent_at and record.sent_at > cutoff_24h:
                        stats.last_24h_sent += 1
                    if not stats.last_message_at or (record.sent_at and record.sent_at > stats.last_message_at):
                        stats.last_message_at = record.sent_at
                elif record.status == "failed":
                    stats.total_failed += 1
                    if record.sent_at and record.sent_at > cutoff_24h:
                        stats.last_24h_failed += 1

            total = stats.total_sent + stats.total_failed
            if total > 0:
                stats.success_rate = (stats.total_sent / total) * 100
            if total_count > 0:
                stats.avg_duration_ms = total_duration / total_count

            sorted_records = sorted(self._records, key=lambda x: x.sent_at or "", reverse=True)
            consecutive = 0
            for record in sorted_records:
                if record.status == "failed":
                    consecutive += 1
                else:
                    break
            stats.consecutive_failures = consecutive
            return stats


# ================== 健康检查 ==================

class TelegramHealthChecker:
    """Telegram 健康检查器"""

    def __init__(self, token: str = None, chat_id: str = None):
        # 优先 TELEGRAM_BOT_TOKEN，兼容 TELEGRAM_TOKEN
        self.token = token or os.environ.get("TELEGRAM_BOT_TOKEN") or os.environ.get("TELEGRAM_TOKEN", "")
        self.chat_id = chat_id or os.environ.get("TELEGRAM_BOT_CHAT_ID") or os.environ.get("TELEGRAM_CHAT_ID", "")

        # 从配置文件加载
        config_path = os.path.join(AGENTDEVFLOW_ROOT, ".claude", "config", "bot_config.json")
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    config = json.load(f)
                    if not self.token:
                        self.token = config.get("telegram", {}).get("token", "")
                    if not self.chat_id:
                        self.chat_id = config.get("telegram", {}).get("chat_id", "")
            except Exception as e:
                logger.warning(f"加载 bot_config 失败: {e}")

        # 代理设置
        self.proxy = {
            "http": os.environ.get("http_proxy", ""),
            "https": os.environ.get("https_proxy", "")
        }
        if not self.proxy.get("http"):
            self.proxy = None

    def check_bot(self) -> Dict[str, Any]:
        """检查 Bot 状态"""
        if not self.token:
            return {"status": "unconfigured", "error": "Telegram token 未配置"}

        url = f"https://api.telegram.org/bot{self.token}/getMe"
        try:
            resp = requests.get(url, timeout=10, proxies=self.proxy)
            result = resp.json()
            if result.get("ok"):
                user = result.get("result", {})
                return {
                    "status": "healthy",
                    "bot_name": user.get("first_name", ""),
                    "bot_username": user.get("username", ""),
                    "is_bot": user.get("is_bot", False),
                }
            else:
                return {"status": "error", "error": result.get("description", "未知错误")}
        except requests.Timeout:
            return {"status": "timeout", "error": "API 请求超时"}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    def check_chat(self, chat_id: str = None) -> Dict[str, Any]:
        """检查 Chat 可用性"""
        if not self.token:
            return {"status": "unconfigured"}
        chat_id = chat_id or self.chat_id
        if not chat_id:
            return {"status": "no_chat_id"}

        url = f"https://api.telegram.org/bot{self.token}/getChat"
        try:
            resp = requests.get(url, params={"chat_id": chat_id}, timeout=10, proxies=self.proxy)
            result = resp.json()
            if result.get("ok"):
                chat = result.get("result", {})
                return {
                    "status": "accessible",
                    "chat_id": chat.get("id"),
                    "chat_type": chat.get("type"),
                    "chat_title": chat.get("title") or chat.get("first_name", ""),
                }
            else:
                return {"status": "inaccessible", "error": result.get("description", "未知错误")}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    def send_test_message(self, chat_id: str = None) -> Dict[str, Any]:
        """发送测试消息"""
        if not self.token or not (chat_id or self.chat_id):
            return {"status": "unconfigured", "success": False}

        chat_id = chat_id or self.chat_id
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        test_message = f"🔔 AgentDevFlow 测试消息\n\n时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n状态: 监控正常运行中 ✅"

        try:
            resp = requests.post(url, json={
                "chat_id": chat_id,
                "text": test_message,
                "parse_mode": "Markdown"
            }, timeout=30, proxies=self.proxy)
            result = resp.json()
            if result.get("ok"):
                return {"status": "success", "success": True, "message_id": result.get("result", {}).get("message_id")}
            else:
                return {"status": "failed", "success": False, "error": result.get("description", "发送失败")}
        except Exception as e:
            return {"status": "error", "success": False, "error": str(e)}

    def get_health_status(self, monitor: TelegramMonitor = None) -> Dict[str, Any]:
        """获取完整健康状态"""
        bot_status = self.check_bot()
        chat_status = self.check_chat()

        if bot_status.get("status") == "healthy":
            base_status = "healthy"
        elif bot_status.get("status") == "unconfigured":
            base_status = "unconfigured"
        else:
            base_status = "unhealthy"

        health = {
            "status": base_status,
            "bot": bot_status,
            "chat": chat_status,
            "timestamp": datetime.now().isoformat()
        }

        if monitor:
            stats = monitor.get_stats()
            health["stats"] = {
                "total_sent": stats.total_sent,
                "total_failed": stats.total_failed,
                "last_24h_sent": stats.last_24h_sent,
                "last_24h_failed": stats.last_24h_failed,
                "last_message_at": stats.last_message_at,
                "success_rate": round(stats.success_rate, 2),
                "avg_duration_ms": round(stats.avg_duration_ms, 2),
                "consecutive_failures": stats.consecutive_failures
            }
        return health


# ================== 全局实例 ==================

_monitor_instance: Optional[TelegramMonitor] = None
_health_checker_instance: Optional[TelegramHealthChecker] = None


def get_telegram_monitor() -> TelegramMonitor:
    """获取 Telegram 监控实例"""
    global _monitor_instance
    if _monitor_instance is None:
        _monitor_instance = TelegramMonitor()
    return _monitor_instance


def get_health_checker(token: str = None, chat_id: str = None) -> TelegramHealthChecker:
    """获取健康检查器实例"""
    global _health_checker_instance
    if _health_checker_instance is None:
        _health_checker_instance = TelegramHealthChecker(token, chat_id)
    return _health_checker_instance
