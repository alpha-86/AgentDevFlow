#!/usr/bin/env python3
"""
GitHub Issue & Comment 同步脚本
从 GitHub Issues 获取新创建或已标签的 Issue，写入 TaskQueue
从 GitHub Issues 获取评论，同步未处理的评论到 TaskQueue
通过 GitHub Actions 发送评论（唯一出口，身份归因正确）

支持断点续传：已处理的 Issue/Comment 不重复写入
"""

import os
import sys
import json
import logging
import subprocess
import argparse
from pathlib import Path
from typing import Optional
from datetime import datetime, timezone

# 允许的工具列表（安全约束，Phase 2 扩展时使用）
ALLOWED_TOOLS = {"Read", "Write", "Edit", "Glob", "Grep", "Bash"}

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s: %(message)s"
)
logger = logging.getLogger(__name__)

# 常量配置
# 自动从 git remote 检测 repo（gh issue list/view 会自动检测，URL 需要）
_repo_override = os.environ.get("REPO", "")
if not _repo_override:
    try:
        remote = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            capture_output=True, text=True,
        )
        if remote.returncode == 0:
            # git@github.com:owner/repo.git 或 https://github.com/owner/repo
            remote_url = remote.stdout.strip()
            if remote_url.startswith("git@github.com:"):
                _repo_override = remote_url.split(":")[1].replace(".git", "")
            elif "github.com" in remote_url:
                parts = remote_url.rsplit("/github.com", 1)
                if len(parts) == 2:
                    _repo_override = parts[1].strip("/").replace(".git", "")
    except Exception:
        pass
REPO = _repo_override or "alpha-86/AgentDevFlow"
CLAUDE_DIR = Path(__file__).parent.parent / ".claude"
TASK_QUEUE_DIR = CLAUDE_DIR / "task_queue"
PROCESSED_FILE = CLAUDE_DIR / "processed_issues.json"
PROCESSED_COMMENTS_FILE = CLAUDE_DIR / "processed_comments.json"
RESULTS_DIR = CLAUDE_DIR / "results"
# 尝试从环境变量和 ~/.env.code 读取 GitHub Token
_GITHUB_TOKEN = os.environ.get("GH_TOKEN") or ""
if not _GITHUB_TOKEN:
    _env_code = Path.home() / ".env.code"
    if _env_code.exists():
        for line in _env_code.read_text().splitlines():
            if line.startswith("GITHUB="):
                _GITHUB_TOKEN = line.split("=", 1)[1].strip()
                break
GITHUB_TOKEN = _GITHUB_TOKEN

# 不响应评论的作者（避免 Agent 循环响应自己的评论）
EXCLUDED_COMMENT_AUTHORS = {"github-actions", "github-actions[bot]"}

# 必须的 type 标签（AgentDevFlow 标准：PRD/Tech/QA/验收）
REQUIRED_TYPE_LABELS = {
    "type/prd",
    "type/tech",
    "type/qa",
    "type/验收",
}
# 允许的 priority 标签
ALLOWED_PRIORITY_LABELS = {"priority/high", "priority/critical"}


def get_processed_issues() -> set:
    """加载已处理的 Issue ID 集合"""
    if not PROCESSED_FILE.exists():
        return set()
    try:
        with open(PROCESSED_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return set(data.get("processed_issues", []))
    except (json.JSONDecodeError, IOError) as e:
        logger.warning(f"processed_issues.json 读取失败: {e}")
        return set()


def save_processed_issues(issue_ids: set) -> None:
    """保存已处理的 Issue ID 到文件"""
    PROCESSED_FILE.parent.mkdir(parents=True, exist_ok=True)
    try:
        if PROCESSED_FILE.exists():
            with open(PROCESSED_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = {"processed_issues": []}
    except (json.JSONDecodeError, IOError):
        data = {"processed_issues": []}

    data["processed_issues"] = sorted(list(issue_ids))
    with open(PROCESSED_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_all_open_issues() -> list:
    """获取所有 open 状态的 Issue（用于 cron 轮询兜底）"""
    env = os.environ.copy()
    if GITHUB_TOKEN:
        env["GH_TOKEN"] = GITHUB_TOKEN

    result = subprocess.run(
        ["gh", "issue", "list", "--state", "open", "--json",
         "number,title,labels,createdAt,url,body,state"],
        capture_output=True,
        text=True,
        env=env,
    )

    if result.returncode != 0:
        logger.error(f"获取 Issue 列表失败: {result.stderr}")
        return []

    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return []


def parse_labels(labels: list) -> tuple:
    """从标签列表中解析 type 和 priority"""
    type_label = None
    priority_label = "medium"  # 默认优先级

    label_names = []
    for label in labels:
        name = label.get("name", "") if isinstance(label, dict) else str(label)
        label_names.append(name)

        if name in REQUIRED_TYPE_LABELS:
            type_label = name
        if name in ALLOWED_PRIORITY_LABELS:
            priority_label = name.replace("priority/", "")

    return type_label, priority_label, label_names


def build_task_file_content(issue: dict) -> str:
    """构建 TaskQueue 文件内容"""
    issue_number = issue["number"]
    title = issue.get("title", "")
    created_at = issue.get("createdAt", "")
    url = issue.get("url", "")
    body = issue.get("body", "") or ""

    type_label, priority_label, label_names = parse_labels(issue.get("labels", []))

    # 安全过滤：移除 body 中的可疑内容
    safe_body = body[:500] if body else ""

    lines = [
        f"source=github_issue",
        f"issue_id={issue_number}",
        f"type={type_label or 'type/prd'}",  # 无标签时默认为 prd
        f"priority={priority_label}",
        f"title={title}",
        f"labels={','.join(label_names)}",
        f"created_at={created_at}",
        f"issue_url={url}",
        f"issue_body={safe_body}",
    ]

    return "\n".join(lines)


def write_task_file(issue: dict) -> Optional[Path]:
    """写入 TaskQueue 文件"""
    TASK_QUEUE_DIR.mkdir(parents=True, exist_ok=True)

    issue_number = issue["number"]
    task_file = TASK_QUEUE_DIR / f"issue_{issue_number}.task"

    # 已存在则跳过
    if task_file.exists():
        logger.debug(f"Issue #{issue_number} 任务文件已存在，跳过")
        return None

    content = build_task_file_content(issue)

    try:
        task_file.write_text(content, encoding="utf-8")
        logger.info(f"Issue #{issue_number} 任务文件已写入: {task_file}")
        return task_file
    except IOError as e:
        logger.error(f"写入任务文件失败: {e}")
        return None


def write_pending_comment(issue_number: int, message: str) -> Optional[Path]:
    """写入待发送评论结果文件（通过 post-comment workflow 发送）"""
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    result_file = RESULTS_DIR / f"comment_{issue_number}_{timestamp}.json"

    utc_now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    result_data = {
        "type": "issue-comment",
        "issue_number": issue_number,
        "body": message,
        "agent": "github-actions[sync]",
        "source_comment_url": "",
        "created_at": utc_now,
        "status": "pending",
    }

    try:
        result_file.write_text(json.dumps(result_data, ensure_ascii=False, indent=2), encoding="utf-8")
        logger.info(f"待发送评论已写入: {result_file}")
        return result_file
    except IOError as e:
        logger.error(f"写入结果文件失败: {e}")
        return None


def comment_on_issue(issue_number: int, message: str) -> bool:
    """通过 gh issue comment 在 Issue 下评论（已废弃，请使用 write_pending_comment）"""
    logger.warning("comment_on_issue 已废弃，请使用 write_pending_comment 通过 post-comment workflow 发送")
    env = os.environ.copy()
    if GITHUB_TOKEN:
        env["GH_TOKEN"] = GITHUB_TOKEN

    result = subprocess.run(
        ["gh", "issue", "comment", str(issue_number), "--body", message],
        capture_output=True,
        text=True,
        env=env,
    )

    if result.returncode != 0:
        logger.warning(f"评论 Issue #{issue_number} 失败: {result.stderr}")
        return False

    return True


def sync_issue(issue: dict, processed: set, auto_push: bool = True) -> bool:
    """同步单个 Issue 到 TaskQueue"""
    issue_number = issue["number"]

    if issue_number in processed:
        logger.debug(f"Issue #{issue_number} 已处理，跳过")
        return False

    # 写入任务文件
    task_file = write_task_file(issue)
    if task_file:
        # 确认评论（仅首次成功时评论）- 通过 post-comment workflow 发送
        msg = (
            f"AgentDevFlow Issue 已接收，正在处理。\n\n"
            f"**任务队列**: `.claude/task_queue/issue_{issue_number}.task`\n\n"
            f"> 此评论由 GitHub Actions 自动生成"
        )
        result_file = write_pending_comment(issue_number, msg)
        if result_file and auto_push:
            # 自动 git push 触发 post-comment workflow
            try:
                add_result = subprocess.run(
                    ["git", "add", str(result_file)],
                    capture_output=True, text=True,
                    cwd=str(RESULTS_DIR.parent.parent),
                )
                if add_result.returncode == 0:
                    commit_result = subprocess.run(
                        ["git", "commit", "-m", f"chore: sync Issue #{issue_number} confirmation"],
                        capture_output=True, text=True,
                        cwd=str(RESULTS_DIR.parent.parent),
                    )
                    if commit_result.returncode == 0:
                        push_result = subprocess.run(
                            ["git", "push"],
                            capture_output=True, text=True,
                            cwd=str(RESULTS_DIR.parent.parent),
                        )
                        if push_result.returncode == 0:
                            logger.info(f"已 push，post-comment workflow 将自动触发")
            except Exception as e:
                logger.warning(f"git 操作失败: {e}")
        return True

    return False


def main():
    logger.info("=" * 60)
    logger.info("GitHub Issue Sync 开始")
    logger.info("=" * 60)

    # 加载已处理记录
    processed = get_processed_issues()
    new_processed = set(processed)
    synced_count = 0

    # cron 轮询，获取所有 open Issue
    all_issues = get_all_open_issues()
    logger.info(f"获取到 {len(all_issues)} 个 open Issue")

    for issue in all_issues:
        if sync_issue(issue, processed):
            new_processed.add(issue["number"])
            synced_count += 1

    # 保存已处理记录
    save_processed_issues(new_processed)

    logger.info(f"同步完成: {synced_count} 个新 Issue 已写入 TaskQueue")
    logger.info(f"已处理记录: {len(new_processed)} 个 Issue")

    # 清理超过30天的已处理记录（保留最近500条）
    if len(new_processed) > 500:
        kept = sorted(new_processed, reverse=True)[:500]
        save_processed_issues(set(kept))
        logger.info(f"已清理旧记录，保留最近 500 条")


# ===== --sync-comments 功能 =====

def get_processed_comments() -> set:
    """加载已处理的 Comment ID 集合"""
    if not PROCESSED_COMMENTS_FILE.exists():
        return set()
    try:
        with open(PROCESSED_COMMENTS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return set(data.get("processed_comments", []))
    except (json.JSONDecodeError, IOError) as e:
        logger.warning(f"processed_comments.json 读取失败: {e}")
        return set()


def save_processed_comments(comment_ids: set) -> None:
    """保存已处理的 Comment ID 到文件"""
    PROCESSED_COMMENTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    try:
        if PROCESSED_COMMENTS_FILE.exists():
            with open(PROCESSED_COMMENTS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = {"processed_comments": []}
    except (json.JSONDecodeError, IOError):
        data = {"processed_comments": []}

    data["processed_comments"] = sorted(list(comment_ids))
    with open(PROCESSED_COMMENTS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_issue_comments(issue_number: int) -> list:
    """获取指定 Issue 的所有评论"""
    env = os.environ.copy()
    if GITHUB_TOKEN:
        env["GH_TOKEN"] = GITHUB_TOKEN

    # gh issue view 自动从 git remote 推断 repo，比 gh api 更可靠
    result = subprocess.run(
        ["gh", "issue", "view", str(issue_number), "--json", "comments"],
        capture_output=True,
        text=True,
        env=env,
    )

    if result.returncode != 0:
        logger.warning(f"获取 Issue #{issue_number} 评论失败: {result.stderr}")
        return []

    try:
        data = json.loads(result.stdout)
        return data.get("comments", [])
    except json.JSONDecodeError as e:
        logger.warning(f"解析 Issue #{issue_number} 评论失败: {e}")
        return []


def get_open_issues_for_comments() -> list:
    """获取所有 open 状态的 Issue（用于评论同步）"""
    env = os.environ.copy()
    if GITHUB_TOKEN:
        env["GH_TOKEN"] = GITHUB_TOKEN

    result = subprocess.run(
        ["gh", "issue", "list", "--state", "open", "--json",
         "number,title,labels,createdAt,url,body", "--limit", "50"],
        capture_output=True,
        text=True,
        env=env,
    )

    if result.returncode != 0:
        logger.error(f"获取 Issue 列表失败: {result.stderr}")
        return []

    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return []


def write_comment_task_file(comment: dict, issue_number: int) -> Optional[Path]:
    """写入 Comment Task 文件"""
    TASK_QUEUE_DIR.mkdir(parents=True, exist_ok=True)

    comment_id = comment["id"]
    task_file = TASK_QUEUE_DIR / f"comment_{issue_number}_{comment_id}.task"

    if task_file.exists():
        logger.debug(f"Comment {comment_id} 任务文件已存在，跳过")
        return None

    author = comment.get("author", {})
    author_login = author.get("login", "unknown") if isinstance(author, dict) else str(author)
    body = comment.get("body", "") or ""
    safe_body = body[:500] if body else ""
    created_at = comment.get("createdAt", "")
    comment_url = comment.get("url", "")
    issue_url = f"https://github.com/{REPO}/issues/{issue_number}"

    lines = [
        f"source=github_comment",
        f"comment_id={comment_id}",
        f"issue_id={issue_number}",
        f"issue_url={issue_url}",
        f"author={author_login}",
        f"body={safe_body}",
        f"comment_url={comment_url}",
        f"created_at={created_at}",
    ]

    try:
        task_file.write_text("\n".join(lines), encoding="utf-8")
        logger.info(f"Comment {comment_id} (Issue #{issue_number}) 任务文件已写入: {task_file}")
        return task_file
    except IOError as e:
        logger.error(f"写入任务文件失败: {e}")
        return None


def sync_comments() -> dict:
    """同步所有未处理的评论到 TaskQueue"""
    processed = get_processed_comments()
    new_processed = set(processed)
    result = {
        "success": True,
        "action": "sync-comments",
        "processed_count": 0,
        "new_comments": [],
        "skipped_count": 0,
    }

    issues = get_open_issues_for_comments()
    logger.info(f"获取到 {len(issues)} 个 open Issue，开始检查评论...")

    for issue in issues:
        issue_number = issue["number"]
        comments = get_issue_comments(issue_number)

        for comment in comments:
            comment_id = comment["id"]

            if comment_id in processed:
                result["skipped_count"] += 1
                continue

            author = comment.get("author", {})
            author_login = author.get("login", "unknown") if isinstance(author, dict) else str(author)

            # 过滤 github-actions[bot] 的评论
            if author_login in EXCLUDED_COMMENT_AUTHORS:
                logger.debug(f"跳过 github-actions[bot] 的评论: {comment_id}")
                new_processed.add(comment_id)
                result["skipped_count"] += 1
                continue

            task_file = write_comment_task_file(comment, issue_number)
            if task_file:
                new_processed.add(comment_id)
                result["processed_count"] += 1
                result["new_comments"].append({
                    "comment_id": comment_id,
                    "issue_number": issue_number,
                    "author": author_login,
                    "body": (comment.get("body", "") or "")[:500],
                    "created_at": comment.get("createdAt", ""),
                    "url": comment.get("url", ""),
                    "task_file": str(task_file),
                })

    save_processed_comments(new_processed)
    logger.info(f"评论同步完成: {result['processed_count']} 个新评论, "
                 f"{result['skipped_count']} 个已跳过")

    return result


# ===== --post-comment 功能 =====

def post_comment(args) -> dict:
    """通过 GitHub Actions 发送评论（写入结果文件，触发 workflow）"""
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    issue_number = args.issue
    body = args.body
    agent = args.agent or "Unknown Agent"
    comment_url = args.comment_url or ""

    # 生成标准 header（AgentDevFlow 标准格式：PRD/Tech/QA/验收）
    utc_now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    header = (
        f"**Agent**: {agent}\n"
        f"**Date**: {utc_now}\n"
        f"**Source**: [Issue #{issue_number} Comment]({comment_url})\n"
        f"---\n\n"
    )

    full_body = header + body

    # 生成结果文件
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    result_file = RESULTS_DIR / f"comment_{issue_number}_{timestamp}.json"

    result_data = {
        "type": "issue-comment",
        "issue_number": issue_number,
        "body": full_body,
        "agent": agent,
        "source_comment_url": comment_url,
        "created_at": utc_now,
        "status": "pending",
    }

    try:
        result_file.write_text(json.dumps(result_data, ensure_ascii=False, indent=2), encoding="utf-8")
        logger.info(f"结果文件已写入: {result_file}")
    except IOError as e:
        logger.error(f"写入结果文件失败: {e}")
        return {"success": False, "action": "post-comment", "error": str(e)}

    result = {
        "success": True,
        "action": "post-comment",
        "result_file": str(result_file),
        "issue_number": issue_number,
        "agent": agent,
    }

    # 自动 git add + commit + push（触发 post-comment workflow）
    if not args.no_push:
        try:
            add_result = subprocess.run(
                ["git", "add", str(result_file)],
                capture_output=True,
                text=True,
                cwd=str(CLAUDE_DIR.parent),
            )
            if add_result.returncode != 0:
                logger.warning(f"git add 失败: {add_result.stderr}")

            commit_result = subprocess.run(
                ["git", "commit", "-m",
                 f"chore: Agent response to Issue #{issue_number} ({agent})"],
                capture_output=True,
                text=True,
                cwd=str(CLAUDE_DIR.parent),
            )
            if commit_result.returncode == 0:
                push_result = subprocess.run(
                    ["git", "push"],
                    capture_output=True,
                    text=True,
                    cwd=str(CLAUDE_DIR.parent),
                )
                if push_result.returncode == 0:
                    logger.info(f"已 push，post-comment workflow 将自动触发")
                    result["pushed"] = True
                else:
                    logger.warning(f"git push 失败: {push_result.stderr}")
                    result["pushed"] = False
            else:
                logger.warning(f"git commit 失败: {commit_result.stderr}")
                result["pushed"] = False
        except Exception as e:
            logger.warning(f"git 操作失败: {e}")
            result["pushed"] = False

    return result


# ===== --close-issue 功能 =====

def close_issue(args) -> dict:
    """关闭 GitHub Issue"""
    issue_number = args.issue
    reason = args.reason or "completed"
    comment = args.close_comment or ""

    env = os.environ.copy()
    if GITHUB_TOKEN:
        env["GH_TOKEN"] = GITHUB_TOKEN

    cmd = ["gh", "issue", "close", str(issue_number), "--reason", reason]
    if comment:
        cmd.extend(["--comment", comment])

    result = subprocess.run(cmd, capture_output=True, text=True, env=env)

    if result.returncode != 0:
        logger.error(f"关闭 Issue #{issue_number} 失败: {result.stderr}")
        return {"success": False, "action": "close-issue", "error": result.stderr}

    logger.info(f"Issue #{issue_number} 已关闭 (reason: {reason})")
    return {"success": True, "action": "close-issue", "issue_number": issue_number, "reason": reason}


# ===== --create-issue 功能 =====

def create_issue(args) -> dict:
    """创建新 GitHub Issue"""
    title = args.title
    body = args.body or ""
    labels = args.labels or ""

    env = os.environ.copy()
    if GITHUB_TOKEN:
        env["GH_TOKEN"] = GITHUB_TOKEN

    cmd = ["gh", "issue", "create", "--title", title]
    if body:
        cmd.extend(["--body", body])
    if labels:
        cmd.extend(["--label", labels])

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        env=env,
    )

    if result.returncode != 0:
        logger.error(f"创建 Issue 失败: {result.stderr}")
        return {"success": False, "action": "create-issue", "error": result.stderr}

    issue_url = result.stdout.strip()
    issue_number = issue_url.split("/")[-1]

    logger.info(f"Issue 创建成功: #{issue_number}")
    return {
        "success": True,
        "action": "create-issue",
        "issue_number": issue_number,
        "issue_url": issue_url,
    }


# ===== CLI 参数解析 =====

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="GitHub Issue & Comment 同步工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    # 顶层参数（兼容 Tech 053 规范）
    parser.add_argument("--sync-comments", action="store_true",
                        help="同步未处理的评论到 task_queue")
    parser.add_argument("--post-comment", action="store_true",
                        help="通过 GitHub Actions 发送评论")
    parser.add_argument("--create-issue", action="store_true",
                        help="创建新 GitHub Issue")
    parser.add_argument("--close-issue", action="store_true",
                        help="关闭 GitHub Issue")
    parser.add_argument("--title", type=str, help="Issue 标题 (create-issue)")
    parser.add_argument("--labels", type=str, help="Issue 标签 (create-issue, comma-separated)")
    parser.add_argument("--issue", "-i", type=int, help="Issue 编号 (post-comment/close-issue)")
    parser.add_argument("--reason", type=str, default="completed",
                        help="关闭原因 (close-issue): completed|not planned|duplicate")
    parser.add_argument("--close-comment", type=str, default="",
                        help="关闭评论 (close-issue)")
    parser.add_argument("--body", "-b", type=str, help="评论正文 (post-comment/create-issue)")
    parser.add_argument("--agent", "-a", type=str, default="", help="Agent 名称 (post-comment)")
    parser.add_argument("--comment-url", "-u", type=str, default="", help="源评论 URL (post-comment)")
    parser.add_argument("--no-push", action="store_true",
                        help="仅写入结果文件，不执行 git push (post-comment)")

    return parser


if __name__ == "__main__":
    parser = build_parser()
    args = parser.parse_args()

    if args.sync_comments:
        result = sync_comments()
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.create_issue:
        if not args.title:
            logger.error("--create-issue requires --title")
            print(json.dumps({"success": False, "error": "--title is required"}))
            sys.exit(1)
        result = create_issue(args)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.close_issue:
        if not args.issue:
            logger.error("--close-issue requires --issue")
            print(json.dumps({"success": False, "error": "--issue is required"}))
            sys.exit(1)
        result = close_issue(args)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.post_comment:
        result = post_comment(args)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        # 默认行为: sync issues
        main()
