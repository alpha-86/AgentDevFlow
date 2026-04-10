# 005 - 2026-04-09 Workflow 与 Template 绑定差距审计

## 结论

当前 AgentDevFlow 已经有：

- 角色规范
- workflow
- template

但三者之间仍存在一个明显执行缺口：

- workflow 说明“该做什么”
- template 提供“写什么格式”
- 但没有足够明确地规定“这一阶段必须落哪个模板、放哪个目录、形成哪个正式文件”

这会导致执行时仍然存在较大自由度。

## 主要差距

### 1. PRD / Tech 绑定还不够明确

虽然已有 template，但 workflow 中没有把目标模板和输出目录写死。

### 2. QA 缺少独立测试报告模板

当前只有 `qa-case-template.md`，还不足以清楚区分：

- Case Design
- Test Report

### 3. Release 缺少独立发布记录模板

当前 release workflow 有规则，但缺统一的 release record 模板。

### 4. Human Review 缺少推荐输出文件清单

虽然定义了 review 结论字段，但还没有明确应优先使用哪些模板承接。

## 本轮决策

1. 新增 `qa-report-template.md`
2. 新增 `release-record-template.md`
3. 在核心 workflow 中增加：
   - 推荐模板
   - 推荐输出目录
   - 阶段完成时的最小产物集合

## 后续项

- 继续把 weekly / monthly / project-portfolio workflow 绑定到项目组合模板
- 继续补 issue comment 与 artifact linkage 的自动检查示例
