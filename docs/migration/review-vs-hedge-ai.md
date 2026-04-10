# 中文版复核与 hedge-ai 对照审计

## 目的

本文件用于重新复核当前中文主版本，并对照 hedge-ai 已阅读的 prompts、agents、skills、workflows，识别：

- 已正确迁移的通用机制
- 已迁移但抽象不足或表达不清的部分
- 尚未完全落地的差距

## 一、复核结论

当前仓库已经具备完整的主干流程框架，但还不能简单理解成“所有细节都和 hedge-ai 对齐完成”。更准确的判断是：

- 主干机制已经落地
- 边界约束已经明确
- 执行层细节已经明显加强
- 仍有少量插件入口承载问题未完全收口

## 二、已确认正确迁移的部分

### 1. 流程主线

- 已建立 `Issue -> PRD -> Tech -> Implementation -> QA -> Release` 的主干链路
- 已建立 Change Record、Todo、Memo、Review Comment、Release Record 等留痕对象

### 2. 组织与角色

- 已建立 Team Lead、PM、Tech Lead、Engineer、QA、Researcher、Platform/SRE 的通用角色
- 已排除基金经理、交易员、量化 CRO/CSO 等业务角色

### 3. 会议、Todo、异常、恢复

- 已保留通用研发日会机制
- 已建立 Todo 闭环、异常升级、上下文恢复机制

### 4. 合规与审计

- 已建立流程合规检查、周/月复盘、重审与回退规则

## 三、这次 review 发现并已修正的问题

### 1. Team Lead 定义层次不清

问题：

- `001_team_topology.md` 和 `002_product_engineering_roles.md` 都在定义 Team Lead，容易让读者误以为存在两套定义

修正：

- 已在 `001_team_topology.md` 明确它只负责团队结构与协作关系
- 已在 `002_product_engineering_roles.md` 明确它负责正式职责、强制规则和输出物

### 2. README 过于偏仓库说明

问题：

- 旧版 `README_CN.md` 更像资产索引，不像给用户看的项目说明

修正：

- 已重写为用户视角，解释项目解决什么问题、如何解决、内部逻辑、核心原则、整体架构和适用边界

### 3. hedge-ai 中 Team Lead 的若干通用硬规则缺失

问题：

- 之前没有显式要求“会议前先读 workflow”
- 之前没有显式要求“实现完成后必须触发 QA”
- 之前没有吸收 “Issue 评论只放摘要与链接，不贴大段正文” 这条通用规则

修正：

- 已补入 `skills/shared/agents/team-lead.md`
- 已补入 `skills/shared/agents/team-lead.playbook.md`
- 已补入 `prompts/013_github_issue_and_review_comments.md`

## 四、对照 hedge-ai 后仍然存在的差距

### P1. Issue 机制已成型，但插件入口层仍弱于 hedge-ai 的“skill 入口”表达

现状：

- 已有状态机、评论模板、禁止无结构结论

仍缺：

- `github-issue/SKILL.md` 的更明确插件承载位置
- `review-org/SKILL.md` 的更明确插件承载位置
- 更明确的插件安装/装载入口描述

### P2. evaluation checker 已加强，但还没有形成独立的“检查入口”

现状：

- 已有完整性、一致性、逻辑性、证据充分性四个维度
- 已有检查器类型与模板字段

仍缺：

- 类似 hedge-ai 中 logic-checker / consistency-checker / completeness-checker 的更独立入口表达

说明：

- 这不是量化业务能力，属于通用流程质量增强项，后续可继续迁移

### P2. 团队启动机制已建立，但插件入口侧仍可更贴近 hedge-ai 的启动手册强度

现状：

- 已有团队启动步骤、并发预算、角色加载顺序

仍缺：

- 更直接的“从插件入口到团队启动”的装载说明
- 更清晰的启动模板汇总入口

## 五、总体判断

如果按“主干机制是否已落地”来判断，当前仓库已经达标。
如果按“是否已经把 hedge-ai 的所有可迁移执行细节全部吸收完”来判断，当前还没有完全结束，剩余最明显的工作是：

1. `github-issue/SKILL.md` 与 `review-org/SKILL.md` 的插件入口承载
2. 插件安装/装载说明继续收紧
3. evaluation checker 的入口表达继续工程化
