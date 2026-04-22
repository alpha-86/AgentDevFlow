---
name: 安装脚本安装结果完备性与路径映射 — Tech Spec v2.0
description: 基于 PRD #019 v2.0 的当前有效 Tech Spec，定义安装到 ~/.claude/ 后全量安装结果的路径映射、逐层依赖分析、引用解析、完备性检查与 fallback 行为
status: Approved
note: "Gate 2 Approved（PM + QA + Engineer 三方签字），Tech Spec 已完成评审收口"
owner: Architect
date: 2026-04-22
update_date: 2026-04-22
issue: "#19"
prd: docs/prd/019_installation_script_doc_path_2026-04-22.md
---

# Tech Spec #019 — 安装脚本安装结果完备性与路径映射（v2.0）

---

**ID**: Tech-19_v2.0
**状态**: Approved
**负责人**: Architect
**日期**: 2026-04-22
**更新日期**: 2026-04-22
**基于**: PRD #019 v2.0（Gate 1 Approved, 2026-04-22）
**当前评审状态**: Gate 2 Approved（PM + QA + Engineer 三签，2026-04-22）

**前提修正**：外部安装态目标路径为 `~/.claude/skills/` 下的稳定版 skill namespace（无 `adf-` 前缀）；`adf-` 前缀仅用于本仓开发态 `.claude/skills/adf-*` 自举隔离。

---

## 上下文

Issue #19 的核心问题是 AgentDevFlow 安装到 `~/.claude/` 后，安装结果是否完整、skill 引用是否能在安装态下真实解析、以及缺失场景是否能被显式暴露。本 Tech Spec 定义全量安装产物的路径映射、逐层依赖分析、打包目录规则、引用解析、完备性检查与 fallback 规则。

**PRD v2.0 重大变更**：新增 §4.5 逐层依赖分析、§4.6 打包目录准入/准出规则、§4.7 CLAUDE.md 规则沉淀。

---

## 1. 路径映射规则

### 1.1 安装态路径映射

| 开发目录 | 安装目录 | 映射规则 | 准入类型 |
|---|---|---|---|
| `prompts/` | `~/.claude/AgentDevFlow/prompts/` | 安装时复制 prompts 到安装目录 | 必须 |
| `docs/` | `~/.claude/AgentDevFlow/docs/` | 安装时复制 docs 到安装目录 | 必须 |
| `docs/governance/` | `~/.claude/AgentDevFlow/docs/governance/` | 安装时复制 governance 到安装目录 | 必须 |
| `skills/*/SKILL.md` | `~/.claude/skills/<stable-skill>/SKILL.md` | 安装时复制到稳定版 skill namespace（无 `adf-` 前缀） | 必须 |
| `skills/workflows/` | `~/.claude/skills/workflows/` | 安装时复制 workflows 到稳定路径 | 必须 |
| `skills/shared/` | `~/.claude/skills/shared/` | 安装时必须创建 shared 安装能力位；当前无共享资产时可为空目录或占位文件 | 必须 |
| `skills/templates/` | `~/.claude/skills/templates/` | 安装时复制 templates 到稳定路径 | 必须 |
| `scripts/` | `~/.claude/AgentDevFlow/scripts/` | 安装时复制 scripts 到安装目录 | 必须 |

**路径隔离原则**：文档安装目录独立于 skill namespace；外部安装态统一使用稳定版 skill namespace（无 `adf-` 前缀），避免与本仓开发态 `.claude/skills/adf-*` 自举产物混淆。

### 1.2 安装态路径适配范围

本 Tech Spec 覆盖安装后 skill 对以下路径的可达性：

- `skills/*/SKILL.md` 中的必读文档引用（prompts/ + docs/ + skills/workflows/ + skills/shared/ + skills/templates/）
- `skills/workflows/*.md` 中的交叉引用
- skill 中对 `scripts/` 下脚本的调用引用
- skill 中对 `docs/governance/` 下治理文档的引用
- 增强层文档 `docs/platforms/enhancement-layer.md` 的引用（当前为开发目录相对路径，需处理）

**统一要求**：安装后所有上述引用均不得再依赖开发目录相对路径，必须能解析到 `~/.claude/AgentDevFlow/` 或 `~/.claude/skills/` 下的稳定安装态路径。

---

## 2. 逐层依赖分析

### 2.1 分析起点与范围

**起点**：`skills/start-agent-team/SKILL.md`

**分析覆盖的所有 Skill（10个）**：

| # | Skill 目录 | 类别 | 准入判定 |
|---|-----------|------|---------|
| 1 | `start-agent-team/` | 入口 Skill | 必须 — 团队启动入口 |
| 2 | `team-setup/` | 核心 Skill | 必须 — start-agent-team 直接引用 |
| 3 | `product-manager/` | 核心 Skill | 必须 — start-agent-team Agent 创建映射 |
| 4 | `architect/` | 核心 Skill | 必须 — start-agent-team Agent 创建映射 |
| 5 | `qa-engineer/` | 核心 Skill | 必须 — start-agent-team Agent 创建映射 |
| 6 | `engineer/` | 核心 Skill | 必须 — start-agent-team Agent 创建映射 |
| 7 | `platform-sre/` | 核心 Skill | 必须 — start-agent-team Agent 创建映射 |
| 8 | `pmo/` | 核心 Skill | 必须 — start-agent-team Agent 创建映射 |
| 9 | `agent-bootstrap/` | 核心 Skill | 必须 — 自举启动入口 |
| 10 | `pmo-review/` | 辅助 Skill | 必须 — pmo 增强能力 |

**顶级共享文件**：
- `skills/README.md` — 项目概述
- `skills/skill-protocol.md` — 共享协议
- `skills/event-bus.md` — 事件总线

### 2.2 依赖分析矩阵

以 start-agent-team 为起点，逐层展开的文件依赖：

| Skill / 文件 | prompts/ | docs/ | docs/gov/ | workflows/ | shared/ | templates/ | scripts/ | 增强层 |
|-------------|----------|-------|-----------|------------|---------|------------|----------|--------|
| start-agent-team | 3项 | 0 | 0 | 5项 | 0 | 0 | 2项 | 引用 |
| team-setup | 3项 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| product-manager | 7项 | 0 | 0 | 3项 | 0 | 2项 | 0 | 引用 |
| architect | 7项 | 0 | 0 | 3项 | 0 | 2项 | 0 | 0 |
| qa-engineer | 8项 | 0 | 0 | 4项 | 0 | 3项 | 0 | 引用 |
| engineer | 8项 | 0 | 0 | 2项 | 0 | 1项 | 0 | 引用 |
| platform-sre | 6项 | 0 | 1项 | 2项 | 0 | 2项 | 0 | 0 |
| pmo | 8项 | 0 | 1项 | 2项 | 0 | 2项 | 0 | 引用 |
| agent-bootstrap | 4项 | 1项 | 1项 | 0 | 0 | 0 | 0 | 0 |

**补充说明**：
- `engineer` 逐层依赖已在 Gate 2 前完成：其一级输入来自 8 个 prompts；二级输入来自 `skills/workflows/implementation.md`、`skills/workflows/qa-validation.md`；三级输入包含 `skills/templates/review-comment-template.md` 与增强层文档 `docs/platforms/enhancement-layer.md`。因此其最小必要安装集合为 prompts + workflows + templates + enhancement-layer 文档，**不再 defer**。
- `platform-sre` 逐层依赖已在 Gate 2 前完成：其一级输入来自 6 个 prompts；二级输入来自 `docs/governance/platform-minimum-checks.md` 与 `skills/workflows/release-review.md`、`skills/workflows/anomaly-response.md`；三级输入来自 `skills/templates/release-record-template.md`、`skills/templates/platform-check-result-template.md`。因此其最小必要安装集合为 prompts + docs/governance + workflows + templates，**不再 defer**。
- `agent-bootstrap` 逐层依赖已在 Gate 2 前完成：其一级输入来自 `prompts/002_develop_pipeline.md`、`prompts/001_team_topology.md`、`prompts/010_team_setup_and_bootstrap.md`；二级输入来自 `skills/start-agent-team.md`、`skills/skill-protocol.md`、`skills/event-bus.md`；三级输入来自 `docs/governance/core-principles.md` 与 `README.md`。因此其最小必要安装集合为 prompts + 顶级 shared skill 源文件 + docs/governance + README，**不再 defer**。
- `docs/todo/` 与 `docs/memo/` 已显式分析：两者均被 start-agent-team / agent-bootstrap 的项目初始化语义间接涉及，但仅作为目标项目运行期状态目录存在，结论均为**不打包历史内容**；如需骨架能力，由安装后的初始化流程创建空目录或模板化起始文件。
- 当前 9 个核心 skill（start-agent-team、team-setup、product-manager、architect、qa-engineer、engineer、platform-sre、pmo、agent-bootstrap）已全部完成逐层依赖分析，满足 PRD §7.7 “覆盖所有核心 skill”的 Gate 2 前置要求。
- 当前仓库内 `skills/shared/` 为独立安装类别，即使本轮逐层依赖未发现显式文件级引用，也必须按 PRD 要求纳入安装产物、完备性检查与异常告警范围，避免后续 shared 资产落地时遗漏安装链路。

### 2.3 关键 prompts 最小清单（解决 v1.0 Conditional 条件1）

基于逐层依赖分析，以下为 **必须打包的 prompts 最小清单**：

| # | 文件 | 准入理由 |
|---|------|---------|
| 1 | `prompts/001_team_topology.md` | 所有角色必读 |
| 2 | `prompts/002_develop_pipeline.md` | 所有角色必读（核心流程） |
| 3 | `prompts/004_delivery_gates.md` | PM/Architect/QA/Engineer 必读 |
| 4 | `prompts/010_team_setup_and_bootstrap.md` | start-agent-team/team-setup 必读 |
| 5 | `prompts/018_issue_routing_and_project_portfolio.md` | start-agent-team/team-setup 必读 |
| 6 | `prompts/003_document_contracts.md` | PM/Architect/QA 必读 |
| 7 | `prompts/007_issue_driven_orchestration.md` | PM/PMO 必读 |
| 8 | `prompts/013_github_issue_and_review_comments.md` | PM/QA/PMO 必读 |
| 9 | `prompts/017_human_review_and_signoff.md` | PM/Architect/QA/Engineer/PMO 必读 |
| 10 | `prompts/019_dual_stage_pr_and_three_layer_safeguard.md` | PM/Engineer/Platform-SRE/PMO 必读 |

**其他 prompts**（如 `002_product_engineering_roles.md`, `005_meeting_and_todo.md`, `008_change_record_and_revalidation.md` 等）在依赖矩阵中被引用但频次较低，归为**可选打包**（安装脚本应复制全部 prompts/ 目录，但完备性检查时优先验证最小清单）。

### 2.4 关键 docs 最小清单

| # | 文件/目录 | 准入理由 |
|---|----------|---------|
| 1 | `docs/governance/core-principles.md` | PMO 必读 |
| 2 | `docs/governance/skill-protocol.md` | PMO 必读 |
| 3 | `docs/governance/issue-naming-convention.md` | PMO 必读 |
| 4 | `docs/governance/platform-minimum-checks.md` | Platform/SRE 必读 |
| 5 | `docs/platforms/enhancement-layer.md` | PM/Architect/QA/PMO/Engineer 增强层引用 |

### 2.4.1 docs/todo 与 docs/memo 依赖分析结论

| 目录 | 结论 | 是否打包 | 理由 |
|------|------|----------|------|
| `docs/todo/` | 治理/运营运行态目录，当前仅在启动与项目状态维护中被引用 | **不打包** | 该目录承载目标项目自己的待办与阶段状态，属于运行期项目状态，不属于安装框架资产；安装后应由目标项目初始化生成，而不是携带 AgentDevFlow 仓库自身的历史任务数据 |
| `docs/memo/` | 治理/运营运行态目录，当前用于 kickoff、status board、审计纪要和 issue 过程留痕 | **不打包** | 该目录保存项目实例自己的会议纪要、审计记录和恢复上下文，属于运行期项目产物；安装脚本应提供骨架能力，但不应分发本仓历史 memo 样例或具体 issue 留痕 |

**结论说明**：
- `docs/todo/` 与 `docs/memo/` 已纳入逐层依赖分析范围，结论为“**运行期生成目录，不应打包**”；
- 其依赖语义属于“目录骨架/能力存在”而非“仓库内历史文件必须分发”；
- 安装脚本若需要支持目标项目初始化，应在首次运行时创建对应空目录或模板化初始文件，但不得复制本仓现有 `TODO_REGISTRY.md`、kickoff memo、project status 等历史内容。

### 2.5 关键 scripts 最小清单

| # | 文件 | 准入理由 |
|---|------|---------|
| 1 | `scripts/github_issue_sync.py` | start-agent-team 直接调用 |
| 2 | `scripts/task_router.py` | start-agent-team 直接调用 |
| 3 | `scripts/task_update.py` | 被 task_router 依赖 |
| 4 | `scripts/install.sh` | 安装脚本自身 |

### 2.6 关键 workflows 最小清单

| # | 文件 | 准入理由 |
|---|------|---------|
| 1 | `skills/workflows/tech-review.md` | Architect 必读 + start-agent-team 引用 |
| 2 | `skills/workflows/qa-validation.md` | QA/Engineer 必读 + start-agent-team 引用 |
| 3 | `skills/workflows/prd-review.md` | PM 必读 + start-agent-team 引用 |
| 4 | `skills/workflows/release-review.md` | Platform-SRE 必读 + start-agent-team 引用 |
| 5 | `skills/workflows/human-review.md` | PM/Architect/QA/Engineer 必读 |
| 6 | `skills/workflows/implementation.md` | Engineer 必读 |
| 7 | `skills/workflows/issue-lifecycle.md` | PMO 必读 |
| 8 | `skills/workflows/weekly-review.md` | start-agent-team/PMO 引用 |

### 2.7 关键 shared 最小清单

| # | 文件/目录 | 准入理由 |
|---|----------|---------|
| 1 | `skills/shared/` | PRD 明确要求安装后校验 shared 类产物完整性；即使当前仓库共享资产为空，也必须保留稳定安装路径与检查位 |
| 2 | `~/.claude/skills/shared/.keep` 或等效占位文件 | 当 shared 暂无业务文件时，确保安装态目录可创建、可检测、可告警 |
| 3 | 后续新增 shared 资产 | 任一核心 skill / workflow 开始依赖 shared 内容后，必须同步进入最小清单、安装脚本复制逻辑与完备性检查 |

**shared 目录规则**：
- `skills/shared/` 定义为**必须存在的安装能力位，内容可为空**；
- 当前若仓库 `skills/shared/` 为空，安装脚本仍需创建 `~/.claude/skills/shared/` 目录或等效占位文件；
- 完备性检查需区分“目录缺失（fail）”与“目录存在但当前无共享资产（warn）”两种状态；
- 一旦未来出现实际 shared 文件，shared 检查从“目录级”升级为“文件级最小清单”检查，无需修改路径模型。

### 2.8 关键 templates 最小清单（解决 QA conditional 条件2）

| # | 文件 | 准入理由 |
|---|------|---------|
| 1 | `skills/templates/tech-spec-template.md` | Architect 使用 |
| 2 | `skills/templates/prd-template.md` | PM 使用 |
| 3 | `skills/templates/qa-case-template.md` | QA 使用 |
| 4 | `skills/templates/qa-report-template.md` | QA 使用 |
| 5 | `skills/templates/review-comment-template.md` | 多角色共用 |
| 6 | `skills/templates/audit-report-template.md` | PMO 使用 |
| 7 | `skills/templates/release-record-template.md` | Platform/SRE 使用 |
| 8 | `skills/templates/platform-check-result-template.md` | Platform/SRE 使用 |

### 2.9 最小必要打包目录集

基于依赖矩阵，以下为 **必须打包的目录集**（解决 PRD v1.0 "关键文件"未定义问题）：

```
必须打包（准入）：
├── prompts/                    # 所有 prompts 文件
├── docs/governance/            # 治理文档
├── docs/platforms/             # 平台文档（含增强层）
├── skills/*/SKILL.md           # 所有稳定版 skill 入口
├── skills/README.md            # 项目概述
├── skills/skill-protocol.md    # 共享协议
├── skills/event-bus.md         # 事件总线
├── skills/workflows/*.md       # 所有 workflow 文件
├── skills/shared/              # shared 安装类别（当前可为空目录，但安装链路必须存在）
├── skills/templates/*.md       # 所有 template 文件
├── scripts/*.py                # 核心脚本
├── scripts/install.sh          # 安装脚本自身
└── README.md                   # 项目根 README（供参考）

不应打包（准出）：
├── .claude/                    # 运行时生成目录
├── docs/prd/                   # 项目特定交付产物（PRD 模板除外）
├── docs/tech/                  # 项目特定交付产物
├── docs/qa/                    # 项目特定交付产物
├── docs/memo/                  # 运行期纪要目录，历史内容不分发
├── docs/todo/                  # 运行期状态目录，历史内容不分发
├── docs/release/               # 项目特定交付产物
├── docs/pmo/                   # 项目特定交付产物
└── .github/                    # CI/CD 配置（非安装态必需）
```

**shared 准入说明**：`skills/shared/` 被视为独立安装类别，不以“当前是否已有业务文件”决定是否打包；目录本身属于路径契约的一部分，缺失即视为安装结果不完整。

**todo/memo 准出说明**：`docs/todo/` 与 `docs/memo/` 已完成依赖分析，但其现存文件属于当前仓库运行历史，不属于安装给外部用户的框架资产；安装态若需要项目骨架，应通过初始化流程创建空目录/初始模板，而不是复制本仓历史数据。

**"项目特定交付产物"界定**（解决 Minor note）：
- **不打包**：已完成的 Issue 交付产物（`docs/prd/PRD-*.md`, `docs/tech/Tech-*.md`, `docs/qa/*_v*.md` 等）
- **打包**：框架模板（`skills/templates/` 下的模板文件用于生成新文档）
- **不打包**：历史 memo、release record、待办 registry

---

## 3. Skill 引用适配

### 3.1 文档引用格式

Skill 中的文档引用统一使用环境变量 `${ADF_DOC_ROOT}` 解析：

```
文档引用格式：${ADF_DOC_ROOT}/prompts/002_develop_pipeline.md
其中 ADF_DOC_ROOT 由安装脚本设置，默认指向 ~/.claude/AgentDevFlow
```

### 3.2 安装前引用路径清理清单

当前 skill 中存在以下开发目录相对路径引用，安装脚本必须重写：

| 当前路径（开发态） | 安装态目标路径 | 处理方式 |
|-------------------|---------------|---------|
| `../../docs/platforms/enhancement-layer.md` | `${ADF_DOC_ROOT}/docs/platforms/enhancement-layer.md` | 安装时重写 |
| `prompts/xxx.md`（无前缀） | `${ADF_DOC_ROOT}/prompts/xxx.md` | 安装时重写 |
| `skills/workflows/xxx.md` | `~/.claude/skills/workflows/xxx.md`（相对 skill 路径） | 安装时重写 |
| `skills/templates/xxx.md` | `~/.claude/skills/templates/xxx.md`（相对 skill 路径） | 安装时重写 |
| `scripts/xxx.py` | `${ADF_DOC_ROOT}/scripts/xxx.py` | 安装时重写 |

---

## 4. ${ADF_DOC_ROOT} 注入时机与生命周期

| 阶段 | 行为 |
|---|---|
| **首次安装** | 安装脚本检测 shell profile（`~/.bashrc`、`~/.zshrc`、`~/.config/fish/config.fish` 等），追加 `export ADF_DOC_ROOT="${HOME}/.claude/AgentDevFlow"` |
| **重装 / 更新** | 安装脚本检查已有 `ADF_DOC_ROOT` 定义，若指向旧路径则替换为新路径；否则保留。写入 `.agentdevflow-version` 记录版本 |
| **运行时** | Skill 启动时检测 `${ADF_DOC_ROOT}` 是否存在，缺失则 fallback 到 `${HOME}/.claude/AgentDevFlow` 并提示用户 |
| **卸载** | 安装脚本提供 `--uninstall` 选项，可选移除环境变量声明（保留备份注释） |

**持久化策略**：环境变量写入用户 shell profile，确保跨 session 生效；Claude Code Desktop/Web 继承系统环境变量。

---

## 5. 安装后完备性检查机制

### 5.1 检查对象清单

安装脚本在完成复制与环境变量注入后，必须立即执行一次**安装后内容完备性检查**。

| 检查对象 | 预期安装路径 | 检查要求 | 成功判据 |
|---|---|---|---|
| prompts 最小清单 | `~/.claude/AgentDevFlow/prompts/` | 最小清单中 10 项全部存在且可读 | 10/10 通过 |
| docs/governance | `~/.claude/AgentDevFlow/docs/governance/` | 目录存在，core-principles.md 等关键文件可读 | 关键文件全部存在 |
| docs/platforms | `~/.claude/AgentDevFlow/docs/platforms/` | 目录存在，enhancement-layer.md 可读 | 文件存在 |
| stable skills | `~/.claude/skills/` 下各稳定版 skill | 目标 skill 存在，且 `SKILL.md` 可读 | 所有 skill 目录与 `SKILL.md` 存在 |
| workflows | `~/.claude/skills/workflows/` | 目录存在，关键 workflow 文件可读 | 8 项关键 workflow 全部存在 |
| shared | `~/.claude/skills/shared/` | 目录必须存在；若当前无共享资产则允许为空目录或占位文件；若有共享资产则最小清单可读 | shared 路径存在，状态统一为 pass/fail/warn |
| templates | `~/.claude/skills/templates/` | 目录存在，关键模板文件可读 | 8 项关键模板全部存在 |
| scripts | `~/.claude/AgentDevFlow/scripts/` | 目录存在，核心脚本可读 | github_issue_sync.py, task_router.py 等存在 |
| 环境变量 | `${ADF_DOC_ROOT}` | 已写入 shell profile 且可解析 | `echo $ADF_DOC_ROOT` 输出正确路径 |

### 5.2 完备性检查输出格式（解决 QA conditional 条件1）

检查结果以结构化 JSON 输出到标准输出（stdout），同时写入日志文件：

```json
{
  "check_version": "2.0",
  "timestamp": "2026-04-22T12:00:00Z",
  "install_path": "~/.claude/AgentDevFlow",
  "overall_status": "complete|incomplete",
  "checks": [
    {
      "category": "prompts",
      "path": "~/.claude/AgentDevFlow/prompts/",
      "status": "pass|fail|warn",
      "checked_items": 10,
      "passed_items": 10,
      "missing_items": [],
      "details": "..."
    },
    {
      "category": "shared",
      "path": "~/.claude/skills/shared/",
      "status": "pass|fail|warn",
      "checked_items": 1,
      "passed_items": 1,
      "missing_items": [],
      "details": "shared 目录存在；当前无共享业务文件时返回 warn，并提示该目录当前处于可接受空能力位状态"
    }
  ],
  "missing_summary": {
    "critical": [],
    "warning": []
  },
  "recommendation": "安装完整，可继续使用。| 安装不完整，建议重新执行安装脚本。"
}
```

**shared 状态解释**：
- `pass`：shared 目录存在，且当前最小共享清单全部可读；
- `warn`：shared 目录存在，但当前仓库无共享业务文件或仅有占位文件，属可接受空能力位状态；
- `fail`：shared 目录不存在，或存在但约定的最小共享清单不可读。

**日志文件位置**：`~/.claude/AgentDevFlow/.install-check.log`

### 5.3 成功判据

安装完成仅在以下条件同时满足时才可宣称**安装完整**：
1. `~/.claude/AgentDevFlow/` 下 prompts/docs 存在且最小清单文件全部可读
2. `~/.claude/skills/` 下稳定版 skill 路径存在，不包含安装态 `adf-` 前缀要求
3. workflows/templates 均已落到稳定路径且关键引用可解析
4. scripts/ 目录存在且核心脚本可读
5. `${ADF_DOC_ROOT}` 已注入并可用于文档路径解析

### 5.4 失败处理边界

- 若检查发现缺失项，安装脚本必须输出缺失路径、失败项分类与重装建议
- 缺失项应被标记为**安装不完整**，不得宣称安装成功闭环
- 单个文档/模板/workflow 缺失时，不应阻断 Issue / Gate / PR 核心流程执行
- 但一旦缺失影响关键引用解析，skill 必须显式提示用户修复安装
- 若 stable skill 路径仍出现安装态 `adf-` 前缀要求，应判定为路径模型错误，而非用户环境问题
- 完备性检查结果必须可供 QA 复核（通过 JSON 日志文件）

### 5.5 关键入口最小验证集（解决 QA conditional 条件2）

安装后以下三类入口必须可真实读取（不仅路径存在）：

| 入口类别 | 最小验证集 | 验证方法 |
|---------|-----------|---------|
| 角色 SKILL | `skills/product-manager/SKILL.md` 中引用的 `prompts/002_develop_pipeline.md` | 通过模拟 Skill 加载读取目标文件 |
| workflow | `skills/workflows/tech-review.md` | 直接读取文件内容 |
| shared | `~/.claude/skills/shared/` 目录自身或约定占位文件 | 直接读取目录/占位文件状态，验证 shared 安装类别已真实落位 |
| template | `skills/templates/prd-template.md` | 直接读取文件内容 |

---

## 6. Fallback 行为

- 若 `${ADF_DOC_ROOT}` 缺失，skill fallback 到 `${HOME}/.claude/AgentDevFlow` 并提示用户
- 若文档路径不存在，skill 应提示用户文档缺失并给出安装目录检查建议
- 若 workflows/shared/templates 路径不存在，skill 应提示安装内容不完整并建议重新执行安装脚本
- 不应因单个引用缺失而阻断核心流程执行
- 核心流程（Issue/Gate/PR）不依赖单个引用文件存在性即可运行，但不得隐瞒安装缺失状态

---

## 7. 安装脚本更新范围

### 7.1 新增/修改内容

| 目标 | 动作 |
|---|---|
| **安装脚本** | 增加 prompts/、docs/、scripts/ 复制逻辑；增加 ADF_DOC_ROOT 注入逻辑；增加完备性检查 |
| **skill 文件** | 重写所有开发目录相对路径引用为安装态可解析格式 |
| **安装说明** | 说明安装后文档路径结构与稳定版 skill 路径结构 |
| **CLAUDE.md** | 新增"安装目录打包规则"章节（§4.7 PRD 要求） |

### 7.2 安装脚本伪代码

```bash
# install.sh 核心逻辑（v2.0）

function install_dev() {
    # 1. 复制 skills/ 到 ~/.claude/skills/（已有）
    # 2. 复制 prompts/ 到 ~/.claude/AgentDevFlow/prompts/（新增）
    # 3. 复制 docs/governance/ 到 ~/.claude/AgentDevFlow/docs/governance/（新增）
    # 4. 复制 docs/platforms/ 到 ~/.claude/AgentDevFlow/docs/platforms/（新增）
    # 5. 复制 scripts/ 到 ~/.claude/AgentDevFlow/scripts/（新增）
    # 6. 注入 ADF_DOC_ROOT 到 shell profile（新增）
    # 7. 执行完备性检查（新增）
    # 8. 输出检查结果 JSON（新增）
}
```

---

## 8. Bootstrap-Sync 协同机制（解决 v1.0 Conditional 条件2）

### 8.1 职责边界

| 组件 | 职责 | 不涉及 |
|------|------|--------|
| **安装脚本** | 定义外部安装态路径、复制文件、注入环境变量、执行完备性检查 | 开发态自举 |
| **bootstrap-sync** | 服务本仓开发态 `.claude/skills/adf-*` 自举产物 | 外部安装态路径 |
| **skill 运行时** | 解析安装态路径、执行 fallback、暴露缺失告警 | 路径定义 |

### 8.2 协同规则

bootstrap-sync 在同步 skills 时，需遵守以下规则（与安装脚本不冲突）：

1. bootstrap-sync **只**处理 `.claude/skills/adf-*/` 开发态产物，不触碰 `~/.claude/` 安装态目录
2. bootstrap-sync 在生成 adf-* skill 时，同步检查 `${ADF_DOC_ROOT}` 路径下 prompts/ 和 docs/ 是否存在，缺失则输出警告（不自动复制，避免越权）
3. 若开发目录的 prompts/ 或 docs/ 有变更，bootstrap-sync 在 CI 日志中提示"安装脚本可能需要同步更新"

---

## 9. CLAUDE.md 规则沉淀（§4.7 PRD 要求）

### 9.1 目标文件

**项目级 CLAUDE.md**：`/home/work/code/AgentDevFlow/CLAUDE.md`（非 Human 全局级）

### 9.2 新增章节内容

在现有 CLAUDE.md 末尾新增"安装目录打包规则"章节，包含：

1. **打包目录清单**：明确列出 §2.8 中的必须打包目录集
2. **目录依赖变更规则**：新增目录必须经过 Architect 评估 + Tech Review 签字
3. **开发态 vs 安装态区分**：
   - 开发态：`.claude/skills/adf-*`（bootstrap-sync 产物）
   - 安装态：`~/.claude/skills/`（稳定版，无 adf- 前缀）
4. **引用路径规范**：skill 中引用文件必须使用 `${ADF_DOC_ROOT}` 或稳定版 skill 路径
5. **安装脚本更新同步规则**：任何新增目录依赖必须同步更新安装脚本的复制逻辑 + 完备性检查 + 安装说明

---

## 10. 接口

- **输入**：PRD #019 v2.0、当前安装脚本、当前 skill 文档引用现状、依赖分析矩阵
- **输出**：
  - 路径映射与安装态解析方案
  - 依赖分析矩阵文档（`docs/tech/019_dependency_matrix.md`）
  - 完备性检查机制
  - 更新后的安装脚本
  - 更新后的 skill 引用路径
  - 更新后的 CLAUDE.md
  - QA Case

---

## 11. 可测试性

QA 可验证：

1. 安装后 prompts/ 和 docs/ 是否存在于安装目录
2. 安装后 stable skills/workflows/templates 是否存在于 `~/.claude/skills/` 稳定路径
3. skill 中的文档引用是否在安装后仍可解析
4. skill 中对 workflows/shared/templates 的关键引用是否在安装后可解析
5. 缺失项出现时是否输出明确告警，并标记为安装不完整
6. 单个引用缺失时是否不阻断核心流程，但不隐藏失败状态
7. 安装说明是否说明路径结构与完备性检查边界
8. **新增**：依赖分析矩阵是否覆盖所有核心 skill
9. **新增**：打包目录准入/准出规则是否与依赖矩阵一致
10. **新增**：CLAUDE.md 中是否新增打包规则章节且与 PRD 一致
11. **新增**：完备性检查 JSON 输出是否结构化且可复核
12. **新增**：三类关键入口是否可真实读取目标内容

---

## 12. 风险

| 风险 | 级别 | 缓解 |
|---|---|---|
| 文档复制与源文件不同步 | 高 | 明确文档更新时同步复制机制；bootstrap-sync CI 提示 |
| 环境变量未设置导致路径失效 | 中 | 安装脚本负责设置，skill 检测缺失时给出提示 |
| stable skills/workflows/templates 未完整安装 | 高 | 安装后立即执行完备性检查并输出缺失清单 |
| 开发态 adf- 前缀与安装态稳定路径混淆 | 中 | 在 Tech 中显式区分本仓自举与外部安装态 |
| 不同操作系统路径差异 | 低 | 使用跨平台路径库 |
| 逐层依赖分析遗漏 skill 或目录 | 高 | 以 start-agent-team 为入口逐层展开，产出矩阵逐项核对 |
| CLAUDE.md 规则与实际安装脚本不一致 | 高 | 规则更新与安装脚本修改同步进行，QA 验证两者一致性 |
| 增强层文档路径引用未处理 | 中 | 已将 `docs/platforms/enhancement-layer.md` 纳入必须打包清单 |

---

## 13. 发布推进

Gate 2 → QA Case → 安装脚本/文档/CLAUDE.md 更新 → 文档 PR → HR#1 → Release

---

## 14. 回滚

- 若路径映射导致安装复杂度显著上升，回退到当前最小必要路径映射并重新评估方案
- 若完备性检查范围过大导致安装不可维护，先保留 prompts/docs + 关键 workflows/templates 检查，其余纳入下一轮补齐
- 若 CLAUDE.md 规则与现有内容冲突，优先保留现有架构设计，将新规则作为补充章节

---

## 15. 评审记录

| 日期 | 评审人 | 备注 | 决策 |
|---|---|---|---|
| 2026-04-22 | Architect | 起草 Tech Draft v1.0 | Draft |
| 2026-04-22 | Architect | v1.1 PM Conditional 修订 | Draft |
| 2026-04-22 | Architect | v1.2 吸收 #30 有效技术点 | Draft |
| 2026-04-22 | PM | 流程违规纠正：Tech Spec 基于未 Approved PRD 起草，签字撤销 | 降级/撤销 |
| 2026-04-22 | Architect | **v2.0 重新起草**：基于 PRD v2.0 重大变更，新增逐层依赖分析（§2）、打包目录规则（§2.8）、CLAUDE.md 沉淀（§9）、完备性检查 JSON 输出格式（§5.2）、关键入口最小验证集（§5.5）、bootstrap-sync 协同细化（§8） | Draft |
| 2026-04-22 | PMO/Team Lead | **违规标记**：Architect 在 Gate 1 正式留痕未补齐前完成 Tech Spec v2.0 起草，违反 PMO 纠正动作时序要求。Tech Spec 内容保留但需 Gate 1 留痕补齐后重新评估 | 违规/待复核 |
| 2026-04-22 | PM | **Gate 1 正式通过**：PRD v2.0 三方签字完成（PM + Architect + QA），违规标记解除，Tech Spec 进入正常 Gate 2 评审流程 | Approved |
| 2026-04-22 | QA + Engineer + PM | Gate 2 完成：shared 口径、JSON schema、依赖分析覆盖等条件项已收口，Tech Spec 通过三方评审 | Approved |

---

## 16. 版本历史

| 版本 | 日期 | 变更说明 | 变更人 |
|------|------|---------|-------|
| v1.0 | 2026-04-22 | 首次起草 | Architect |
| v1.1 | 2026-04-22 | PM Conditional 修订：统一采用方案A | Architect |
| v1.2 | 2026-04-22 | 吸收 #30 有效技术点 | Architect |
| v2.0 | 2026-04-22 | **重大重写**：基于 PRD v2.0 新增 §4.5-4.7 内容；新增逐层依赖分析矩阵、打包目录准入/准出规则、CLAUDE.md 规则沉淀章节；解决 v1.0 Conditional 条件（关键文件定义、bootstrap-sync 细化）；解决 QA conditional 条件（输出格式、最小验证集） | Architect |
