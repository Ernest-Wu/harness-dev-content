# PM Gate Points — 里程碑跟踪

> **本文件跟踪 PM Gate Points 实施进度。** 每次完成一个任务，更新状态并记录完成日期。
> 
> **上下文恢复**: 新 session 请先阅读 `PM-GATE-DESIGN.md` 了解完整设计意图，然后查看本文件了解当前进度。
>
> ⚠️ **角色区分**: 本文件在 `docs/` 目录（开发者文档），不是 `.claude/docs/`（运行时文档）。

---

## 当前里程碑: M4 — PM Enrichment（已完成）

---

## M1: 基础加固（P0 — 修复安全漏洞 + 显式化 PM 角色）

**目标**: 修复 release-builder 空占位符，显式化所有隐式 PM 决策点  
**状态**: ✅ 已完成  
**前置条件**: PM-GATE-DESIGN.md 已写入项目 ✅

| # | 任务 | 修改文件 | 验收标准 | 状态 |
|---|------|---------|---------|------|
| 1.1 | 实现 release-builder/exit-check.py | `.claude/skills/dev/release-builder/exit-check.py` | 运行后能验证 smoke test、回滚计划、task-history、P0 features | ✅ |
| 1.2 | CLAUDE.md 增加 PM Decision Points 段 | `.claude/CLAUDE.md` | 包含完整的 G0-G5 + CG0-CG5 定义 | ✅ |
| 1.3 | FEEDBACK-OBSERVER 增加 PM 反馈类型 | `.claude/agents/FEEDBACK-OBSERVER.md` | 新增 5 个 PM 类型 + 毕业阈值调整 | ✅ |
| 1.4 | 设计文档已写入项目 | `docs/PM-GATE-DESIGN.md` | 文件存在于 `docs/`（开发者文档区） | ✅ |
| 1.5 | 里程碑跟踪文件已创建 | `docs/PM-GATE-MILESTONES.md` | 文件存在于 `docs/`（开发者文档区） | ✅ |

**M1 完成标志**: harness 仍然能正常运行 (`check-harness.py` 通过)，但现在已经显式化了所有 PM 决策点。任何新 session 读 CLAUDE.md 就能理解 PM 决策发生在哪里。

---

## M2: Spec 增强（P1 — 提升 PM 决策质量基础设施）

**目标**: 增强 State 文件和 exit-check，建立目标追溯链  
**状态**: ✅ 已完成  
**前置条件**: M1 完成

| # | 任务 | 修改文件 | 验收标准 | 状态 |
|---|------|---------|---------|------|
| 2.1 | product-spec-builder 增加 Entry Modes | `.claude/skills/dev/product-spec-builder/SKILL.md` | 支持 Guided/Context dump/Best guess 三种模式 + PM Discovery Gate 检查清单 + PM 决策字段输出 | ✅ |
| 2.2 | L2-spec.md 模板增加 PM 字段 | `.claude/state/L2-spec.md` | 含业务目标、假设列表、P0/P1/P2、MVP 边界 | ✅ |
| 2.3 | L3-design.md 模板增加品牌规范引用 | `.claude/state/L3-design.md` | 含品牌规范引用字段、可访问性声明 | ✅ |
| 2.4 | L4-plan.md 模板增加 PM 字段 | `.claude/state/L4-plan.md` | 含业务目标、优先级标记、风险标志 | ✅ |
| 2.5 | product-spec-builder exit-check 增加 PM 警告 | `.claude/skills/dev/product-spec-builder/exit-check.py` | 检测 missing prioritization、no MVP boundary、no business goal | ✅ |
| 2.6 | 新增 L0-strategy.md 模板 | `.claude/state/L0-strategy.md` | 内容策略验证模板（业务目标、受众、KPI） | ✅ |
| 2.7 | 新增 L6-distribution.md 模板 | `.claude/state/L6-distribution.md` | 分发就绪检查模板（平台、标题、标签、UTM） | ✅ |

**M2 完成标志**: PM 决策的数据基础建好了——每个 Gate 都有对应的 State 文件字段承载 PM 决策。

---

## M3: PM Gate 验证增强（P2 — 让 Gate 真正把关）

**目标**: 安装 PM Gate 的 Hard Gate 检查机制  
**状态**: ✅ 已完成  
**前置条件**: M2 完成

| # | 任务 | 修改文件 | 验收标准 | 状态 |
|---|------|---------|---------|------|
| 3.1 | code-review exit-check 增加 spec compliance 量化 | `.claude/skills/dev/code-review/exit-check.py` | 检查每条 spec item 有验证结果、检测 scope creep、HIGH issue 未评估 user impact | ✅ |
| 3.2 | dev-planner exit-check 增加 Phase→Spec 映射 | `.claude/skills/dev/dev-planner/exit-check.py` | Feature-Phase Mapping、P0→MVP 对齐、Business Goal追溯、Risk Flags | ✅ |
| 3.3 | design-brief-builder exit-check 增加品牌验证 | `.claude/skills/dev/design-brief-builder/exit-check.py` | 品牌规范引用或明确"无品牌约束"、可访问性声明、spec 用户对齐 | ✅ |
| 3.4 | Spec Gap Protocol 写入 code-review SKILL.md | `.claude/skills/dev/code-review/SKILL.md` | A/B/C/D/E 分类表、记录格式、Reviewer 职责 | ✅ |
| 3.5 | Content track 增加 CG0 Content Strategy Gate 定义 | `.claude/CLAUDE.md` | CG0 的输入/输出/验收标准（Hard Gate + Creative Gate） | ✅ |
| 3.6 | tts-engine Creative Gate 改为不可跳过 | `.claude/skills/content/tts-engine/SKILL.md` + `.claude/CLAUDE.md` | G4a-1/CG2 标注为必选、不可跳过 | ✅ |

**M3 完成标志**: PM Gate 不只是"概念上的决策点"了——有 exit-check 在物理上验证每个 Gate 的条件。

---

## M4: PM Enrichment（P3 — 从 pm-skills 注入决策框架）

**目标**: 将 pm-skills 的 PM 决策框架注入到对应 Skill，创建新 Skill  
**状态**: ✅ 已完成  
**前置条件**: M3 完成

| # | 任务 | 修改文件 | 验收标准 | 状态 |
|---|------|---------|---------|------|
| 4.1 | product-spec-builder Key Concepts 注入 pm-skills 框架 | `.claude/skills/dev/product-spec-builder/SKILL.md` | 含 problem-statement + proto-persona + prioritization-advisor 框架摘要 | ✅ |
| 4.2 | design-brief-builder Key Concepts 注入 pm-skills 框架 | `.claude/skills/dev/design-brief-builder/SKILL.md` | 含 positioning-statement + user-story-mapping 框架摘要 | ✅ |
| 4.3 | dev-planner Key Concepts 注入 pm-skills 框架 | `.claude/skills/dev/dev-planner/SKILL.md` | 含 roadmap-planning + epic-hypothesis + lean-ux-canvas 框架摘要 | ✅ |
| 4.4 | 新建 pm/validation Skill | `.claude/skills/pm/validation/SKILL.md` + `exit-check.py` | G5 验证 Skill | ✅ |
| 4.5 | 新建 pm/content-strategy Skill | `.claude/skills/pm/content-strategy/SKILL.md` + `exit-check.py` | CG0 内容策略 Skill | ✅ |
| 4.6 | 新建 pm/distribution-planner Skill | `.claude/skills/pm/distribution-planner/SKILL.md` + `exit-check.py` | CG4 分发规划 Skill | ✅ |
| 4.7 | 新建 pm/content-validation Skill | `.claude/skills/pm/content-validation/SKILL.md` + `exit-check.py` | CG5 内容验证 Skill | ✅ |
| 4.8 | router.py 增加 pm/ 域路由 | `.claude/router.py` | 支持 `--domain pm` 过滤 | ✅ |
| 4.9 | check-harness.py 增加 PM 域检查 | `.claude/check-harness.py` | 三域健康检查 | ✅ |

**M4 完成标志**: PM 决策层完整了——有 pm/ 域的 Skill 提供方法论，有 exit-check 提供验证，有 Gate Points 提供决策点。

---

## 变更日志

| 日期 | 变更 | 作者 |
|------|------|------|
| 2026-04-17 | M1 任务 1.1-1.3 实施：exit-check.py 实现、CLAUDE.md PM 决策点、FEEDBACK-OBSERVER PM 类型 | Session 2 |
| 2026-04-17 | M2 任务 2.1-2.7 实施：State 模板增强、exit-check PM 警告、L0/L6 新模板 | Session 3 |
| 2026-04-17 | M3 任务 3.1-3.6 实施 | Session 4 |
| 2026-04-17 | M4 任务 4.1-4.9 实施：pm-skills 框架注入 3 个 dev Skill、4 个新 pm/ Skill、router 三域路由、check-harness 三域检查 | Session 5 |