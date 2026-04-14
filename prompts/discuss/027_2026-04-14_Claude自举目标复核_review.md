# 027：Claude 自举目标复核报告

**编号**: 027
**日期**: 2026-04-14
**类型**: review
**来源**: 基于 `026_2026-04-14_迁移进展审计报告_review.md` 及其 P0 / P1 / P2 阶段结项文档的进一步复核

---

## 一、复核背景

在 `026` 系列文档中，AgentDevFlow 已对迁移进展、P0 / P1 / P2 修复状态和 1.0 验收结论做过阶段性沉淀。

本次 `027` 的目标不是重复迁移审计，而是单独回答一个更聚焦的问题：

**当前仓库，是否已经达到“Claude Code 可基于 AgentDevFlow 自举”的 1.0 目标？**

该问题的判断依据主要来自：

1. `prompts/by-me/005_AgentDevFlow_1.0_自举_里程碑目标.md`
2. Claude 侧入口文档和适配器技能
3. 共享技能与生成产物的一致性
4. `install / bootstrap` 链路是否闭合

---

## 二、目标口径

根据 `005_AgentDevFlow_1.0_自举_里程碑目标.md`，Claude 自举目标的核心要求是：

1. AgentDevFlow 能在 Claude Code 中使用自身机制迭代自己
2. Claude 已有 Agent Team 能力，不应重复创造新的 Team Lead 产品能力
3. 重点应放在约束 Team Lead 按共享规则启动和运转
4. 1.0 的能力边界应等同于 hedge-ai 中研发全流程多 Agent 机制边界，不能额外创造新能力

因此，本次复核的最低验收口径不是“文档看起来合理”，而是：

- Claude 启动入口口径一致
- Team Lead 处理方式一致
- 共享源定义与 Claude 侧产物一致
- 安装与自举链路可形成可信闭环

---

## 三、复核结论

**结论：当前状态仍未达到 Claude 自举目标。**

更准确地说：

**主机制和大部分角色口径已经接近目标，但仍存在两个硬阻断项，因此当前不能判定“Claude 自举已达成”。**

---

## 四、已达到的部分

### 1. Claude 侧入口框架已经基本建立

以下文档和入口已经具备 Claude 自举所需的主体骨架：

- `docs/platforms/claude-code.md`
- `adapters/claude/.claude/skills/TEAM_SETUP.md`
- `adapters/claude/.claude/skills/start-agent-team/SKILL.md`
- `adapters/claude/.claude/skills/create-agent/SKILL.md`
- `adapters/claude/.claude/skills/agent-bootstrap/SKILL.md`

这些文件已经明确：

- Claude 侧需要复用现有 Team 能力
- 启动前应先确认 `project_id`、主 issue、当前 Gate 和启动工件
- 默认正式角色集已收口为：
  - `team-lead`
  - `product-manager`
  - `architect`
  - `qa-engineer`
  - `engineer`
  - `platform-sre`
  - `pmo`

### 2. 角色口径已大体统一

P0 之后，旧角色口径已经大体收口：

- `process-auditor` 已收口为 `pmo`
- `research-support` 已从正式入口移除
- `researcher` 已不再作为正式角色
- `tech-lead` 当前仅保留兼容层语义

### 3. 安装链路已有基础能力

`scripts/install.sh --channel dev --dry-run` 可以跑通，说明当前仓库已经具备把：

- `skills/shared/`
- `adapters/claude/.claude/skills/`

安装到 Claude 本地目录的基础能力。

这说明 Claude 自举所需的“资产入口层”已经基本具备。

---

## 五、未达标的阻断项

### 阻断项 1：Team Lead 处理方式仍然自相矛盾

当前 Claude 入口层存在一组尚未收口的冲突：

#### 入口文档与 Team Setup 的口径

`docs/platforms/claude-code.md` 与 `adapters/claude/.claude/skills/TEAM_SETUP.md` 都要求：

- 先创建 Team Lead
- 再创建其他角色

#### create-agent 的口径

但 `adapters/claude/.claude/skills/create-agent/SKILL.md` 与 `skills/shared/create-agent.md` 又同时明确：

- `team-lead` 是 Human 本身
- 不需要创建新的 Team Lead Agent
- 如果尝试创建，应拒绝创建

#### 为什么这是阻断项

这不是简单的文案不一致，而是直接影响 Claude 如何启动：

- 如果 Claude 应该“创建 Team Lead”，那它就仍在创造一个新 agent
- 如果 Claude 应该“把当前主会话视为 Team Lead”，那启动文档就不应继续写“先创建 Team Lead”

而 `005_AgentDevFlow_1.0_自举_里程碑目标.md` 的要求非常明确：

**Claude 已有 Team Lead，就不应再创造新的 Team Lead，只需要约束其按规范运行。**

因此，这一冲突未收口之前，Claude 自举目标不能判定为完成。

### 阻断项 2：bootstrap-sync 生成产物仍未形成可信闭环

当前最直接的问题是：

`.claude/skills/adf-agents/SKILL.md`

仍然不是 `agents/` 目录入口，而是一份错误生成的 QA 角色内容。

这说明至少在当前正式状态下：

- `skills/shared/agents/` 源定义
- `.github/workflows/bootstrap-sync.py`
- `.claude/skills/adf-agents/SKILL.md`

三者之间的闭环还没有真正打通。

即使当前工作区中已经出现了：

- `skills/shared/agents/README.md`

这样的修复方向，它也仍然只是未提交状态，还没有完成正式生成与验收。

#### 为什么这是 Claude 自举阻断项

Claude 自举并不只是“共享源文档存在”，还要求：

- Claude 可直接消费的技能包产物必须可信
- 共享源和生成物不能持续漂移

如果 `.claude/skills/adf-agents/SKILL.md` 仍然是错误内容，就说明：

**当前 Claude 自举包还不能被视为“已经可靠生成完成”。**

---

## 六、暂不构成 1.0 通过证据的项

以下内容虽然是积极进展，但当前还不能单独用来证明 Claude 自举已达成：

### 1. install.sh dry-run 通过

这只能说明安装脚本路径大致可执行，不能替代：

- 干净 Claude 环境中的真实安装
- 安装后读取技能并按启动顺序实际运行成功

### 2. bootstrap-sync.py dry-run 通过

这只能说明扫描和映射逻辑会运行，不能直接推出：

- `.claude/skills/adf-*/SKILL.md` 已全部生成正确

### 3. 角色文档和平台文档大体一致

这说明主叙事趋于收口，但如果：

- Team Lead 启动逻辑仍冲突
- 生成产物仍错误

就仍不足以支撑“Claude 可自举”。

---

## 七、修正后的判断

当前最准确的状态应表述为：

**`AgentDevFlow 已接近 Claude 自举目标，但当前仍未达标。`**

具体口径为：

1. Claude 侧入口框架已建立
2. 正式角色口径已大体统一
3. 安装链路已有基础能力
4. 但 Team Lead 启动口径尚未统一
5. 但 bootstrap 生成产物尚未形成可信闭环

因此，当前阶段更准确的结论是：

**`Claude 自举目标尚未达成，仍需完成最后两项关键收口。`**

---

## 八、建议的下一步

如果要真正把 Claude 自举目标收口，我建议下一步只聚焦下面两项：

### 1. 统一 Team Lead 启动口径

必须在以下文件中统一表述：

- `docs/platforms/claude-code.md`
- `adapters/claude/.claude/skills/TEAM_SETUP.md`
- `adapters/claude/.claude/skills/create-agent/SKILL.md`
- `skills/shared/create-agent.md`

目标是明确：

- Claude 当前主会话 / 宿主 Team 能力是否直接承担 Team Lead
- 是否禁止创建独立 Team Lead agent
- 启动顺序到底是“先确认 Team Lead 身份”还是“先创建 Team Lead”

### 2. 收口 bootstrap 生成包

必须让以下链路闭合：

- `skills/shared/agents/README.md` 或等价入口
- `.github/workflows/bootstrap-sync.py`
- `.claude/skills/adf-agents/SKILL.md`

目标是确保：

- `adf-agents/SKILL.md` 成为正确的目录入口说明
- Claude 自举技能包可被视为可信生成产物

在这两项完成后，再补一轮：

- 干净 Claude 环境安装
- 按文档启动顺序演练
- 记录一次真实自举验收结果

那时才适合判断 Claude 自举目标是否真正完成。

---

*复核完成 | 2026-04-14*
