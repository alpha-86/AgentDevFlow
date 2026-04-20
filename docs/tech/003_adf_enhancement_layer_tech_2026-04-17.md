---
name: AgentDevFlow gstack/superpower 增强层接入 — Tech Spec v5
description: 定义增强层接入的文档交付架构、检测机制语义、角色映射、技术风险与研发计划
status: In Review
owner: Architect
date: 2026-04-17
update_date: 2026-04-20
issue: "#3"
prd: docs/prd/003_adf_enhancement_layer_2026-04-17.md (v4.1)
---

# Tech Spec #003 — gstack/superpower 增强层接入（v5）

---

**ID**: Tech-3_v5
**状态**: In Review
**负责人**: 架构师
**日期**: 2026-04-17
**更新日期**: 2026-04-20
**基于**: PRD #003 v4.1（2026-04-20）
**版本说明**: v4 → v5：新增检测机制实现逻辑（Section 3）、各 Gate 增强能力使用映射（Section 4.3）
**版本说明**: v5 → v5.1：PRD v4.1 强制增强语义对齐、Section 4.3 补充 HR#1/HR#2、清理 Section 3 重复内容

### Gate 2 Review Record（v5 迭代）

| 日期 | 评审人 | 结论 | 关键意见 | 待办 |
|---|---|---|---|---|
| 2026-04-17 | PM | Gate 2 发起 | Tech Spec v4 起草完成 | 等待 Engineer + QA 签字 |
| 2026-04-17 | Engineer | **Approved** ✅ | skill 名称映射准确，检测机制语义可实现，文档交付流程可行 | — |
| 2026-04-17 | QA | **Approved** ✅ | TC-1~TC-9 完整覆盖 PRD v4 Section 7，验证方法可执行 | — |
| 2026-04-20 | Engineer | **Approved** ✅（v5 确认）| Tech Spec v5 检测脚本可实现、Gate×角色矩阵与 PRD v4.1 一致、Section 4.3 补充 HR#1/HR#2 | — |
| 2026-04-20 | QA | **Approved** ✅（v5 确认）| TC-3-10（检测脚本）+ TC-3-11（Gate映射一致性）新增覆盖 Tech Spec v5；QA Case v2 追溯矩阵更新 | — |

---

## 上下文

本 Tech Spec 对应 Issue #3 PRD #003 v4.1（2026-04-20），PRD v4.1 为产品视角，不含技术细节。

**PRD v4.1 产品层决策**（Tech Spec 技术层需完整承接）：

1. **增强层定位**：gstack/superpower = 能力插件层，不替代 AgentDevFlow 流程约束层
2. **开关语义**：开关打开 = 强制依赖 gstack/superpower，卸载即回落 AgentDevFlow 原生机制；增强能力在适用 Gate 阶段强制使用
3. **角色增强映射**：6 角色 × 增强能力范围 × 适用 Gate × 来源（产品层抽象，不含具体 skill 名称）
4. **输出边界**：增强能力输出不能替代正式交付物
5. **非目标**：不改造核心流程、不含技术选型/接口设计/架构设计、不支持选择性关闭

**本 Tech Spec 范围**：纯文档交付，**含检测逻辑说明**。Tech Spec 负责填补 PRD v4 中产品层未覆盖的技术细节（检测机制实现逻辑、skill 名称映射、各 Gate 增强能力映射）。

---

## 架构

### 检测机制（PRD v4 移入）

PRD v4 Section 4 未描述技术实现细节，Tech Spec 补充以下技术语义和实现逻辑。

**增强层检测机制**：
- **检测时机**：`start-agent-team` 入口统一检测 gstack / superpower 是否已安装（只检测一次）
- **结果共享**：检测结果在各 Agent 间共享，无需重复检测
- **回落保障**：均未安装时自动回落 AgentDevFlow 原生机制 + 提示建议安装
- **零配置**：用户无需手动开启或关闭增强层

**用户视角**：
> "安装 gstack/superpower → 启动 start-agent-team → 自动检测一次 → 各 Agent 自动获得增强 → 卸载 → 自动回落原生机制"

### 检测机制实现逻辑

#### 两种检测方式对比

| 检测方式 | 原理 | 优点 | 缺点 |
|---------|------|------|------|
| **Prompts 检测** | 在 `start-agent-team` skill 的 prompt 中写入检测指令，Agent 执行时通过读取 skill 目录判断 | 无需额外脚本，Skill 内可自包含 | 依赖 Agent 执行 prompt，检测结果不可预测，有副作用 |
| **Python 脚本检测** | 在 `start-agent-team` skill 的 prompt 中调用 Python 脚本，脚本通过文件系统检查 skill 包是否已安装 | 结果可预测、无副作用、可独立测试 | 需额外维护脚本文件 |

#### 推荐方案：Python 脚本检测

采用 **Python 脚本检测**，理由：
1. **无副作用**：脚本只读文件系统，不修改任何状态
2. **结果可预测**：脚本返回确定的布尔值或列表，Skill prompt 无需解析复杂输出
3. **可独立测试**：脚本可单独运行验证，无需完整执行 start-agent-team
4. **与 prompts 解耦**：Skill prompt 只负责调用脚本和解读结果，检测逻辑独立演进

#### 检测脚本实现

**脚本路径**：`scripts/detect_enhancement_layer.py`

```python
#!/usr/bin/env python3
"""检测 gstack / superpower 增强层是否已安装"""

import os
import sys

SKILL_SEARCH_PATHS = [
    os.path.expanduser("~/.claude/skills"),       # 全局 skill 目录
    os.path.join(os.getcwd(), ".claude/skills"),  # 项目本地 skill 目录
]

def detect_skill(skill_name: str) -> bool:
    """检测指定 skill 是否存在于任意 search path 中。"""
    for base in SKILL_SEARCH_PATHS:
        skill_path = os.path.join(base, skill_name)
        # 检查 skill 目录或 skill 文件是否存在
        if os.path.isdir(skill_path) or os.path.isfile(f"{skill_path}.md"):
            return True
    return False

def main():
    has_gstack = detect_skill("gstack")
    has_superpower = detect_skill("superpower")

    print(f"gstack={'installed' if has_gstack else 'not_found'}")
    print(f"superpower={'installed' if has_superpower else 'not_found'}")

    # 返回码表示是否有任一增强层安装
    sys.exit(0 if (has_gstack or has_superpower) else 1)

if __name__ == "__main__":
    main()
```

**调用方式**（在 `start-agent-team` skill prompt 中）：
```
执行检测脚本确定增强层状态：
bash python scripts/detect_enhancement_layer.py
根据输出：
- gstack=installed → 在支持 gstack 的 Agent 中启用 gstack 增强 skill
- superpower=installed → 在支持 superpower 的 Agent 中启用 superpower 增强 skill
- 均 not_found → 回落到原生机制，提示建议安装 gstack 和 superpower
```

**检测结果共享机制**：
- `start-agent-team` 在 team 创建时执行一次检测
- 检测结果通过 Team 配置（`~/.claude/teams/{project_id}/config.json`）的 metadata 字段持久化，供各 Agent 读取
- 各 Agent 初始化时从 Team config 读取增强层状态，无需重复检测

**回落行为**：
- 脚本返回码 0（任一已安装）：正常启用增强能力
- 脚本返回码 1（均未安装）：AgentDevFlow 原生机制运行 + 建议性提示
- 回落不影响任何核心流程运行

#### 整体逻辑关系图

```text
start-agent-team 执行
        │
        ▼
┌──────────────────────────────────────┐
│  scripts/detect_enhancement_layer.py │
│  遍历 ~/.claude/skills + .claude/skills│
│  检查 gstack / superpower 是否存在    │
└──────────────────────────────────────┘
        │
        ├── gstack installed ──┐
        │                      ├──→ Team config metadata
        ├── superpower installed ─┤  (增强层状态持久化)
        │                      │        │
        └── 均 not found ──────┘        ▼
                         回落原生机制   各 Agent 读取 Team config
                         + 提示安装    启用/回落增强能力
```

#### 为什么不采用 Prompts 检测

| 维度 | Prompts 检测 | Python 脚本检测 |
|------|------------|----------------|
| 结果确定性 | 依赖 LLM 理解 prompt，结果不确定 | 脚本返回确定布尔值 |
| 副作用 | LLM 可能执行 prompt 以外的操作 | 只读文件系统，无副作用 |
| 可测试性 | 需完整运行 Agent 才能验证 | 脚本可单独运行测试 |
| 可维护性 | 检测逻辑分散在多个 Skill prompt 中 | 检测逻辑集中在单一脚本 |
| 跨 Agent 一致性 | 不同 Agent 对 prompt 理解可能不同 | 脚本结果一致 |

> **注**：Claude Code 的 Skill 工具本身已具备 skill 发现能力（扫描 `~/.claude/skills/` 和项目 `.claude/skills/` 目录）。增强层检测脚本复用此发现机制，不需要额外的 skill 注册流程。

### 交付域分析

基于 PRD #003 v4.1，Issue #3 的交付内容分为 4 个文档域：

| # | 交付域 | 文档位置 | 操作 |
|---|--------|---------|------|
| 1 | 增强层定位总述 + 检测机制语义 | `docs/platforms/enhancement-layer.md` | 新建 |
| 2 | 增强层回落机制 + 边界说明 | `docs/platforms/enhancement-layer.md` | 合并入域1 |
| 3 | 6 角色增强能力映射 | 对应角色文档 | 修改 |
| 4 | 增强层安装与使用指南 | `docs/guides/enhancement-guide.md` | 新建 |

> **注**：PRD v4.1 将检测机制移出产品层，Tech Spec 在域1中补充技术语义描述。PRD v4.1 Section 4.2 的角色增强映射为产品层抽象，Tech Spec 在域3中提供具体 skill 名称映射供参考。

### 文档结构

```
docs/
├── platforms/
│   └── enhancement-layer.md    # 新建：增强层定位 + 检测机制语义 + 回落 + 边界
└── guides/
    └── enhancement-guide.md     # 新建：增强层安装与使用指南
README.md                       # 修改：补充增强层定位链接
skills/*/SKILL.md               # 修改：各角色文档补充增强能力说明（6 个角色）
```

---

## 接口

### 角色增强能力 — 产品层（来自 PRD v4.1 Section 4.2）

| 角色 | 增强能力范围 | 适用阶段 | 来源 |
|------|------------|---------|------|
| Product Manager | brainstorming、方案评审增强 | 需求澄清、PRD 起草前 | superpower、gstack |
| Architect | 方案评审增强 | Tech Spec 起草前、技术方案评审前 | gstack、superpower |
| QA Engineer | 验证覆盖增强 | QA Case Design 后、QA 验证阶段 | gstack |
| Engineer | 代码审查增强、问题定位增强 | 开发前、修 Bug、代码 PR 前 | gstack |
| Team Lead | 流程改进增强 | 流程改进 | superpower、gstack |
| PMO | 流程审计增强 | 流程合规检查 | superpower、gstack |

### 角色增强能力 — 技术层（Tech Spec 补充）

> **注**：以下为 gstack/superpower 包中已验证存在的 skill 名称对照，仅供参考。具体 skill 调用以 Agent 初始化时 skill 系统的实际发现为准。

| 角色 | 增强能力范围（产品层）| 对应 skill 名称（技术层）| 验证状态 |
|------|---------------------|------------------------|----------|
| Product Manager | brainstorming、方案评审增强 | `brainstorming`, `plan-ceo-review` | ✅ 已验证 |
| Architect | 方案评审增强 | `plan-eng-review`, `brainstorming` | ✅ 已验证 |
| QA Engineer | 验证覆盖增强 | `qa-only`, `qa` | ✅ 已验证 |
| Engineer | 代码审查增强、问题定位增强 | `review`, `investigate` | ✅ 已验证 |
| Team Lead | 流程改进增强 | `brainstorming`, `plan-design-review`, `document-release` | ✅ 已验证 |
| PMO | 流程审计增强 | `brainstorming`, `plan-design-review`, `document-release` | ✅ 已验证 |

> **更新**：经 Engineer 验证，`plan-devex-review` 不存在，已更正为 `plan-design-review`（gstack 中存在）。其余 skill 均已确认。

### 各 Gate 增强能力使用映射（PRD v4 Section 4.2 技术层展开）

以下映射基于 PRD v4.1 Section 4.2 角色增强映射，将"适用 Gate"展开为完整 Gate 矩阵，指定各角色在哪些 Gate 强制使用哪些增强能力：

| Gate | PM | Architect | QA | Engineer | Team Lead | PMO |
|------|----|-----------|----|----------|-----------|-----|
| Gate 0 Startup | — | — | — | — | brainstorming（流程改进规划）| — |
| Gate 1 PRD Review | brainstorming（需求澄清）| plan-eng-review（技术可行性）| — | — | — | — |
| HR#1 设计确认 | — | plan-eng-review + brainstorming | brainstorming（评审视角）| — | — | — |
| Gate 2 Tech Review | brainstorming（方案评审）| plan-eng-review + brainstorming | — | — | — | — |
| Gate 3 Implementation | — | — | — | review（代码 PR 前）| — | — |
| Gate 4 QA Validation | — | — | qa + qa-only | investigate（Bug 定位）| — | — |
| HR#2 实现确认 | — | — | qa + qa-only | — | — | plan-design-review |
| Gate 5 Release | — | — | — | — | document-release | — |

> **说明**（来自 PRD v4.1 Section 4.2 强制增强语义）：
> - 空白表示该 Gate 该角色不使用增强能力
> - 开关打开 = 强制依赖，增强能力在适用 Gate **强制使用**，不支持选择性关闭
> - 增强能力由检测脚本确认已安装后，在对应 Gate 自动触发，无需手动配置
> - 增强能力输出不能替代正式 Gate 结论

### 外部依赖验证项

| 依赖项 | 状态 | 说明 |
|--------|------|------|
| skill 名称与 gstack/superpower 包实际命名一致 | ✅ 已验证 | Engineer 确认：plan-devex-review → plan-design-review；其余 skill 均已确认 |
| gstack/superpower 包可用性 | 待实施 | 安装前置条件，文档说明安装来源 |

---

## 数据流

### 文档交付流程

```text
1. 创建 docs/platforms/enhancement-layer.md（增强层定位 + 检测机制语义 + 回落 + 边界）
        ↓
2. 创建 docs/guides/enhancement-guide.md（安装与使用指南）
        ↓
3. 修改各角色文档（6 个角色补充增强能力说明）
        ↓
4. 修改 README.md（补充增强层定位链接）
        ↓
5. Human Review #1（文档 PR）
```

---

## 可测试性

### 文档验收测试

| # | 对应 PRD v4 | 验证项 | 验证方法 | 预期结果 |
|---|------------|--------|---------|---------|
| TC-1 | 7.1 定位声明 | 增强层定位说明 | 文档搜索"能力插件层"或"增强层" | 文档可找到定位说明 |
| TC-2 | 7.1 定位声明 | 三者定位关系 | 搜索"工具层"、"方法层"、"流程层" | 文档明确说明 gstack/superpower/AgentDevFlow 三者定位关系 |
| TC-3 | 7.2 角色映射 | 6 角色增强能力清单 | 检查 6 个角色文档 | 每个角色文档包含增强能力说明 |
| TC-4 | 7.2 角色映射 | 适用阶段明确 | 检查角色文档 | 各角色增强能力适用阶段已标注 |
| TC-5 | 7.2 角色映射 | 来源标注 | 检查角色文档 | 各角色增强能力来源（gstack/superpower）已标注 |
| TC-6 | 7.3 输出边界 | 增强能力不能替代正式交付物 | 搜索"不能替代"或"边界" | 文档明确说明增强能力输出不能替代 Gate 结论 |
| TC-7 | 7.3 输出边界 | 增强与留痕口径 | 搜索"流程留痕" | 文档明确"增强能力负责增强思考，正式文件负责流程留痕" |
| TC-8 | 7.4 安装前置 | 安装前置条件 | 检查 enhancement-guide.md | 文档包含 gstack + superpower 安装前置说明 |
| TC-9 | — | 检测机制语义 | 搜索"start-agent-team"+"检测" | 文档明确说明 start-agent-team 入口检测语义 |
| TC-10 | — | 检测脚本实现 | 运行 `scripts/detect_enhancement_layer.py`，验证输出与实际 skill 目录状态一致 | 脚本正确识别 gstack/superpower 安装状态，返回码正确 |
| TC-11 | — | 各 Gate 增强能力映射 | 检查 Tech Spec Section 4.3 与 PRD v4 Section 4.2 一致性 | 每个 Gate 的增强能力映射有 PRD v4 Section 4.2 作为依据 |

> **注**：TC-1~TC-9 直接映射自 PRD v4 Section 7 验收标准（7.1~7.4），TC-10~TC-11 为 Tech Spec 补充的验证项。

---

## 风险

| 风险 | 级别 | 缓解 |
|------|------|------|
| skill 名称与 gstack/superpower 实际命名不一致 | **高** | Engineer 已验证；TC-5 记录验证方法 |
| 文档与 PRD v4.1 产品层决策描述漂移 | 中 | Tech Spec 直接引用 PRD #003 v4.1 Section 4 作为基准；变更需回链 PRD |
| 检测机制语义与实际 start-agent-team 实现不符 | 低 | 检测机制语义仅作文档描述，不实现代码；实际行为由 start-agent-team skill 定义 |
| 检测脚本路径或权限问题导致脚本无法执行 | 中 | 脚本路径固定为 `scripts/detect_enhancement_layer.py`，在 start-agent-team 执行环境中确保可读可执行；脚本异常时自动回落原生机制 |

---

## 发布推进

### 阶段 1：文档创建与修改

- `docs/platforms/enhancement-layer.md`：增强层定位 + 检测机制语义 + 回落 + 边界
- `docs/guides/enhancement-guide.md`：增强层安装与使用指南
- 各角色文档：补充增强能力说明（6 个角色）
- `README.md`：补充增强层定位链接

### 阶段 2：文档 PR

- 分支：`doc-3-enhancement-layer`
- 包含：所有增强层相关文档修改

### 阶段 3：Human Review #1

- 评审人：PM + QA + Architect
- 重点：文档是否完整覆盖 PRD v4.1 Section 7 验收标准

---

## 回滚

### 回滚方案

文档 PR 回滚：删除或 close `doc-3-enhancement-layer` PR。

### 回滚条件

- skill 名称与实际包命名不一致且无法在当前 PR 中修正
- 文档与 PRD v4.1 产品层决策描述存在冲突

---

## 评审记录

| 日期 | 评审人 | 备注 | 决策 |
|---|---|---|---|
| 2026-04-17 | 架构师 | 基于 PRD v4 起草 Tech Spec v4 | Draft |
| 2026-04-17 | PM | 发起 Gate 2 评审 | In Review |
| 2026-04-17 | Engineer | Gate 2 Approved | skill 名称映射准确，检测机制语义可实现 |
| 2026-04-17 | QA | Gate 2 Approved | TC-1~TC-9 完整覆盖 PRD v4 Section 7 |
| 2026-04-20 | 架构师 | HR#1 反馈迭代 v5 | Draft |
| 2026-04-20 | 架构师 | **HR#1 反馈迭代 v5.1**：PRD v4.1 强制增强语义对齐、Section 4.3 补充 HR#1/HR#2、清理 Section 3 重复内容 | Draft |
| 2026-04-20 | Engineer | Gate 2 v5 确认 Approved ✅ | Tech Spec v5 可实现性确认：检测脚本可执行、Gate×角色矩阵与 PRD v4.1 一致、交付域文档结构完整 | — |
| 2026-04-20 | QA | Gate 2 v5 确认 Approved ✅ | TC-3-10/TC-3-11 新增覆盖 Tech Spec v5；QA Case v2 追溯矩阵已更新 | — |
