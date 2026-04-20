#!/usr/bin/env python3
"""
Bootstrap Sync Script for AgentDevFlow (adf-prefix version)

Reads all .md files from skills/ and generates corresponding skill files
in .claude/skills/ with adf- prefix.

Each skill gets its own subdirectory: .claude/skills/adf-{name}/
SKILL.md is generated for top-level entries; subdirectory contents are copied.

Step 0: Clear .claude/skills/
Step 1: Dynamically scan skills/ and generate adf- prefix mapping
Step 2: Generate SKILL.md files to .claude/skills/adf-*/
Step 3: Batch replace internal references
Step 4: git add -> commit -> push to main
"""

import os
import sys
import re
import shutil
import hashlib
from pathlib import Path
from typing import Optional

SKILLS_SHARED_DIR = Path("skills")
TARGET_DIR = Path(".claude/skills")

# Files that should NOT be synced (internal/shared use only)
SKIP_FILES = {
    "skill-protocol.md",
    "event-bus.md",
    "README.md",
}


def compute_hash(content: str) -> str:
    """Compute SHA256 hash of content (first 16 chars)."""
    return hashlib.sha256(content.encode()).hexdigest()[:16]


def slugify(name: str) -> str:
    """Convert a filename to a valid skill name (use dashes)."""
    return name.replace(".md", "").replace("_", "-")


def extract_name_and_description(content: str) -> tuple[str, str]:
    """Extract name and description from file content.

    Looks for:
    1. YAML frontmatter with name/description
    2. First markdown heading as name
    3. First paragraph as description
    """
    fm_match = re.match(r"^---\n(.*?)\n---\n", content, re.DOTALL)
    if fm_match:
        fm_text = fm_match.group(1)
        for line in fm_text.split("\n"):
            if line.startswith("name:"):
                name = line.split(":", 1)[1].strip().strip('"').strip("'")
            elif line.startswith("description:"):
                desc = line.split(":", 1)[1].strip().strip('"').strip("'")
        if name and desc:
            return name, desc

    name_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
    name = name_match.group(1).strip() if name_match else "unknown"

    lines = content.split("\n")
    desc = ""
    for line in lines:
        line = line.strip()
        if line and not line.startswith("#") and not line.startswith("---"):
            desc = line[:100]
            break

    return slugify(name), desc


def build_name_mapping() -> dict[str, str]:
    """Dynamically scan skills/ and build {original_name: adf_name} mapping."""
    mapping = {}

    # Top-level .md files → top-level skills
    for f in sorted(SKILLS_SHARED_DIR.glob("*.md")):
        if f.name in SKIP_FILES:
            continue
        name = f.stem  # filename without extension
        mapping[name] = f"adf-{name}"

    # Subdirectories → subdirectory skills
    for subdir in sorted(SKILLS_SHARED_DIR.iterdir()):
        if not subdir.is_dir():
            continue
        name = subdir.name
        # Exclude workflows and templates — they are shared dirs, not individual skills
        if name in ("workflows", "templates"):
            continue
        mapping[name] = f"adf-{name}"

    return mapping


def replace_internal_references(content: str, mapping: dict[str, str]) -> str:
    """Replace all internal skill references in content.

    Patterns replaced:
    - /{orig} → /adf-{adf}  (skill invocation paths)
    - Skill("{orig}") → Skill("{adf}")  (skill invocation calls)
    - {orig}/SKILL.md → .claude/skills/{adf}/SKILL.md  (skill file references)
    - skills/{orig}/SKILL.md → .claude/skills/{adf}/SKILL.md  (skills prefix references)
    """

    # Only apply replacements for non-skipped items
    skip_set = {*SKIP_FILES}

    replacements = []

    for orig, adf in mapping.items():
        if orig in skip_set:
            continue

        # Skill invocation paths: /agent-bootstrap → /adf-agent-bootstrap
        replacements.append((f"/{orig}", f"/{adf}"))

        # Skill invocation calls: Skill("product-manager") → Skill("adf-product-manager")
        replacements.append((f'Skill("{orig}")', f'Skill("{adf}")'))

        # Subdirectory references: product-manager/SKILL.md → .claude/skills/adf-product-manager/SKILL.md
        replacements.append((f"{orig}/SKILL.md", f".claude/skills/{adf}/SKILL.md"))

        # Also handle skills/ prefix: skills/architect/SKILL.md → .claude/skills/adf-architect/SKILL.md
        replacements.append((f"skills/{orig}/SKILL.md", f".claude/skills/{adf}/SKILL.md"))

    # Sort by length descending to avoid partial replacement issues
    replacements.sort(key=lambda x: -len(x[0]))

    for old, new in replacements:
        content = content.replace(old, new)

    return content


def needs_update(target_file: Path, new_content: str) -> bool:
    """Check if file needs update by comparing content hash."""
    if not target_file.exists():
        return True
    old_hash = compute_hash(target_file.read_text())
    new_hash = compute_hash(new_content)
    return old_hash != new_hash


def sync_top_level_skill(name: str, adf_name: str, source_path: Path) -> bool:
    """Sync a top-level .md file to .claude/skills/adf-{name}/SKILL.md."""
    target_dir = TARGET_DIR / adf_name
    target_file = target_dir / "SKILL.md"

    source_content = source_path.read_text()
    name_val, desc = extract_name_and_description(source_content)

    # Remove existing frontmatter
    cleaned = re.sub(r"^---\n.*?\n---\n", "", source_content, flags=re.DOTALL)

    # Build adf-prefixed frontmatter
    new_content = f"""---
name: {adf_name}
description: {desc}
user-invocable: true
---

{cleaned}
"""

    # Replace internal references
    mapping = build_name_mapping()
    new_content = replace_internal_references(new_content, mapping)

    if not needs_update(target_file, new_content):
        return False

    target_dir.mkdir(parents=True, exist_ok=True)
    target_file.write_text(new_content)
    return True


def sync_subdirectory_skill(subdir_name: str, adf_subdir_name: str, subdir_path: Path) -> bool:
    """Sync a subdirectory of .md files to .claude/skills/adf-{subdir}/.

    - Creates .claude/skills/adf-{subdir}/SKILL.md from the main entry file
    - Copies all other .md files from the subdirectory as-is
    - Replaces internal references in all generated files
    """
    mapping = build_name_mapping()
    changed = False
    target_dir = TARGET_DIR / adf_subdir_name

    # Find main entry file (subdir_name.md or README.md in subdir)
    entry_file = subdir_path / f"{subdir_name}.md"
    if not entry_file.exists():
        entry_file = subdir_path / "README.md"
    if not entry_file.exists():
        md_files = list(subdir_path.glob("*.md"))
        if md_files:
            entry_file = md_files[0]

    # Generate SKILL.md from entry file
    if entry_file.exists():
        entry_content = entry_file.read_text()
        name_val, desc = extract_name_and_description(entry_content)
        cleaned = re.sub(r"^---\n.*?\n---\n", "", entry_content, flags=re.DOTALL)

        skill_content = f"""---
name: {adf_subdir_name}
description: {desc}
user-invocable: true
---

{cleaned}
"""
        skill_content = replace_internal_references(skill_content, mapping)

        if needs_update(target_dir / "SKILL.md", skill_content):
            target_dir.mkdir(parents=True, exist_ok=True)
            (target_dir / "SKILL.md").write_text(skill_content)
            changed = True

    # Copy all .md files from subdirectory
    for md_file in sorted(subdir_path.glob("*.md")):
        target_file = target_dir / md_file.name
        content = md_file.read_text()
        content = replace_internal_references(content, mapping)

        if needs_update(target_file, content):
            target_dir.mkdir(parents=True, exist_ok=True)
            target_file.write_text(content)
            changed = True

    return changed


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Sync shared skills to .claude/skills/ with adf prefix")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be synced without making changes",
    )
    args = parser.parse_args()
    dry_run = args.dry_run

    changed = []
    unchanged = []

    # Step 0: Clear target directory
    if not dry_run:
        if TARGET_DIR.exists():
            shutil.rmtree(TARGET_DIR)
        TARGET_DIR.mkdir(parents=True)
        print(f"[CLEARED] {TARGET_DIR}/")
    else:
        print(f"[DRY-RUN] Would clear {TARGET_DIR}/")

    if not SKILLS_SHARED_DIR.exists():
        print(f"WARNING: {SKILLS_SHARED_DIR} does not exist")
        sys.exit(0)

    # Build name mapping
    mapping = build_name_mapping()
    print(f"\n[DISCOVERED] {len(mapping)} skills:")
    for orig, adf in mapping.items():
        print(f"  {orig} -> {adf}")

    # Step 1 & 2 & 3: Sync top-level .md files
    for source_path in sorted(SKILLS_SHARED_DIR.glob("*.md")):
        if source_path.name in SKIP_FILES:
            print(f"[SKIP] {source_path.name}")
            continue

        name = source_path.stem
        adf_name = mapping.get(name, f"adf-{name}")

        if dry_run:
            print(f"[DRY-RUN] Would sync: {source_path.name} -> {adf_name}/SKILL.md")
            continue

        if sync_top_level_skill(name, adf_name, source_path):
            print(f"[SYNCED] {source_path.name} -> {adf_name}/SKILL.md")
            changed.append(adf_name)
        else:
            print(f"[UNCHANGED] {source_path.name}")
            unchanged.append(adf_name)

    # Step 1 & 2 & 3: Sync subdirectories
    for subdir_path in sorted(SKILLS_SHARED_DIR.iterdir()):
        if not subdir_path.is_dir():
            continue

        subdir_name = subdir_path.name
        # Exclude workflows and templates — shared dirs, not individual skills
        if subdir_name in ("workflows", "templates"):
            continue
        adf_subdir_name = mapping.get(subdir_name, f"adf-{subdir_name}")

        if dry_run:
            print(f"[DRY-RUN] Would sync subdir: {subdir_name}/ -> {adf_subdir_name}/")
            continue

        if sync_subdirectory_skill(subdir_name, adf_subdir_name, subdir_path):
            print(f"[SYNCED] {subdir_name}/ -> {adf_subdir_name}/")
            changed.append(adf_subdir_name)
        else:
            print(f"[UNCHANGED] {subdir_name}/")
            unchanged.append(adf_subdir_name)

    # Output summary
    has_changes = "true" if changed else "false"
    changed_str = ",".join(sorted(changed))

    if "GITHUB_OUTPUT" in os.environ:
        with open(os.environ["GITHUB_OUTPUT"], "a") as f:
            f.write(f"has_changes={has_changes}\n")
            f.write(f"changed_skills={changed_str}\n")

    print(f"\nSummary:")
    print(f"  Changed: {changed}")
    print(f"  Unchanged: {unchanged}")
    print(f"  Has changes: {has_changes}")

    sys.exit(0)


if __name__ == "__main__":
    main()
