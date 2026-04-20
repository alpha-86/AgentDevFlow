#!/usr/bin/env python3
"""检测 gstack / superpower 增强层是否已安装"""

import os
import sys

SKILL_SEARCH_PATHS = [
    os.path.expanduser("~/.claude/skills"),       # 全局 skill 目录
    os.path.join(os.getcwd(), ".claude/skills"),  # 项目本地 skill 目录
]

ENHANCEMENT_SKILLS = ["gstack", "superpower"]


def detect_skill(skill_name: str) -> bool:
    """检测指定 skill 是否存在于任意 search path 中。"""
    for base in SKILL_SEARCH_PATHS:
        skill_path = os.path.join(base, skill_name)
        # 检查 skill 目录或 skill 文件是否存在
        if os.path.isdir(skill_path) or os.path.isfile(f"{skill_path}.md"):
            return True
    return False


def main():
    installed = {}
    for skill in ENHANCEMENT_SKILLS:
        status = "installed" if detect_skill(skill) else "not_found"
        installed[skill] = status
        print(f"{skill}={status}")

    # 返回码表示是否有任一增强层安装
    any_installed = any(v == "installed" for v in installed.values())
    if not any_installed:
        print("hint: install gstack and/or superpower to enable enhancement layer")
    sys.exit(0 if any_installed else 1)


if __name__ == "__main__":
    main()
