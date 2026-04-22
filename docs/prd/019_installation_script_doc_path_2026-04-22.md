---
name: 安装脚本安装结果完备性与路径映射
description: 定义 Issue #19 的当前有效 PRD，唯一主线为安装脚本执行后的整体安装完备性验证，覆盖路径映射、引用解析、真实入口读取与 fallback 行为，并吸收 #30 的有效范围
status: Approved
owner: Product Manager
date: 2026-04-22
update_date: 2026-04-22
issue: "#19"
---

# PRD #019 — 安装脚本安装结果完备性与路径映射

## 1. 背景

Issue #19 的当前有效问题不再只是安装后文档路径失效，而是 AgentDevFlow 安装到 `~/.claude/` 后，是否形成了**完整、可读取、可解析、可告警**的安装结果。用户最新明确要求：#19 必须以“安装脚本执行后整个安装内容的完备性测试”为唯一主线推进。

同时，Issue #30 中关于 `skills/*/SKILL.md`、`skills/workflows/*.md`、`skills/shared/*`、`skills/templates/*` 在安装后因开发态硬编码路径而失效的问题，经核对后属于 #19 的同一主问题范围，需作为有效输入吸收到 #19，而不再独立推进。

## 2. 问题

当前需要被统一解决和验证的问题包括：

- 安装后 `prompts/`、`docs/` 是否完整复制到 `~/.claude/AgentDevFlow/`
- 安装后稳定版 skill namespace 是否正确落到 `~/.claude/skills/`，且**不要求 `adf-` 前缀**
- `skills/*/SKILL.md`、`skills/workflows/*.md`、`skills/shared/*`、`skills/templates/*` 中的引用是否仍依赖开发目录相对路径
- `${ADF_DOC_ROOT}` 是否被正确注入、更新、fallback，并用于文档路径解析
- 缺失/错误路径场景下，系统是否能显式暴露安装不完整，而不是输出模糊“安装成功”
- 关键入口是否能真实读取目标内容，而非仅停留在静态路径存在性检查

## 3. 目标

形成 #19 的当前有效产品层需求定义，明确：

1. #19 是安装脚本安装后内容完备性验证的**唯一主线**
2. 安装后需同时覆盖 docs/prompts/skills/workflows/shared/templates 六类产物完整性
3. 安装后所有关键引用必须能解析到 `~/.claude/AgentDevFlow/` 或 `~/.claude/skills/` 的稳定路径
4. `${ADF_DOC_ROOT}` 生命周期与 fallback 行为必须明确且可验证
5. 缺失场景必须输出明确告警与修复建议，不得掩盖安装不完整状态
6. #30 的有效范围必须并入 #19，不再独立形成 PRD / Tech / QA / Gate 推进链

## 4. 范围

### 4.1 安装结果完备性范围

必须检查并验证以下安装产物：

- `~/.claude/AgentDevFlow/prompts/`
- `~/.claude/AgentDevFlow/docs/`
- `~/.claude/skills/` 下稳定版 skill 目录与 `SKILL.md`
- `~/.claude/skills/workflows/`
- `~/.claude/skills/shared/`
- `~/.claude/skills/templates/`
- shell profile 中 `${ADF_DOC_ROOT}` 注入项

#### 4.1.1 "关键文件"判定标准

PRD 中多次出现"关键 prompts/docs/skill files"，为避免歧义，定义判定标准如下：

**关键文件判定标准**（满足至少一项即视为关键）：
1. 被至少一个核心 skill（start-agent-team, team-setup, product-manager, architect, qa-engineer, engineer, platform-sre, pmo, agent-bootstrap）的**必读文档列表**直接引用
2. 被 workflow 文件交叉引用且影响流程执行（如 prd-review.md 引用 tech-review.md 的评审规则）
3. 被 scripts/ 中核心脚本（github_issue_sync.py, task_router.py 等）依赖且无法在安装后重新生成
4. 属于共享协议或基础设施文档，缺失会导致角色初始化失败（如 skill-protocol.md, event-bus.md）
5. 属于治理或运营基础设施，被 PMO 或 Team Lead 工作流程直接依赖（如 docs/governance/core-principles.md）

**非关键文件**（不满足完备性检查硬性要求，但建议包含）：
- 项目历史交付物（如已完成的 PRD、Tech Spec、QA Report）——安装脚本只打包框架和模板，不打包项目历史
- 仅用于开发测试的文件
- 安装后可重新生成的运行时产物

**说明**：具体的"最小完整关键文件清单"由 §4.5 逐层依赖分析产出，列入 Tech Spec。PRD 只定义判定标准，不罗列具体文件清单。

### 4.2 引用解析范围

必须覆盖以下安装后真实可达性：

- skill → prompts/docs
- skill → workflows
- skill → shared
- skill → templates
- 其他安装后仍依赖仓库根目录相对路径的引用

### 4.3 关键入口读取范围

至少验证三类真实入口：

- 角色 SKILL 必读文档入口
- workflow 文档入口
- template 文档入口

要求验证“可真实读取目标内容”，而不是仅验证文件存在。

### 4.4 与 #30 的关系

- #19：当前唯一主线，负责安装脚本执行后的整体安装完备性验证
- #30：重复 issue，仅保留为背景/补充分析留档
- #30 中关于 `skills/workflows/shared/templates` 路径失效、稳定版 skill namespace、运行时 fallback、职责边界等有效内容，必须吸收到 #19 当前交付
- 后续正式评审、实现、QA 与 comment 统一以 #19 为准，不再发布 #30 独立 Gate 2 / QA 结论

### 4.5 逐层依赖分析范围

安装脚本的打包目录清单不能仅由直觉列出，而必须从入口 skill 开始逐层分析文件依赖，确定"哪些目录被引用、哪些目录必须打包"。

**分析起点**：`skills/start-agent-team/SKILL.md`

**分析范围**：
1. 从 start-agent-team 开始，逐层向下分析每个被引用的 skill（team-setup, product-manager, architect, qa-engineer, engineer, platform-sre, pmo, agent-bootstrap 等）对文件系统的依赖
2. 分析每个 skill 引用的 prompts/、docs/、skills/workflows/、skills/shared/、skills/templates/、scripts/ 等目录中的具体文件
3. 分析 workflow 文件之间的交叉引用（如 prd-review.md 引用 tech-review.md 等）
4. 分析 scripts/ 目录中被 skill 直接调用的脚本（如 github_issue_sync.py, task_router.py）
5. 分析 docs/governance/、docs/todo/、docs/memo/ 等治理和运营目录的依赖关系
6. 产出**依赖分析矩阵**：每行一个 skill/workflow，每列一个目录类别，标记依赖强度（必须/可选/无）

**分析产出要求**：
- 依赖分析矩阵文档（`docs/tech/019_dependency_matrix.md` 或 Tech Spec 内嵌）
- 基于依赖矩阵得出"最小必要打包目录集"
- 明确哪些目录属于"必须打包"、哪些属于"可选打包"、哪些属于"运行时生成"（不应打包）

**边界**：具体的依赖分析执行由 Architect 在 Tech Spec 中完成，PRD 只定义分析范围和产出要求。

### 4.6 打包目录准入/准出规则

基于逐层依赖分析结果，定义打包目录的准入和准出规则，避免无限制增加目录依赖。

**准入规则**（新增目录必须满足至少一项）：
1. 被至少一个核心 skill（start-agent-team, team-setup, product-manager, architect, qa-engineer, engineer）直接引用
2. 被 workflow 文件交叉引用且影响流程执行
3. 被 scripts/ 中核心脚本依赖且无法在安装后重新生成
4. 属于治理或运营基础设施，缺失会导致角色初始化失败（如 docs/governance/core-principles.md）

**准出规则**（以下目录不应打包）：
1. 运行时生成的目录（如 `.claude/logs/`、`.claude/teams/`、`.claude/task_queue/`）
2. 项目特定交付产物（如 `docs/prd/` 中已完成的 PRD 文件）——安装脚本只打包框架和模板，不打包项目历史交付物
3. 开发态自举产物（如 `.claude/skills/adf-*`）
4. 平台适配层中仅用于开发测试的文件

**审批流程**：
- 新增目录纳入打包范围必须经过 Tech Review（Architect 评估必要性）
- 新增目录必须同步更新 CLAUDE.md 中的目录清单
- 新增目录必须同步更新安装脚本的复制逻辑和完备性检查清单

### 4.7 CLAUDE.md 规则沉淀

将打包目录规则和禁止无限制增加目录依赖的治理要求沉淀到本项目的 `CLAUDE.md` 中。

**必须沉淀的规则**：
1. **打包目录清单**：明确列出安装脚本必须打包的目录和文件清单，以及每个目录的准入理由
2. **目录依赖变更规则**：新增目录依赖必须经过 Architect 评估 + Tech Review 签字
3. **开发态 vs 安装态区分**：明确哪些目录属于开发态（如 `.claude/skills/adf-*`）、哪些属于安装态（如 `~/.claude/skills/`），禁止混淆
4. **引用路径规范**：skill 中引用文件必须使用 `${ADF_DOC_ROOT}` 或稳定版 skill 路径，禁止硬编码开发目录相对路径
5. **安装脚本更新同步规则**：任何新增目录依赖必须同步更新安装脚本的复制逻辑 + 完备性检查 + 安装说明

**产出要求**：
- `CLAUDE.md` 中新增"安装目录打包规则"章节
- 规则必须与 PRD 中的准入/准出规则一致
- 规则必须包含具体目录清单和变更审批流程

## 5. 非目标

- 不在本 PRD 中直接提交实现 diff
- 不要求在 Gate 1 阶段给出所有脚本实现细节
- 不把本仓开发态 `.claude/skills/adf-*` 自举机制误当作外部安装态要求
- 不保留 #30 的独立推进链路或独立验收口径
- 逐层依赖分析的具体执行细节（如每行矩阵内容）不在 PRD 中产出，由 Architect 在 Tech Spec 中完成
- CLAUDE.md 规则沉淀的具体文案不在 PRD 中产出，由 Engineer 在实现阶段完成，PRD 只定义规则范围和准入/准出标准
- 不覆盖运行时生成目录（如 `.claude/logs/`、`.claude/teams/`）的打包策略，这些目录属于安装后运行时产物

## 6. 用户故事

### US-1：安装使用者
> 作为安装 AgentDevFlow 的用户，我希望安装后整个内容集是完整的，所有关键引用都能解析，关键入口都能真实读取，而不是遇到失效路径后再手工修补。

### US-2：维护者
> 作为维护者，我希望 docs/prompts/skills/workflows/shared/templates 的安装结果、路径模型、环境变量与 fallback 行为都有统一标准，这样后续修复不会出现双主线和重复补丁。

## 7. 验收标准

### 7.1 路径映射规则

- [ ] 已明确 `prompts/ -> ~/.claude/AgentDevFlow/prompts/`
- [ ] 已明确 `docs/ -> ~/.claude/AgentDevFlow/docs/`
- [ ] 已明确稳定版 skill 路径落到 `~/.claude/skills/`，安装态不要求 `adf-` 前缀
- [ ] 已明确 workflows/shared/templates 的稳定安装路径

### 7.2 安装后引用仍有效

- [ ] skill 对 prompts/docs 的引用可通过 `${ADF_DOC_ROOT}` 或默认 fallback 解析
- [ ] skill 对 workflows/shared/templates 的引用在安装态可解析
- [ ] 不再依赖开发目录相对路径

### 7.3 fallback 行为

- [ ] `${ADF_DOC_ROOT}` 缺失时可 fallback 到 `${HOME}/.claude/AgentDevFlow`
- [ ] 缺失/错误路径时输出明确缺失项、修复建议与安装不完整提示
- [ ] 不因单个引用缺失阻断 Issue / Gate / PR 核心流程，但不得隐瞒失败状态

### 7.4 安装脚本自动映射与完备性检查

- [ ] 安装脚本完成后自动检查 docs/prompts/skills/workflows/shared/templates 六类产物
- [ ] 安装完成仅在关键产物存在、关键引用可解析、`${ADF_DOC_ROOT}` 可用时才可宣称“安装完整”
- [ ] 完备性检查结果可供 QA 复核，不得只给出模糊成功提示

### 7.5 关键入口真实读取

- [ ] 至少一个角色 SKILL 入口可读取目标文档
- [ ] 至少一个 workflow 入口可读取目标文档
- [ ] 至少一个 template 入口可读取目标文档

### 7.6 流程与边界

- [ ] 本 issue 已按严格研发交付流程作为唯一主线重新进入 Gate 1
- [ ] 已明确 #30 仅作 duplicate/background，不再独立推进

### 7.7 逐层依赖分析覆盖率（新增）

- [ ] 已从 `skills/start-agent-team/SKILL.md` 开始完成逐层依赖分析
- [ ] 依赖分析覆盖所有核心 skill（start-agent-team, team-setup, product-manager, architect, qa-engineer, engineer, platform-sre, pmo, agent-bootstrap）
- [ ] 依赖分析覆盖所有 workflow 文件的交叉引用
- [ ] 依赖分析覆盖 scripts/ 中被 skill 直接调用的核心脚本
- [ ] 已产出依赖分析矩阵，明确每行（skill/workflow）对每列（目录类别）的依赖强度
- [ ] 基于依赖矩阵确定了"最小必要打包目录集"

### 7.8 打包目录规则完整性（新增）

- [ ] 已定义打包目录准入规则（新增目录必须满足的条件）
- [ ] 已定义打包目录准出规则（哪些目录不应打包）
- [ ] 已定义新增目录审批流程（Tech Review 评估 + 同步更新安装脚本 + 同步更新 CLAUDE.md）
- [ ] 准入/准出规则与依赖分析矩阵结论一致

### 7.9 CLAUDE.md 规则沉淀完整性（新增）

- [ ] `CLAUDE.md` 中已新增"安装目录打包规则"章节
- [ ] 规则章节包含打包目录清单及每个目录的准入理由
- [ ] 规则章节包含目录依赖变更规则（新增目录需 Architect 评估 + Tech Review 签字）
- [ ] 规则章节包含开发态 vs 安装态区分说明
- [ ] 规则章节包含引用路径规范（`${ADF_DOC_ROOT}` 使用要求）
- [ ] 规则章节包含安装脚本更新同步规则

## 8. 成功判据

仅当以下条件同时满足时，才可宣称 #19 方案闭环：

1. `~/.claude/AgentDevFlow/` 下 prompts/docs 存在且关键文件可读
2. `~/.claude/skills/` 下稳定版 skill / workflows / shared / templates 存在且关键文件可读
3. `${ADF_DOC_ROOT}` 已被注入并可用于文档解析
4. 三类关键入口可真实读取目标内容
5. 缺失场景下输出明确告警，且不会错误宣称安装成功
6. **逐层依赖分析已完成，依赖矩阵已产出，最小必要打包目录集已确定**
7. **打包目录准入/准出规则已定义，新增目录审批流程已明确**
8. **`CLAUDE.md` 中已沉淀安装目录打包规则，且规则与 PRD 一致**

## 9. 风险

| 风险 | 影响 | 缓解 |
|------|------|------|
| 只检查 docs/prompts，遗漏 skills/workflows/shared/templates | 高 | 将六类产物纳入统一完备性检查清单 |
| 误把 `adf-` 前缀当作安装态要求 | 高 | 在 PRD/Tech/QA 中显式区分开发态自举与外部安装态 |
| 仅验证路径存在，未验证真实读取 | 高 | 增加三类关键入口读取验收项 |
| #19 / #30 双主线再次漂移 | 高 | 明确 #19 为唯一主线，#30 仅留背景，不再独立推进 |
| 逐层依赖分析遗漏 scripts/、docs/governance/ 等目录 | 高 | 明确分析范围包含所有被核心 skill 引用的目录，产出依赖矩阵逐项核对 |
| CLAUDE.md 规则与实际安装脚本不一致 | 高 | 规则更新与安装脚本修改同步进行，QA 验证两者一致性 |
| 新增目录无审批流程导致打包范围膨胀 | 中 | 定义准入/准出规则和审批流程，Tech Review 必须评估新增目录必要性 |

## 10. 依赖

- 当前安装脚本 `scripts/install.sh`
- 当前 `skills/` 源文件中的路径引用现状
- `docs/tech/019_installation_script_doc_path_tech_2026-04-22.md`
- `docs/qa/019_installation_script_doc_path_qa_2026-04-22.md`
- Issue #30 的有效背景输入（仅供吸收，不作独立交付依据）

## 11. 评审记录

| 日期 | 评审人 | 备注 | 决策 |
|---|---|---|---|
| 2026-04-22 | PM | 按用户最新纠正重建 #19 当前有效 PRD：统一为安装后整体完备性验证主线，并吸收 #30 有效范围 | Draft |
| 2026-04-22 | PM | **重大变更回滚**：Human comment #19#issuecomment-4296509380 指出 PRD 未覆盖逐层依赖分析和 CLAUDE.md 规则沉淀；PM 评估确认两个交付域缺失；按重大变更回滚到 Gate 1，产出 PRD v2.0 | 回滚至 Gate 1 |
| 2026-04-22 | PM | Gate 1 v2.0 评审 — PRD v2.0 需求口径确认：问题陈述明确、范围边界完整、非目标已声明、验收标准 9 项覆盖充分、4.1.1 "关键文件"判定标准已补充 | ✅ Approved |
| 2026-04-22 | Architect | Gate 1 v2.0 评审 — 技术可行性确认：PRD v2.0 范围边界清晰、逐层依赖分析范围合理、准入/准出规则技术可落地；Conditional 条件 1（"关键文件"定义）已由 4.1.1 补充满足；条件 2（bootstrap-sync 协同）defer 到 Tech Spec | ✅ Approved |
| 2026-04-22 | QA | Gate 1 v2.0 评审 — 验收标准可测试性确认：9 项验收标准均可测试、关键入口真实读取验证方法可行、缺失场景可模拟；QA 签字为 Conditional：待 Tech Spec 中确认"关键文件"最小清单和 bootstrap-sync 协同机制的具体实现 | ✅ Conditional Approved |

## 12. 版本历史

| 版本 | 日期 | 变更说明 | 变更人 |
|------|------|---------|-------|
| v1.0 | 2026-04-22 | 初始版本：安装后整体完备性验证主线，六类产物 + 引用解析 + fallback | PM |
| v2.0 | 2026-04-22 | 重大变更：新增 4.5 逐层依赖分析范围、4.6 打包目录准入/准出规则、4.7 CLAUDE.md 规则沉淀；新增 4.1.1 "关键文件"判定标准（回应 Architect Conditional 条件）；新增 7.7-7.9 验收标准；更新 8. 成功判据；新增风险项 | PM |
