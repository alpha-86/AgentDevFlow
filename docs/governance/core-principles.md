# AgentDevPipeline 核心原则

## 目的

本文件只沉淀能从 `hedge-ai` 源文档中直接抽出的顶层方法，不写脱离源文档的新方法论。后续流程、角色、模板、插件入口的演进，都必须受这些原则约束。

## 原则 1：Issue First

来源：

- `change_record/V2.0_研发流程与GitHubIssue结合及QA角色引入.md`

结论：

- Issue 是正式研发流程的强制入口。
- 无 Issue 不得进入 PRD、Tech、开发、QA、发布等正式阶段。
- 讨论结论、PRD、Tech、QA、Release 等关键产物都必须回链到对应 Issue。

## 原则 2：问题先于方案

来源：

- `change_record/V2.0_研发流程与GitHubIssue结合及QA角色引入.md`

结论：

- 当 Issue 中已经带有用户提出的方案时，PM 也不能直接接受。
- 正式流程必须先回到问题本身，澄清目标、边界、约束，再形成 PRD。
- PRD 只描述问题、方案和边界，不写技术实现。

## 原则 3：Human Review 必须显式存在

来源：

- `change_record/V2.2_双PR机制引入.md`

结论：

- 关键交付物不能只在 Agent 内部流转。
- 设计确认和实现确认都必须有明确的 Human Review 节点。
- Human Review 的对象、结论和后续动作必须可追溯。

## 原则 4：双阶段交付

来源：

- `change_record/V2.2_双PR机制引入.md`

结论：

- 文档阶段和代码阶段必须拆开。
- 文档 PR 合并代表设计确认。
- 代码 PR 合并代表实现确认。
- QA Case Design 必须前置到文档阶段，而不是拖到代码阶段之后。

## 原则 5：正式留痕优先

来源：

- `011_文档规范.md`
- `015_会议记录规范.md`
- `016_Todo管理机制.md`
- `change_record/V2.2.5_Issue_Comment机制修复与强制Gate建立.md`

结论：

- 聊天不能代替正式交付物和正式记录。
- 关键结论必须进入文档、Issue Comment、Memo、Todo、Change Record 等正式对象。
- Comment 只有真实写入目标 Issue 后才算完成。

## 原则 6：Gate 不可绕过

来源：

- `012_交付物Checklist.md`
- `change_record/V2.2.5_Issue_Comment机制修复与强制Gate建立.md`
- `change_record/V2.3_Gate_流程保障机制.md`

结论：

- 阶段缺产物、缺签字、缺 Comment、缺证据时，不能视为完成。
- 未满足上游条件时，不得直接进入下游阶段。
- Comment 缺失或投递失败时，必须阻断相应的 PR / Gate 动作。

## 原则 7：合规检查是独立治理职责

来源：

- `change_record/V2.6_PMO-Agent引入_流程合规主动检查机制.md`

结论：

- 合规检查者是独立角色，不替代 PM、Tech Lead、QA、SRE 的正式职责。
- 每次 PR 都是独立的检查触发点。
- 合规检查默认负责发现、记录、升级和推动改进，不负责代替别人签字或关闭问题。

## 原则 8：只迁移通用研发机制

来源：

- `001_Agent团队架构.md`
- `004_工作流程规范.md`
- `hedge-ai` 全量源文档的迁移边界审计

结论：

- 本项目只抽取通用研发流程机制。
- 量化交易角色、交易节奏、策略研究、因子、回测、交易日报等内容不得进入插件主干。

## 使用方式

- 新增规则前，先确认能否回溯到 `hedge-ai` 源文件。
- 若某条规则无法指出明确源文件，就不应直接提升为核心原则。
- 若原则与实现不一致，以源文档可追溯的原则为准，先回写审计再改实现。
