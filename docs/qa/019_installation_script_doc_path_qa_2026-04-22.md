---
name: 安装脚本安装结果完备性与路径映射 — QA Case Design v2.0
description: 基于 PRD #019 v2.0 与 Tech-19_v2.0 的当前有效 QA Case Design，定义安装脚本执行后的全量安装结果、逐层依赖分析、打包目录规则、引用解析、完备性检查与 fallback 行为的验证用例
status: Approved
owner: QA Engineer
date: 2026-04-22
update_date: 2026-04-22
issue: "#19"
prd: docs/prd/019_installation_script_doc_path_2026-04-22.md
tech: docs/tech/019_installation_script_doc_path_tech_2026-04-22.md
---

# QA Case Design #019 — 安装脚本安装结果完备性与路径映射

---

## 当前有效状态

- **当前有效版本**：v2.0 Approved
- **当前有效输入**：PRD #019 v2.0（Gate 1 Approved）+ Tech Spec #019 v2.0（Gate 2 Approved）
- **当前阶段**：QA Case Design（PM + Architect + Engineer 三方评审完成）
- **规则说明**：本文件为 Issue #19 的当前有效 QA Case Design，覆盖安装脚本执行后的全量安装结果完备性测试，并吸收 #30 的有效测试关注点
- **范围收口说明**：Issue #30 已确认为与 #19 同问题的 duplicate background，其有效测试关注点已回并至本 QA Case；后续不再单独为 #30 建立独立 QA 交付链

## 追溯关系

- **PRD**: `docs/prd/019_installation_script_doc_path_2026-04-22.md`
- **Tech Spec**: `docs/tech/019_installation_script_doc_path_tech_2026-04-22.md`

### PRD #019 → QA Case 追溯矩阵

| PRD Section | 对应 TC | 覆盖状态 |
|-------------|---------|---------|
| 7.1 路径映射规则 | TC-19-01, TC-19-02 | ✅ |
| 7.2 安装后引用仍有效 | TC-19-03, TC-19-09 | ✅ |
| 7.3 fallback 行为 | TC-19-10, TC-19-11 | ✅ |
| 7.4 安装脚本自动映射与完备性检查 | TC-19-05, TC-19-06, TC-19-07 | ✅ |
| 7.5 关键入口真实读取 | TC-19-08, TC-19-09 | ✅ |
| 7.6 流程与边界 | TC-19-12 | ✅ |
| 7.7 逐层依赖分析覆盖率 | TC-19-13, TC-19-14 | ✅ |
| 7.8 打包目录规则完整性 | TC-19-14 | ✅ |
| 7.9 CLAUDE.md 规则沉淀完整性 | TC-19-15 | ✅ |

### Tech Spec #019 → QA Case 追溯矩阵

| Tech Spec Section | 对应 TC | 覆盖状态 |
|-------------------|---------|---------|
| 1. 路径映射规则 | TC-19-01, TC-19-02, TC-19-09 | ✅ |
| 2. 逐层依赖分析 | TC-19-13, TC-19-14 | ✅ |
| 3. Skill 引用适配 | TC-19-03, TC-19-09 | ✅ |
| 4. ADF_DOC_ROOT 生命周期 | TC-19-04 | ✅ |
| 5. 完备性检查机制 | TC-19-05, TC-19-06, TC-19-07, TC-19-08 | ✅ |
| 6. Fallback 行为 | TC-19-10, TC-19-11 | ✅ |
| 7. 安装脚本更新范围 | TC-19-02, TC-19-05, TC-19-14 | ✅ |
| 8. Bootstrap-Sync 协同机制 | TC-19-12 | ✅ |
| 9. CLAUDE.md 规则沉淀 | TC-19-15 | ✅ |

---

## TC-19-01：安装目录路径映射规则验证

| 字段 | 内容 |
|------|------|
| 用例 ID | TC-19-01 |
| 标题 | 安装目录路径映射规则验证 |
| 追溯 | PRD 7.1；Tech 1 |
| 前置条件 | 安装脚本与说明文档已更新 |
| 测试步骤 | 检查是否明确存在 `prompts/ -> ~/.claude/AgentDevFlow/prompts/`、`docs/ -> ~/.claude/AgentDevFlow/docs/`、`skills/* -> ~/.claude/skills/`、`skills/workflows/`、`skills/shared/`、`skills/templates/` 的稳定版安装态路径映射关系 |
| 预期结果 | 六类路径映射规则明确，安装态 skill 路径不依赖 adf-prefix 假设，文档与 skill 安装路径职责清晰 |
| 验证方法 | 文档内容验证 |
| 优先级 | P1 |

## TC-19-02：六类安装产物完备性验证

| 字段 | 内容 |
|------|------|
| 用例 ID | TC-19-02 |
| 标题 | 六类安装产物完备性验证 |
| 追溯 | PRD 7.1, 7.4；Tech 1, 5 |
| 前置条件 | 已执行完整安装脚本 |
| 测试步骤 | 对照检查清单核对 `prompts/`、`docs/`、stable skills、`workflows/`、`shared/`、`templates/`、`scripts/` 与 `ADF_DOC_ROOT` 注入项 |
| 预期结果 | 六类产物与核心脚本均完整落位；shared 至少存在目录或占位文件；无安装态 `adf-*` 命名空间残留 |
| 验证方法 | 安装后文件系统验证 |
| 优先级 | P0 |

## TC-19-03：安装后引用解析验证

| 字段 | 内容 |
|------|------|
| 用例 ID | TC-19-03 |
| 标题 | 安装后引用解析验证 |
| 追溯 | PRD 7.2；Tech 3 |
| 前置条件 | skill 文档引用已更新 |
| 测试步骤 | 抽查 skill 中 docs/prompts/workflows/shared/templates/scripts 引用，验证安装后均能解析到 `~/.claude/AgentDevFlow/` 或 `~/.claude/skills/` 稳定路径 |
| 预期结果 | 所有关键引用可解析；不再依赖开发目录相对路径 |
| 验证方法 | 文档搜索 + 安装后解析验证 |
| 优先级 | P0 |

## TC-19-04：ADF_DOC_ROOT 注入与生命周期验证

| 字段 | 内容 |
|------|------|
| 用例 ID | TC-19-04 |
| 标题 | ADF_DOC_ROOT 注入与生命周期验证 |
| 追溯 | Tech 4 |
| 前置条件 | 安装脚本支持首次安装、更新、卸载 |
| 测试步骤 | 验证首次安装写入、更新替换、运行时 fallback、卸载清理逻辑 |
| 预期结果 | ADF_DOC_ROOT 生命周期行为与 Tech 描述一致 |
| 验证方法 | 安装脚本行为验证 |
| 优先级 | P1 |

## TC-19-05：完备性检查对象覆盖验证

| 字段 | 内容 |
|------|------|
| 用例 ID | TC-19-05 |
| 标题 | 完备性检查对象覆盖验证 |
| 追溯 | PRD 7.4；Tech 5.1 |
| 前置条件 | 已执行安装脚本 |
| 测试步骤 | 校验检查对象是否覆盖 prompts、docs/governance、docs/platforms、stable skills、workflows、shared、templates、scripts、环境变量 |
| 预期结果 | 完备性检查对象与 PRD/Tech 要求一致，无 shared 遗漏 |
| 验证方法 | JSON 输出 + 日志文件校验 |
| 优先级 | P0 |

## TC-19-06：JSON 输出与 .install-check.log 校验

| 字段 | 内容 |
|------|------|
| 用例 ID | TC-19-06 |
| 标题 | JSON 输出与 .install-check.log 校验 |
| 追溯 | PRD 7.4；Tech 5.2 |
| 前置条件 | 完备性检查已执行 |
| 测试步骤 | 读取 stdout JSON 与 `~/.claude/AgentDevFlow/.install-check.log`，核对 `check_version`、`overall_status`、`checks`、`missing_summary`、`recommendation` 字段；确认 shared 状态支持 `pass/fail/warn`，其中空目录/仅占位文件通过 `warn + details` 表达 |
| 预期结果 | 输出结构化、字段完整、日志落盘正确、可供 QA 复核；shared 空能力位以 `warn` 呈现而非独立 `empty` 枚举 |
| 验证方法 | JSON 结构校验 + 日志文件校验 |
| 优先级 | P0 |

## TC-19-07：成功判据与失败边界验证

| 字段 | 内容 |
|------|------|
| 用例 ID | TC-19-07 |
| 标题 | 成功判据与失败边界验证 |
| 追溯 | PRD 7.4；Tech 5.3, 5.4 |
| 前置条件 | 可执行完整安装与异常安装场景 |
| 测试步骤 | 分别在完整安装与缺失项场景下运行检查，验证 `overall_status`、缺失分类、重装建议与“不隐瞒失败状态”要求 |
| 预期结果 | 仅在全部条件满足时宣称安装完整；异常场景输出明确告警与建议 |
| 验证方法 | 正常/异常场景对比验证 |
| 优先级 | P0 |

## TC-19-08：关键入口最小验证集执行

| 字段 | 内容 |
|------|------|
| 用例 ID | TC-19-08 |
| 标题 | 关键入口最小验证集执行 |
| 追溯 | PRD 7.5；Tech 5.5 |
| 前置条件 | 已执行安装脚本并完成环境变量注入 |
| 测试步骤 | 分别验证：1）PM Skill → `prompts/002_develop_pipeline.md`；2）`skills/workflows/tech-review.md`；3）`~/.claude/skills/shared/` 目录或占位文件；4）`skills/templates/prd-template.md` |
| 预期结果 | 四类关键入口均可真实读取或被正确检测，不仅停留在静态路径存在 |
| 验证方法 | 实际入口读取验证 |
| 优先级 | P0 |

## TC-19-09：六类关键入口扩展验证

| 字段 | 内容 |
|------|------|
| 用例 ID | TC-19-09 |
| 标题 | 六类关键入口扩展验证 |
| 追溯 | PRD 7.2, 7.5；Tech 1, 3, 5.5 |
| 前置条件 | 安装完成 |
| 测试步骤 | 分别抽查 docs / prompts / skills / workflows / shared / templates 的代表性入口，验证可读性与落点职责 |
| 预期结果 | 六类关键入口均可在安装态访问，职责边界清晰 |
| 验证方法 | 安装后路径解析与读取验证 |
| 优先级 | P0 |

## TC-19-10：缺失路径 fallback 验证

| 字段 | 内容 |
|------|------|
| 用例 ID | TC-19-10 |
| 标题 | 缺失路径 fallback 验证 |
| 追溯 | PRD 7.3；Tech 6 |
| 前置条件 | 模拟 docs/prompts/workflows/shared/templates 任一缺失 |
| 测试步骤 | 制造缺失路径并触发 skill 读取逻辑，观察 fallback、提示与流程行为 |
| 预期结果 | 系统输出明确缺失路径与修复建议；不阻断核心流程；不隐瞒安装缺失 |
| 验证方法 | 异常场景验证 |
| 优先级 | P0 |

## TC-19-11：错误路径与命名空间错误验证

| 字段 | 内容 |
|------|------|
| 用例 ID | TC-19-11 |
| 标题 | 错误路径与命名空间错误验证 |
| 追溯 | PRD 7.3；Tech 5.4, 6 |
| 前置条件 | 模拟错误路径或安装态 `adf-*` 残留 |
| 测试步骤 | 制造 stable skill 路径错误、错误 fallback 或 `adf-*` 命名空间残留，执行检查与读取 |
| 预期结果 | 系统将其判定为路径模型错误/安装不完整，并输出明确告警 |
| 验证方法 | 异常场景验证 |
| 优先级 | P0 |

## TC-19-12：流程边界与 bootstrap-sync 协同验证

| 字段 | 内容 |
|------|------|
| 用例 ID | TC-19-12 |
| 标题 | 流程边界与 bootstrap-sync 协同验证 |
| 追溯 | PRD 7.6；Tech 8 |
| 前置条件 | bootstrap-sync 与安装脚本协同逻辑已实现 |
| 测试步骤 | 验证 bootstrap-sync 仅作用于开发态 `.claude/skills/adf-*`，不触碰安装态目录；验证 #19 / #30 主线收口与告警逻辑 |
| 预期结果 | 边界清晰，#30 不形成独立 QA 主线，安装态与开发态不混淆 |
| 验证方法 | 文档 + 行为校验 |
| 优先级 | P1 |

## TC-19-13：逐层依赖分析结果验证

| 字段 | 内容 |
|------|------|
| 用例 ID | TC-19-13 |
| 标题 | 逐层依赖分析结果验证 |
| 追溯 | PRD 7.7；Tech 2.1, 2.2 |
| 前置条件 | 依赖矩阵已产出 |
| 测试步骤 | 复核 start-agent-team 起点、10 个 skill 覆盖、Engineer / Platform-SRE / agent-bootstrap 展开说明、shared 独立安装类别说明 |
| 预期结果 | 依赖矩阵覆盖所有核心 skill，未再 defer，shared 被纳入独立安装类别 |
| 验证方法 | 文档内容验证 |
| 优先级 | P0 |

## TC-19-14：最小必要打包目录集与安装脚本覆盖验证

| 字段 | 内容 |
|------|------|
| 用例 ID | TC-19-14 |
| 标题 | 最小必要打包目录集与安装脚本覆盖验证 |
| 追溯 | PRD 7.7, 7.8；Tech 2.3-2.9, 7 |
| 前置条件 | 打包目录规则与安装脚本已更新 |
| 测试步骤 | 验证最小必要打包目录集是否覆盖 prompts/docs/governance/platforms/skills/workflows/shared/templates/scripts/README；验证不应打包目录未被错误复制 |
| 预期结果 | 打包目录准入/准出规则与依赖矩阵一致，安装脚本覆盖最小必要目录集 |
| 验证方法 | 文档 + 安装后目录对比验证 |
| 优先级 | P0 |

## TC-19-15：CLAUDE.md 规则沉淀验证

| 字段 | 内容 |
|------|------|
| 用例 ID | TC-19-15 |
| 标题 | CLAUDE.md 规则沉淀验证 |
| 追溯 | PRD 7.9；Tech 9 |
| 前置条件 | CLAUDE.md 已更新 |
| 测试步骤 | 检查 `CLAUDE.md` 是否新增“安装目录打包规则”章节，并覆盖打包目录清单、目录依赖变更规则、开发态 vs 安装态区分、引用路径规范、安装脚本更新同步规则 |
| 预期结果 | CLAUDE.md 规则与 PRD/Tech 一致，且与实际安装脚本行为可对齐 |
| 验证方法 | 文档内容对照验证 |
| 优先级 | P0 |

---

## 当前评审状态

- **当前状态**：Approved
- **下一动作**：进入文档 PR / HR#1 前置收敛
- **评审前提**：以 PRD #019 v2.0 与 Tech Spec #019 v2.0 为准，后续实现与文档修改不得绕过 QA Case 评审

## 成功判据

- 六类安装产物全部落位，且 shared 作为必须存在的安装能力位已落位；当前无共享业务文件时可为空目录/占位文件，并以 `warn + details` 表达
- 六类关键入口（docs/prompts/skills/workflows/shared/templates）均可在安装态访问
- JSON 输出与 `.install-check.log` 结构完整、状态准确、可复核
- 缺失/错误路径场景下输出明确告警与修复建议，且不阻断核心流程
- 逐层依赖分析覆盖所有核心 skill，最小必要打包目录集被安装脚本完整覆盖
- CLAUDE.md 中安装目录打包规则与实际安装脚本行为一致
- #30 仅保留 duplicate/background 追溯语义，不再形成独立 QA 推进或独立放行结论

## v2.0 Draft 变更说明（2026-04-22）

| 变更项 | 说明 |
|--------|------|
| 输入升级 | 基于 PRD #019 v2.0 + Tech Spec #019 v2.0 重建 QA Case |
| 追溯升级 | 追溯矩阵扩展至 PRD 7.1-7.9 与 Tech 1-9 |
| 新增依赖分析验证 | 新增 TC-19-13 / 14 覆盖逐层依赖分析与打包目录规则 |
| 新增 shared 验证 | 新增 shared 最小清单、完备性检查与关键入口验证 |
| 新增输出格式验证 | 新增 TC-19-06 覆盖 JSON 输出与 `.install-check.log` |
| 新增 CLAUDE.md 验证 | 新增 TC-19-15 覆盖规则沉淀一致性 |
| 入口范围扩展 | 从三类入口扩展为六类安装类别 + 四类最小验证集 |

## 评审记录

| 日期 | 评审人 | 备注 | 决策 |
|---|---|---|---|
| 2026-04-22 | PM | QA Case 最终评审：测试追溯已覆盖 PRD v2.0 / Tech v2.0 当前有效范围，shared 检查口径与 JSON schema 已统一为最终版本，不改变 #19 主线范围，可作为文档 PR / HR#1 前置输入 | ✅ Approved |
| 2026-04-22 | Architect | QA Case 已完整承接 PRD v2.0 / Tech Spec v2.0，六类产物、JSON 输出、fallback、bootstrap-sync 边界与 CLAUDE.md 规则验证覆盖充分 | ✅ Approved |
| 2026-04-22 | Engineer | shared 与 JSON schema 口径已统一，不再构成实现或验收阻塞，QA Case 可作为文档 PR / HR#1 前置输入 | ✅ Approved |
