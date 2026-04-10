#!/usr/bin/env python3
"""Post issue comments via GitHub REST API.

Called by post-comment.yml workflow step.
Reads .claude/results/comment_*.json files and posts comments via GitHub API.
"""

import json
import os
import sys
import subprocess
import urllib.request
import urllib.parse


def post_comment(repo: str, issue_number: int, body: str, gh_token: str) -> tuple:
    """Post a comment to a GitHub issue via REST API. Returns (success, http_code, response)."""
    url = f"https://api.github.com/repos/{repo}/issues/{issue_number}/comments"
    payload = json.dumps({"body": body}).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=payload,
        headers={
            "Authorization": f"token {gh_token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req) as resp:
            return (resp.status == 201, resp.status, resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return (False, e.code, e.read().decode("utf-8"))
    except Exception as e:
        return (False, 0, str(e))


def main():
    files_str = os.environ.get("FILES", "")
    gh_token = os.environ.get("GH_TOKEN", "")
    repo = os.environ.get("REPO", "")

    if not gh_token:
        print("ERROR: GH_TOKEN not set")
        sys.exit(1)

    if not repo:
        print("ERROR: REPO not set")
        sys.exit(1)

    if not files_str.strip():
        print("No files to process")
        sys.exit(0)

    files = files_str.strip().split()
    print(f"Processing {len(files)} file(s)")

    failed_count = 0
    success_count = 0

    for filepath in files:
        filepath = filepath.strip()
        if not filepath:
            continue

        print(f"\nProcessing: {filepath}")

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (IOError, json.JSONDecodeError) as e:
            print(f"ERROR: Cannot read {filepath}: {e}")
            continue

        issue_number = data.get("issue_number", "")
        body = data.get("body", "")
        agent = data.get("agent", "unknown")

        if not issue_number:
            print(f"ERROR: No issue_number in {filepath}")
            data["status"] = "failed"
            data["error"] = "no_issue_number"
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            continue

        print(f"Posting to Issue #{issue_number} as github-actions[bot]...")

        success, http_code, response = post_comment(repo, issue_number, body, gh_token)

        if success:
            print(f"SUCCESS: Comment posted to Issue #{issue_number} (HTTP {http_code})")
            data["status"] = "sent"
            data["http_code"] = http_code
        else:
            print(f"ERROR: Failed to post to Issue #{issue_number} (HTTP {http_code})")
            print(f"Response: {response[:200]}")
            data["status"] = "failed"
            data["http_code"] = http_code
            data["error"] = response[:200] if response else "unknown"

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Status updated to '{data['status']}'")

        if data["status"] == "sent":
            success_count += 1
        else:
            failed_count += 1

    print(f"\n=== Summary ===")
    print(f"Success: {success_count}")
    print(f"Failed: {failed_count}")

    if failed_count > 0:
        print(f"\nERROR: {failed_count} comment(s) failed to post")
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
