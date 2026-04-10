"""
Telegram 机器人服务器（通用版）

从 hedge-ai/hedge_ai/telegram/bot_server.py 迁移
剥离：交易信号推送、策略推送、回测报告推送等业务逻辑
保留：通用消息收发、健康检查、重试机制、轮询循环
"""

import os
import json
import time
import logging
import threading
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Callable

import requests


AGENTDEVFLOW_ROOT = Path(__file__).parent.parent.parent.resolve()
LOG_FILE = AGENTDEVFLOW_ROOT / "logs" / "telegram_bot.log"


def _init_logging():
    """初始化日志"""
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    handler = logging.FileHandler(LOG_FILE)
    handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logging.getLogger().addHandler(handler)
    logging.getLogger().setLevel(logging.INFO)
    logging.info(f"[BOT SERVER 启动] 日志初始化完成 at {datetime.now().isoformat()}")


_init_logging()
logger = logging.getLogger(__name__)


class TelegramBotServer:
    """Telegram Bot 服务器（轮询模式）"""

    def __init__(self, token: str = None, config_path: str = None):
        # 加载 Token
        self.token = token or os.environ.get("TELEGRAM_TOKEN", "")
        if not self.token:
            config_file = AGENTDEVFLOW_ROOT / ".claude" / "config" / "bot_config.json"
            if config_file.exists():
                with open(config_file) as f:
                    config = json.load(f)
                    self.token = config.get("telegram", {}).get("token", "")

        if not self.token:
            raise ValueError("未配置 Telegram Bot Token")

        self.api_url = f"https://api.telegram.org/bot{self.token}"

        # 加载 chat_ids
        self.chat_ids: List[int] = []
        config_file = AGENTDEVFLOW_ROOT / ".claude" / "config" / "bot_config.json"
        if config_file.exists():
            with open(config_file) as f:
                config = json.load(f)
                raw = config.get("telegram", {}).get("chat_ids", [])
                if isinstance(raw, list):
                    self.chat_ids = raw
                elif isinstance(raw, str):
                    self.chat_ids = [raw]

        # 状态
        self.is_running = False
        self.offset: Optional[int] = None
        self.polling_timeout = 60

        # 已授权的用户（动态添加）
        self.authorized_chats: List[int] = list(self.chat_ids)

        # 回调
        self.on_message: Optional[Callable] = None
        self.on_command: Optional[Callable] = None

    # ===== API 方法 =====

    def send_message(
        self,
        chat_id: int,
        text: str,
        parse_mode: str = "Markdown",
        reply_markup: Dict = None
    ) -> Optional[Dict]:
        """发送消息"""
        try:
            url = f"{self.api_url}/sendMessage"
            data = {
                "chat_id": chat_id,
                "text": text,
            }
            if parse_mode:
                data["parse_mode"] = parse_mode
            if reply_markup:
                data["reply_markup"] = reply_markup

            resp = requests.post(url, json=data, timeout=30)
            result = resp.json()

            if result.get("ok"):
                return result.get("result")
            else:
                logger.error(f"发送消息失败: {result}")
                return None
        except Exception as e:
            logger.error(f"发送消息异常: {e}")
            return None

    def get_updates(self, timeout: int = None) -> List[Dict]:
        """获取更新"""
        try:
            url = f"{self.api_url}/getUpdates"
            data = {"timeout": timeout or self.polling_timeout}
            if self.offset:
                data["offset"] = self.offset

            resp = requests.post(url, json=data, timeout=(timeout or self.polling_timeout) + 10)
            if resp.status_code == 409:
                logger.warning("Telegram 409 Conflict: 等待其他进程释放...")
                time.sleep(5)
                data["offset"] = self.offset + 1 if self.offset else None
                resp = requests.post(url, json=data, timeout=(timeout or self.polling_timeout) + 10)

            result = resp.json()
            if result.get("ok"):
                updates = result.get("result", [])
                if updates:
                    self.offset = updates[-1].get("update_id", 0) + 1
                return updates
            return []
        except Exception as e:
            logger.error(f"获取更新失败: {e}")
            return []

    def set_commands(self) -> bool:
        """设置命令菜单"""
        commands = [
            {"command": "start", "description": "启动机器人"},
            {"command": "help", "description": "帮助信息"},
            {"command": "status", "description": "系统状态"},
            {"command": "health", "description": "健康检查"},
        ]
        try:
            url = f"{self.api_url}/setMyCommands"
            resp = requests.post(url, json={"commands": commands}, timeout=10)
            return resp.status_code == 200
        except Exception as e:
            logger.error(f"设置命令菜单失败: {e}")
            return False

    def answer_callback(self, callback_query_id: str, text: str = None, show_alert: bool = False):
        """回答回调查询"""
        try:
            url = f"{self.api_url}/answerCallbackQuery"
            data = {"callback_query_id": callback_query_id}
            if text:
                data["text"] = text
            data["show_alert"] = show_alert
            requests.post(url, json=data, timeout=10)
        except Exception as e:
            logger.error(f"回答回调失败: {e}")

    # ===== 消息处理 =====

    def _process_update(self, update: Dict):
        """处理更新"""
        update_id = update.get("update_id", 0)
        message = update.get("message", {})
        chat_id = message.get("chat", {}).get("id")
        text = message.get("text", "")
        first_name = message.get("from", {}).get("first_name", "")

        logger.info(f"[收到消息] update_id={update_id} chat_id={chat_id} text={text}")

        # 自动授权发送过消息的用户
        if chat_id and chat_id not in self.authorized_chats:
            self.authorized_chats.append(chat_id)

        # 如果配置了 chat_ids 白名单，则检查授权
        if self.chat_ids and chat_id not in self.chat_ids:
            logger.warning(f"未授权的用户: {chat_id}")
            return

        # 解析命令
        response = None
        if text:
            if text.startswith("/start"):
                response = "👋 AgentDevFlow Bot 已启动。发送 /help 查看可用命令。"
            elif text.startswith("/help"):
                response = (
                    "📋 *可用命令*\n\n"
                    "/start - 启动机器人\n"
                    "/help - 帮助信息\n"
                    "/status - 系统状态\n"
                    "/health - 健康检查\n\n"
                    "也可以直接发送文本消息。"
                )
            elif text.startswith("/status"):
                response = self._get_status_text()
            elif text.startswith("/health"):
                response = self._health_check_text()

        # 触发回调
        if response:
            self.send_message(chat_id, response)

        if self.on_message:
            self.on_message(update, response)

    def _get_status_text(self) -> str:
        """获取状态文本"""
        return (
            "✅ *AgentDevFlow Bot 运行中*\n\n"
            f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"授权用户: {len(self.authorized_chats)}\n"
            f"模式: polling"
        )

    def _health_check_text(self) -> str:
        """健康检查文本"""
        try:
            url = f"{self.api_url}/getMe"
            resp = requests.get(url, timeout=10)
            result = resp.json()
            if result.get("ok"):
                bot_info = result.get("result", {})
                return (
                    "✅ *Bot 健康*\n\n"
                    f"名称: {bot_info.get('first_name', '')}\n"
                    f"用户名: @{bot_info.get('username', '')}\n"
                    f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                )
        except Exception as e:
            pass
        return "⚠️ *Bot 健康检查失败*"

    def _polling_loop(self):
        """轮询循环"""
        logger.info("Telegram Bot 轮询启动...")
        retry_count = 0
        max_retries = 5

        while self.is_running:
            try:
                updates = self.get_updates(timeout=self.polling_timeout)
                if updates:
                    retry_count = 0
                    for update in updates:
                        self._process_update(update)
            except KeyboardInterrupt:
                logger.info("收到中断信号，停止轮询")
                break
            except Exception as e:
                retry_count += 1
                logger.error(f"轮询异常 ({retry_count}/{max_retries}): {e}")
                if retry_count >= max_retries:
                    logger.warning("连续失败，重置offset...")
                    self.offset = None
                    retry_count = 0
                wait_time = min(5 * retry_count, 30)
                time.sleep(wait_time)

        logger.info("Telegram Bot 轮询已停止")

    # ===== 生命周期 =====

    def start(self):
        """启动 Bot 服务器"""
        if self.is_running:
            logger.warning("Bot 已在运行中")
            return
        self.set_commands()
        self.is_running = True
        self.polling_thread = threading.Thread(target=self._polling_loop, daemon=True)
        self.polling_thread.start()
        logger.info("Telegram Bot 服务器已启动")

    def stop(self):
        """停止 Bot 服务器"""
        self.is_running = False
        logger.info("Telegram Bot 服务器已停止")

    # ===== 便捷方法 =====

    def send_to_all(self, message: str, parse_mode: str = "Markdown"):
        """发送消息给所有授权用户"""
        for chat_id in (self.chat_ids or self.authorized_chats):
            self.send_message(chat_id, message, parse_mode=parse_mode)


# ===== 全局实例 =====

_bot_server_instance: Optional["TelegramBotServer"] = None


def get_bot_server(token: str = None) -> "TelegramBotServer":
    """获取 Bot 服务器实例"""
    global _bot_server_instance
    if _bot_server_instance is None:
        _bot_server_instance = TelegramBotServer(token)
    return _bot_server_instance


def run_bot_server(token: str = None):
    """运行 Bot 服务器"""
    if not token:
        token = os.environ.get("TELEGRAM_TOKEN", "")
        config_file = AGENTDEVFLOW_ROOT / ".claude" / "config" / "bot_config.json"
        if not token and config_file.exists():
            with open(config_file) as f:
                config = json.load(f)
                token = config.get("telegram", {}).get("token", "")

    if not token:
        print("请设置 TELEGRAM_TOKEN 环境变量或传入 token 参数")
        return

    bot = TelegramBotServer(token)
    bot.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("正在停止 Bot...")
        bot.stop()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="AgentDevFlow Telegram Bot 服务器")
    parser.add_argument("--token", type=str, help="Telegram Bot Token")
    args = parser.parse_args()
    run_bot_server(token=args.token)
