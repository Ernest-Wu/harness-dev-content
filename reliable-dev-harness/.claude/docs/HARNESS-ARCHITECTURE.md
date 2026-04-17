# Reliable Dev Harness 架构说明书

## 设计哲学：为什么做这套 Harness

Vibe Coding 的困境不是模型不够聪明，而是**模型周围没有系统**。一个聪明但不受控的 Agent，会在以下环节反复失败：

1. **方向漂移**：没有结构化需求文档，AI 边做边猜，后期推翻重来
2. **审美盲区**：没有设计图作为最高权威，AI 拼凑默认样式
3. **错误传染**：上下文过长，前面的错误假设被后面的任务继承
4. **质量妥协**：写完代码就宣称完成，跳过测试和审查
5. **重复犯错**：同样的修正说三遍，第四遍 AI 还是忘

这套 Harness 的核心理念是 **Harness Engineering**：不优化你跟 AI 说话的 Prompt，而是搭建一整套**约束、引导、反馈、进化**的基础设施。

---

## 核心概念

### Guides（前馈控制）= Skills
在 Agent 行动之前，把方法论、验收标准、反模式写进 `SKILL.md`。Agent 动手前就知道：
- 该做什么
- 按什么顺序做
- 什么算合格
- 常见错误是什么

### Sensors（反馈控制）= Hooks + exit-check.py
在 Agent 行动之后，用**确定性脚本**检查结果。不依赖模型自律，只依赖物理规则：
- 编译不过 → 阻断
- 测试不过 → 阻断
- exit-check 失败 → 阻断
- 代码没 review → 不让停

### Steering Loop（方向盘迭代）= feedback + evolution
从使用中学习。但关键升级：从毒舌产品经理的"自动升级"改为**"自动提案 + 人类确认"**，防止 LLM 自动改写规则带来的 regression。

### Context Firewall（上下文防火墙）= 全新实例 + 文件传递
每个 Task 的 Sub-Agent 都是全新实例，不继承历史上下文。状态通过 `.claude/state/` 的 L1-L4 分层文件传递。

---

## 五层架构详解

### 第一层：调度层 (Orchestrator)
**载体**：`.claude/CLAUDE.md`

调度层是用户与 Harness 的唯一入口。它：
- 理解用户意图
- 查询 `router.py` 确定该调用哪个 Skill
- 按标准流程编排 Sub-Agent
- 在关键节点执行 Hook
- 对违反规则的行为说"不"

### 第二层：执行层 (Sub-Agents)
**载体**：`.claude/agents/` 下的协议定义

四个角色：
| 角色 | 职责 | 隔离要求 |
|------|------|----------|
| implementer | 按 Skill 执行编码/设计/文档 | 每个 Task 新实例 |
| code-reviewer | 执行两阶段审查 | 每个 Review 新实例 |
| feedback-observer | 记录用户修正 | 每次反馈事件新实例 |
| evolution-runner | 扫描 feedback 积累，生成进化提案 | 每次 session 启动时运行 |

### 第三层：引导层 (Skills)
**载体**：`.claude/skills/<name>/SKILL.md`

每个 Skill 遵循 Product-Manager-Skills 的标准结构：
- **Purpose**：做什么、什么时候用
- **Key Concepts**：核心方法论、反模式（Anti-Patterns）
- **Application**：逐步执行指南
- **Examples**：至少一个好例子 + 一个坏例子
- **Common Pitfalls**：常见失败模式及修复
- **References**：相关 Skill 链接

**创新点**：每个 Skill 必须配 `exit-check.py`——确定性出口证书。

### 第四层：检查层 (Sensors)
**载体**：`.claude/hooks/` + `.claude/skills/*/exit-check.py`

两类传感器：
1. **计算型（确定性）**：`pre-commit-check.sh`、`stop-gate.sh`、各 `exit-check.py`
2. **推理型（语义级）**：`code-review` Skill 的两阶段审查

**规则**：推理型传感器之后，必须再过一层计算型传感器的验证。

### 第五层：进化层 (Steering Loop)
**载体**：`.claude/feedback/` + `.claude/docs/EVOLUTION-PROTOCOL.md`

四层进化：
1. **记录**：`feedback-observer` 把修正写入 feedback 文件
2. **毕业**：同类型反馈出现 3 次，`evolution-runner` 标记为"待毕业"
3. **优化**：生成 Skill 修正案 diff，提交人类确认
4. **创建**：某类操作反复出现却无 Skill 覆盖，提案创建新 Skill

---

## 状态管理：分层上下文 (L1-L4)

为了解决 Context Firewall 的"失忆"问题，我们设计了分层上下文：

| 层级 | 文件 | 大小控制 | 传递策略 |
|------|------|----------|----------|
| L1 | `state/L1-summary.md` | < 300 tokens | **每个 Task 必带** |
| L2 | `state/L2-spec.md` | < 2000 tokens | 按需引用，首 Task 必读 |
| L3 | `state/L3-design.md` | < 1500 tokens | 设计相关 Task 必读 |
| L4 | `state/L4-plan.md` | < 1000 tokens | 每个 Phase 启动时必读 |
| Task History | `state/task-history.yaml` | < 500 tokens | 只读索引，不传递细节 |

**L1 摘要模板**包含：
- 项目一句话目标
- 目标用户
- 核心功能（3 条以内）
- 技术栈
- 当前活跃 Phase
- 下一个待完成 Task

---

## 标准工作流示例

### 场景：从零开发一个写作工具

**Step 1：需求定义**
- 调用 `product-spec-builder`
- 输出 `state/L2-spec.md`
- 运行 `exit-check.py`（检查是否有 Problem Statement、验收标准、Scope 边界）
- **失败** → 退回补全；**通过** → 下一步

**Step 2：设计规范**
- 调用 `design-brief-builder`
- 输出 `state/L3-design.md`
- 运行 `exit-check.py`（检查是否有配色 hex、交互风格、动效级别）
- **失败** → 退回补全；**通过** → 下一步

**Step 3：设计稿**
- 调用 `design-maker`（通过 MCP 在 Figma/Pencil 中作图）
- 产出设计稿链接/文件

**Step 4：开发计划**
- 调用 `dev-planner`
- 输出 `state/L4-plan.md`
- 运行 `exit-check.py`（检查 Phase 是否拆分清晰、依赖是否可获取）

**Step 5：迭代开发（Loop）**
- 对每个 Task：
  1. `dev-builder` 实现 → `exit-check.py`（编译+测试）
  2. `code-review` 审查 → `exit-check.py`（必须指出至少1个问题）
  3. `pre-commit-check` → `auto-push`
  4. 更新 `task-history.yaml`

**Step 6：发布**
- 调用 `release-builder`
- 运行 `exit-check.py`
- Done

---

## 关键设计决策

### 1. 为什么每个 Skill 都要有 exit-check.py？
因为自然语言规则（"请确保编译通过"）不可靠。LLM 会在上下文压力下"忘记"规则。`exit-check.py` 是**物理强制**，不通过就卡死流程。

### 2. 为什么 Steering Loop 不自动写入？
毒舌产品经理 4.0 的"自动升级"在理念上先进，但工程上危险。LLM 修改规则时可能：
- 破坏原有边界条件
- 丢失"为什么这样设计"的上下文
- 引入与现有 Skill 冲突的规则

我们的方案是：**自动发现、自动提案、人工确认、可控合并**。

### 3. 为什么设计图是最高权威？
因为自然语言描述视觉（"深色主题、极简风格"）歧义度极高。设计图是唯一无歧义的视觉 Source of Truth。code-review 时必须对照设计图验证 UI。

### 4. 为什么 Sub-Agent 要全新实例？
因为 LLM 的"记忆"是不可靠的。一个 Task 中的错误假设（"这个 API 返回字符串"）如果带入下一个 Task，会导致连锁错误。全新实例虽然增加了初始化成本，但换来了**错误隔离**。

---

## 与 Product-Manager-Skills 的关系

Reliable Dev Harness 是 Product-Manager-Skills 思想的**运行时工程化实现**：

- PM-Skills 教你**如何写好一个 Skill**（ pedagogic-first ）
- Reliable Dev Harness 确保**Skill 在真实产品开发中被严格执行**（hard gates ）

两者是互补的：PM-Skills 提供知识和标准，Harness 提供执行和约束。
