#!/usr/bin/env bash
#
# AgentDevFlow 安装脚本 v2.0
#
# 用法:
#   ./scripts/install.sh [--channel stable|dev] [--target DIR] [--dry-run]
#   ./scripts/install.sh --uninstall [--target DIR]
#
# 示例:
#   ./scripts/install.sh                        # 默认安装（dev）
#   ./scripts/install.sh --channel stable       # 安装稳定版
#   ./scripts/install.sh --target ~/.claude     # 指定安装目录
#   ./scripts/install.sh --dry-run              # 预览模式
#   ./scripts/install.sh --uninstall            # 卸载
#
# 安装内容（Tech Spec #019 v2.0 定义的全量安装产物）:
#   - skills/       -> {target}/skills/             (稳定版 skill namespace)
#   - prompts/      -> {target}/AgentDevFlow/prompts/
#   - docs/governance/ -> {target}/AgentDevFlow/docs/governance/
#   - docs/platforms/  -> {target}/AgentDevFlow/docs/platforms/
#   - scripts/      -> {target}/AgentDevFlow/scripts/
#   - README.md     -> {target}/AgentDevFlow/README.md
#   - adapters/claude/.claude/skills/ -> {target}/skills/
#   - ADF_DOC_ROOT 环境变量注入到 shell profile
#   - 安装后完备性检查（JSON 输出 + 日志）
#
# 注意:
#   - 不覆盖已存在的文件（保留用户本地修改）
#   - 使用 --force 强制覆盖
#   - 建议先 --dry-run 预览

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CHANNEL="dev"
TARGET_DIR="${CLAUDE_CONFIG_DIR:-${HOME}/.claude}"
FORCE=false
DRY_RUN=false
VERBOSE=false
UNINSTALL=false

# 安装路径常量
ADF_INSTALL_DIR="${TARGET_DIR}/AgentDevFlow"
ADF_SKILLS_DIR="${TARGET_DIR}/skills"

# ADF 管理的 skill 目录清单（用于安全卸载）
ADF_MANAGED_SKILL_DIRS=(
    "start-agent-team" "team-setup" "team-lead"
    "product-manager" "architect" "qa-engineer"
    "engineer" "platform-sre" "pmo" "pmo-review"
    "agent-bootstrap" "create-agent"
    "workflows" "templates" "shared"
)
ADF_MANAGED_SKILL_FILES=(
    "README.md" "skill-protocol.md" "event-bus.md"
    ".agentdevflow-version"
)

# 关键清单（Tech Spec §2.3-2.8 最小清单）
PROMPTS_MINIMUM=(
    "001_team_topology.md"
    "002_develop_pipeline.md"
    "003_document_contracts.md"
    "004_delivery_gates.md"
    "010_team_setup_and_bootstrap.md"
    "018_issue_routing_and_project_portfolio.md"
    "007_issue_driven_orchestration.md"
    "013_github_issue_and_review_comments.md"
    "017_human_review_and_signoff.md"
    "019_dual_stage_pr_and_three_layer_safeguard.md"
)

GOVERNANCE_MINIMUM=(
    "core-principles.md"
    "skill-protocol.md"
    "issue-naming-convention.md"
    "platform-minimum-checks.md"
)

PLATFORMS_MINIMUM=(
    "enhancement-layer.md"
)

WORKFLOWS_MINIMUM=(
    "tech-review.md"
    "qa-validation.md"
    "prd-review.md"
    "release-review.md"
    "human-review.md"
    "implementation.md"
    "issue-lifecycle.md"
    "weekly-review.md"
)

TEMPLATES_MINIMUM=(
    "tech-spec-template.md"
    "prd-template.md"
    "qa-case-template.md"
    "qa-report-template.md"
    "review-comment-template.md"
    "audit-report-template.md"
    "release-record-template.md"
    "platform-check-result-template.md"
)

SCRIPTS_MINIMUM=(
    "github_issue_sync.py"
    "task_router.py"
    "task_update.py"
    "install.sh"
)

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
  --channel stable|dev   选择安装频道 (默认: dev)
  --target DIR           指定安装目标目录 (默认: ~/.claude)
  --force                强制覆盖已存在的文件
  --dry-run              预览模式，不做任何实际变更
  --uninstall            卸载 AgentDevFlow
  -v, --verbose          显示详细信息
  -h, --help             显示此帮助信息

安装频道:
  stable   安装已发布的稳定版本（从 GitHub release 下载）
  dev      安装当前仓库 HEAD（本地开发用）

安装产物（Tech Spec #019 v2.0）:
  ~/.claude/skills/                    稳定版 skill namespace
  ~/.claude/AgentDevFlow/prompts/      Prompts 文档
  ~/.claude/AgentDevFlow/docs/         治理与平台文档
  ~/.claude/AgentDevFlow/scripts/      核心脚本
  ~/.claude/AgentDevFlow/README.md     项目 README
  ADF_DOC_ROOT                         环境变量注入

示例:
  $(basename "$0") --channel dev --target ~/.claude
  $(basename "$0") --dry-run
  $(basename "$0") --uninstall
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
                ADF_INSTALL_DIR="${TARGET_DIR}/AgentDevFlow"
                ADF_SKILLS_DIR="${TARGET_DIR}/skills"
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
            --uninstall)
                UNINSTALL=true
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

    # v2.0: prompts/ 为必须目录
    if [[ ! -d "$REPO_ROOT/prompts" ]]; then
        error "prompts/ 目录不存在"
        exit 1
    fi

    # v2.0: docs/governance/ 为必须目录
    if [[ ! -d "$REPO_ROOT/docs/governance" ]]; then
        error "docs/governance/ 目录不存在"
        exit 1
    fi

    # v2.0: scripts/ 为必须目录
    if [[ ! -d "$REPO_ROOT/scripts" ]]; then
        error "scripts/ 目录不存在"
        exit 1
    fi

    # adapters 为可选（dev 模式使用）
    if [[ "$CHANNEL" == "dev" && ! -d "$REPO_ROOT/adapters/claude/.claude/skills" ]]; then
        warn "adapters/claude/.claude/skills/ 目录不存在（适配器技能将跳过）"
    fi

    success "前置条件检查通过"
}

get_current_version() {
    grep -m1 '^| `' "$REPO_ROOT/CHANGELOG.md" | sed -E 's/^\| `v?([^`]+)`.*/\1/' | tr -d ' '
}

get_installed_version() {
    local version_file="${ADF_SKILLS_DIR}/.agentdevflow-version"
    if [[ -f "$version_file" ]]; then
        cat "$version_file"
    fi
}

# ============================================================
# 复制辅助函数
# ============================================================

# 复制目录下所有 .md 文件，保留目录结构
copy_md_files() {
    local src_dir="$1"
    local tgt_dir="$2"
    local label="$3"

    info "安装 ${label} 到 ${tgt_dir}..."
    if $DRY_RUN; then
        info "[DRY-RUN] copy ${src_dir}/*.md -> ${tgt_dir}/"
        return
    fi

    mkdir -p "$tgt_dir"
    find "$src_dir" -type f -name "*.md" | while read -r src_file; do
        local rel_path="${src_file#$src_dir/}"
        local tgt_file="${tgt_dir}/${rel_path}"
        local tgt_subdir
        tgt_subdir=$(dirname "$tgt_file")

        mkdir -p "$tgt_subdir"

        if [[ -f "$tgt_file" && "$FORCE" == false ]]; then
            verbose "跳过（已存在）: ${label}/${rel_path}"
        else
            verbose "安装: ${label}/${rel_path}"
            cp "$src_file" "$tgt_file"
        fi
    done
}

# 复制指定文件列表（不保留子目录结构，文件直接放入目标目录）
copy_file_list() {
    local src_dir="$1"
    local tgt_dir="$2"
    shift 2
    local files=("$@")
    local label="${label:-files}"

    mkdir -p "$tgt_dir"

    for f in "${files[@]}"; do
        local src_file="${src_dir}/${f}"
        local tgt_file="${tgt_dir}/${f}"

        if [[ ! -f "$src_file" ]]; then
            warn "源文件缺失: ${f}"
            continue
        fi

        if [[ -f "$tgt_file" && "$FORCE" == false ]]; then
            verbose "跳过（已存在）: ${f}"
        else
            verbose "安装: ${f}"
            cp "$src_file" "$tgt_file"
        fi
    done
}

# ============================================================
# ADF_DOC_ROOT 环境变量注入（Tech Spec §4）
# ============================================================

inject_adf_doc_root() {
    local doc_root="${ADF_INSTALL_DIR}"
    local target_val="export ADF_DOC_ROOT=\"${doc_root}\""

    info "注入 ADF_DOC_ROOT 环境变量..."

    if $DRY_RUN; then
        info "[DRY-RUN] 会写入 ADF_DOC_ROOT=${doc_root} 到 shell profile"
        return
    fi

    # 检测并写入各 shell profile
    local profiles=()
    [[ -f "${HOME}/.bashrc" ]] && profiles+=("${HOME}/.bashrc")
    [[ -f "${HOME}/.zshrc" ]] && profiles+=("${HOME}/.zshrc")
    [[ -f "${HOME}/.config/fish/config.fish" ]] && profiles+=("${HOME}/.config/fish/config.fish")

    # 如果没有 profile 文件，创建 .bashrc
    if [[ ${#profiles[@]} -eq 0 ]]; then
        touch "${HOME}/.bashrc"
        profiles+=("${HOME}/.bashrc")
    fi

    for profile in "${profiles[@]}"; do
        local fish=false
        if [[ "$profile" == *"/fish/config.fish" ]]; then
            fish=true
        fi

        if grep -q 'ADF_DOC_ROOT' "$profile" 2>/dev/null; then
            # 已存在：更新旧路径
            if $fish; then
                sed -i "s|set -gx ADF_DOC_ROOT .*|set -gx ADF_DOC_ROOT \"${doc_root}\"|" "$profile"
            else
                sed -i "s|export ADF_DOC_ROOT=.*|export ADF_DOC_ROOT=\"${doc_root}\"|" "$profile"
            fi
            verbose "更新 ADF_DOC_ROOT in ${profile}"
        else
            # 首次写入
            {
                echo ""
                echo "# AgentDevFlow document root"
                if $fish; then
                    echo "set -gx ADF_DOC_ROOT \"${doc_root}\""
                else
                    echo "export ADF_DOC_ROOT=\"${doc_root}\""
                fi
            } >> "$profile"
            verbose "写入 ADF_DOC_ROOT to ${profile}"
        fi
    done

    # 设置当前 session 的环境变量
    export ADF_DOC_ROOT="${doc_root}"

    success "ADF_DOC_ROOT 已注入: ${doc_root}"
}

# ============================================================
# 安装主逻辑
# ============================================================

install_dev() {
    info "安装模式: dev (本地仓库)"
    verbose "源目录: $REPO_ROOT"
    verbose "目标目录: $TARGET_DIR"
    verbose "安装目录: $ADF_INSTALL_DIR"

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

    # 1. 安装共享技能（skills/）-> ~/.claude/skills/
    local shared_source="${REPO_ROOT}/skills"
    local shared_target="${ADF_SKILLS_DIR}"

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

    # 2. 安装 Claude 适配器技能包
    local adapter_source="${REPO_ROOT}/adapters/claude/.claude/skills"
    local adapter_target="${ADF_SKILLS_DIR}"

    if [[ -d "$adapter_source" ]]; then
        info "安装 Claude 适配器到 ${adapter_target}..."
        if $DRY_RUN; then
            info "[DRY-RUN] cp -r ${adapter_source}/* ${adapter_target}/"
        else
            mkdir -p "$adapter_target"
            for skill_dir in "$adapter_source"/*/; do
                [[ -d "$skill_dir" ]] || continue
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
    fi

    # 3. 安装 prompts/ -> ~/.claude/AgentDevFlow/prompts/（Tech Spec §1.1 新增）
    copy_md_files "${REPO_ROOT}/prompts" "${ADF_INSTALL_DIR}/prompts" "prompts"

    # 4. 安装 docs/governance/ -> ~/.claude/AgentDevFlow/docs/governance/（Tech Spec §1.1 新增）
    copy_md_files "${REPO_ROOT}/docs/governance" "${ADF_INSTALL_DIR}/docs/governance" "docs/governance"

    # 5. 安装 docs/platforms/ -> ~/.claude/AgentDevFlow/docs/platforms/（Tech Spec §1.1 新增）
    if [[ -d "${REPO_ROOT}/docs/platforms" ]]; then
        copy_md_files "${REPO_ROOT}/docs/platforms" "${ADF_INSTALL_DIR}/docs/platforms" "docs/platforms"
    fi

    # 6. 安装 scripts/ -> ~/.claude/AgentDevFlow/scripts/（Tech Spec §1.1 新增）
    info "安装 scripts 到 ${ADF_INSTALL_DIR}/scripts/..."
    if $DRY_RUN; then
        info "[DRY-RUN] copy scripts/*.py -> ${ADF_INSTALL_DIR}/scripts/"
    else
        mkdir -p "${ADF_INSTALL_DIR}/scripts"
        for script_file in "${REPO_ROOT}/scripts"/*.py "${REPO_ROOT}/scripts"/*.sh; do
            [[ -f "$script_file" ]] || continue
            local script_name
            script_name=$(basename "$script_file")
            local tgt_script="${ADF_INSTALL_DIR}/scripts/${script_name}"

            if [[ -f "$tgt_script" && "$FORCE" == false ]]; then
                verbose "跳过（已存在）: scripts/${script_name}"
            else
                verbose "安装: scripts/${script_name}"
                cp "$script_file" "$tgt_script"
            fi
        done
    fi

    # 7. 安装 README.md -> ~/.claude/AgentDevFlow/README.md（Tech Spec §1.1 新增）
    if [[ -f "${REPO_ROOT}/README.md" ]]; then
        info "安装 README.md..."
        if ! $DRY_RUN; then
            if [[ -f "${ADF_INSTALL_DIR}/README.md" && "$FORCE" == false ]]; then
                verbose "跳过（已存在）: README.md"
            else
                cp "${REPO_ROOT}/README.md" "${ADF_INSTALL_DIR}/README.md"
            fi
        fi
    fi

    # 8. 创建 shared 占位文件（Tech Spec §2.7）
    info "创建 shared 安装能力位..."
    if ! $DRY_RUN; then
        mkdir -p "${ADF_SKILLS_DIR}/shared"
        if [[ ! -f "${ADF_SKILLS_DIR}/shared/.keep" ]]; then
            touch "${ADF_SKILLS_DIR}/shared/.keep"
            verbose "创建: skills/shared/.keep"
        fi
    fi

    # 9. 注入 ADF_DOC_ROOT 环境变量（Tech Spec §4）
    inject_adf_doc_root

    # 写入版本文件
    if ! $DRY_RUN; then
        mkdir -p "${ADF_SKILLS_DIR}"
        echo "$current_version" > "${ADF_SKILLS_DIR}/.agentdevflow-version"
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

# ============================================================
# 安装后完备性检查（Tech Spec §5）
# ============================================================

# 检查最小清单中的文件是否存在且可读
check_minimum_files() {
    local dir="$1"
    shift
    local files=("$@")
    local missing=()
    local checked=0
    local passed=0

    for f in "${files[@]}"; do
        checked=$((checked + 1))
        if [[ -f "${dir}/${f}" && -r "${dir}/${f}" ]]; then
            passed=$((passed + 1))
        else
            missing+=("$f")
        fi
    done

    echo "$checked" "$passed" "${missing[*]}"
}

completeness_check() {
    info "执行安装后完备性检查..."

    if $DRY_RUN; then
        info "[DRY-RUN] 跳过完备性检查"
        return
    fi

    local timestamp
    timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    local overall="complete"
    local checks_json="["

    # --- prompts ---
    local prompts_result
    prompts_result=$(check_minimum_files "${ADF_INSTALL_DIR}/prompts" "${PROMPTS_MINIMUM[@]}")
    read -r prompts_checked prompts_passed prompts_missing <<< "$prompts_result"
    local prompts_status="pass"
    local prompts_missing_arr=()
    if [[ -n "$prompts_missing" ]]; then
        IFS=' ' read -ra prompts_missing_arr <<< "$prompts_missing"
        prompts_status="fail"
        overall="incomplete"
    fi
    local prompts_missing_json="[]"
    if [[ ${#prompts_missing_arr[@]} -gt 0 ]]; then
        prompts_missing_json=$(printf '"%s",' "${prompts_missing_arr[@]}")
        prompts_missing_json="[${prompts_missing_json%,}]"
    fi
    checks_json+="{\"category\":\"prompts\",\"path\":\"${ADF_INSTALL_DIR}/prompts/\",\"status\":\"${prompts_status}\",\"checked_items\":${prompts_checked},\"passed_items\":${prompts_passed},\"missing_items\":${prompts_missing_json},\"details\":\"prompts 最小清单检查\"},"

    # --- docs/governance ---
    local gov_result
    gov_result=$(check_minimum_files "${ADF_INSTALL_DIR}/docs/governance" "${GOVERNANCE_MINIMUM[@]}")
    read -r gov_checked gov_passed gov_missing <<< "$gov_result"
    local gov_status="pass"
    local gov_missing_arr=()
    if [[ -n "$gov_missing" ]]; then
        IFS=' ' read -ra gov_missing_arr <<< "$gov_missing"
        gov_status="fail"
        overall="incomplete"
    fi
    local gov_missing_json="[]"
    if [[ ${#gov_missing_arr[@]} -gt 0 ]]; then
        gov_missing_json=$(printf '"%s",' "${gov_missing_arr[@]}")
        gov_missing_json="[${gov_missing_json%,}]"
    fi
    checks_json+="{\"category\":\"docs/governance\",\"path\":\"${ADF_INSTALL_DIR}/docs/governance/\",\"status\":\"${gov_status}\",\"checked_items\":${gov_checked},\"passed_items\":${gov_passed},\"missing_items\":${gov_missing_json},\"details\":\"docs/governance 最小清单检查\"},"

    # --- docs/platforms ---
    local plat_result
    plat_result=$(check_minimum_files "${ADF_INSTALL_DIR}/docs/platforms" "${PLATFORMS_MINIMUM[@]}")
    read -r plat_checked plat_passed plat_missing <<< "$plat_result"
    local plat_status="pass"
    local plat_missing_arr=()
    if [[ -n "$plat_missing" ]]; then
        IFS=' ' read -ra plat_missing_arr <<< "$plat_missing"
        plat_status="fail"
        overall="incomplete"
    fi
    local plat_missing_json="[]"
    if [[ ${#plat_missing_arr[@]} -gt 0 ]]; then
        plat_missing_json=$(printf '"%s",' "${plat_missing_arr[@]}")
        plat_missing_json="[${plat_missing_json%,}]"
    fi
    checks_json+="{\"category\":\"docs/platforms\",\"path\":\"${ADF_INSTALL_DIR}/docs/platforms/\",\"status\":\"${plat_status}\",\"checked_items\":${plat_checked},\"passed_items\":${plat_passed},\"missing_items\":${plat_missing_json},\"details\":\"docs/platforms 最小清单检查\"},"

    # --- stable skills ---
    local skill_dirs=("start-agent-team" "team-setup" "product-manager" "architect" "qa-engineer" "engineer" "platform-sre" "pmo" "pmo-review" "agent-bootstrap")
    local skill_checked=${#skill_dirs[@]}
    local skill_passed=0
    local skill_missing_arr=()
    for sd in "${skill_dirs[@]}"; do
        if [[ -f "${ADF_SKILLS_DIR}/${sd}/SKILL.md" && -r "${ADF_SKILLS_DIR}/${sd}/SKILL.md" ]]; then
            skill_passed=$((skill_passed + 1))
        else
            skill_missing_arr+=("${sd}/SKILL.md")
        fi
    done
    local skill_status="pass"
    if [[ ${#skill_missing_arr[@]} -gt 0 ]]; then
        skill_status="fail"
        overall="incomplete"
    fi
    local skill_missing_json="[]"
    if [[ ${#skill_missing_arr[@]} -gt 0 ]]; then
        skill_missing_json=$(printf '"%s",' "${skill_missing_arr[@]}")
        skill_missing_json="[${skill_missing_json%,}]"
    fi
    checks_json+="{\"category\":\"stable-skills\",\"path\":\"${ADF_SKILLS_DIR}/\",\"status\":\"${skill_status}\",\"checked_items\":${skill_checked},\"passed_items\":${skill_passed},\"missing_items\":${skill_missing_json},\"details\":\"稳定版 skill 目录与 SKILL.md 检查\"},"

    # --- workflows ---
    local wf_result
    wf_result=$(check_minimum_files "${ADF_SKILLS_DIR}/workflows" "${WORKFLOWS_MINIMUM[@]}")
    read -r wf_checked wf_passed wf_missing <<< "$wf_result"
    local wf_status="pass"
    local wf_missing_arr=()
    if [[ -n "$wf_missing" ]]; then
        IFS=' ' read -ra wf_missing_arr <<< "$wf_missing"
        wf_status="fail"
        overall="incomplete"
    fi
    local wf_missing_json="[]"
    if [[ ${#wf_missing_arr[@]} -gt 0 ]]; then
        wf_missing_json=$(printf '"%s",' "${wf_missing_arr[@]}")
        wf_missing_json="[${wf_missing_json%,}]"
    fi
    checks_json+="{\"category\":\"workflows\",\"path\":\"${ADF_SKILLS_DIR}/workflows/\",\"status\":\"${wf_status}\",\"checked_items\":${wf_checked},\"passed_items\":${wf_passed},\"missing_items\":${wf_missing_json},\"details\":\"workflows 最小清单检查\"},"

    # --- shared ---
    local shared_status="fail"
    local shared_checked=1
    local shared_passed=0
    local shared_missing_json="[]"
    local shared_details=""
    if [[ -d "${ADF_SKILLS_DIR}/shared" ]]; then
        if [[ -f "${ADF_SKILLS_DIR}/shared/.keep" ]]; then
            shared_status="warn"
            shared_passed=1
            shared_details="shared 目录存在；当前无共享业务文件时为可接受空能力位状态"
        else
            # 目录存在但无 .keep，检查是否有其他文件
            local shared_file_count
            shared_file_count=$(find "${ADF_SKILLS_DIR}/shared" -type f 2>/dev/null | wc -l)
            if [[ "$shared_file_count" -gt 0 ]]; then
                shared_status="pass"
                shared_passed=1
                shared_details="shared 目录存在，包含 ${shared_file_count} 个共享资产文件"
            else
                shared_status="warn"
                shared_passed=1
                shared_details="shared 目录存在但为空（无占位文件），建议创建 .keep"
            fi
        fi
    else
        shared_status="fail"
        shared_missing_json="[\"shared/\"]"
        shared_details="shared 目录缺失，安装不完整"
        overall="incomplete"
    fi
    checks_json+="{\"category\":\"shared\",\"path\":\"${ADF_SKILLS_DIR}/shared/\",\"status\":\"${shared_status}\",\"checked_items\":${shared_checked},\"passed_items\":${shared_passed},\"missing_items\":${shared_missing_json},\"details\":\"${shared_details}\"},"

    # --- templates ---
    local tmpl_result
    tmpl_result=$(check_minimum_files "${ADF_SKILLS_DIR}/templates" "${TEMPLATES_MINIMUM[@]}")
    read -r tmpl_checked tmpl_passed tmpl_missing <<< "$tmpl_result"
    local tmpl_status="pass"
    local tmpl_missing_arr=()
    if [[ -n "$tmpl_missing" ]]; then
        IFS=' ' read -ra tmpl_missing_arr <<< "$tmpl_missing"
        tmpl_status="fail"
        overall="incomplete"
    fi
    local tmpl_missing_json="[]"
    if [[ ${#tmpl_missing_arr[@]} -gt 0 ]]; then
        tmpl_missing_json=$(printf '"%s",' "${tmpl_missing_arr[@]}")
        tmpl_missing_json="[${tmpl_missing_json%,}]"
    fi
    checks_json+="{\"category\":\"templates\",\"path\":\"${ADF_SKILLS_DIR}/templates/\",\"status\":\"${tmpl_status}\",\"checked_items\":${tmpl_checked},\"passed_items\":${tmpl_passed},\"missing_items\":${tmpl_missing_json},\"details\":\"templates 最小清单检查\"},"

    # --- scripts ---
    local scr_result
    scr_result=$(check_minimum_files "${ADF_INSTALL_DIR}/scripts" "${SCRIPTS_MINIMUM[@]}")
    read -r scr_checked scr_passed scr_missing <<< "$scr_result"
    local scr_status="pass"
    local scr_missing_arr=()
    if [[ -n "$scr_missing" ]]; then
        IFS=' ' read -ra scr_missing_arr <<< "$scr_missing"
        scr_status="fail"
        overall="incomplete"
    fi
    local scr_missing_json="[]"
    if [[ ${#scr_missing_arr[@]} -gt 0 ]]; then
        scr_missing_json=$(printf '"%s",' "${scr_missing_arr[@]}")
        scr_missing_json="[${scr_missing_json%,}]"
    fi
    checks_json+="{\"category\":\"scripts\",\"path\":\"${ADF_INSTALL_DIR}/scripts/\",\"status\":\"${scr_status}\",\"checked_items\":${scr_checked},\"passed_items\":${scr_passed},\"missing_items\":${scr_missing_json},\"details\":\"核心脚本检查\"},"

    # --- ADF_DOC_ROOT ---
    local env_status="fail"
    local env_checked=1
    local env_passed=0
    local env_details=""
    if [[ -n "${ADF_DOC_ROOT:-}" && "${ADF_DOC_ROOT}" == "${ADF_INSTALL_DIR}" ]]; then
        env_status="pass"
        env_passed=1
        env_details="ADF_DOC_ROOT 已设置为 ${ADF_DOC_ROOT}"
    elif [[ -n "${ADF_DOC_ROOT:-}" ]]; then
        env_status="fail"
        env_details="ADF_DOC_ROOT 指向旧路径: ${ADF_DOC_ROOT}（期望: ${ADF_INSTALL_DIR}）"
        overall="incomplete"
    else
        env_details="ADF_DOC_ROOT 未设置，请重启终端或手动执行: export ADF_DOC_ROOT=\"${ADF_INSTALL_DIR}\""
        overall="incomplete"
    fi
    checks_json+="{\"category\":\"adf-doc-root\",\"path\":\"环境变量\",\"status\":\"${env_status}\",\"checked_items\":${env_checked},\"passed_items\":${env_passed},\"missing_items\":[],\"details\":\"${env_details}\"}"

    checks_json+="]"

    # --- 关键入口最小验证集（Tech Spec §5.5）---
    # 验证四类关键入口可真实读取
    local entry_missing=()

    # 1) PM Skill → prompts/002_develop_pipeline.md
    if [[ ! -r "${ADF_INSTALL_DIR}/prompts/002_develop_pipeline.md" ]]; then
        entry_missing+=("prompts/002_develop_pipeline.md（PM Skill 必读）")
    fi

    # 2) workflows/tech-review.md
    if [[ ! -r "${ADF_SKILLS_DIR}/workflows/tech-review.md" ]]; then
        entry_missing+=("workflows/tech-review.md（Architect 必读）")
    fi

    # 3) skills/shared/ 目录或占位文件
    if [[ ! -d "${ADF_SKILLS_DIR}/shared" ]]; then
        entry_missing+=("skills/shared/（shared 安装能力位）")
    fi

    # 4) templates/prd-template.md
    if [[ ! -r "${ADF_SKILLS_DIR}/templates/prd-template.md" ]]; then
        entry_missing+=("templates/prd-template.md（PM 使用）")
    fi

    if [[ ${#entry_missing[@]} -gt 0 ]]; then
        overall="incomplete"
    fi

    # --- 汇总 missing ---
    local critical_missing=()
    local warning_missing=()

    # 收集所有 fail 类别的 missing items
    for check in "${prompts_missing_arr[@]}" "${gov_missing_arr[@]}" "${plat_missing_arr[@]}" "${skill_missing_arr[@]}" "${wf_missing_arr[@]}" "${tmpl_missing_arr[@]}" "${scr_missing_arr[@]}"; do
        [[ -n "$check" ]] && critical_missing+=("$check")
    done
    if [[ "$shared_status" == "fail" ]]; then
        critical_missing+=("skills/shared/ 目录缺失")
    fi
    if [[ "$env_status" == "fail" ]]; then
        warning_missing+=("ADF_DOC_ROOT 环境变量未正确设置")
    fi
    if [[ "$shared_status" == "warn" ]]; then
        warning_missing+=("skills/shared/ 当前无共享业务文件（可接受空能力位状态）")
    fi
    for e in "${entry_missing[@]}"; do
        critical_missing+=("$e")
    done

    local critical_json="[]"
    if [[ ${#critical_missing[@]} -gt 0 ]]; then
        critical_json=$(printf '"%s",' "${critical_missing[@]}")
        critical_json="[${critical_json%,}]"
    fi
    local warning_json="[]"
    if [[ ${#warning_missing[@]} -gt 0 ]]; then
        warning_json=$(printf '"%s",' "${warning_missing[@]}")
        warning_json="[${warning_json%,}]"
    fi

    local recommendation="安装完整，可继续使用。"
    if [[ "$overall" == "incomplete" ]]; then
        recommendation="安装不完整，建议重新执行安装脚本。"
    fi

    # 构建最终 JSON
    local json_output
    json_output=$(cat <<EOJSON
{
  "check_version": "2.0",
  "timestamp": "${timestamp}",
  "install_path": "${ADF_INSTALL_DIR}",
  "overall_status": "${overall}",
  "checks": ${checks_json},
  "missing_summary": {
    "critical": ${critical_json},
    "warning": ${warning_json}
  },
  "recommendation": "${recommendation}"
}
EOJSON
)

    # 输出到 stdout
    echo ""
    echo "$json_output"

    # 写入日志文件（Tech Spec §5.2）
    mkdir -p "${ADF_INSTALL_DIR}"
    echo "$json_output" > "${ADF_INSTALL_DIR}/.install-check.log"
    verbose "完备性检查日志: ${ADF_INSTALL_DIR}/.install-check.log"

    # 友好输出
    echo ""
    if [[ "$overall" == "complete" ]]; then
        success "安装完备性检查: 通过"
    else
        warn "安装完备性检查: 不完整"
        if [[ ${#critical_missing[@]} -gt 0 ]]; then
            error "关键缺失项:"
            for m in "${critical_missing[@]}"; do
                echo "  - $m"
            done
        fi
        if [[ ${#warning_missing[@]} -gt 0 ]]; then
            warn "警告项:"
            for m in "${warning_missing[@]}"; do
                echo "  - $m"
            done
        fi
    fi
}

# ============================================================
# 卸载（Tech Spec §4 卸载）
# ============================================================

do_uninstall() {
    info "卸载 AgentDevFlow..."

    local version
    version=$(get_installed_version)
    if [[ -z "$version" ]]; then
        warn "未检测到已安装的 AgentDevFlow 版本"
    else
        info "当前已安装版本: v${version}"
    fi

    echo ""
    warn "即将卸载 AgentDevFlow，以下 ADF 管理的 skill 和文件将被删除："
    echo ""
    info "Skill 目录（${ADF_SKILLS_DIR}/ 下）："
    for sd in "${ADF_MANAGED_SKILL_DIRS[@]}"; do
        [[ -d "${ADF_SKILLS_DIR}/${sd}" ]] && echo "  - ${sd}/"
    done
    echo ""
    info "文档目录："
    echo "  - ${ADF_INSTALL_DIR}/"
    echo ""
    warn "注意：${ADF_SKILLS_DIR}/ 下非 ADF 管理的 skill 不会被删除"
    echo ""
    warn "Shell profile 中的 ADF_DOC_ROOT 将被注释保留（不删除）"
    echo ""

    if $DRY_RUN; then
        info "[DRY-RUN] 跳过实际卸载"
        return
    fi

    # 交互式确认
    read -r -p "确认卸载? [y/N] " confirm
    if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
        info "已取消卸载"
        return
    fi

    # 只删除 ADF 管理的 skill 目录（安全卸载，不碰用户其他 skill）
    local removed_any=false
    if [[ -d "${ADF_SKILLS_DIR}" ]]; then
        for sd in "${ADF_MANAGED_SKILL_DIRS[@]}"; do
            local skill_path="${ADF_SKILLS_DIR}/${sd}"
            if [[ -d "$skill_path" ]]; then
                rm -rf "$skill_path"
                verbose "已删除 skill: ${sd}/"
                removed_any=true
            fi
        done

        # 删除 ADF 管理的根级文件
        for sf in "${ADF_MANAGED_SKILL_FILES[@]}"; do
            local file_path="${ADF_SKILLS_DIR}/${sf}"
            if [[ -f "$file_path" ]]; then
                rm -f "$file_path"
                verbose "已删除文件: ${sf}"
                removed_any=true
            fi
        done

        # 若 skills/ 目录已空（无子目录且无文件），则删除目录本身
        if $removed_any; then
            local remaining_dirs
            remaining_dirs=$(find "${ADF_SKILLS_DIR}" -mindepth 1 -maxdepth 1 -type d 2>/dev/null | wc -l)
            local remaining_files
            remaining_files=$(find "${ADF_SKILLS_DIR}" -maxdepth 1 -type f 2>/dev/null | wc -l)
            if [[ "$remaining_dirs" -eq 0 && "$remaining_files" -eq 0 ]]; then
                rmdir "${ADF_SKILLS_DIR}" 2>/dev/null || true
                verbose "已删除空目录: ${ADF_SKILLS_DIR}/"
            else
                info "保留非 ADF skill 和文件在 ${ADF_SKILLS_DIR}/"
            fi
            success "ADF 管理的 skill 已卸载"
        else
            warn "未找到 ADF 管理的 skill 目录"
        fi
    fi

    # 删除 AgentDevFlow 文档目录（安全，ADF 专属）
    if [[ -d "${ADF_INSTALL_DIR}" ]]; then
        rm -rf "${ADF_INSTALL_DIR}"
        success "已删除: ${ADF_INSTALL_DIR}/"
    fi

    # 注释 ADF_DOC_ROOT（保留备份）
    local profiles=()
    [[ -f "${HOME}/.bashrc" ]] && profiles+=("${HOME}/.bashrc")
    [[ -f "${HOME}/.zshrc" ]] && profiles+=("${HOME}/.zshrc")
    [[ -f "${HOME}/.config/fish/config.fish" ]] && profiles+=("${HOME}/.config/fish/config.fish")

    for profile in "${profiles[@]}"; do
        if grep -q 'ADF_DOC_ROOT' "$profile" 2>/dev/null; then
            # 注释掉 ADF_DOC_ROOT 行（保留备份）
            if [[ "$profile" == *"/fish/config.fish" ]]; then
                sed -i 's|^\(\s*set -gx ADF_DOC_ROOT .*\)|# [ADF uninstalled] \1|' "$profile"
            else
                sed -i 's|^\(\s*export ADF_DOC_ROOT=.*\)|# [ADF uninstalled] \1|' "$profile"
            fi
            sed -i 's|^\(\s*# AgentDevFlow document root\)|# [ADF uninstalled] \1|' "$profile"
            verbose "已注释 ADF_DOC_ROOT in ${profile}"
        fi
    done

    echo ""
    success "AgentDevFlow 卸载完成"
}

# ============================================================
# 入口
# ============================================================

show_next_steps() {
    local version="$1"
    echo ""
    echo "============================================"
    success "AgentDevFlow v${version} 安装完成！"
    echo "============================================"
    echo ""
    info "安装目录:"
    echo "  Skills:   ${ADF_SKILLS_DIR}/"
    echo "  Docs:     ${ADF_INSTALL_DIR}/"
    echo ""
    info "下一步:"
    echo "  1. 重启终端或执行: source ~/.bashrc（使 ADF_DOC_ROOT 生效）"
    echo "  2. 重启 Claude Code 以加载新技能"
    echo "  3. 在 Claude Code 中使用以下命令启动团队:"
    echo "     /agent-bootstrap   # 自举 AgentDevFlow 项目"
    echo "     /start-agent-team  # 启动交付团队"
    echo ""
    info "更多信息请查看:"
    echo "  - ${ADF_INSTALL_DIR}/README.md"
    echo "  - ${ADF_SKILLS_DIR}/README.md"
    echo ""
}

main() {
    parse_args "$@"

    echo ""
    echo "============================================"
    echo "  AgentDevFlow Install Script v2.0"
    echo "============================================"
    echo ""

    if $DRY_RUN; then
        warn "DRY-RUN 模式：不会进行实际变更"
        echo ""
    fi

    if $UNINSTALL; then
        do_uninstall
        return
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

    completeness_check

    if ! $UNINSTALL; then
        local version
        version=$(get_current_version)
        show_next_steps "$version"
    fi
}

main "$@"
