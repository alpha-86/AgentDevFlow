本文档定义AgentDevFlow项目的1.0里程碑目标：
1. 确保001～004文档的内容能完成，然后确保能在claude Code中能够使用本项目（AgentDevFlow）来迭代自己，即能够自举。即 1.0的关键里程碑是 “***自举***” 。明确1.0能达到Claude Code自举即可，1.1版本会支持codex自举。
2. 当前AgentDevFlow的实现还有很多问题，有遗漏、错误、无意义实现、重复造轮子，请独立review当前AgentDevFlow的实现，是否匹配原hedge-ai的内容。举个例子，是否可以把hedge-ai的产品能力从agent-team内去掉，直接使用AgentDevFlow。
3. 你可以创建两个subagent，分别作为 hedge-ai下 prompts/V3.0 和 .claude/skill 的专家，让这两个subagent阅读完整的这两个目录下的所有问题。你通过跟这两个subagent讨论的形式，对齐能力。001～005需求，都有很多不完备的地方，你要彻底review，你可以跟这两个subagent讨论对齐gap。
4. 能够自举要确保跟Claude、Codex兼容，例如Claude 要基于Agent Team能力来实现，Agent Team已经有Team Lead就不需要创建新的，但是要约束Team Lead阅读相关规范、按照规范运转。具体可以参考 原hedge-ai下.claude/skills相关文档
5. 对于Codex来说，Codex没有agent team的能力，但是要看如何基于Codex编排多agent，来做到跟Claude对等的能力。
6. 同时，明确强调准则和红线：1.0版本的能力要求是从hedge-ai迁移出研发全流程的多agent机制和工作流程，工作要求，不要创造hedge-ai之外的新能力。即1.0版本的研发全流程能力边界要等同于hedge-ai的agent team的研发全流程的能力边界，不能超过。

请基于以上的需求和内容，与hedge-ai项目进行整体的review和对比，创建任务的plan文件（放在prompts/discuss/，并遵守该目录下README.md的规范），然后就plan文件的内容跟我讨论，并基于讨论后的结论修改plan文件。
然后合理规划任务 如何并行及依赖，创建多个subagent来完成需求，达成1.0里程碑
