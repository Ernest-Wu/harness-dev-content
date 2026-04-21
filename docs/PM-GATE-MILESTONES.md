# PM Gate Points — 里程碑跟踪

> **本文件跟踪 PM Gate Points 实施进度。** 每次完成一个任务，更新状态并记录完成日期。
> 
> **上下文恢复**: 新 session 请先阅读 `PM-GATE-DESIGN.md` 了解完整设计意图，然后查看本文件了解当前进度。
>
> ⚠️ **角色区分**: 本文件在 `docs/` 目录（开发者文档），不是 `.claude/docs/`（运行时文档）。

---

## 当前里程碑: M4 — PM Enrichment（已完成）

**M4 完成标志**: PM 决策层完整了——有 pm/ 域的 Skill 提供方法论，有 exit-check 提供验证，有 Gate Points 提供决策点。

---

## M5: 工程化基座（P0 — 让 exit-check 代码质量可维护）

**目标**: 统一 exit-check 代码规范，增强 check-harness.py 的深度检查能力，为后续迭代建立工程基线
**状态**: ✅ 已完成
**完成日期**: 2026-04-20
**前置条件**: M4 完成
**详细设计**: 参见 `docs/OPTIMIZATION-ROADMAP.md` Phase 1

| # | 任务 | 修改文件 | 验收标准 | 状态 |
|---|------|---------|---------|------|
| 5.1 | exit-check 代码质量标准化 | 全部 17 个 `exit-check.py` | 所有 `add_issue` 显式声明 `level=`；`ensure_project_root()` 被调用；check-harness.py AST 检查强制 level 显式 | ✅ |
| 5.2 | check-harness.py 深度检查增强 | `.claude/check-harness.py` | 新增 `check_skill_coverage`（SKILL.md Exit-Check Criteria vs exit-check.py add_issue code 对齐）；`check_print_and_exit`（AST 确认 print_and_exit 被调用）；`check_state_cross_reference`（L2 Business Goal 与 L4 Business Goal 一致性） | ✅ |

**M5 完成标志**: 修改任何一个 exit-check 后，check-harness.py 能检测出 level 缺失、print_and_exit 遗漏、skill coverage 不匹配等问题。

---

## M6: 运行时 Enforcement（P1 — 让协议不只是文档）

**目标**: 给 Creative Gate、Steering Loop、状态追溯增加物理验证层
**状态**: ⬜ 未开始
**前置条件**: M5 完成
**详细设计**: 参见 `docs/OPTIMIZATION-ROADMAP.md` Phase 2 + Phase 3（部分）+ Phase 4（部分）

| # | 任务 | 修改文件 | 验收标准 | 状态 |
|---|------|---------|---------|------|
| 6.1 | Creative Gate 记录验证机制 | `tts-engine/exit-check.py`, `script-writer/exit-check.py`, `visual-designer/exit-check.py`, `frontend-slides/exit-check.py` | 每个 exit-check 验证对应 state 文件中存在 Creative Gate 选择记录 | ✅ |
| 6.2 | feedback-analyzer.py | `.claude/hooks/feedback-analyzer.py` | 纯 stdlib 实现；扫描 feedback/ 目录并按 (skill, type) 聚合计数；输出达到毕业阈值的候选提案 | ✅ |
| 6.3 | FEEDBACK-INDEX.md 初始结构 | `.claude/feedback/FEEDBACK-INDEX.md` | 含示例条目和毕业阈值说明；feedback-analyzer 输出可写入此文件 | ✅ |
| 6.4 | L0→L2→L4 跨文件追溯验证 | `dev-planner/exit-check.py`, `product-spec-builder/exit-check.py` | dev-planner 验证 Phase 0 覆盖所有 P0 features；product-spec-builder 验证 L0→L2 Business Goal 对齐 | ✅ |

**M6 完成标志**: ✅ 已完成（2026-04-20）

---

## M7: 可观测性与开发者体验（P2 — 让 harness 使用者看得见进度）

**目标**: 降低 Orchestrator 和用户的认知负担，让项目状态一目了然
**状态**: ✅ 已完成
**完成日期**: 2026-04-21
**前置条件**: M6 完成
**详细设计**: 参见 `docs/OPTIMIZATION-ROADMAP.md` Phase 2（剩余部分）+ Phase 3（剩余部分）

| # | 任务 | 修改文件 | 验收标准 | 状态 |
|---|------|---------|---------|------|
| 7.1 | exit-check 单元测试框架 | 新增 `tests/` | 为 5 个核心 exit-check 提供 mock state 测试；运行时间 < 5 秒 | ✅ |
| 7.2 | Task Package 自动化生成器 | 新增 `.claude/package-task.py` | CLI: `--skill`, `--phase`, `--task`；自动读取 L1-L4 state 文件和 SKILL.md；输出填充好的 Task Package Markdown | ✅ |
| 7.3 | 当前进度仪表盘 | 新增 `.claude/status-board.py` | 读取全部 state 文件；输出 dev/content/pm track 的 Gate 通过状态、当前活跃 Phase、阻塞项 | ✅ |
| 7.4 | Steering Loop 端到端测试 | 新增 `.claude/hooks/test-steering-loop.sh` | 模拟 3 次同类反馈 → feedback-analyzer 检测毕业 → evolution-runner 生成提案 → 人类确认 → 应用到 SKILL.md | ✅ |

**M7 完成标志**: ✅ 新用户可以在 30 秒内通过 `status-board.py` 了解项目全局状态；修改 exit-check 后可以在 10 秒内通过单元测试验证正确性。

---

## M8: 扩展性与动态发现（P3 — 让新增 skill 零摩擦）

**目标**: 消除新增 skill 时的手动配置负担
**状态**: ⬜ 未开始
**前置条件**: M7 完成
**详细设计**: 参见 `docs/OPTIMIZATION-ROADMAP.md` Phase 5

| # | 任务 | 修改文件 | 验收标准 | 状态 |
|---|------|---------|---------|------|
| 8.1 | check-harness.py 动态发现 | `.claude/check-harness.py` | 从 `.claude/skills/{domain}/` 目录自动扫描子目录；不再硬编码 DEV_SKILLS / CONTENT_SKILLS / PM_SKILLS | ⬜ |
| 8.2 | router.py 动态索引 | `.claude/router.py` | 从每个 skill 的 `SKILL.md` frontmatter 或独立索引文件读取 triggers；不再硬编码 SKILL_INDEX | ⬜ |
| 8.3 | 双轨运行时冲突检测 | `.claude/check-harness.py` | 当 L2-spec.md 和 L2-content-spec.md 同时存在时，检测 Business Goal 是否冲突 | ⬜ |

**M8 完成标志**: 新增一个 skill 只需创建目录（`SKILL.md` + `exit-check.py`），无需修改任何其他文件即可被 harness 识别和路由。

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