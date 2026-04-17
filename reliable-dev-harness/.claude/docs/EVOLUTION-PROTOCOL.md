# Steering Loop 安全协议

## 核心原则

> **自动记录可以发生，自动提案可以发生，自动写入绝对禁止。**

这是 Reliable Dev Harness 与毒舌产品经理 4.0 最关键的分野。LLM 自动修改规则文件是 regression 的高危区，必须由人类确认。

---

## 四层进化机制（带安全门）

### Layer 1: 静默记录 (Silent Capture)

**触发条件**：用户在任何消息中表达修正、不满、补充或纠正。

**执行者**：`feedback-observer` Sub-Agent（全新实例）。

**动作**：
1. 读取用户的修正消息
2. 提取：问题类型、触发场景、期望行为、涉及 Skill
3. 写入 `.claude/feedback/YYYY-MM-DD_{hash}.md`
4. 更新 `.claude/feedback/FEEDBACK-INDEX.md`

**记录格式**：
```markdown
---
date: 2026-04-15
skill: dev-builder
type: [missing-test | wrong-approach | scope-creep | ui-mismatch | ...]
source_task: "实现登录页面"
trigger: "你又忘了写单元测试"
---

## Expected Behavior
每次新增 API 路由时，必须同步编写对应的单元测试。

## Why It Matters
没有测试的代码在后续重构中极易回归，且 review 时无法验证正确性。

## Proposed Rule Addition
在 `dev-builder/SKILL.md` 的 Application 中增加一条：
"每个 API 路由完成后，立即在 `__tests__/` 下编写单元测试，测试不通过不允许进入 code-review。"
```

---

### Layer 2: 毕业检测 (Graduation Scan)

**触发条件**：每次 session 启动时，`evolution-runner` 扫描 feedback 积累。

**毕业标准**：
- `type` + `skill` 组合出现 **≥ 3 次**
- 或者同一 `type` 跨多个 skill 出现 **≥ 5 次**

**执行者**：`evolution-runner` Sub-Agent（全新实例）。

**动作**：
1. 读取 `FEEDBACK-INDEX.md`
2. 按 `(type, skill)` 聚合计数
3. 对达到毕业门槛的条目，生成 `PROPOSAL_{timestamp}.md`

**提案内容**：
```markdown
---
proposal_id: PROP-20260415-001
status: pending_review  # 绝不允许直接 applied
skill_affected: dev-builder
feedback_count: 3
type: missing-test
---

## Current Rule Gap
`dev-builder/SKILL.md` 虽然提到"编译验证"，但没有明确要求"测试覆盖"。

## Proposed Change
在 `dev-builder/SKILL.md` 的 Application Step 3 后插入：

### Step 3b: 编写单元测试
- 每个新 API 路由必须同步编写单元测试
- 测试文件放在 `__tests__/` 目录
- 运行 `npm test`（或对应命令），测试不通过不进入 review

## Affected exit-check.py
同时修改 `dev-builder/exit-check.py`，增加：
- 检查 `__tests__/` 下是否有新增测试文件
- 检查 `npm test` 是否通过

## Risk Assessment
- **低风险**：增强质量，不破坏现有流程
- **注意点**：如果项目本身没有测试框架，需要先由 `dev-planner` 规划测试基础设施
```

---

### Layer 3: 人类确认 (Human Gate)

**触发条件**：`evolution-runner` 生成提案后，由调度层向用户展示。

**用户动作三选一**：
1. **Approve**：接受提案，由调度层调用 `implementer` 执行修改
2. **Revise**：用户提出修改意见，`evolution-runner` 重生成提案
3. **Reject**：不采纳，将该 feedback 标记为 `rejected`（记录原因，防止重复提案）

**关键规则**：
- 在人类说 "Approve" 之前，**任何 Sub-Agent 不得触碰 `SKILL.md` 或 `exit-check.py`**
- 修改完成后，必须运行 `check-harness.py` 确保 Harness 自身健康

---

### Layer 4: 新 Skill 提案 (New Skill Creation)

**触发条件**：某类操作模式反复出现（≥ 5 次 feedback 提及），但现有 7 个 Skill 均不覆盖。

**执行者**：`evolution-runner`

**动作**：
1. 生成 `NEW_SKILL_PROPOSAL_{timestamp}.md`
2. 提案包含：Skill 名称、类型（component/interactive/workflow）、Purpose、Application 大纲
3. 提交人类确认
4. 确认后，由 `implementer` 按 PM-Skills 标准格式创建完整 Skill 文件

---

## FEEDBACK-INDEX.md 格式

```markdown
# Feedback Index

## Unprocessed (未毕业)
| Date | ID | Skill | Type | Trigger | Count |
|------|-----|-------|------|---------|-------|
| 2026-04-15 | fb-001 | dev-builder | missing-test | 你又忘了写单元测试 | 3 ⭐ |
| 2026-04-14 | fb-002 | code-review | too-lenient | review 没指出明显问题 | 2 |

## Graduated (待提案)
- [fb-001] missing-test @ dev-builder → `PROPOSAL_20260415_001.md` (pending_review)

## Applied (已确认合并)
- [fb-000] ui-sync @ design-maker → 已合并到 SKILL.md v1.2

## Rejected (已拒绝)
- [fb-003] complex-config @ dev-planner → 拒绝原因：项目特异性，不适合通用 Skill
```

---

## Anti-Patterns（Steering Loop 的禁忌）

### Anti-Pattern 1: Auto-Apply
**症状**：evolution-runner 直接修改 SKILL.md，不经过人类确认。

**后果**：
- 可能破坏 Skill 的现有边界条件
- 可能引入与引用该 Skill 的 workflow 冲突的规则
- 丢失修改的"为什么"，导致 Skill 变成补丁堆

**修复**：强制执行 Human Gate。任何对 `.claude/skills/` 的修改必须由人类触发。

### Anti-Pattern 2: Over-Generalization
**症状**：把一次项目特异性的反馈（"这个项目的颜色应该是紫色"）升级成通用 Skill 规则。

**后果**：Skill 失去通用性，未来项目被错误约束。

**修复**：evolution-runner 在生成提案时必须评估："这条规则是否适用于 80% 的类似产品开发场景？"

### Anti-Pattern 3: Feedback Amnesia
**症状**：用户已经给过反馈，但系统没有记录或没有检索到，导致重复犯错。

**后果**：用户失去对 Harness 的信任，宁愿回到手动管理。

**修复**：
- 每次启动 session，`check-evolution` Hook 必须读取 `FEEDBACK-INDEX.md`
- 如果有 "applied" 的规则与用户当前场景相关，调度层必须在 Task Package 中显式引用

---

## 与毒舌产品经理 4.0 的差异总结

| 维度 | 毒舌产品经理 4.0 | Reliable Dev Harness（本协议） |
|------|-----------------|------------------------------|
| 自动升级 | 3 次直接写入 Skill | 3 次生成提案，人类确认后写入 |
| 安全性 | 中（快但风险高） | 高（慢但可防 regression） |
| 透明度 | 后台静默升级 | 每次升级都有提案文档和 diff |
| 可回滚 | 困难 | 容易（提案和修改都在 git 中） |
| 信任度 | 依赖系统自律 | 依赖人类最终把关 |

**结论**：我们的产品开发 Harness 选择**安全优先**，因为规则的 regression 比代码的 regression 更难发现和修复。
