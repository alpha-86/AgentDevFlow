#!/usr/bin/env bash
#
# AgentDevFlow 安装脚本
#
# 用法:
#   ./scripts/install.sh [--channel stable|dev] [--target DIR] [--dry-run]
#
# 示例:
#   ./scripts/install.sh                        # 默认安装（stable）
#   ./scripts/install.sh --channel dev          # 安装开发版
#   ./scripts/install.sh --target ~/.claude     # 指定安装目录
#   ./scripts/install.sh --dry-run              # 预览模式
#
# 安装内容:
#   - skills/ -> {target}/skills/
#   - adapters/claude/.claude/ -> {target}/skills/
#
# 注意:
#   - 不覆盖已存在的文件（保留用户本地修改）
#   - 使用 --force 强制覆盖
#   - 建议先 --dry-run 预览

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CHANNEL="stable"
TARGET_DIR="${CLAUDE_CONFIG_DIR:-${HOME}/.claude}"
FORCE=false
DRY_RUN=false
VERBOSE=false

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

info() { echo -e "${BLUE}[INFO]${NC} $1"; }
success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
error() { echo -e "${RED}[ERROR]${NC} $1"; }
verbose() { $VERBOSE && echo -e "${CYAN}[VERBOSE]${NC} $1" || true; }

usage() {
    cat <<EOF
用法: $(basename "$0") [选项]

选项:
  --channel stable|dev   选择安装频道 (默认: stable)
  --target DIR           指定安装目标目录 (默认: ~/.claude)
  --force                强制覆盖已存在的文件
  --dry-run              预览模式，不做任何实际变更
  -v, --verbose         显示详细信息
  -h, --help            显示此帮助信息

安装频道:
  stable   安装已发布的稳定版本（从 GitHub release 下载）
  dev      安装当前仓库 HEAD（本地开发用）

示例:
  $(basename "$0") --channel dev --target ~/.claude
  $(basename "$0") --dry-run
EOF
}

parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                usage
                exit 0
                ;;
            --channel)
                CHANNEL="$2"
                if [[ "$CHANNEL" != "stable" && "$CHANNEL" != "dev" ]]; then
                    error "--channel 必须是 stable 或 dev"
                    exit 1
                fi
                shift 2
                ;;
            --target)
                TARGET_DIR="$2"
                shift 2
                ;;
            --force)
                FORCE=true
                shift
                ;;
            --dry-run)
                DRY_RUN=true
                shift
                ;;
            -v|--verbose)
                VERBOSE=true
                shift
                ;;
            *)
                error "未知选项: $1"
                usage
                exit 1
                ;;
        esac
    done
}

check_prerequisites() {
    info "检查前置条件..."

    if [[ ! -d "$REPO_ROOT/.git" ]]; then
        error "不是 git 仓库（或 .git 目录缺失）"
        exit 1
    fi

    if [[ ! -d "$REPO_ROOT/skills" ]]; then
        error "skills/ 目录不存在"
        exit 1
    fi

    if [[ ! -d "$REPO_ROOT/adapters/claude/.claude/skills" ]]; then
        error "adapters/claude/.claude/skills/ 目录不存在"
        exit 1
    fi

    if [[ ! -f "$REPO_ROOT/CHANGELOG.md" ]]; then
        error "CHANGELOG.md 不存在"
        exit 1
    fi

    success "前置条件检查通过"
}

get_current_version() {
    grep -m1 '^| `' "$REPO_ROOT/CHANGELOG.md" | sed -E 's/^\| `v?([^`]+)`.*/\1/' | tr -d ' '
}

get_installed_version() {
    local version_file="${TARGET_DIR}/skills/.agentdevflow-version"
    if [[ -f "$version_file" ]]; then
        cat "$version_file"
    fi
}

install_dev() {
    info "安装模式: dev (本地仓库)"
    verbose "源目录: $REPO_ROOT"
    verbose "目标目录: $TARGET_DIR"

    local current_version
    current_version=$(get_current_version)
    local installed_version
    installed_version=$(get_installed_version)

    echo ""
    info "AgentDevFlow v${current_version}"
    if [[ -n "$installed_version" && "$installed_version" != "$current_version" ]]; then
        warn "当前已安装版本: v${installed_version}"
        warn "将升级到 v${current_version}"
    elif [[ -n "$installed_version" ]]; then
        info "当前已安装版本: v${installed_version} (已是最新)"
    fi
    echo ""

    # 安装共享技能（skills/）
    local shared_source="${REPO_ROOT}/skills"
    local shared_target="${TARGET_DIR}/skills"

    info "安装共享技能到 ${shared_target}..."
    if $DRY_RUN; then
        info "[DRY-RUN] cp -r ${shared_source}/* ${shared_target}/"
    else
        mkdir -p "$shared_target"
        # 只复制 .md 文件，保留目录结构
        find "$shared_source" -type f -name "*.md" | while read -r src_file; do
            local rel_path="${src_file#$shared_source/}"
            local tgt_file="${shared_target}/${rel_path}"
            local tgt_dir
            tgt_dir=$(dirname "$tgt_file")

            mkdir -p "$tgt_dir"

            if [[ -f "$tgt_file" && "$FORCE" == false ]]; then
                verbose "跳过（已存在）: $rel_path"
            else
                verbose "安装: $rel_path"
                cp "$src_file" "$tgt_file"
            fi
        done
    fi

    # 安装 Claude 适配器技能包
    local adapter_source="${REPO_ROOT}/adapters/claude/.claude/skills"
    local adapter_target="${TARGET_DIR}/skills"

    info "安装 Claude 适配器到 ${adapter_target}..."
    if $DRY_RUN; then
        info "[DRY-RUN] cp -r ${adapter_source}/* ${adapter_target}/"
    else
        mkdir -p "$adapter_target"
        for skill_dir in "$adapter_source"/*/; do
            local skill_name
            skill_name=$(basename "$skill_dir")
            local tgt_skill_dir="${adapter_target}/${skill_name}"
            local tgt_skill_file="${tgt_skill_dir}/SKILL.md"

            if [[ -f "$tgt_skill_file" && "$FORCE" == false ]]; then
                verbose "跳过（已存在）: ${skill_name}/SKILL.md"
            else
                verbose "安装: ${skill_name}/SKILL.md"
                mkdir -p "$tgt_skill_dir"
                cp "${adapter_source}/${skill_name}/SKILL.md" "$tgt_skill_file"
            fi
        done
    fi

    # 写入版本文件
    if ! $DRY_RUN; then
        mkdir -p "${TARGET_DIR}/skills"
        echo "$current_version" > "${TARGET_DIR}/skills/.agentdevflow-version"
    fi

    echo ""
    success "AgentDevFlow v${current_version} 安装完成！"
}

install_stable() {
    info "安装模式: stable (从 GitHub release)"

    local repo
    repo=$(git -C "$REPO_ROOT" remote get-url origin | sed 's/.*github.com[:/]\(.*\)\.git/\1/')

    # 获取最新 release 版本
    local latest_tag
    latest_tag=$(git ls-remote --tags "https://github.com/${repo}.git" 2>/dev/null | grep -v '\^{}' | awk -F/ '{print $3}' | sed 's/v//' | sort -V | tail -1)

    if [[ -z "$latest_tag" ]]; then
        warn "无法获取最新 release，将使用 dev 模式"
        install_dev
        return
    fi

    info "最新稳定版本: v${latest_tag}"
    echo ""
    info "从 GitHub release 安装的完整说明："
    echo ""
    echo "  1. 访问 https://github.com/${repo}/releases/latest"
    echo "  2. 下载 Source code (tarball 或 zipball)"
    echo "  3. 解压到临时目录"
    echo "  4. 运行: ./install.sh --target ~/.claude"
    echo ""
    warn "自动下载功能尚未实现，请手动完成上述步骤"
}

post_install_check() {
    info "安装后验证..."

    local skill_count=0
    local adapter_count=0

    if [[ -d "${TARGET_DIR}/skills" ]]; then
        skill_count=$(find "${TARGET_DIR}/skills" -name "*.md" 2>/dev/null | wc -l)
    fi

    if [[ -d "${TARGET_DIR}/skills" ]]; then
        adapter_count=$(find "${TARGET_DIR}/skills" -name "SKILL.md" -path "*/.claude/*" 2>/dev/null | wc -l)
        # Also check for top-level adapter skills
        adapter_count=$((adapter_count + $(find "${TARGET_DIR}/skills" -maxdepth 1 -name "*.md" 2>/dev/null | wc -l)))
    fi

    verbose "共享技能文件数: $skill_count"
    verbose "适配器技能文件数: $adapter_count"

    if [[ $skill_count -eq 0 ]]; then
        warn "未检测到共享技能文件"
    else
        success "共享技能: $skill_count 个文件"
    fi

    if [[ $adapter_count -eq 0 ]]; then
        warn "未检测到适配器技能"
    else
        success "适配器技能: $adapter_count 个文件"
    fi
}

show_next_steps() {
    local version="$1"
    echo ""
    echo "============================================"
    success "AgentDevFlow v${version} 安装完成！"
    echo "============================================"
    echo ""
    info "下一步:"
    echo "  1. 重启 Claude Code 以加载新技能"
    echo "  2. 在 Claude Code 中使用以下命令启动团队:"
    echo "     /agent-bootstrap   # 自举 AgentDevFlow 项目"
    echo "     /start-agent-team  # 启动交付团队"
    echo ""
    info "更多信息请查看:"
    echo "  - ${REPO_ROOT}/README.md"
    echo "  - ${REPO_ROOT}/skills/README.md"
    echo ""
}

main() {
    parse_args "$@"

    echo ""
    echo "============================================"
    echo "  AgentDevFlow Install Script"
    echo "============================================"
    echo ""

    if $DRY_RUN; then
        warn "DRY-RUN 模式：不会进行实际变更"
        echo ""
    fi

    check_prerequisites

    case "$CHANNEL" in
        dev)
            install_dev
            ;;
        stable)
            install_stable
            ;;
    esac

    post_install_check

    local version
    version=$(get_current_version)
    show_next_steps "$version"
}

main "$@"
