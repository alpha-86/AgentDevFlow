# Tech Spec: CI/CD 自动化增强 — Gate 检查逻辑修复

## Issue

#5: AgentDevFlow bootstrap: 完善 ADF 技能系统、文档与自动化流程

---

**ID**: Tech-5_v1
**状态**: Approved
**负责人**: 架构师
**日期**: 2026-04-15
**更新日期**: 2026-04-15（Pattern A C1/C2/C3/C4 修正）

---

## 上下文

本 Tech Spec 对应 PRD-5 Section 4.4（CI/CD 自动化增强），包含两部分：

1. **4.4.1 CI 检查逻辑修复**（P0，代码修改）：修复 `doc-pr-checks.yml` Gate 签字检查的 keyword grep 假阳性问题和角色口径不一致问题
2. **bootstrap-sync 直接 commit 到 main 的设计决策**（架构评审）：评估当前 CI 不检查 bootstrap-sync.yml 自动 commit 的合理性及风险

### 当前 CI 缺陷分析

`doc-pr-checks.yml` 的 Gate 签字检查存在两类核心缺陷：

1. **P0-1（仍存在）**：签字匹配使用简单的 keyword grep（`grep -i "PM" | grep -i "sign"`），存在假阳性，且无法验证语义完整性（角色+日期+结论三字段同现）
2. **P0-2（仍存在）**：Gate 1 角色检查使用 `"架构"`（模糊匹配），PRD-5 Section 4.4.1 P0-2 明确要求统一为 `"架构评审人"`

> **注意**：本 Tech Spec 不涉及 bootstrap-sync.py 脚本逻辑修改（按 PRD Section 5 非目标）。bootstrap-sync 的 CI/CD 配置说明属于 4.4.2 文档工作，在本 Tech Spec 中记录架构决策，待后续处理。

---

## 架构

### 变更范围

```
.github/workflows/doc-pr-checks.yml  (修改 — P0-1 正则升级 + P0-2 角色名统一)
.github/workflows/bootstrap-sync.yml  (修改 — commit message 工程加固)
docs/tech/Tech-5_v1.md              (本文件)
```

> bootstrap-sync.py 脚本逻辑本身不变（按 PRD 非目标）。

### 核心思路

将 `doc-pr-checks.yml` 中的 Gate 签字检查从 **keyword grep** 升级为 **结构化正则模式匹配**，在 Review Record 表格行中同时验证角色名、日期、结论三个字段。

### Review Record 表格格式基准

所有 PRD/Tech/QA 文档使用统一的 Review Record 表格格式：

```markdown
## 评审记录

| 日期 | 评审人 | 备注 | 决策 |
|---|---|---|---|
| 2026-04-15 | 某人 | 关键意见 | 通过 |
```

签字判断依据：
- **日期**：格式为 `YYYY-MM-DD`
- **评审人**：包含标准角色名（PM / 架构师 / QA / Engineer / 技术负责人）
- **备注/决策**：包含签字结论（Approved / Conditional / Rejected）

---

## 接口

### Gate 签字检查正则模式

每个 Gate 需要验证的角色字段如下：

| Gate | 必签角色（PRD-5 / Gate 文档一致口径） |
|------|--------------------------------------|
| Gate 1 PRD | PM、架构评审人 |
| Gate 2 Tech | PM、技术负责人、QA |
| Gate 3 QA Case Design | PM、架构评审人、Engineer |
| Gate 5 QA Test Report | QA、PM、Engineer |

> 注：角色名使用 Gate 文档（prompts/004_delivery_gates.md）的标准口径"架构评审人"，CI 检查与文档保持一致。

### 结构化正则模式

#### 模式 A：表格行匹配（推荐）

```bash
# 格式：| 日期 | 评审人 | 备注 | 决策 |
# 示例：| 2026-04-15 | PM | OK | Approved |
# 注意：角色名前后空格可变（|PM|、| PM |、|PM | 均支持）
# 注意：决策词支持中英文（Approved/通过/Conditional/附条件通过/Rejected/退回）

# 匹配某角色的签字行（role 可替换）
# C1: 空格可变 C2: 备注列允许为空 C3: 中英文决策词
SIG_LINE=$(grep "^|" "${DOC_FILE}" \
  | awk -F'|' -v role="${ROLE}" -v decision_regex="(?i)(approved|conditional|rejected|通过|有条件通过|驳回)" '
    NF >= 5 && $3 ~ role && $2 ~ /[0-9]{4}-[0-9]{2}-[0-9]{2}/ && $5 ~ decision_regex { print }
  ')

# 等价简化版（使用 grep -E + 可选空格）：
SIG_LINE=$(grep "^|" "${DOC_FILE}" \
  | grep -iE "\| *${ROLE} *\|" \
  | awk -F'|' 'NF >= 5 && $2 ~ /[0-9]{4}-[0-9]{2}-[0-9]{2}/ && $5 ~ /(?i)(approved|conditional|rejected|通过|有条件通过|驳回)/')

# 必须同时满足：
# 1. 行以 | 开头（表格行）
# 2. 评审人列为标准角色名（空格可变）
# 3. 日期列格式为 YYYY-MM-DD
# 4. 备注列：允许为空（.*），不参与验证
# 5. 决策列包含有效决策（中英文，大小写不敏感）
```

#### 模式 B：Gate 块区域匹配（备选，适用于无标准表格格式的文档）

```bash
# 先定位 Gate 块区域，再在该区域内查找签字行
GATE_BLOCK=$(sed -n '/Gate [0-9]/,/## /p' "${DOC_FILE}" | head -n -1)
SIG_LINE=$(echo "$GATE_BLOCK" \
  | grep -iE "\| *${ROLE} *\|" \
  | awk -F'|' 'NF >= 5 && $2 ~ /[0-9]{4}-[0-9]{2}-[0-9]{2}/ && $5 ~ /(?i)(approved|conditional|rejected|通过|有条件通过|驳回)/')
```

### CI 友好错误输出格式

```bash
echo "  [PRD Gate 1] FAILED: Missing required signature"
echo "    Required: PM sign-off (角色名 + 日期 + 决策)"
echo "    Required: 架构评审人 sign-off (角色名 + 日期 + 决策)"
echo "    Fix: Add review record to Gate 1 Review Record table in ${DOC_FILE}"
```

---

## 数据流

### 变更前（keyword grep — 有缺陷）

```text
grep -i "PM" doc.md | grep -i "sign" | head -1
                          ↓
              假阳性：备注行、说明文字也能匹配
              不完整：只验证关键字存在，不验证日期/结论字段
```

### 变更后（结构化正则 — 修复）

```text
检查 Review Record 表格行
    ↓
验证同一行中同时包含：
  - 角色名（如 PM）  ✅
  - 日期格式（YYYY-MM-DD）  ✅
  - 有效决策（Approved/Conditional/Rejected）  ✅
    ↓
三字段同时满足 → 签字通过
任一缺失 → exit 1 + 友好错误
```

---

## 可测试性

### 验证方法

#### 场景 1：合规文档通过检查

- 创建含完整 Review Record 的 PRD（PM + 架构师签字）
- 触发 doc-pr-checks.yml
- **预期**：Gate check 通过，CI 成功

#### 场景 2：缺失 PM 签字被阻断

- 创建 PRD，含架构师签字但无 PM 签字
- 触发 doc-pr-checks.yml
- **预期**：`exit 1`，输出友好错误 "Missing required signature: PM"

#### 场景 3：伪签字被识别

- 创建 PRD，含 "PM" 字样的行（如 `备注：需要 PM review`）但无正式 Review Record 表格行
- **预期**：`exit 1`（结构化模式不会匹配备注行）

#### 场景 4：Gate 1 角色名验证

- 创建 PRD，使用 "架构" 而非 "架构评审人" 作为 Review Record 评审人
- **预期**：`exit 1`（必须使用标准角色名"架构评审人"）

---

## bootstrap-sync 直接 commit 到 main：架构设计决策

### 当前设计

```
skills/shared/ → PR 评审通过 → 合并到 main
                                    ↓
                        bootstrap-sync.yml 触发
                                    ↓
                    .claude/skills/ 自动生成
                                    ↓
                    github-actions[bot] 直接 commit 到 main
                                    ↓
                    ❌ doc-pr-checks.yml 不检查此 commit
```

**关键事实**：
- bootstrap-sync.yml 的 `on: push: branches: [main]` 触发时，当前 workflow 的 PR 检查（`doc-pr-checks.yml`）不会运行（PR 合并后的 push 不会触发 PR 事件）
- 即 `.claude/skills/` 的自动 commit **没有任何 Gate 检查**

### 架构评估

| 维度 | 评估 | 说明 |
|------|------|------|
| **.claude/skills/ 性质** | 生成产物，非源码 | 这些文件是 `skills/shared/` 的确定性派生，由 bootstrap-sync.py 自动生成，不是人类直接编写的源码 |
| **设计合理性** | ✅ 基本合理 | 生成产物走 build pipeline 直接 commit 是工程惯例（如 `node_modules`、`dist/`） |
| **"所有变更需 PR" 原则冲突** | ⚠️ 表面冲突，实际不冲突 | 原则约束的是**人类创作的内容**（源码、文档）。bootstrap-sync 的产物是**机械派生**，源文件的 PR 审查已覆盖变更意图 |
| **Gate 检查缺失风险** | ⚠️ 需有后备保障 | 如果 bootstrap-sync.py 有 bug，错误产物会直接进入 main |
| **git 冲突风险** | ✅ 极低 | Step 0 先 `rmtree` 清理再写入，无合并冲突 |
| **CI 不检查 bootstrap-sync.yml 变更** | ✅ 设计如此 | bootstrap-sync.yml 变更走正常 PR 流程（doc-pr-checks.yml 会检查），产物 commit 不需额外检查 |

### 架构师技术意见

**结论：接受当前设计，理由如下：**

1. **.claude/skills/ 是生成产物，不是设计决策**：`skills/shared/` 是唯一的真实来源（已在 CLAUDE.md 中明确），`.claude/skills/` 是被动派生品。修改源文件必须走 PR → 人的审查已覆盖变更意图。

2. **bootstrap-sync 是幂等 build step**：SHA256 hash 对比确保只在内容变化时重写，无内容漂移风险。

3. **有后备保障**：如果产物异常，可通过 `workflow_dispatch` + `force_resync` 强制重新同步，或直接 revert 产物 commit。

4. **不需要引入 PR 流程的额外开销**：为生成产物引入 doc PR 审查会增加流程噪音，但安全收益极低（源文件 PR 已覆盖）。

**建议保持现状，不引入额外检查层。**

### 唯一需修复的已知问题

`bootstrap-sync.yml` 的 commit message 使用多行 shell 字符串引号（`[ci skip]"` 结尾），可能导致 YAML 解析失败。

**修复方案**：使用单行 commit message，CI workflow 层面通过 `[ci skip]` 或单独配置 skip ci。

```yaml
# 建议修复
git commit -m "chore: sync adf-prefix skills to .claude/skills [skip ci]"
```

此修复属于工程加固，不改变设计决策，可在 Tech Spec 评审通过后由 Engineer 一并处理。

---

## 风险

| 风险 | 级别 | 缓解 |
|------|------|------|
| 正则模式无法适配非标准 Review Record 格式 | 中 | 提供模式 B 作为备选；文档中明确 Review Record 表格格式要求 |
| 正则模式与实际文档格式不匹配导致漏检 | 中 | 先行验证当前所有 PRD/Tech/QA 文档格式覆盖率；如有不符，更新文档格式 |
| CI 误报导致合规 PR 被阻断 | 中 | 友好错误明确指出缺失字段；提供 dry-run 脚本供本地验证 |
| PRD-5 Section 4.4.2 CI/CD 配置文档与实现不同步 | 低 | 文档变更与 CI 变更同 PR，Gate 评审时一并验证 |
| bootstrap-sync 产物异常（脚本 bug）进入 main | 低 | force_resync 可强制重同步；产物 commit 可 revert；源文件 PR 审查已覆盖变更意图 |
| bootstrap-sync.yml commit message YAML 解析失败 | 低 | 改用单行 commit message + `[skip ci]` 标记（见上方设计决策） |

---

## 发布推进

### 阶段 1：代码修改

1. 修改 `doc-pr-checks.yml` Gate 检查逻辑
   - 将 keyword grep 替换为结构化正则（表格行三字段验证）
   - Gate 1 角色名统一为 `"架构评审人"`（与 004_delivery_gates.md 和 CI 口径一致）
   - 保留所有 `exit 1`（已在 HEAD 中修复）
   - 优化友好错误输出格式

2. 加固 `bootstrap-sync.yml` commit message（工程加固）
   - 将多行 shell 字符串 commit message 改为单行
   - 添加 `[skip ci]` 标记避免循环触发

3. 本地测试脚本验证
   - 用现有 PRD-1_v1.md / Tech-1_v1.md / QA-1_v1.md 验证正则模式覆盖率
   - 测试缺失签字场景

### 阶段 2：文档 PR

- 分支：`doc-5-ci-gate-fix`
- 包含：修改后的 `doc-pr-checks.yml`、加固后的 `bootstrap-sync.yml`、本 Tech Spec
- 不包含：bootstrap-sync.py（按 PRD 非目标）

### 阶段 3：Human Review #1

- 评审人：PM、QA Engineer、Team Lead
- 重点验证：正则模式对现有文档格式的覆盖率

---

## 回滚

### 回滚方案

若 CI 修改导致误报：

1. **紧急回滚**：Team Lead 或 Engineer 直接 revert `doc-pr-checks.yml` 的修改 commit
2. **文档 PR 回滚**：删除或 close `doc-5-ci-gate-fix` PR

若 bootstrap-sync commit message 加固导致循环触发或 push 失败：
- Revert `bootstrap-sync.yml` 的 commit message 变更
- 验证 sync 行为恢复正常

### 回滚条件

- CI 误报率 > 5%（超过 5% 的合规 PR 被阻断）
- 正则模式无法覆盖现有文档格式
- bootstrap-sync push 因 commit message 格式问题持续失败

---

## 评审记录

| 日期 | 评审人 | 备注 | 决策 |
|---|---|---|---|
| 2026-04-15 | 架构师 | 初始起草 | Draft |
| 2026-04-15 | 架构师 | Tech Spec 起草完成，确认技术方案可行，覆盖 P0-1/P0-2 修复 + bootstrap-sync 架构决策 | Approved |
| 2026-04-15 | PM | 范围一致性确认 — Tech Spec 覆盖 PRD #005 Section 4.4.1，架构决策合理，风险可接受 | Approved |
| 2026-04-15 | QA Engineer | Gate 2 Tech Review — 结构化正则思路正确，附 4 个 Conditional 项需解决 | Conditional |
| 2026-04-15 | Team Lead | Tech Review — 方案可行，通过 | Approved |
| 2026-04-15 | 架构师 | Pattern A 修正：C1 空格可选、C2 备注列可空、C3 中英文决策词、C4 角色名统一为"架构评审人" | Approved |
| 2026-04-15 | QA Engineer | Conditional 关闭 — Pattern A 修正方案可接受，4 项条件全部满足 | Approved |
| 2026-04-15 | QA Engineer | PR #6 Human Review #1 — CI 实现验证通过（22/22 PASS），Gate Status table "架构评审人"修正确认，PR #6 QA Approved（GitHub self-approval blocked，签字以此为准） | **Approved** ✅ |
