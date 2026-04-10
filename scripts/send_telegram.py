#!/usr/bin/env python3
"""
Telegram 消息推送工具（通用版）

从 AgentDevFlow 原项目中迁移，剥离业务逻辑（回测报告、研发日报），保留通用消息推送
"""

import os
import sys
import json
import requests
from pathlib import Path

AGENTDEVFLOW_ROOT = Path(__file__).parent.parent.resolve()
CONFIG_FILE = AGENTDEVFLOW_ROOT / ".claude" / "config" / "bot_config.json"


def get_token():
    """获取 Token"""
    # 1. 环境变量
    token = os.environ.get("TELEGRAM_TOKEN", "")
    if token:
        return token
    # 2. 配置文件
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE) as f:
            config = json.load(f)
            return config.get("telegram", {}).get("token", "")
    return ""


def get_chat_id():
    """获取 chat_id（通过 getUpdates）"""
    token = get_token()
    if not token:
        print("❌ 未配置 Telegram Token")
        return None
    url = f"https://api.telegram.org/bot{token}/getUpdates"
    try:
        resp = requests.get(url, timeout=10)
        data = resp.json()
        if data.get('ok') and data.get('result'):
            return data['result'][-1]['message']['chat']['id']
    except:
        pass
    return None


def load_config():
    """加载配置"""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE) as f:
            return json.load(f)
    return {}


def save_config(config):
    """保存配置"""
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)


def send_message(text, chat_id=None, parse_mode="Markdown"):
    """发送消息到 Telegram"""
    if not chat_id:
        chat_id = load_config().get("telegram", {}).get("chat_id")

    if not chat_id:
        print("❌ 未配置 chat_id")
        return False

    token = get_token()
    if not token:
        print("❌ 未配置 Telegram Token")
        return False

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        resp = requests.post(url, json={
            "chat_id": chat_id,
            "text": text,
            "parse_mode": parse_mode
        }, timeout=30)
        result = resp.json()
        if result.get("ok"):
            print(f"✅ 消息发送成功到 {chat_id}")
            return True
        else:
            print(f"❌ 发送失败: {result}")
            return False
    except Exception as e:
        print(f"❌ 发送失败: {e}")
        return False


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Telegram 消息推送（通用版）")
    parser.add_argument("--chat-id", help="指定 chat_id")
    parser.add_argument("--setup", action="store_true", help="设置 chat_id")
    parser.add_argument("--text", type=str, help="发送自定义文本")

    args = parser.parse_args()

    if args.setup:
        chat_id = get_chat_id()
        if chat_id:
            config = load_config()
            if "telegram" not in config:
                config["telegram"] = {}
            config["telegram"]["chat_id"] = chat_id
            save_config(config)
            print(f"✅ Chat ID 已保存: {chat_id}")
        else:
            print("❌ 获取 chat_id 失败，请先发送 /start 给机器人")

    elif args.text:
        send_message(args.text, args.chat_id)

    else:
        print("用法:")
        print("  --setup         设置 chat_id")
        print("  --text 'xxx'    发送自定义消息")
