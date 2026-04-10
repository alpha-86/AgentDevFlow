在项目hedge-ai中基于claude code的 agent team定义了一组agent team的工作方式，在 该项目的 @prompts/V3.0  记录了agent的promoto描述，并通过 @.claude/skills下面的一系列skill来保障agent的创建是follow prompts/V3.0文档的规范的。描述需求如下：
1. 我希望能把hedge-ai的agent team中关于产研的agent，流程，整体能力迁移出来，作为一个独立的可以用于claude、codex、opencode使用的插件包或者skill包。hedge-ai中关于量化基金运营部分的不需要，例如基金经理、CRO、CSO这些都不需要。
2. 拆分出来的，放在该项目中，该项目命名为 AgentDevFlow，即定义了一套产研流程的agent能力。
3. 该项目要方便其他人，或者其他项目在claude、codex、opencode中的各类项目中使用。
4. 要讲清楚依赖，例如依赖了gstack等。
5. 另外，避免重复造轮子，可以梳理调研一下superpowers等claude插件包的能力，直接引用或者调用。同时在依赖文件里描述清楚依赖于了哪些skill包，方便安装时一块安装。
6. 本项目（AgentDevFlow），要有严禁的CHANGLOG.md记录，以及README.md。
7. 建议参考其他优秀的项目，建立规范化的目录/文档结构。并且要有层层递进的文档结构描述和约束，方便后续AI/agent的阅读和理解。

附：hedge-ai的项目信息：
hedge-ai的github：https://github.com/alpha-86/hedge-ai
hedge-ai部署在本机的： /home/work/code/hedge-ai
