本文档定义AgentDevFlow项目的1.0里程碑目标：
1. 确保001～004文档的内容能完成，然后确保能在claude Code、Codex中能够使用本项目（AgentDevFlow）来迭代自己，即能够自举。即 1.0的关键里程碑是 “***自举***” 。
2. 能够自举要确保跟Claude、Codex兼容，例如Claude 要基于Agent Team能力来实现，Agent Team已经有Team Lead就不需要创建新的，但是要约束Team Lead阅读相关规范、按照规范运转。具体可以参考 原hedge-ai下.claude/skills相关文档
4. 对于Codex来说，Codex没有agent team的能力，但是要看如何基于Codex编排多agent，来做到跟Claude对等的能力。
5. 同时，明确强调准则和红线：1.0版本的能力要求是从hedge-ai迁移出研发全流程的多agent机制和工作流程，工作要求，不要创造hedge-ai之外的新能力。即1.0版本的研发全流程能力边界要等同于hedge-ai的agent team的研发全流程的能力边界，不能超过。

请基于以上的需求和内容，与hedge-ai项目进行整体的review和对比，创建任务的plan文件（放在prompts/discuss/，并遵守该目录下README.md的规范），然后就plan文件的内容跟我讨论，并基于讨论后的结论修改plan文件。
然后合理规划任务 如何并行及依赖，创建多个subagent来完成需求，达成1.0里程碑
