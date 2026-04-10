#!/usr/bin/env python3
"""
Bootstrap Sync Script

Reads all .md files from skills/shared/ and generates corresponding SKILL.md
files in adapters/claude/.claude/skills/.

Each .md file in skills/shared/ becomes a skill with the same name.
The generated SKILL.md includes:
- The original file content
- A YAML frontmatter with name and description
"""

import os
import sys
import re
import hashlib
from pathlib import Path
from typing import Optional

SKILLS_SHARED_DIR = Path("skills/shared")
ADAPTER_SKILLS_DIR = Path("adapters/claude/.claude/skills")

# Skills that have subdirectories with their own SKILL.md — skip top-level files for these
SUBDIR_SKILLS = {
    "start-agent-team": SKILLS_SHARED_DIR / "start-agent-team",
    "create-agent": SKILLS_SHARED_DIR / "create-agent",
}

# Skills that should NOT be synced (internal/shared use only, not Claude adapter skills)
SKIP_SKILLS = {
    "skill-protocol.md",
    "event-bus.md",
    "README.md",
}


def slugify(name: str) -> str:
    """Convert a filename to a valid skill name."""
    return name.replace(".md", "").replace("-", "-").replace("_", "-")


def extract_name_and_description(content: str) -> tuple[str, str]:
    """Extract name and description from file content.

    Looks for:
    1. YAML frontmatter with name/description
    2. First markdown heading as name
    3. First paragraph as description
    """
    # Check for existing YAML frontmatter
    fm_match = re.match(r"^---\n(.*?)\n---\n", content, re.DOTALL)
    if fm_match:
        fm_text = fm_match.group(1)
        fm_lines = fm_text.split("\n")
        name = None
        desc = None
        for line in fm_lines:
            if line.startswith("name:"):
                name = line.split(":", 1)[1].strip().strip('"').strip("'")
            elif line.startswith("description:"):
                desc = line.split(":", 1)[1].strip().strip('"').strip("'")
        if name and desc:
            return name, desc

    # Fallback: extract from content
    name_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
    name = name_match.group(1).strip() if name_match else "unknown"

    # Get first non-empty non-heading line as description
    lines = content.split("\n")
    desc = ""
    for line in lines:
        line = line.strip()
        if line and not line.startswith("#") and not line.startswith("---"):
            desc = line[:100]
            break

    return slugify(name), desc


def generate_skill_md(skill_name: str, source_content: str) -> str:
    """Generate a SKILL.md file content from source markdown."""
    # Extract name and description from source
    name, desc = extract_name_and_description(source_content)

    # Clean up the source content — remove existing frontmatter
    cleaned = re.sub(r"^---\n.*?\n---\n", "", source_content, flags=re.DOTALL)

    skill_id = skill_name.replace(".md", "")

    return f"""---
name: {skill_id}
description: {desc}
user-invocable: true
---

{cleaned}
"""


def compute_file_hash(path: Path) -> str:
    """Compute SHA256 hash of file content."""
    return hashlib.sha256(path.read_bytes()).hexdigest()[:16]


def skill_needs_update(skill_dir: Path, new_content: str) -> bool:
    """Check if a skill needs to be updated by comparing content hash."""
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return True

    new_hash = hashlib.sha256(new_content.encode()).hexdigest()[:16]
    old_hash = compute_file_hash(skill_md)

    return new_hash != old_hash


def sync_skill(skill_name: str, source_path: Path) -> bool:
    """Sync a single shared skill to the adapter directory. Returns True if changed."""
    source_content = source_path.read_text()
    skill_id = skill_name.replace(".md", "")
    skill_dir = ADAPTER_SKILLS_DIR / skill_id
    new_content = generate_skill_md(skill_id, source_content)

    if not skill_needs_update(skill_dir, new_content):
        return False

    skill_dir.mkdir(parents=True, exist_ok=True)
    (skill_dir / "SKILL.md").write_text(new_content)
    return True


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Sync shared skills to Claude adapter")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force resync all skills (ignore diff check)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be synced without making changes",
    )
    args = parser.parse_args()

    force = os.environ.get("FORCE_RESYNC", "false").lower() == "true"
    force = force or args.force
    dry_run = args.dry_run

    changed = []
    skipped = []

    # Create target directory
    ADAPTER_SKILLS_DIR.mkdir(parents=True, exist_ok=True)

    # Process top-level .md files in skills/shared/
    if not SKILLS_SHARED_DIR.exists():
        print(f"WARNING: {SKILLS_SHARED_DIR} does not exist")
        sys.exit(0)

    for source_path in sorted(SKILLS_SHARED_DIR.glob("*.md")):
        skill_name = source_path.name

        # Skip files that are subdirectory skills or explicitly skipped
        if skill_name in SKIP_SKILLS:
            skipped.append(skill_name)
            continue

        # Skip if this skill has a subdirectory (those have their own SKILL.md)
        if source_path.stem in SUBDIR_SKILLS:
            skipped.append(f"{skill_name} (has subdirectory, handled separately)")
            continue

        source_content = source_path.read_text()
        skill_id = skill_name.replace(".md", "")
        skill_dir = ADAPTER_SKILLS_DIR / skill_id
        new_content = generate_skill_md(skill_id, source_content)

        if force or skill_needs_update(skill_dir, new_content):
            if dry_run:
                print(f"[DRY-RUN] Would sync: {skill_name} -> {skill_id}/SKILL.md")
            else:
                skill_dir.mkdir(parents=True, exist_ok=True)
                (skill_dir / "SKILL.md").write_text(new_content)
                print(f"SYNCED: {skill_name} -> {skill_id}/SKILL.md")
                changed.append(skill_id)
        else:
            print(f"UNCHANGED: {skill_name}")

    # Handle subdirectory skills — read the main .md file in the subdirectory
    for skill_id, subdir_path in SUBDIR_SKILLS.items():
        if not subdir_path.exists():
            continue

        # Find the main .md file (either skill_id.md or README.md in subdir)
        main_md = subdir_path / f"{skill_id}.md"
        if not main_md.exists():
            main_md = subdir_path / "README.md"
        if not main_md.exists():
            # Look for any .md file
            md_files = list(subdir_path.glob("*.md"))
            if md_files:
                main_md = md_files[0]
            else:
                print(f"WARNING: No .md file found in {subdir_path}")
                continue

        source_content = main_md.read_text()
        skill_dir = ADAPTER_SKILLS_DIR / skill_id
        new_content = generate_skill_md(skill_id, source_content)

        if force or skill_needs_update(skill_dir, new_content):
            if dry_run:
                print(f"[DRY-RUN] Would sync subdir: {main_md.name} -> {skill_id}/SKILL.md")
            else:
                skill_dir.mkdir(parents=True, exist_ok=True)
                (skill_dir / "SKILL.md").write_text(new_content)
                print(f"SYNCED: {main_md.name} -> {skill_id}/SKILL.md")
                changed.append(skill_id)
        else:
            print(f"UNCHANGED: {skill_id}/ (subdir)")

    # Output for GitHub Actions
    has_changes = "true" if changed else "false"
    changed_skills = ",".join(changed)

    if "GITHUB_OUTPUT" in os.environ:
        with open(os.environ["GITHUB_OUTPUT"], "a") as f:
            f.write(f"has_changes={has_changes}\n")
            f.write(f"changed_skills={changed_skills}\n")
    else:
        print(f"\nSummary:")
        print(f"  Changed: {changed}")
        print(f"  Skipped: {skipped}")
        print(f"  Has changes: {has_changes}")

    if changed and not dry_run:
        # Write a marker file for the PR creation step
        (Path("adapters/claude/.claude/skills")).mkdir(parents=True, exist_ok=True)

    sys.exit(0)


if __name__ == "__main__":
    main()
