#!/usr/bin/env python3
"""
Issue → Task 路由脚本

读取 .claude/task_queue/ 目录下的 .task 文件，按 type 标签路由到对应角色。
输出路由日志到 .claude/results/。
"""

import os
import sys
import json
import re
import glob
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional


AGENTDEVFLOW_ROOT = Path(__file__).parent.parent.resolve()
TASK_QUEUE_DIR = AGENTDEVFLOW_ROOT / ".claude" / "task_queue"
RESULTS_DIR = AGENTDEVFLOW_ROOT / ".claude" / "results"
LOG_FILE = RESULTS_DIR / "routing.log"


# ===== 角色路由表 =====

ROLE_MAP = {
    "type/prd": "Product Manager",
    "type/tech": "架构师",
    "type/bug": "Engineer",
    "type/qa": "QA Engineer",
    "type/research": "研究支持",
    "type/release": "Platform/SRE",
    "type/anomaly": "Team Lead",
    "type/process": "PMO",
    "telegram": "Team Lead",  # Telegram 用户消息 -> Team Lead 处理
}


def parse_task_file(path: Path) -> Optional[Dict]:
    """解析 .task 文件"""
    try:
        content = path.read_text(encoding="utf-8")
        task = {}
        for line in content.splitlines():
            line = line.strip()
            if "=" in line:
                key, _, value = line.partition("=")
                task[key.strip()] = value.strip()
        return task
    except Exception as e:
        print(f"⚠️  解析失败 {path}: {e}")
        return None


def route_task(task: Dict) -> str:
    """根据 type 标签路由到角色"""
    task_type = task.get("type", "").lower().strip()
    role = ROLE_MAP.get(task_type, "Engineer")
    return role


def write_pending_comment(task: Dict, role: str, log_entry: Dict):
    """写入 pending comment 到 results 目录"""
    issue_id = task.get("issue_id", "unknown")
    title = task.get("title", "无标题")
    task_type = task.get("type", "").lower().strip()

    # 构建基础内容
    content_lines = [
        f"# Pending Task: {issue_id}\n",
        f"**Title:** {title}\n",
        f"**Type:** {task.get('type', 'N/A')}\n",
        f"**Priority:** {task.get('priority', 'N/A')}\n",
        f"**Labels:** {task.get('labels', 'N/A')}\n",
    ]

    # Telegram 类型特殊字段
    if task_type == "telegram":
        content_lines.extend([
            f"**Source:** telegram\n",
            f"**Chat ID:** {task.get('chat_id', 'N/A')}\n",
            f"**Username:** @{task.get('username', 'N/A')}\n",
            f"**First Name:** {task.get('first_name', 'N/A')}\n",
            f"**Issue URL:** (Telegram 消息，无需 GitHub Issue URL)\n",
        ])
    else:
        content_lines.extend([
            f"**Issue URL:** {task.get('issue_url', 'N/A')}\n",
            f"**Source:** agentdevflow\n",
        ])

    content_lines.extend([
        f"**Created:** {task.get('created_at', 'N/A')}\n",
        f"**Assigned Role:** {role}\n\n",
        f"---\n\n",
        f"## Content\n\n{task.get('content', 'N/A')}\n\n",
        f"---\n\n",
        f"## Routing Log\n\n",
        f"- **Routed at:** {log_entry['timestamp']}\n",
        f"- **Routed to:** {role}\n",
        f"- **Source file:** `{log_entry['source_file']}`\n",
    ])

    comment_file = RESULTS_DIR / f"pending_{issue_id}.md"
    comment_file.write_text("".join(content_lines), encoding="utf-8")


def route_all(verbose: bool = False) -> Dict[str, int]:
    """路由所有 task 文件"""
    TASK_QUEUE_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    # 初始化日志
    log_entries = []
    summary = {}

    task_files = sorted(TASK_QUEUE_DIR.glob("*.task"))
    if not task_files:
        print("📭 没有找到待路由的 task 文件")
        return summary

    for tf in task_files:
        task = parse_task_file(tf)
        if task is None:
            continue

        role = route_task(task)
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "source_file": str(tf.name),
            "issue_id": task.get("issue_id", "unknown"),
            "title": task.get("title", "无标题"),
            "type": task.get("type", "unknown"),
            "priority": task.get("priority", "unknown"),
            "routed_to": role,
        }
        log_entries.append(log_entry)

        # 写入 pending comment
        write_pending_comment(task, role, log_entry)

        summary[role] = summary.get(role, 0) + 1

        if verbose:
            print(f"  [{role}] {task.get('issue_id', '?')} - {task.get('title', '无标题')[:50]}")

    # 写入路由日志
    log_data = {
        "routed_at": datetime.now().isoformat(),
        "total": len(log_entries),
        "summary": summary,
        "entries": log_entries,
    }
    with open(LOG_FILE, 'w', encoding='utf-8') as f:
        json.dump(log_data, f, ensure_ascii=False, indent=2)

    return summary


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Issue → Task 路由")
    parser.add_argument("--verbose", "-v", action="store_true", help="详细输出")
    parser.add_argument("--dry-run", action="store_true", help="仅显示路由结果，不写入文件")
    args = parser.parse_args()

    if args.verbose:
        print(f"📂 Task Queue: {TASK_QUEUE_DIR}")
        print(f"📂 Results: {RESULTS_DIR}\n")

    task_files = sorted(TASK_QUEUE_DIR.glob("*.task"))
    if not task_files:
        print("📭 没有找到待路由的 task 文件")
        sys.exit(0)

    print(f"📋 找到 {len(task_files)} 个 task 文件，开始路由...\n")

    if args.dry_run:
        # 仅预览路由结果
        for tf in task_files:
            task = parse_task_file(tf)
            if task:
                role = route_task(task)
                print(f"  [{role}] {task.get('issue_id', '?')} - {task.get('title', '无标题')[:60]}")
        sys.exit(0)

    summary = route_all(verbose=args.verbose)

    print(f"\n✅ 路由完成，共 {len(task_files)} 个任务\n")
    for role, count in sorted(summary.items(), key=lambda x: -x[1]):
        print(f"  {role}: {count} 个")

    print(f"\n📝 路由日志: {LOG_FILE}")
