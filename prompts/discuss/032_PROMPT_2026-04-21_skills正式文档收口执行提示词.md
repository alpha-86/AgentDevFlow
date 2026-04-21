# 032 Prompt: skills 正式文档收口执行提示词

请按以下要求收口 `skills/` 下正式规则文档，不要扩散范围，不要发明新机制：

## 必读基准

1. `prompts/002_develop_pipeline.md`
2. `prompts/discuss/032_2026-04-20_002流程错误复核.md`
3. `prompts/discuss/032_PLAN_2026-04-21_skills正式文档与002流程一致性收口计划.md`
4. `prompts/discuss/032_2026-04-21_skills正式文档一致性抽检与后续迭代建议.md`

## 范围

只处理：

- `skills/*.md`
- `skills/*/SKILL.md`
- `skills/workflows/*.md`

不要改：

- `prompts/discuss/*.md`
- `prompts/*.md`
- `docs/*.md`

## 执行优先级

先处理 P0：

1. `skills/agent-bootstrap/SKILL.md`
2. `skills/engineer/SKILL.md`
3. `skills/architect/SKILL.md`
4. `skills/workflows/qa-validation.md`
5. `skills/workflows/human-review.md`

再处理 P1：

6. `skills/team-lead/SKILL.md`
7. `skills/product-manager/SKILL.md`
8. `skills/qa-engineer/SKILL.md`
9. `skills/pmo/SKILL.md`

## 必须收口的口径

1. `Gate 3 = Implementation`
2. `Gate 4 = QA Validation`
3. `Gate 5 = Release`
4. `HR#1 / HR#2` 是 Human review / merge decision，不是 Agent 签字节点
5. 文档 PR 合并后，Engineer 可进入 Implementation
6. 不再把 `Human 通知 Engineer` 写成必要前置
7. 纯文档交付与开发交付同等重要
8. 纯文档交付也必须走 Issue 主线与 `HR#1`
9. 纯文档交付不经过 `Gate 3 / Gate 4 / HR#2`
10. PR 合并与 Issue 关闭都是 Human 专属操作
11. 所有签字矩阵以 `prompts/002_develop_pipeline.md` 当前版本为准

## 修改要求

- 优先删掉冲突口径，再补必要说明
- 不新增 Gate
- 不新增审批层
- 不新增“通知链路”作为流程前置
- 不把 Team Lead 写成 PR merge 的必要中继

## 修改后请自检

请对修改后的 `skills/` 文档做关键词抽检，至少检查：

- `Gate 3: 文档 PR 合并`
- `Gate 4: 代码 PR 合并`
- `Gate 5: Issue Comment Gate`
- `等待文档 PR 合并通知`
- `收到 Human 通知后开始实现`
- `通知 Team Lead 执行文档 PR 合并`
- `签字（HR#1）`
- `签字（HR#2）`
- `PM + Architect + QA`
- `QA + PM + Engineer`
- `Issue Comment Gate`

## 输出要求

修改完成后，请输出：

1. 改了哪些文件
2. 每份文件收口了什么
3. 关键词抽检结果
4. 还剩哪些建议下一轮继续做
