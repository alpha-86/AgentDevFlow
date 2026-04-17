# Tech Spec: gstack / superpower 增强层接入 — 文档交付

## Issue

#3: 讨论 gstack 与 superpower 增强层接入

---

**ID**: Tech-3_v4
**状态**: Draft
**负责人**: 架构师
**日期**: 2026-04-17
**基于**: PRD #003 v4（2026-04-17）

---

## 上下文

本 Tech Spec 对应 Issue #3 PRD #003 v4（2026-04-17），PRD v4 为产品视角，不含技术细节。

**PRD v4 产品层决策**（Tech Spec 技术层需完整承接）：

1. **增强层定位**：gstack/superpower = 能力插件层，不替代 AgentDevFlow 流程约束层
2. **角色增强映射**：6 角色 × 增强能力范围 × 适用阶段 × 来源（产品层抽象，不含具体 skill 名称）
3. **输出边界**：增强能力输出不能替代正式交付物
4. **渐进式启用**：安装即增强，卸载即回落，不影响 AgentDevFlow 本体独立运行
5. **非目标**：不改造核心流程、不作为强依赖、不含技术选型/接口设计/架构设计

**本 Tech Spec 范围**：纯文档交付，无代码实现。Tech Spec 负责填补 PRD v4 中产品层未覆盖的技术细节（检测机制语义、skill 名称映射）。

---

## 架构

### 检测机制（PRD v4 移入）

PRD v4 Section 4 未描述技术实现细节，Tech Spec 补充以下技术语义：

**增强层检测机制**：
- **检测时机**：`start-agent-team` 入口统一检测 gstack / superpower 是否已安装（只检测一次）
- **结果共享**：检测结果在各 Agent 间共享，无需重复检测
- **回落保障**：均未安装时自动回落 AgentDevFlow 原生机制 + 提示建议安装
- **零配置**：用户无需手动开启或关闭增强层

**用户视角**：
> "安装 gstack/superpower → 启动 start-agent-team → 自动检测一次 → 各 Agent 自动获得增强 → 卸载 → 自动回落原生机制"

> **注**：检测机制的具体实现由 `start-agent-team` skill 负责。Tech Spec 只需在增强层文档中描述其语义，不实现代码逻辑。

### 交付域分析

基于 PRD #003 v4，Issue #3 的交付内容分为 4 个文档域：

| # | 交付域 | 文档位置 | 操作 |
|---|--------|---------|------|
| 1 | 增强层定位总述 + 检测机制语义 | `docs/platforms/enhancement-layer.md` | 新建 |
| 2 | 增强层回落机制 + 边界说明 | `docs/platforms/enhancement-layer.md` | 合并入域1 |
| 3 | 6 角色增强能力映射 | 对应角色文档 | 修改 |
| 4 | 增强层安装与使用指南 | `docs/guides/enhancement-guide.md` | 新建 |

> **注**：PRD v4 将检测机制移出产品层，Tech Spec 在域1中补充技术语义描述。PRD v4 Section 4.2 的角色增强映射为产品层抽象，Tech Spec 在域3中提供具体 skill 名称映射供参考。

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

### 角色增强能力 — 产品层（来自 PRD v4 Section 4.2）

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

> **注**：TC-1~TC-9 直接映射自 PRD v4 Section 7 验收标准（7.1~7.4），每项验收标准对应至少一个 TC。

---

## 风险

| 风险 | 级别 | 缓解 |
|------|------|------|
| skill 名称与 gstack/superpower 实际命名不一致 | **高** | Engineer 已验证；TC-5 记录验证方法 |
| 文档与 PRD v4 产品层决策描述漂移 | 中 | Tech Spec 直接引用 PRD #003 v4 Section 4 作为基准；变更需回链 PRD |
| 检测机制语义与实际 start-agent-team 实现不符 | 低 | 检测机制语义仅作文档描述，不实现代码；实际行为由 start-agent-team skill 定义 |

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
- 重点：文档是否完整覆盖 PRD v4 Section 7 验收标准

---

## 回滚

### 回滚方案

文档 PR 回滚：删除或 close `doc-3-enhancement-layer` PR。

### 回滚条件

- skill 名称与实际包命名不一致且无法在当前 PR 中修正
- 文档与 PRD v4 产品层决策描述存在冲突

---

## 评审记录

| 日期 | 评审人 | 备注 | 决策 |
|---|---|---|---|
| 2026-04-17 | 架构师 | 基于 PRD v4 起草 Tech Spec v4 | Draft |
