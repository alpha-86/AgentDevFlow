#!/usr/bin/env bash
#
# AgentDevFlow Release Script
#
# 用法:
#   ./scripts/release.sh [version] [--dry-run]
#
# 示例:
#   ./scripts/release.sh              # 自动确定下一个版本
#   ./scripts/release.sh 0.4.0        # 指定版本号
#   ./scripts/release.sh --dry-run    # 预览模式
#
# 流程:
#   1. 确认当前 git 状态（无未提交变更）
#   2. 确认 CHANGELOG.md 已更新
#   3. 确定版本号（支持手动指定或自动递增）
#   4. 更新 CHANGELOG.md 中的版本主索引（如需要）
#   5. 创建版本 commit
#   6. 创建并推送 git tag
#   7. 生成 release notes
#
# 注意:
#   - 此脚本必须在 main 分支上运行
#   - 未提交的变更会被阻止发布
#   - tag 格式: v{version} (例如: v0.4.0)

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CHANGELOG="${REPO_ROOT}/CHANGELOG.md"
DRY_RUN=false
SPECIFIED_VERSION=""

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

info() { echo -e "${BLUE}[INFO]${NC} $1"; }
success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
error() { echo -e "${RED}[ERROR]${NC} $1"; }

usage() {
    cat <<EOF
用法: $(basename "$0") [version] [--dry-run]

选项:
  version      指定版本号（如 0.4.0）。不指定时自动从 CHANGELOG.md 递增。
  --dry-run    预览模式，不做任何实际变更。
  -h, --help   显示此帮助信息。
EOF
}

parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                usage
                exit 0
                ;;
            --dry-run)
                DRY_RUN=true
                shift
                ;;
            -*)
                error "未知选项: $1"
                usage
                exit 1
                ;;
            *)
                if [[ -n "$SPECIFIED_VERSION" ]]; then
                    error "只能指定一个版本号"
                    exit 1
                fi
                SPECIFIED_VERSION="$1"
                shift
                ;;
        esac
    done
}

check_prerequisites() {
    info "检查前置条件..."

    # 必须在 git 仓库中
    if ! git -C "$REPO_ROOT" rev-parse --git-dir > /dev/null 2>&1; then
        error "不是 git 仓库"
        exit 1
    fi

    # 必须在 main 分支
    current_branch=$(git -C "$REPO_ROOT" branch --show-current)
    if [[ "$current_branch" != "main" ]]; then
        error "必须在 main 分支上发布（当前: $current_branch）"
        exit 1
    fi

    # 检查未提交变更
    if ! git -C "$REPO_ROOT" diff-index --quiet HEAD --; then
        error "存在未提交的变更，请先提交"
        git -C "$REPO_ROOT" status --short
        exit 1
    fi

    # 检查 CHANGELOG.md 是否存在
    if [[ ! -f "$CHANGELOG" ]]; then
        error "CHANGELOG.md 不存在"
        exit 1
    fi

    success "前置条件检查通过"
}

get_latest_version() {
    # 从 CHANGELOG.md 提取最新版本号
    local latest
    latest=$(grep -m1 '^| `' "$CHANGELOG" | sed -E 's/^\| `v?([^`]+)`.*/\1/' | tr -d ' \r')
    if [[ -z "$latest" ]]; then
        error "无法从 CHANGELOG.md 提取最新版本"
        exit 1
    fi
    echo "$latest"
}

bump_version() {
    local current="$1"
    # 自动递增 patch 版本
    local major minor patch
    IFS='.' read -r major minor patch <<< "$current"
    patch=$((patch + 1))
    echo "${major}.${minor}.${patch}"
}

prompt_version() {
    local suggested="$1"
    # Non-interactive (no tty) — use suggested version directly
    if [[ ! -t 0 ]]; then
        echo "$suggested"
        return
    fi
    echo -n "请输入版本号 [${suggested}]: "
    read -r version
    if [[ -z "$version" ]]; then
        echo "$suggested"
    else
        echo "$version"
    fi
}

check_changelog_updated() {
    info "检查 CHANGELOG.md 是否已更新..."

    # 检查最新版本条目是否有内容（不是只有标题）
    # 简单检查：最新版本块之后是否有实际内容行
    local latest_block
    latest_block=$(awk '/^## [0-9]/ && ++c==1 {found=1; next} found && /^## [0-9]/ {exit} found' "$CHANGELOG")

    if [[ -z "$(echo "$latest_block" | grep -vE '^\s*$|^## |^\|')" ]]; then
        warn "CHANGELOG.md 的最新版本条目似乎只有标题，请确认是否已填写变更内容"
        echo -n "是否继续? [y/N]: "
        read -r confirm
        if [[ "${confirm:-N}" != "y" ]]; then
            error "请先更新 CHANGELOG.md"
            exit 1
        fi
    fi

    success "CHANGELOG.md 检查通过"
}

update_version_index() {
    # 在版本主索引表中添加新版本条目（如果不存在）
    local version="$1"
    local today
    today=$(date '+%Y-%m-%d')

    if grep -q "| \`v\?${version}\` " "$CHANGELOG"; then
        info "版本 ${version} 已在索引表中"
        return
    fi

    info "在 CHANGELOG.md 索引表中添加版本 ${version}..."

    if $DRY_RUN; then
        info "[DRY-RUN] 会在索引表顶部添加: | \`${version}\` | ${today} | ... | 进行中 |"
        return
    fi

    # 插入新版本行到索引表（在第二行之后，即表头之后的第一行）
    local temp_file
    temp_file=$(mktemp)
    awk -v v="$version" -v d="$today" '
        NR == 1 { print; next }  # 表头原样输出
        NR == 2 {  # 第二行（第一个版本行）之前插入新行
            printf "| \\`%s\\` | %s | 新版本 | 进行中 |\n", v, d
            print
            next
        }
        { print }
    ' "$CHANGELOG" > "$temp_file" && mv "$temp_file" "$CHANGELOG"

    success "版本索引已更新"
}

create_release_commit() {
    local version="$1"

    info "创建发布 commit..."

    if $DRY_RUN; then
        info "[DRY-RUN] git add CHANGELOG.md && git commit -m 'release: v${version}'"
        return
    fi

    git -C "$REPO_ROOT" add CHANGELOG.md
    git -C "$REPO_ROOT" commit -m "release: v${version}"

    success "Release commit 已创建"
}

create_and_push_tag() {
    local version="$1"

    info "创建并推送 tag v${version}..."

    if $DRY_RUN; then
        info "[DRY-RUN] git tag -a v${version} -m 'AgentDevFlow v${version}' && git push origin v${version}"
        return
    fi

    git -C "$REPO_ROOT" tag -a "v${version}" -m "AgentDevFlow v${version}" -f
    git -C "$REPO_ROOT" push origin "v${version}" -f

    success "Tag v${version} 已推送"
}

generate_release_notes() {
    local version="$1"

    # 生成 release notes 内容
    local notes
    notes=$(awk -v v="$version" '
        BEGIN { in_section=0; notes="" }
        /^## [0-9]/ && ++count == 1 {
            in_section=1
            next
        }
        in_section && /^## [0-9]/ { exit }
        in_section { notes = notes $0 "\n" }
        END {
            # Clean up notes
            gsub(/^\n+/, "", notes)
            gsub(/\n+$/, "", notes)
            print notes
        }
    ' "$CHANGELOG")

    echo ""
    info "Release Notes (v${version}):"
    echo "================================"
    echo "$notes"
    echo "================================"
}

main() {
    parse_args "$@"

    echo ""
    echo "============================================"
    echo "  AgentDevFlow Release Script"
    echo "================================"
    echo ""

    if $DRY_RUN; then
        warn "DRY-RUN 模式：不会进行实际变更"
        echo ""
    fi

    check_prerequisites

    # 确定版本号
    local version
    if [[ -n "$SPECIFIED_VERSION" ]]; then
        version="$SPECIFIED_VERSION"
        info "使用指定版本: $version"
    else
        local latest
        latest=$(get_latest_version)
        version=$(bump_version "$latest")
        info "当前最新版本: $latest"
        info "建议发布版本: $version"
        version=$(prompt_version "$version")
    fi

    # 验证版本号格式
    if ! [[ "$version" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
        error "版本号格式无效，请使用 SemVer 格式 (如 0.4.0)"
        exit 1
    fi

    echo ""
    info "准备发布版本: v${version}"
    echo ""

    check_changelog_updated
    update_version_index "$version"
    create_release_commit "$version"
    create_and_push_tag "$version"

    echo ""
    success "AgentDevFlow v${version} 发布完成！"
    echo ""

    generate_release_notes "$version"

    echo ""
    info "下一步:"
    info "  1. GitHub Actions 会自动构建并验证"
    info "  2. 访问 https://github.com/$(git -C "$REPO_ROOT" remote get-url origin | sed 's/.*github.com[:/]\(.*\)\.git/\1/')/releases 查看"
    info "  3. 用户可以通过 ./scripts/install.sh 安装新版本"
    echo ""
}

main "$@"
