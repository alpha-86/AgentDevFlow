---
name: QA Case Design — ADF Bootstrap Skill System Enhancement
description: QA Case Design for Issue #5 — ADF 技能系统、文档与自动化流程完善
status: Draft
owner: QA Engineer
date: 2026-04-15
update_date: 2026-04-15
issue: "#5"
prd: PRD #005 (docs/prd/005_adf_bootstrap_skill_system_2026-04-15.md)
tech: Pending (Architect drafting)
---

# QA Case Design — Issue #5: ADF Bootstrap Skill System Enhancement

**ID**: QA-5_v1
**Status**: Draft
**Issue**: #5
**PRD**: PRD #005 Section 7 (Acceptance Criteria 7.1–7.4)
**Tech Spec**: Tech-5_v1.md (已对齐，Section 7 可测试性场景已整合)
**Gate**: 3 (QA Case Design)

## 追溯关系

| PRD AC | 测试区域 | TC 编号 |
|--------|---------|---------|
| AC 7.1 | bootstrap-sync 机制文档 | TC-B1 ~ TC-B8 |
| AC 7.2 | 接入使用指南 | TC-U1 ~ TC-U4 |
| AC 7.3 | Agent 角色能力边界文档 | TC-R1 ~ TC-R3 |
| AC 7.4.1 | CI 检查逻辑修复（P0） | TC-CI1 ~ TC-CI5 |
| AC 7.4.2 | CI/CD 配置说明文档 | TC-CD1 ~ TC-CD4 |

> **Tech Spec 对齐说明**：TC-CI2 已整合 Tech-5_v1 Section 7 可测试性场景，Gate 角色映射采用 Tech-5_v1 权威定义（Gate 1=PM+架构师, Gate 2=PM+技术负责人+QA, Gate 3=PM+架构师+Engineer, Gate 5=QA+PM+Engineer）。TC-CI5 追加自 Tech-5_v1 Section 9 回滚方案验证。

## 测试范围

验证 Issue #5 的文档交付物和 CI 行为是否符合 PRD #005 Section 7 验收标准。

**范围说明**：
- 本次测试以文档审查和行为验证为主，不修改任何源代码
- CI 行为验证基于代码审查结果（`doc-pr-checks.yml` 当前实现），目标验证修复后行为
- Tech Spec 完成后将对齐测试路径

**排除范围**：
- 不测试 `skills/shared/` 源文件的内容质量
- 不测试非 GitHub 平台等效实现
- 不测试 bootstrap-sync.py 脚本逻辑变更（本 PRD 不修改脚本）

## 测试环境

- **平台**：Linux (ubuntu-latest) + GitHub Actions
- **工具**：Python 3.x, grep, diff, SHA256, GitHub CLI
- **前提条件**：
  - 仓库为 AgentDevFlow 最新 main 分支
  - `skills/shared/` 目录存在且包含源文件
  - `.github/workflows/doc-pr-checks.yml` 存在

---

## 测试用例

### 区域 1：bootstrap-sync 机制文档 (AC 7.1)

#### TC-B1: 同步映射表存在且覆盖完整

**追溯**：PRD #005 AC 7.1.1
**测试类型**：文档存在性 + 覆盖完整性

**步骤**：
1. 在仓库中定位 bootstrap-sync 机制文档（预期位置：`docs/technicals/bootstrap-sync.md` 或 `README.md` 相关章节）
2. 提取文档中列出的 `skills/shared/` 源文件列表
3. 提取文档中列出的 `.claude/skills/adf-*/` 产物文件列表
4. 与实际目录对比：`skills/shared/` 下的非 SKIP_FILES 文件数 vs 文档中映射表条目数
5. 验证 `.claude/skills/` 下每个 `adf-*/SKILL.md` 都在映射表中有对应条目

**预期结果**：
- [ ] 映射表文档存在
- [ ] 映射表覆盖 `skills/shared/` 下所有非 SKIP_FILES 的 `.md` 文件
- [ ] 映射表覆盖所有 `.claude/skills/adf-*/` 子目录
- [ ] 实际目录与文档列表完全匹配（无遗漏、无多余）

**通过标准**：文档存在且实际文件与映射表条目数一致

---

#### TC-B2: 安装前置指南完整

**追溯**：PRD #005 AC 7.1.2
**测试类型**：文档内容审查

**步骤**：
1. 在 bootstrap-sync 机制文档中找到安装前置部分
2. 验证 Python 3.x 依赖说明存在
3. 验证触发条件"push to main"或"push 到 main 分支"说明存在
4. 执行 `python .github/workflows/bootstrap-sync.py --help` 或检查脚本可执行性
5. 验证文档描述的触发路径与 `bootstrap-sync.yml` 中的 `on: push: branches: [main]` 一致

**预期结果**：
- [ ] Python 依赖（3.x）说明存在
- [ ] 触发条件说明存在
- [ ] 脚本可执行或存在明确的依赖说明
- [ ] 文档与 CI workflow 实际配置一致

**通过标准**：依赖说明和触发条件均已文档化，且与实际 CI 配置一致

---

#### TC-B3: 故障排查指南覆盖至少 3 种已知失败模式

**追溯**：PRD #005 AC 7.1.3
**测试类型**：文档覆盖完整性

**步骤**：
1. 在 bootstrap-sync 机制文档中找到故障排查章节
2. 统计已知失败模式条目数
3. 验证以下 3 种必须覆盖的模式至少各有一个：
   - **F1**: YAML frontmatter 解析失败（描述中含 "---" 或 "frontmatter"）
   - **F2**: commit message 引号问题导致 CI YAML 解析失败
   - **F3**: 路径替换不一致（产物 vs 源文件内容差异）
4. 对每个失败模式，验证文档包含：问题描述 + 修复/缓解方法

**预期结果**：
- [ ] 故障排查章节存在
- [ ] 失败模式总数 ≥ 3
- [ ] F1 (frontmatter 解析) 有对应条目
- [ ] F2 (commit message 引号) 有对应条目
- [ ] F3 (路径替换) 有对应条目
- [ ] 每个条目包含问题描述和修复方法

**通过标准**：至少 3 种失败模式，且含 F1/F2/F3，修复方法非空

---

#### TC-B4: hash 对比验证方法已说明

**追溯**：PRD #005 AC 7.1.4
**测试类型**：文档可执行性

**步骤**：
1. 在 bootstrap-sync 机制文档中找到验证方法章节
2. 验证文档包含以下内容：
   - **方法说明**：可通过 hash 对比确认产物与源文件一致性
   - **命令示例**：如 `sha256sum`、`git diff` 或脚本辅助的验证命令
   - **一致性标准**：说明什么样的 diff 可接受、什么样的 diff 表示失败
3. 实际执行一次 hash 对比（如选择任意一对已知的源→产物文件），验证文档描述的方法可操作

**预期结果**：
- [ ] 验证方法说明存在
- [ ] 包含可执行命令示例
- [ ] 说明一致性判定标准
- [ ] 命令示例经实测可执行

**通过标准**：文档方法说明完整且实测可执行

---

#### TC-B5: bootstrap-sync 跳过文件验证

**追溯**：PRD #005 AC 7.1 (bootstrap-sync 行为一致性)
**测试类型**：行为验证

**步骤**：
1. 确认 `bootstrap-sync.py` 中的 SKIP_FILES 集合：`skill-protocol.md`, `event-bus.md`, `README.md`
2. 检查 `skills/shared/` 中是否存在这些文件
3. 检查 `.claude/skills/` 下是否**不存在**对应的 `adf-skill-protocol`、`adf-event-bus`、`adf-readme` 产物目录
4. 在 bootstrap-sync 机制文档中确认 SKIP_FILES 列表已文档化

**预期结果**：
- [ ] SKIP_FILES 中的文件在 `skills/shared/` 中存在
- [ ] 对应的 `adf-*/` 产物目录不存在于 `.claude/skills/`
- [ ] SKIP_FILES 列表在文档中有说明

**通过标准**：SKIP_FILES 行为与文档一致

---

#### TC-B6: 产物 frontmatter 正确性

**追溯**：PRD #005 AC 7.1 (产物一致性)
**测试类型**：内容验证

**步骤**：
1. 从 `.claude/skills/` 下选择至少 3 个 `adf-*/SKILL.md` 文件
2. 对每个文件，验证 frontmatter 包含：
   - `name: adf-{name}`（非 `skills/shared/` 原始 name）
   - `description:` 非空字符串
   - `user-invocable: true`
3. 验证 frontmatter 之后的内容为原始源文件去掉 frontmatter 的正文
4. 验证正文中 `skills/shared/` 路径已替换为 `.claude/skills/adf-/`

**预期结果**：
- [ ] 每个产物的 frontmatter `name` 格式正确（`adf-` 前缀）
- [ ] `description` 非空
- [ ] `user-invocable: true` 存在
- [ ] 正文去掉原始 frontmatter
- [ ] 路径替换正确（3种模式）

**通过标准**：所有检查项通过

---

#### TC-B7: 路径替换完整性

**追溯**：PRD #005 AC 7.1 (产物一致性)
**测试类型**：内容验证

**步骤**：
1. 读取 `skills/shared/` 中包含 3 种路径引用的源文件（`/` 开头的 skill 调用路径、`skills/shared/` 目录引用、`skills/shared/*.md` 文件引用）
2. 验证对应的 `.claude/skills/adf-*/SKILL.md` 中：
   - `/skill-name` → `/adf-skill-name`
   - `skills/shared/{name}/` → `.claude/skills/adf-{name}/`
   - `skills/shared/{name}.md` → `.claude/skills/adf-{name}/SKILL.md`
3. 验证产物中**不存在**未替换的 `skills/shared/` 路径（排除 SKIP_FILES 相关内容）

**预期结果**：
- [ ] 3 种路径替换模式均正确执行
- [ ] 产物中无残留的 `skills/shared/` 引用（SKIP_FILES 相关除外）

**通过标准**：3 种模式均正确，无残留引用

---

#### TC-B8: bootstrap-sync --dry-run 行为

**追溯**：PRD #005 AC 7.1 (可验证性)
**测试类型**：行为验证

**步骤**：
1. 在本地仓库执行 `python .github/workflows/bootstrap-sync.py --dry-run`
2. 验证输出包含：
   - `[DRY-RUN]` 标记
   - 列出每个会同步的 skill 名称
   - 列出跳过的文件（SKIP_FILES）
3. 验证执行前后 `.claude/skills/` 目录**未发生任何变更**
4. 验证 dry-run 输出与上一次实际 sync 结果数量一致

**预期结果**：
- [ ] 输出包含 `[DRY-RUN]` 标记
- [ ] 列出 skill 同步计划
- [ ] `.claude/skills/` 目录无变更

**通过标准**：dry-run 不产生副作用，输出信息准确

---

### 区域 2：接入使用指南 (AC 7.2)

#### TC-U1: 新建项目场景指南

**追溯**：PRD #005 AC 7.2.1
**测试类型**：文档存在性 + 内容完整性

**步骤**：
1. 定位新建项目场景指南（预期位置：`docs/guides/` 或 `docs/onboarding/`）
2. 验证指南覆盖以下关键步骤：
   - **S1**: skill 安装（skill 安装到 `.claude/skills/` 的步骤）
   - **S2**: 角色初始化（各角色 Agent 加载方式）
   - **S3**: Issue 机制建立（Issue 目录结构、命名规范）
3. 验证每个步骤包含可执行的操作命令或操作说明
4. 验证关键路径无明显断裂（如引用的文件路径存在）

**预期结果**：
- [ ] 新建项目指南存在
- [ ] S1 skill 安装步骤完整
- [ ] S2 角色初始化步骤完整
- [ ] S3 Issue 机制建立步骤完整
- [ ] 引用的文件/路径实际存在

**通过标准**：三步骤均覆盖，引用路径可验证

---

#### TC-U2: 接入已有项目场景指南

**追溯**：PRD #005 AC 7.2.2
**测试类型**：文档存在性 + 内容完整性

**步骤**：
1. 定位接入已有项目场景指南
2. 验证指南包含：
   - **M1**: 最小配置清单（必须创建的文件/目录）
   - **M2**: 验证步骤（如何确认接入成功）
3. 对最小配置清单中的每一项，验证对应文件/目录在仓库中存在
4. 验证验证步骤可执行（按步骤操作能确认成功）

**预期结果**：
- [ ] 接入已有项目指南存在
- [ ] 最小配置清单非空
- [ ] 清单中每一项实际存在
- [ ] 验证步骤可执行

**通过标准**：清单可验证，步骤可操作

---

#### TC-U3: 启动多 Agent 协作团队指南

**追溯**：PRD #005 AC 7.2.3
**测试类型**：文档存在性 + 内容完整性

**步骤**：
1. 定位启动多 Agent 协作团队指南
2. 验证指南包含：
   - **T1**: `adf-start-agent-team` 使用说明（含关键步骤）
   - **T2**: 角色分配规则（如 PM/Architect/QA/Engineer 分配原则）
   - **T3**: Gate 流转规则（如 Gate 0→1→2→3 的流转条件）
3. 验证 `adf-start-agent-team` 引用的关键文件存在（如 SKILL.md 产物路径）
4. 验证 Gate 流转规则与 `prompts/004_delivery_gates.md` 一致

**预期结果**：
- [ ] 启动团队指南存在
- [ ] T1 `adf-start-agent-team` 使用说明完整
- [ ] T2 角色分配规则已文档化
- [ ] T3 Gate 流转规则已文档化
- [ ] 关键引用文件存在
- [ ] Gate 流转规则与 Gate 文档一致

**通过标准**：三项均通过，引用可验证

---

#### TC-U4: 三份指南交叉引用完整性

**追溯**：PRD #005 AC 7.2.4
**测试类型**：交叉引用验证

**步骤**：
1. 读取新建项目指南（TC-U1）、接入已有项目指南（TC-U2）、启动团队指南（TC-U3）
2. 验证三份指南之间存在交叉链接：
   - 新建项目指南 → 接入已有项目指南（顺承关系）
   - 接入已有项目指南 → 启动团队指南（顺承关系）
   - 新建项目指南 → 启动团队指南（直达关系，可选）
3. 验证链路为：新用户从"新建"到"接入"到"启动团队"可无断点地完整阅读
4. 验证所有交叉链接指向的文档/章节实际存在

**预期结果**：
- [ ] 新建 → 接入 链接存在且目标可访问
- [ ] 接入 → 启动团队 链接存在且目标可访问
- [ ] 链路完整，无死链

**通过标准**：交叉引用链路完整，死链数为 0

---

### 区域 3：Agent 角色能力边界文档 (AC 7.3)

#### TC-R1: 6 个角色能力映射文档化

**追溯**：PRD #005 AC 7.3.1
**测试类型**：文档覆盖完整性

**步骤**：
1. 定位 Agent 角色能力边界文档（预期位置：`docs/guides/role-boundaries.md` 或 `skills/shared/agents/` 下的汇总文档）
2. 验证以下 6 个角色均已文档化：PM、Architect、QA、Engineer、Team Lead、Platform-SRE
3. 对每个角色，验证包含：
   - **P**: prompt 约束说明（该角色被赋予的规则/边界）
   - **S**: skill 能力说明（该角色可调用的 skill）
   - **P↔S**: prompt 约束与 skill 能力的对应关系

**预期结果**：
- [ ] 6 个角色均已在文档中覆盖
- [ ] PM: prompt 约束 + skill 能力映射存在
- [ ] Architect: prompt 约束 + skill 能力映射存在
- [ ] QA: prompt 约束 + skill 能力映射存在
- [ ] Engineer: prompt 约束 + skill 能力映射存在
- [ ] Team Lead: prompt 约束 + skill 能力映射存在
- [ ] Platform-SRE: prompt 约束 + skill 能力映射存在

**通过标准**：6 个角色均完整覆盖

---

#### TC-R2: 角色间协作最小接口文档化

**追溯**：PRD #005 AC 7.3.2
**测试类型**：文档内容验证

**步骤**：
1. 在角色能力边界文档中找到角色间协作接口章节
2. 验证以下 3 个接口维度已文档化：
   - **I1**: Issue 评论格式（结构化评论模板，最小字段要求）
   - **I2**: Gate 留痕要求（各 Gate 签字要求、Review Record 格式）
   - **I3**: 文档追溯链（PRD→Tech→QA→PR 的产物链路）
3. 对每个接口维度，验证：
   - 格式/模板说明存在
   - 最小字段/要素非空
   - 与对应规范文档（如 `prompts/020_issue_comment_gate_and_artifact_linkage.md`）一致

**预期结果**：
- [ ] I1 Issue 评论格式已文档化
- [ ] I2 Gate 留痕要求已文档化
- [ ] I3 文档追溯链已文档化
- [ ] 格式说明非空
- [ ] 与上游规范一致

**通过标准**：3 个接口维度均覆盖

---

#### TC-R3: 角色协作失败模式不少于 3 个

**追溯**：PRD #005 AC 7.3.3
**测试类型**：文档覆盖完整性

**步骤**：
1. 在角色能力边界文档中找到常见失败模式章节
2. 统计失败模式条目数（每个模式包含：场景描述 + 根因 + 纠正机制）
3. 验证至少 3 个失败模式条目均包含：
   - **场景**：什么情况下会失败
   - **根因**：为什么会失败
   - **纠正**：如何修复或缓解

**预期结果**：
- [ ] 失败模式章节存在
- [ ] 失败模式总数 ≥ 3
- [ ] 每个模式含场景 + 根因 + 纠正

**通过标准**：≥ 3 个失败模式，结构完整

---

### 区域 4：CI 检查逻辑修复 (AC 7.4.1)

#### TC-CI1: Gate 签字缺失时 exit 1

**追溯**：PRD #005 AC 7.4.1 P0-1（第一项）
**测试类型**：行为验证（代码审查 + 实测）

**前置状态**（commit `05e89ef` 已修复）：
- ✅ WARNING → exit 1 已修复（PRD Gate 1、Tech Gate 2、QA Gate 3、Gate 5 均已 exit 1）
- ⚠️ 但仍使用 keyword grep，非 Tech-5_v1 定义的 structured regex

**步骤**：
1. 读取 `doc-pr-checks.yml` Gate 检查相关步骤
2. **代码审查**：验证所有 Gate 检查步骤使用 `exit 1`（而非 WARNING/echo）
3. 创建测试 PR（分支名 `test/qa-ci-gate-{timestamp}`）：
   - PR title 为 `[DOC #5]` 格式
   - PRD 文件含 Gate 1 块（PM 签字 + 架构评审人签字），但**缺失 Tech Gate 2 签字**
4. 验证 CI **exit code = 1**

**预期结果**：
- [ ] doc-pr-checks.yml 中所有 Gate 检查使用 `exit 1`
- [ ] CI 在缺失签字时 exit 1（不是 WARNING）
- [ ] CI 输出明确指出缺失的签字角色

**通过标准**：所有 Gate 检查使用 exit 1，输出包含缺失签字信息

**风险备注**：此 TC 需要实际创建 PR 并触发 CI，可能影响仓库状态。执行后应删除测试分支。

---

#### TC-CI2: Gate 签字结构化正则 — 模式设计验证

**追溯**：PRD #005 AC 7.4.1 P0-1（第二项）+ Tech-5_v1 Section 6
**测试类型**：模式设计准确性验证

**当前状态**：Tech-5_v1 定义了结构化正则 Pattern A，但 Engineer 尚未实现（代码 PR 待创建）。**当前 CI (commit 05e89ef) 仍使用 keyword grep**。Engineer 实现时需要正确实施 Tech-5_v1 的 Pattern A。

**Tech-5_v1 Pattern A 正则设计审查发现 3 个具体问题**：

1. **Pattern A `| ${ROLE} |` 空格要求过严**：Tech-5_v1 示例使用 `| PM |`，但实际 Review Record 表格（如 PRD #005 第188行）使用 `| Team Lead |`（空格在角色名内）。如果正则写为 `| PM |`（精确匹配），则 `|PM|` 或 `| PM|`，乃至 `| Team Lead |` 都可能不匹配。

2. **Pattern A 要求"备注"列非空**：Tech-5_v1 Section 6 示例 `| 2026-04-15 | PM | OK | Approved |` 中 `OK` 是备注内容，但实际 Review Record（如 PRD #005 第188行）使用 `| 2026-04-15 | Team Lead | Problem Statement Approved | 通过 |` — 备注列内容长度和格式差异大。

3. **Pattern A 仅支持英文决策词**：`grep -E "(Approved|Conditional|Rejected)"` 但实际 Review Record 使用中文决策词"通过"。Tech-5_v1 自身第188行评审记录使用"通过"，而非"Approved"。

**步骤**（Engineer PR 完成后执行）：
1. 读取 Engineer 实现后的 `doc-pr-checks.yml` Gate 签字检查代码
2. 验证是否使用了结构化正则（而非 keyword grep）
3. 验证正则处理上述 3 个具体问题
4. 验证所有 Gate 的正则模式一致

**预期结果**：
- [ ] Engineer 实现使用结构化正则（表格行三字段验证）
- [ ] Pattern A 空格要求或为可选匹配（`\| ?PM ?\|`）
- [ ] 备注列支持空值或可变长度
- [ ] 决策词支持中英文（通过/Approved, 退回/Rejected, Conditional/附条件通过）
- [ ] 无假阳性：备注行（无表格格式）被正确拒绝

**通过标准**：正则设计能覆盖实际 Review Record 格式，无系统性假阳性

---

#### TC-CI3: Gate 1 角色口径验证

**追溯**：PRD #005 AC 7.4.1 P0-2（第一项）
**测试类型**：配置一致性验证

**⚠️ 关键不一致**（Tech Spec 层面）：

| 文档 | Gate 1 角色名 |
|------|-------------|
| Tech-5_v1 Section 6 | PM + **架构师** |
| 004_delivery_gates.md | PM + **架构评审人** |
| commit 05e89ef CI | PM + **架构评审人** |

Tech-5_v1 定义"架构师"，但 004_delivery_gates.md 和当前 CI 使用"架构评审人"。**Gate 文档与 CI 一致，但 Tech Spec 偏差**。

**Engineer 实现时需要决策**：将 CI 改为检查"架构师"（与 Tech Spec 一致），还是 Tech Spec 改为"架构评审人"（与 Gate 文档一致）。

**步骤**：
1. 验证 Tech-5_v1 Gate 角色映射表中的角色名与 Gate 文档一致性
2. 对照 004_delivery_gates.md Gate 1 定义
3. 对照当前 CI (commit 05e89ef) 实际检查的角色名
4. 验证 Engineer 实现后的 CI 与选定标准一致

**预期结果**：
- [ ] Tech Spec 中 Gate 1 角色名已明确（"架构师"或"架构评审人"）
- [ ] CI 实现与 Tech Spec/004_delivery_gates.md 中选定标准一致
- [ ] "架构"（最短变体）被 CI 拒绝

**通过标准**：Gate 1 角色名在 Tech Spec、Gate 文档、CI 实现三方统一

---

#### TC-CI4: Gate 3 QA Case Design 三方签字检查正确

**追溯**：PRD #005 AC 7.4.1 P0-2（第二项）
**测试类型**：配置正确性验证

**步骤**：
1. 读取 `doc-pr-checks.yml` 中 Gate 3 QA Case Design 检查步骤
2. 验证检查项包含：
   - PM 签字（角色名包含 "PM"）
   - 架构师签字（角色名包含 "架构师" 或 "Architect"）
   - Engineer 签字（角色名包含 "Engineer" 或 "ENG"）
3. 构造测试文件：
   - 只有 PM 签字 → 应 fail
   - PM + Architect 签字，无 Engineer → 应 fail
   - PM + Architect + Engineer 三方签字 → 应 pass
4. 验证 CI 行为与预期一致

**预期结果**：
- [ ] 检查项覆盖 PM + 架构师 + Engineer 三方
- [ ] 缺失任一方时 CI exit 1
- [ ] 三方齐全时 CI 不因此项 fail

**通过标准**：三方签字检查完整且逻辑正确

---

#### TC-CI5: 回滚条件和方案已文档化

**追溯**：Tech-5_v1 Section 9 (回滚)
**测试类型**：文档存在性 + 可操作性

**步骤**：
1. 读取 Tech-5_v1 Section 9 回滚方案
2. 验证包含：
   - **紧急回滚方法**：revert `doc-pr-checks.yml` 修改 commit 的操作步骤
   - **文档 PR 回滚方法**：删除或 close `doc-5-ci-gate-fix` PR 的操作步骤
   - **回滚条件**：CI 误报率 > 5% 或正则模式无法覆盖现有文档格式
3. 验证回滚操作步骤包含可执行命令

**预期结果**：
- [ ] 紧急回滚方法已文档化
- [ ] 文档 PR 回滚方法已文档化
- [ ] 回滚条件阈值已明确
- [ ] 操作步骤可执行

**通过标准**：回滚方案完整且可操作

---

### 区域 5：CI/CD 配置说明文档 (AC 7.4.2)

#### TC-CD1: doc-pr-checks.yml Gate 签字检查逻辑有配置说明

**追溯**：PRD #005 AC 7.4.2.1
**测试类型**：文档存在性 + 内容完整性

**步骤**：
1. 定位 CI 配置说明文档（预期位置：`docs/technicals/` 或 `docs/ci/`）
2. 验证包含 `doc-pr-checks.yml` 的配置说明：
   - Gate 签字检查的正则模式说明（含实际正则表达式）
   - 检查触发的 PR title 前缀要求（`[DOC]` 或 `[DOC #N]`）
   - 各 Gate 要求的签字角色列表
3. 验证文档中的正则模式与 `doc-pr-checks.yml` 实际代码一致

**预期结果**：
- [ ] doc-pr-checks.yml 配置说明文档存在
- [ ] 正则模式说明存在
- [ ] PR title 前缀要求已说明
- [ ] Gate 签字角色列表已说明
- [ ] 文档与实际代码一致

**通过标准**：文档完整且与代码一致

---

#### TC-CD2: CI 在 Gate 缺失时输出友好错误

**追溯**：PRD #005 AC 7.4.2.2
**测试类型**：输出格式验证

**步骤**：
1. 执行 TC-CI1 触发 CI fail
2. 捕获 CI 输出日志
3. 验证输出包含：
   - 明确指出**哪个 Gate** 失败
   - 明确指出**缺失的签字角色**（如"PM 签字: 未通过"）
   - 提供**修复建议或参考文档链接**

**预期结果**：
- [ ] 输出包含失败 Gate 名称
- [ ] 输出包含缺失签字角色
- [ ] 输出包含修复建议或文档链接

**通过标准**：3 项均满足

---

#### TC-CD3: bootstrap-sync.yml 触发条件和预期行为有配置说明

**追溯**：PRD #005 AC 7.4.2.3
**测试类型**：文档存在性 + 内容一致性

**步骤**：
1. 定位 bootstrap-sync CI 配置说明（在 bootstrap-sync 机制文档中或独立章节）
2. 验证包含：
   - **触发条件**：`on: push: branches: [main]` + `paths: skills/shared/**/*.md`
   - **预期行为**：同步源→产物、直接 commit 到 main、无 PR
   - **force_resync 参数**说明（workflow_dispatch）
3. 读取 `bootstrap-sync.yml` 验证文档描述与实际配置一致

**预期结果**：
- [ ] 触发条件已说明
- [ ] 预期行为已说明
- [ ] force_resync 参数已说明
- [ ] 文档与 CI workflow 配置一致

**通过标准**：配置说明与 CI 代码一致

---

#### TC-CD4: CI 配置可在 30 分钟内完成等效部署

**追溯**：PRD #005 AC 7.4.2.4
**测试类型**：文档可操作性

**步骤**：
1. 阅读 CI 配置说明文档
2. 验证文档是否包含将 CI 配置迁移到新仓库的操作步骤
3. 验证步骤包含：
   - 需要复制的文件列表（workflow YAML 文件）
   - 需要配置的 secrets（如果有）
   - 触发条件配置方法
   - 验证步骤（如何确认 CI 工作）
4. 对照步骤估计操作时间（文档质量验证）

**预期结果**：
- [ ] 迁移步骤已说明
- [ ] 需要复制的文件列表完整
- [ ] 验证步骤存在

**通过标准**：文档提供可操作的迁移路径

---

## 执行说明

### TC 执行优先级

| 优先级 | TC | 理由 |
|--------|-----|------|
| P0 | TC-CI1, TC-CI2 | 验证 CI Gate 真正守门（P0-1 修复） |
| P0 | TC-CI3, TC-CI4 | 验证 Gate 角色口径（P0-2 修复） |
| P1 | TC-B1 ~ TC-B8 | bootstrap-sync 机制文档（核心 AC 7.1） |
| P1 | TC-CD1 ~ TC-CD3 | CI/CD 配置说明（AC 7.4.2） |
| P2 | TC-U1 ~ TC-U4 | 接入使用指南（AC 7.2） |
| P2 | TC-R1 ~ TC-R3 | 角色能力边界（AC 7.3） |
| P3 | TC-CD4 | CI 迁移部署（文档质量） |

### 执行前置条件

- 仓库 main 分支最新
- 所有 `skills/shared/` 源文件存在
- `.github/workflows/` 下的 CI 文件存在
- Tech Spec for Issue #5 已完成并对齐（TC-CI1~CI5 已与 Tech-5_v1 整合）；Gate 2 Tech Review 已完成，QA 签字为 Approved（4个Conditional项已关闭）

---

## 缺陷记录

| 缺陷 ID | TC 编号 | 描述 | 严重性 | 状态 | 来源 |
|---------|---------|------|--------|------|------|
| DEF-CI-01 | TC-CI2 | ~~Pattern A 3个设计问题~~ | 🟡 中 | **Closed** | Tech Spec 已修正（awk列位置匹配+空格可变+中英文决策词） |
| DEF-CI-02 | TC-CI3 | ~~Gate 1角色名不一致~~ | 🟡 中 | **Closed** | Team Lead决策：统一"架构评审人"，Tech Spec/CI/Gate文档三方一致 |
| （待定） | TC-CI1 | **Engineer 代码 PR 尚未创建**：commit 05e89ef 仅修复了 exit 1，结构化正则升级（Tech-5_v1 Section 6 Pattern A）尚未实现。TC-CI1 将在 Engineer PR 完成后执行。 | - | Pending | 正常状态 |

---

## 残留风险

| 风险 | 说明 | 缓解措施 |
|------|------|---------|
| R1 | bootstrap-sync 直接 commit 到 main，无 PR review 保障 | Team Lead 决策：Option A（接受当前设计）。缓解：通过 hash 对比自动检测产物损坏并报警（待 PRD 文档化） |
| R2 | Tech Spec (Tech-5_v1) 仅覆盖 PRD Section 4.4.1 CI 检查逻辑修复，不覆盖 7.1/7.2/7.3/7.4.2 | 7.1/7.2/7.3/7.4.2 的 QA Case Design 基于 PRD 验收标准 |
| R3 | ~~DEF-CI-01 已关闭~~ Pattern A 设计问题 | ✅ 已修正 — Tech Spec Pattern A 使用 awk 列位置匹配，空格可变，备注可空，中英文决策词 |
| R4 | ~~DEF-CI-02 已关闭~~ Gate 1 角色名不一致 | ✅ 已修正 — Team Lead决策统一"架构评审人"，Tech Spec/CI/Gate文档三方一致 |
| R5 | 文档与代码可能随时间漂移 | 建议在 CI 中增加文档-代码一致性检查（本 PRD 范围外） |
| R6 | TC-CI1 需要创建实际 PR 触发 CI，可能产生临时分支 | 执行后删除测试分支 |

---

## 签字

| 日期 | 评审人 | 备注 | 决策 |
|---|---|---|---|
| 2026-04-15 | QA Engineer | v1 完成，已对齐 Tech-5_v1（CI 部分），Gate 2 Tech Review 已签字（Conditional → Approved） | Draft |
| | PM | 待 Human Review #1 | |
| | Architect | 待 Tech Review 确认 | |
| | Engineer | 待实现确认 | |
