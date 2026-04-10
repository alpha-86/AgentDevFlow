AgentDevFlow从hedge-ai迁移出来的内容有一定的碎片化，并且中间过程AI自己发挥撰写了很多内容，而hedge-ai项目有很多关键点都是在实际项目中发现的并解决的，但是这些点在AgentDevFlow中并没有，例如对Team Lead创建的唯一性要求，PRD约束等。甚至流程图也不如原hedge-ai的清晰。请：
1. 重新对比hedge-ai项目下的 prompts/V3.0 和 .claude/skills 下的每一个文件，每个文件的内容。看看涉及AgentDevFlow项目定位相关的是否迁移过来了。
2. 请阅读hedge-ai项目下 docs/prd下面的文档，有些文档也是研发全流程的能力建设相关的，看看是否迁移过来了。
3. 请review telegram channel的代码，看看用户通过telegram发消息是否会通知到team lead，以及是否能把team lead的回复发给用户。
4. 请review本项目 prompts/by-me/ 下的所有文档，看需求满足上面第1，第2点要求。
5. 请你工作时，不要以prompts/discuss下面已有的文档为准，已经建成的能力可能是事实而非的。
6. 请你阅读 prompts/discuss/README.md，落实好本需求的plan文档，并合理规划subagent，并行开展任务。
