#!/usr/bin/env python3
"""
Task 状态更新脚本

更新 .claude/task_queue/*.task 文件的 owner 和 status 字段。
支持 claim（领取）、complete（完成）、block（阻塞）等状态操作。
"""

import os
import sys
import glob
from datetime import datetime
from pathlib import Path
from typing import Optional, List


AGENTDEVFLOW_ROOT = Path(__file__).parent.parent.resolve()
TASK_QUEUE_DIR = AGENTDEVFLOW_ROOT / ".claude" / "task_queue"


# ===== Task 文件字段 =====

TASK_FIELDS = [
    "source",
    "issue_id",
    "type",
    "priority",
    "title",
    "labels",
    "created_at",
    "issue_url",
    "owner",
    "status",
    "blocked_by",
    "blocks",
    "updated_at",
]


def parse_task_file(path: Path) -> dict:
    """解析 task 文件"""
    content = path.read_text(encoding="utf-8")
    task = {}
    for line in content.splitlines():
        line = line.strip()
        if "=" in line:
            key, _, value = line.partition("=")
            task[key.strip()] = value.strip()
    return task


def write_task_file(path: Path, task: dict):
    """写入 task 文件"""
    lines = []
    for field in TASK_FIELDS:
        value = task.get(field, "")
        if value:
            lines.append(f"{field}={value}")
        elif field in task:
            lines.append(f"{field}=")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def list_tasks(pattern: str = "*", status_filter: Optional[str] = None) -> List[Path]:
    """列出 task 文件"""
    TASK_QUEUE_DIR.mkdir(parents=True, exist_ok=True)
    files = sorted(TASK_QUEUE_DIR.glob(f"{pattern}.task"))
    if status_filter:
        filtered = []
        for f in files:
            task = parse_task_file(f)
            if task.get("status") == status_filter:
                filtered.append(f)
        return filtered
    return files


def show_task(path: Path):
    """显示 task 详情"""
    task = parse_task_file(path)
    print(f"\n📋 {path.name}")
    print(f"  issue_id:  {task.get('issue_id', 'N/A')}")
    print(f"  type:      {task.get('type', 'N/A')}")
    print(f"  priority:  {task.get('priority', 'N/A')}")
    print(f"  title:     {task.get('title', 'N/A')}")
    print(f"  labels:    {task.get('labels', 'N/A')}")
    print(f"  owner:     {task.get('owner', 'N/A')}")
    print(f"  status:    {task.get('status', 'N/A')}")
    print(f"  blocked_by:{task.get('blocked_by', 'N/A')}")
    print(f"  created:   {task.get('created_at', 'N/A')}")
    print(f"  updated:   {task.get('updated_at', 'N/A')}")


def cmd_claim(task_id: str, owner: str):
    """领取任务"""
    files = list_tasks(f"*{task_id}*")
    if not files:
        print(f"❌ 未找到任务: {task_id}")
        return False
    now = datetime.now().isoformat()
    for f in files:
        task = parse_task_file(f)
        task["owner"] = owner
        task["status"] = "in_progress"
        task["updated_at"] = now
        write_task_file(f, task)
        print(f"✅ 已领取: {f.name} → {owner}")
    return True


def cmd_complete(task_id: str):
    """完成任务"""
    files = list_tasks(f"*{task_id}*")
    if not files:
        print(f"❌ 未找到任务: {task_id}")
        return False
    now = datetime.now().isoformat()
    for f in files:
        task = parse_task_file(f)
        task["status"] = "completed"
        task["updated_at"] = now
        write_task_file(f, task)
        print(f"✅ 已完成: {f.name}")
    return True


def cmd_block(task_id: str, blocked_by: str):
    """标记阻塞"""
    files = list_tasks(f"*{task_id}*")
    if not files:
        print(f"❌ 未找到任务: {task_id}")
        return False
    now = datetime.now().isoformat()
    for f in files:
        task = parse_task_file(f)
        task["status"] = "blocked"
        task["blocked_by"] = blocked_by
        task["updated_at"] = now
        write_task_file(f, task)
        print(f"🔒 已阻塞: {f.name} (blocked_by: {blocked_by})")
    return True


def cmd_unblock(task_id: str):
    """解除阻塞"""
    files = list_tasks(f"*{task_id}*")
    if not files:
        print(f"❌ 未找到任务: {task_id}")
        return False
    now = datetime.now().isoformat()
    for f in files:
        task = parse_task_file(f)
        task["status"] = "in_progress"
        task["blocked_by"] = ""
        task["updated_at"] = now
        write_task_file(f, task)
        print(f"🔓 已解除阻塞: {f.name}")
    return True


def cmd_set_field(task_id: str, field: str, value: str):
    """设置字段"""
    files = list_tasks(f"*{task_id}*")
    if not files:
        print(f"❌ 未找到任务: {task_id}")
        return False
    now = datetime.now().isoformat()
    for f in files:
        task = parse_task_file(f)
        task[field] = value
        task["updated_at"] = now
        write_task_file(f, task)
        print(f"✅ 已更新: {f.name} [{field}] = {value}")
    return True


def cmd_list(pattern: str = "*", status_filter: Optional[str] = None):
    """列出任务"""
    files = list_tasks(pattern, status_filter)
    if not files:
        print(f"📭 没有找到任务: pattern={pattern}, status={status_filter}")
        return

    print(f"\n📋 任务列表 ({len(files)} 个)\n")
    for f in files:
        task = parse_task_file(f)
        status = task.get("status", "N/A")
        owner = task.get("owner", "—")
        issue_id = task.get("issue_id", "?")
        title = task.get("title", "无标题")
        status_icon = {
            "pending": "⏳",
            "in_progress": "🔄",
            "completed": "✅",
            "blocked": "🔒",
        }.get(status, "❓")
        print(f"  {status_icon} [{status:12}] {issue_id:>6} | {owner:>12} | {title[:50]}")
    print()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Task 状态更新")
    sub = parser.add_subparsers(dest="cmd", required=True)

    # list
    p_list = sub.add_parser("list", help="列出任务")
    p_list.add_argument("--pattern", default="*", help="文件名匹配")
    p_list.add_argument("--status", help="按状态过滤 (pending/in_progress/completed/blocked)")

    # claim
    p_claim = sub.add_parser("claim", help="领取任务")
    p_claim.add_argument("task_id", help="任务 ID（部分匹配）")
    p_claim.add_argument("owner", help="领取人")

    # complete
    p_complete = sub.add_parser("complete", help="完成任务")
    p_complete.add_argument("task_id", help="任务 ID（部分匹配）")

    # block
    p_block = sub.add_parser("block", help="标记阻塞")
    p_block.add_argument("task_id", help="任务 ID（部分匹配）")
    p_block.add_argument("blocked_by", help="阻塞原因/依赖")

    # unblock
    p_unblock = sub.add_parser("unblock", help="解除阻塞")
    p_unblock.add_argument("task_id", help="任务 ID（部分匹配）")

    # set
    p_set = sub.add_parser("set", help="设置字段")
    p_set.add_argument("task_id", help="任务 ID（部分匹配）")
    p_set.add_argument("field", help="字段名")
    p_set.add_argument("value", help="字段值")

    # show
    p_show = sub.add_parser("show", help="显示任务详情")
    p_show.add_argument("task_id", help="任务 ID（部分匹配）")

    args = parser.parse_args()

    if args.cmd == "list":
        cmd_list(args.pattern, args.status)
    elif args.cmd == "claim":
        cmd_claim(args.task_id, args.owner)
    elif args.cmd == "complete":
        cmd_complete(args.task_id)
    elif args.cmd == "block":
        cmd_block(args.task_id, args.blocked_by)
    elif args.cmd == "unblock":
        cmd_unblock(args.task_id)
    elif args.cmd == "set":
        cmd_set_field(args.task_id, args.field, args.value)
    elif args.cmd == "show":
        files = list_tasks(f"*{args.task_id}*")
        if not files:
            print(f"❌ 未找到任务: {args.task_id}")
        elif len(files) == 1:
            show_task(files[0])
        else:
            print(f"⚠️  匹配到多个任务:")
            for f in files:
                print(f"  - {f.name}")
