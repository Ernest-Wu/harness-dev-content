# Reliable Dev Harness — 优化路线图

> **本文件是上下文持久化文档。** 记录 M4 完成后 harness 的系统性优化方向、优先级排序和实施建议。
> 
> **阅读顺序**: `PM-GATE-DESIGN.md` → `PM-GATE-MILESTONES.md` → **本文件** → `.claude/CLAUDE.md`
>
> ⚠️ **角色区分**: `docs/` 是开发者文档（👷 你），`.claude/docs/` 是运行时文档（🏃 harness 用户）。不要混淆。

---

## 一、当前健康度快照（基准: 2026-04-19）

| 维度 | 评分 | 关键证据 |
|------|------|---------|
| **架构完整性** | 4.5/5 | M1-M4 全部完成，三域分离，L0-L6 状态分层，PM Gate Points 横切层已定义 |
| **Hard Gate 覆盖率** | 4/5 | 17/17 exit-check 存在且使用 `_utils.exit_check_base`，但质量不均匀 |
| **运行时可靠性** | 2.5/5 | Orchestrator 行为全靠文档约定，Creative Gate 无物理验证，Steering Loop 未启动 |
| **代码工程化** | 3/5 | exit-check 中 `add_issue` 的 `level` 显式声明率 <15%；`ensure_project_root()` 提供但 0 人使用 |
| **可观测性** | 1.5/5 | 无进度仪表盘、无 Gate 状态追踪、Task Package 纯手动组装 |
| **测试** | 0.5/5 | harness 本身无测试，exit-check 脚本无测试，修改后只能靠运行验证 |

**核心结论**: 骨架完整，但**设计意图和物理实现之间存在断层**——大量"应该"还没有变成"必须"。

---

## 二、优化路径总览

```
Phase 1: 工程化基座（让代码更可靠）
├── 1.1 exit-check 代码质量标准化
├── 1.2 为 exit-check 编写单元测试
└── 1.3 check-harness.py 深度检查增强

Phase 2: 运行时 Enforcement（让协议不只是文档）
├── 2.1 Creative Gate 记录验证机制
├── 2.2 Task Package 自动化生成器
└── 2.3 当前进度仪表盘

Phase 3: Steering Loop 启动（让反馈闭环真的转起来）
├── 3.1 feedback-analyzer.py 自动化脚本
└── 3.2 反馈毕业 → 提案生成的端到端测试

Phase 4: 状态一致性（让 L0-L6 不互相撒谎）
├── 4.1 L0→L2→L4 跨文件追溯验证
└── 4.2 双轨运行时冲突检测

Phase 5: 扩展性（让新增 skill 不踩坑）
└── 5.1 check-harness.py 和 router.py 的动态发现
```

---

## 三、Phase 1: 工程化基座

### 1.1 exit-check 代码质量标准化

**问题**: 17 个 exit-check 中 `add_issue(..., level=...)` 的显式声明率极低。多数脚本依赖默认 `"high"`，代码审查时需要查阅 `exit_check_base.py` 才能知道默认行为。

**方向**:
- 制定 exit-check 代码规范：`add_issue` 必须显式声明 `level`，禁止依赖默认参数
- 在 `check-harness.py` 中增加 AST 检查：扫描所有 `add_issue` 调用，强制要求 `level=` 关键字存在
- 统一启用 `ensure_project_root()` — 当前 `exit_check_base.py` 已提供但 0 个 exit-check 使用

**实施难度**: 低（批量重构，无逻辑变更）

### 1.2 为 exit-check 编写单元测试

**问题**: 修改 exit-check 后，验证方式只有两种：(1) 运行 `check-harness.py`（只验证语法）(2) 手动在真实项目上运行（慢、有副作用）。这导致 exit-check 的迭代风险很高。

**方向**: 创建 `tests/` 目录（或 `.claude/skills/_utils/test_exit_checks.py`），为每个 exit-check 提供**假文件测试（mock state）**:

```python
# 示例：测试 release-builder exit-check
def test_release_blocks_when_no_rollback():
    with tempfile.TemporaryDirectory() as tmp:
        create_minimal_state(tmp, rollback=False)
        result = run_exit_check("release-builder", cwd=tmp)
        assert result.exit_code == 1
        assert "no_rollback_plan" in result.stdout
```

**关键收益**:
- 修改 exit-check 正则时，可以秒级验证
- 新增 state 文件字段时，可以验证旧 exit-check 不崩溃
- 符合 harness 自身的"物理验证"哲学

**实施难度**: 中（需要设计 mock state 生成器）

### 1.3 check-harness.py 深度检查增强

**当前能力**: 检查文件存在、语法、frontmatter、import、state 非空。

**缺失能力**:
- SKILL.md 中提到的交付物，exit-check.py 是否覆盖了？
- exit-check 是否调用了 `print_and_exit()`？
- SKILL.md 的 `## Exit-Check Criteria` 段与 exit-check.py 的实际检查是否对齐？
- State 文件之间的交叉引用是否一致？

**方向**:
- 新增 `check_skill_coverage()`: 读取 SKILL.md 的 `Exit-Check Criteria` 段，提取编号列表，与 exit-check.py 中的 `add_issue` code 交叉验证
- 新增 `check_print_and_exit()`: AST 确认每个 exit-check 最终调用了 `print_and_exit`
- 新增 `check_state_cross_reference()`: 验证 L2-spec.md 中的 `## Business Goal` 与 L4-plan.md 中的 `## Business Goal` 是否同时存在（或同时不存在）

**实施难度**: 中（需要解析 Markdown 结构）

---

## 四、Phase 2: 运行时 Enforcement

这是 harness **从"好设计"走向"好工具"**的关键。

### 2.1 Creative Gate 记录验证机制

**问题**: `CLAUDE.md` 规定"Creative Gate 不可跳过"，但没有任何 exit-check 验证 Creative Gate 的选择是否被记录到 state 文件。

**方向**: 在每个涉及 Creative Gate 的 exit-check 中，增加 **Gate Log 验证**:

```python
# tts-engine/exit-check.py 新增
def check_creative_gate_record():
    l3_design = Path(".claude/state/L3-design.md")
    if l3_design.exists():
        content = l3_design.read_text()
        if "## TTS" not in content:
            add_issue("cg2_not_recorded",
                      "CG2 PM Voice Direction Gate selection not recorded in L3-design.md",
                      level="high")
```

**关键洞察**: 这本质上是在 exit-check 中加入 **"人类确认的痕迹"** 验证——state 文件中必须有明确标记证明用户做了选择，而不是 agent 擅自用了默认值。

**受影响 exit-check**: `tts-engine`, `script-writer`, `visual-designer`（共 3-4 个）

**实施难度**: 低

### 2.2 Task Package 自动化生成器

**问题**: `CLAUDE.md` 提供了详细的 Sub-Agent Task Package 模板，但完全依赖 Orchestrator 手动组装。容易遗漏 PM 横切核对点，L1-L4 上下文需要从多个文件手动复制粘贴。

**方向**: 新增 `.claude/package-task.py`:

```bash
python3 .claude/package-task.py --skill dev/dev-builder --phase "Phase 2" --task "Implement login API"
```

自动读取 `L1-summary.md` → L1 Context, `L2-spec.md` + `L3-design.md` + `L4-plan.md` → L2-L4 References, `dev/dev-builder/SKILL.md` → Active Skill, 当前 Phase 信息 → PM 核对点。

**实施难度**: 中（需要设计 CLI 接口和模板渲染）

### 2.3 当前进度仪表盘

**问题**: 用户（或 Orchestrator）无法快速回答"项目现在在哪一步？哪个 Gate 通过了？哪个 blocked 了？"

**方向**: 新增 `.claude/status-board.py`，输出类似:

```
═══ Harness Status Board ═══

Project: {从 L1-summary.md 读取}
Tracks:  dev [████████░░] 80%  |  content [████░░░░░░] 40%

Dev Track Gates:
  G0 Discovery      ✅ L2-spec.md (P0: 3 features)
  G1 Direction      ✅ L3-design.md (brand: explicit none)
  G2 Scope          ✅ L4-plan.md (Phase 0/1/2 defined)
  G3 Compliance     ⬜ LAST_REVIEW.md not found
  G4 Release        ⬜ ROLLBACK.md missing
  G5 Validation     ⏸  Waiting for 7-day data
```

**实施难度**: 中（需要维护 Gate 状态映射表）

---

## 五、Phase 3: Steering Loop 启动

### 3.1 feedback-analyzer.py 自动化脚本

**问题**: `EVOLUTION-RUNNER.md` 定义了反馈毕业阈值（dev ≥3, PM ≥2, content ≥5），但没有物理工具实现"group by (skill, type) and count"。`FEEDBACK-INDEX.md` 是空的。

**方向**: 新增 `.claude/hooks/feedback-analyzer.py`（纯 stdlib，符合零依赖原则）:

```python
#!/usr/bin/env python3
"""Scan feedback/ directory and report graduated issues."""

from pathlib import Path
from collections import Counter

feedback_dir = Path(".claude/feedback")
entries = []  # Parse all YYYY-MM-DD_*.md files

# Group by (skill, type)
counts = Counter((e.skill, e.type) for e in entries)

THRESHOLDS = {"dev": 3, "pm": 2, "content": 5}

for (skill, ftype), count in counts.most_common():
    domain = infer_domain(skill)
    if count >= THRESHOLDS.get(domain, 3):
        print(f"🎓 GRADUATED: {skill}/{ftype} = {count}")
```

**配套**: 为 `FEEDBACK-INDEX.md` 提供初始模板 + 示例条目。

**实施难度**: 低

### 3.2 反馈毕业 → 提案生成的端到端测试

**问题**: 即使 feedback-analyzer.py 报告了"已毕业"的问题，EVOLUTION-RUNNER.md 要求手动生成提案 diff、人类确认后再写入。整个流程没有端到端验证。

**方向**: 创建 `.claude/hooks/test-steering-loop.sh`:
1. 在 `feedback/` 中放入 3 个相同的测试反馈（模拟毕业）
2. 运行 feedback-analyzer.py → 确认检测到毕业
3. 运行 evolution-runner（模拟）→ 确认生成提案文件
4. 人类确认 → 确认可以安全应用到 SKILL.md
5. 清理测试反馈

**实施难度**: 中（需要设计测试脚手架）

---

## 六、Phase 4: 状态一致性

### 4.1 L0→L2→L4 跨文件追溯验证

**问题**: `script-writer/exit-check.py` 已开始检查 L0→L2 追溯链（audience、KPI 对齐），但 dev track 完全没有类似检查。

- L2-spec.md 定义了 Business Goal 和 P0/P1/P2
- L4-plan.md 定义了 Phase 和 Feature-Phase Mapping
- 但 L4-plan.md 中的 Phase 0 是否覆盖了 L2-spec.md 中所有 P0 features？没有物理验证。

**方向**:
- 在 `dev-planner/exit-check.py` 中增加 L2→L4 对齐检查（P0 features 与 Phase 0 的映射完整性）
- 在 `product-spec-builder/exit-check.py` 中增加 L0→L2 对齐检查（如果 L0-strategy.md 存在）

**实施难度**: 低（正则提取 + 集合比较）

### 4.2 双轨运行时冲突检测

**问题**: 当一个项目同时进行 dev 和 content 工作时，L2-spec.md（dev）和 L2-content-spec.md（content）独立存在，但 Business Goal 可能冲突，没有检测机制。

**方向**: 在 `check-harness.py` 中新增可选的 `check_multi_track_consistency()`:

```python
def check_multi_track_consistency():
    if L2_SPEC.exists() and L2_CONTENT_SPEC.exists():
        dev_goal = extract_business_goal(L2_SPEC)
        content_goal = extract_business_goal(L2_CONTENT_SPEC)
        if dev_goal and content_goal and dev_goal != content_goal:
            add_issue("multi_track_goal_conflict", ...)
```

**实施难度**: 低

---

## 七、Phase 5: 扩展性

### 5.1 check-harness.py 和 router.py 的动态发现

**问题**:
- `check-harness.py` 的 `DEV_SKILLS`、`CONTENT_SKILLS`、`PM_SKILLS` 是硬编码列表
- `router.py` 的 `SKILL_INDEX` 是硬编码数组
- 新增一个 skill 需要修改两处

**方向**:
- `check-harness.py`: 改为从 `.claude/skills/{domain}/` 目录动态扫描子目录
- `router.py`: 改为从每个 skill 的 `SKILL.md` frontmatter 中读取 `triggers`，或从单独的索引文件读取

**实施难度**: 低

---

## 八、优先级排序

| 优先级 | 方向 | 预估工作量 | 影响范围 | 推荐里程碑 | 状态 |
|--------|------|-----------|---------|-----------|------|
| **P0** | 1.1 exit-check 代码质量标准化 | 2h | 17 个 exit-check | M5 | ✅ 已完成 |
| **P0** | 1.3 check-harness.py 深度检查 | 3h | check-harness.py | M5 | ✅ 已完成 |
| **P1** | 2.1 Creative Gate 记录验证 | 2h | 4-5 个 exit-check | M6 | ✅ 已完成 |
| **P1** | 3.1 feedback-analyzer.py | 2h | hooks/, feedback/ | M6 | ✅ 已完成 |
| **P1** | 4.1 L0→L2→L4 追溯验证 | 2h | dev-planner, product-spec-builder | M6 | ✅ 已完成 |
| **P2** | 1.2 exit-check 单元测试 | 6h | 新增 tests/ 目录 | M7 | ✅ 已完成 |
| **P2** | 2.2 Task Package 生成器 | 4h | 新增 package-task.py | M7 | ✅ 已完成 |
| **P2** | 2.3 进度仪表盘 | 4h | 新增 status-board.py | M7 | ✅ 已完成 |
| **P3** | 5.1 动态发现 | 2h | check-harness.py, router.py | M8 | ⬜ 待实施 |
| **P3** | 3.2 Steering Loop 端到端测试 | 3h | 新增 test-steering-loop.sh | M7 | ✅ 已完成 |
| **P3** | 4.2 双轨冲突检测 | 1h | check-harness.py | M8 | ⬜ 待实施 |

---

## 九、核心洞察：从"设计文档"到"物理系统"

当前 harness 最大的 gap 不是缺少功能，而是**设计意图和物理实现之间的断层**:

| 设计意图 | 当前实现 | 缺失的物理层 | M5-M6 修复状态 |
|---------|---------|-------------|---------------|
| Creative Gate 不可跳过 | 文档约定 | exit-check 不验证"人类确认痕迹" | ✅ M6: tts-engine/script-writer/visual-designer/frontend-slides 已增加 CG 记录验证 |
| Steering Loop 自动进化 | 文档约定 | 无 feedback-analyzer 脚本 | ✅ M6: feedback-analyzer.py 已上线 |
| Task Package 精确组装 | 手动复制粘贴 | 无自动化生成器 | ⬜ M7: package-task.py |
| PM 横切决策层 | Gate 定义在 CLAUDE.md | Orchestrator 行为无法验证 | ⬜ 长期 |
| L-state 一致性 | 文件分离 | 跨文件内容一致性无验证 | ✅ M5-M6: check_state_cross_reference() + L0→L2→L4 追溯验证已上线 |

**下一步最关键的动作**不是新增更多 Skill，而是**给现有设计增加物理 enforcement 层**——让每个"应该"变成"必须"，让每个"文档约定"变成"exit-check 验证"。

---

## 十、上下文恢复（给新 Session）

> 如果你是新 session，正在考虑优化 harness，按以下顺序阅读：
> 
> 1. `docs/PM-GATE-DESIGN.md` — 完整设计意图（PM Gate Points 架构、Spec Gap Protocol、State 文件定义）
> 2. `docs/PM-GATE-MILESTONES.md` — 已完成里程碑（M1-M4）和待实施里程碑（M5-M8）
> 3. **本文档** — 优化路径全景、优先级、核心洞察
> 4. `.claude/CLAUDE.md` — 当前运行时协议（确认 Gate 定义是否已写入）
> 5. 运行 `python3 .claude/check-harness.py` — 确认 harness 健康基线
> 
> 然后：选择一个 P0/P1 方向开始实施，完成后更新 `PM-GATE-MILESTONES.md`。

---

## 变更日志

| 日期 | 变更 | 作者 |
|------|------|------|
| 2026-04-19 | 初始创建：M4 完成后的系统性优化路径 | Session 6 |
| 2026-04-20 | M5 完成：exit-check 代码质量标准化 + check-harness.py 深度检查增强 | Session 7 |
| 2026-04-20 | M6 完成：Creative Gate 记录验证 + feedback-analyzer.py + L0→L2→L4 追溯验证 | Session 7 |
