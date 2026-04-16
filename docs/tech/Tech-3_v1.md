# Tech Spec: gstack / superpower 增强层接入 — 文档交付

## Issue

#3: 讨论 gstack 与 superpower 增强层接入

---

**ID**: Tech-3_v1
**状态**: Approved
**负责人**: 架构师
**日期**: 2026-04-15
**更新日期**: 2026-04-15（基于 PRD #003 v2 更新）

---

## 上下文

本 Tech Spec 对应 Issue #3 PRD #003 v2（Section 4.2 迭代版）。

**PRD v2 关键变更**：增强层从"手动开关"改为"自动检测 + 回落机制"

**关键决策（PRD #003 v2 Section 4.2 统一结论）**：

1. 角色初始化时**自动检测** gstack / superpower 是否已安装
2. 已安装 → **自动使用**对应增强 skill（零配置）
3. 均未安装 → **回落**原生机制 + 提示建议安装
4. 增强层输出不能替代正式交付物和 Gate 结论
5. AgentDevFlow 本体在无增强层时仍可独立完整运行
6. skill 名称精确性属于**外部依赖**，由 Engineer 在实现阶段确认，Tech Spec 仅记录映射关系

**本 Tech Spec 范围**：纯文档交付，无代码实现。

---

## 架构

### 交付域分析

基于 PRD #003 v2，Issue #3 的交付内容分为 5 个文档域：

| # | 交付域 | 文档位置 | 操作 |
|---|--------|---------|------|
| 1 | 增强层定位总述 + 自动检测机制 | docs/platforms/enhancement-layer.md | 新建 |
| 2 | 增强层回落机制说明 | docs/platforms/enhancement-layer.md | 合并入域1 |
| 3 | 角色增强映射（PM/Architect/QA/Engineer/Team Lead/PMO） | 对应角色文档 | 修改 |
| 4 | 增强层安装与使用指南 | docs/guides/enhancement-guide.md | 新建 |
| 5 | 增强层边界说明（可做/不可做） | docs/platforms/enhancement-layer.md | 合并入域1 |

> 注：v2 将原手动开关语义改为自动检测 + 回落，原交付域 1/2/5 合并为一个增强层总述文档。

### 文档结构

```
docs/
├── platforms/
│   └── enhancement-layer.md    # 新建：增强层定位 + 自动检测机制 + 回落语义 + 边界说明
└── guides/
    └── enhancement-guide.md     # 新建：增强层安装与使用指南
README.md                       # 修改：补充增强层 FAQ 或引用
skills/shared/agents/*.md      # 修改：各角色文档补充可选增强 skill 列表
```

### 增强层自动检测机制

**语义**：
- **自动检测**：角色初始化时自动判断 gstack / superpower 是否已安装
- **自动启用**：已安装时自动使用对应增强 skill，无需用户配置
- **回落保障**：均未安装时自动回落 AgentDevFlow 原生机制 + 提示建议安装
- **零配置**：用户无需手动开启或关闭增强层

**用户视角**：
> "安装 gstack/superpower → 自动获得增强 → 卸载 → 自动回落原生机制"

---

## 接口

### 角色增强映射表

> **重要**：以下 skill 名称为基于 028 讨论的映射关系，精确名称由 Engineer 在实现阶段对照 gstack/superpower 包确认。Tech Spec 记录映射框架，skill 名称精确性作为外部依赖验证项。

| 角色 | 可选增强 skill | 适用阶段 | 增强价值 | 验证状态 |
|------|--------------|---------|---------|----------|
| Product Manager | `brainstorming`, `plan-ceo-review` | 需求澄清、PRD 起草前 | 需求边界澄清、方案收敛 | ✅ |
| 架构师 | `plan-eng-review`, `brainstorming` | Tech Spec 起草前、技术评审前 | 架构边界收敛、风险识别 | ✅ |
| QA Engineer | `qa-only`, `qa` | QA Case Design 后、验证阶段 | 验证覆盖率、缺陷暴露率 | ✅ |
| Engineer | `review`, `investigate` | 开发前、代码 PR 前、修 Bug 时 | 结构化审查、根因定位 | ✅ |
| Team Lead / PMO | `brainstorming`, `plan-design-review`, `document-release` | 流程改进、发布后文档同步 | 机制设计质量 | ✅ |

> **更新**：经 Engineer 验证，`plan-devex-review` 不存在，已更正为 `plan-design-review`（gstack 中真实存在）。所有 skill 名称已验证。

### 外部依赖验证项

| 依赖项 | 状态 | 说明 |
|--------|------|------|
| skill 名称与 gstack/superpower 包实际命名一致 | ✅ 已验证 | Engineer 确认：`plan-devex-review` → `plan-design-review`；其余 skill 均已确认 |
| gstack/superpower 包可用性 | 待实施 | 安装前置条件，文档说明安装来源 |

---

## 数据流

### 文档交付流程

```text
1. Engineer 确认 skill 名称（外部依赖验证）
        ↓
2. 创建 docs/platforms/enhancement-layer.md（增强层定位 + 自动检测 + 回落 + 边界）
        ↓
3. 创建 docs/guides/enhancement-guide.md（安装与使用指南）
        ↓
4. 修改各角色文档（补充可选增强 skill 列表）
        ↓
5. 修改 README.md（补充增强层 FAQ 或引用）
        ↓
6. Human Review #1（文档 PR）
```

---

## 可测试性

### 文档验收测试

| # | 验证项 | 验证方法 | 预期结果 |
|---|--------|---------|---------|
| TC-1 | 增强层定位说明 | 文档搜索"能力插件层"或"增强层" | 文档可找到定位说明 |
| TC-2 | 自动检测机制说明 | 搜索"自动检测"关键词 | 文档明确说明自动检测语义 |
| TC-3 | 回落机制说明 | 搜索"回落"关键词 | 文档明确说明未安装时的回落行为 |
| TC-4 | skill 名称与外部包一致 | Engineer 提供 skill 名称对照确认单，逐一核对 | 文档引用的 skill 名称与 Engineer 确认单匹配 |
| TC-5 | 各角色文档包含增强 skill 引用 | 检查 6 个角色文档中是否有增强 skill 列表 | 每个角色文档至少有一条增强 skill 引用 |
| TC-6 | 增强层边界清晰 | 搜索"不能替代"或"边界"关键词 | 文档明确说明 skill 输出不能替代 Gate 结论 |
| TC-7 | 零配置语义 | 搜索"零配置"或"无需配置" | 文档明确说明用户无需手动配置 |
| TC-8 | 增强层与 AgentDevFlow 解耦 | 搜索增强 skill 是否标注为"可选" | 角色文档中增强 skill 均标注为可选，不强制 |

---

## 风险

| 风险 | 级别 | 缓解 |
|------|------|------|
| skill 名称与 gstack/superpower 实际命名不一致 | **高** | Engineer 在实现阶段确认，Tech Spec 标注为外部依赖验证项；TC-4 记录验证方法 |
| 文档与 PRD v2 自动检测机制描述漂移 | 中 | Tech Spec 直接引用 PRD #003 v2 Section 4.2 结论作为基准 |
| 回落机制描述不清晰导致用户困惑 | 低 | TC-3 覆盖回落语义验证 |
| 增强层文档与 bootstrap-sync 机制冲突 | 低 | 增强层属于外部包，ADF bootstrap-sync 不处理 |

---

## 发布推进

### 阶段 1：skill 名称确认（外部依赖）

- Engineer 读取 gstack/superpower 包的实际 skill 列表
- 确认角色映射表中 skill 名称的精确形式
- 输出确认单作为 TC-4 验证基准

### 阶段 2：文档创建与修改

- `docs/platforms/enhancement-layer.md`：增强层定位 + 自动检测 + 回落语义 + 边界说明
- `docs/guides/enhancement-guide.md`：增强层安装与使用指南
- 各角色文档：补充可选增强 skill 列表（标注"待确认"直到 Engineer 完成验证）
- `README.md`：补充增强层 FAQ 或引用

### 阶段 3：文档 PR

- 分支：`doc-3-enhancement-layer`
- 包含：所有增强层相关文档修改

### 阶段 4：Human Review #1

- 评审人：PM + QA + Architect
- 重点：自动检测机制描述准确性、skill 名称外部依赖验证完成度

---

## 回滚

### 回滚方案

文档 PR 回滚：删除或 close `doc-3-enhancement-layer` PR。

### 回滚条件

- skill 名称与实际包命名不一致且无法在当前 PR 中修正
- 文档与 PRD v2 自动检测机制描述存在冲突

---

## 评审记录

| 日期 | 评审人 | 备注 | 决策 |
|---|---|---|---|
| 2026-04-15 | 架构师 | 初始起草（v1，基于手动开关方案） | Draft |
| 2026-04-15 | 架构师 | 更新至 v2：增强层改为自动检测+回落机制，skill 名称标注为外部依赖验证项，TC-4 补充验证方法 | Draft |
| 2026-04-15 | QA Engineer | v1 Conditional 项（C1/C2）已解决；TC-1~TC-8 覆盖完整；v2 新增自动检测/回落/零配置验证 | Approved |
| 2026-04-15 | PM | PM 评审 v2 — 范围与 PRD #003 v2 一致，文档结构清晰，skill 名称外部依赖处理合理，TC 覆盖完整 | Approved |
| 2026-04-15 | 架构师（Tech Lead） | Gate 2 Tech Review — 技术可行性确认，v2 变更（自动检测+回落）可行，外部依赖处理方式合理，DEF-3 已关闭 | Approved |
| 2026-04-15 | PM | Skill 名称验证更新：plan-devex-review → plan-design-review（Engineer 验证通过）；外部依赖表中 skill 名称验证状态更新为已验证 | v2.1 |
| 2026-04-15 | Team Lead | Gate 2 补签 — Tech Spec #3 v2 文档交付方案合理，架构评审通过 | **Approved** ✅ |
