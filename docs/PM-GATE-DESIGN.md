# PM Gate Points — 全生命周期 PM 把控设计文档

> **本文件是上下文持久化文档。** 任何新 session 只需阅读此文件即可完整理解 PM Gate Points 的设计意图、架构决策和实施细节。本文件由多个分析 session 贡献，是唯一的事实来源（Single Source of Truth）。

---

## 一、设计背景与动机

### 1.1 问题陈述

Reliable Dev Harness 当前的 PM 角色处理有根本性缺陷：

**PM 只在项目开始时出现（product-spec-builder），在整个开发/内容生产过程中消失了。** 这与现实世界 PM 的实际参与方式完全不符——真实 PM 在产品发现、设计、规划、实现、审查、发布和验证的每个阶段都有决策权威。

### 1.2 核心洞察

PM 本质是**决策权威**，不是**执行产出**。因此 PM 不应该是与 dev/content 平行的第三轨道，而是**横切所有轨道的决策层**：

```
❌ 错误模型：PM 作为平行轨道
skills/
├── dev/        ← 执行
├── content/    ← 执行
└── pm/         ← 也是执行？但 PM 不"执行"产品，PM "决策"产品方向

✅ 正确模型：PM 作为横切决策层
┌──────────────────────────────────────────────────────────┐
│                    PM Decision Layer                      │
│  G0: 需求验证 → G1: 方向确认 → G2: 范围把控 →            │
│  G3: 实现合规 → G4: 发布就绪 → G5: 效果验证              │
└──────────────────────────────────────────────────────────┘
      ↓ 产出           ↓ 产出           ↓ 产出
┌─────────────┐  ┌─────────────┐  ┌──────────────┐
│  dev track  │  │content track│  │  (future)    │
│  执行产出    │  │  执行产出    │  │              │
└─────────────┘  └─────────────┘  └──────────────┘
```

### 1.3 设计原则

1. **PM 是横切层**，不是独立轨道 — PM Gate Points 贯穿 dev 和 content
2. **每个 Gate 有明确的输入/输出/验收标准** — 不是模糊的"PM 参与"
3. **PM Enrichment Skills 从 pm-skills 注入**，不重新发明 — 利用 pm-skills 已有的决策框架
4. **Hard Gate 检查格式，Creative Gate 检查方向** — PM 决策涉及两者
5. **Spec Gap Protocol 是关键的"活"机制** — 实现过程中发现 spec 缺口时，PM 有明确的分类和升级路径
6. **设计意图必须在代码中可追溯** — 每个改动都应引用本文档中的相关章节

### 1.4 参考来源

- Marty Cagan《Empowered Product Teams》—— PM 负责业务可行性（Value Risk）
- Teresa Torres《Continuous Discovery》—— PM 通过 Product Trio 持续参与，不是前置参与
- Stage-Gate Model —— Gate 是协作检查点，不是 PM 独裁决策
- Scrum/Agile PO 模型 —— PO 拥有验收标准和 backlog 优先级

---

## 二、当前状态审计

### 2.1 Dev Track PM 决策缺口完整清单

| 阶段 | 当前 Skill | 显式 PM 决策 | 隐式 PM 决策（应显式） | 缺失的 PM 关注 |
|------|-----------|-------------|---------------------|--------------|
| **Spec** | product-spec-builder | Problem/User/Features/Metrics/Scope/Tradeoffs | Feature 数量(3-5)合理性、Out-of-Scope质量 | Metrics→业务目标挂钩、Feature→Problem对齐 |
| **Design** | design-brief-builder | 视觉风格问题(设计师) | 品牌调性方向(PM)、交互风格影响用户体验(PM)、平台选择影响覆盖率(PM) | 品牌规范引用、WCAG无障碍、用户画像关联 |
| **Planning** | dev-planner | Phase数量和划分 | Phase顺序=业务优先级(PM)、风险标志=业务风险(PM)、Library选择影响技术债务(PM) | Phase→Spec feature映射、MVP边界、timeline约束 |
| **Implementation** | dev-builder | 无 | Task scope 边界(PM)、Scope外需求升级路径(PM)、Refactor影响进度(PM) | Spec对齐检查、Feature flag策略、scope creep检测 |
| **Review** | code-review | Spec合规检查(Stage1) | Spec条目验证标准(谁定义"完成"？PM)、Extra scope处理(PM决定接受/拒绝)、Partial implementation是否接受(PM) | 每条spec item验证、scope creep标记、user impact评估 |
| **Bug Fix** | bug-fixer | 无 | Bug优先级=业务影响(PM)、修bug vs重构决策(PM)、3次重复→架构审视(PM) | Bug priority framework(MoSCoW)、业务影响映射、升级路径 |
| **Release** | release-builder | 无（⚠️ exit-check.py 是空占位符！） | Smoke test范围(PM定义关键路径)、回滚标准(PM定义错误率阈值)、监控时长(PM根据业务SLA)、Stakeholder通知(PM) | PM sign-off gate、go/no-go checklist |

### 2.2 Content Track PM 决策缺口完整清单

| 阶段 | 当前 Skill | 显式 Creative Gate | 隐式 PM 决策（应显式） | 缺失的 PM 关注 |
|------|-----------|-------------------|---------------------|--------------|
| **Script** | script-writer | G0: 平台/Mood/时长<br>G0a: 选题方向（topic 入口）<br>G0b: 参数确认（topic 入口）<br>G1: 场景拆分 | 内容主题适用性、目标受众定义、核心信息优先级、Hook有效性、CTA定义 | 品牌调性验证、KPI定义、差异化策略、合规检查 |
| **Visual** | visual-designer | G2a: 图片策略<br>G2b: Style Preview | 品牌视觉规范符合性、配图appropriateness、视觉层次结构、字幕区可读性 | 品牌指南引用、版权图片、文化敏感性、可访问性 |
| **TTS** | tts-engine | G4a-1: TTS风格（可跳过⚠️） | 声音品牌符合性、语速内容适配、发音准确性、音频一致性 | 背景音乐策略、音频质量标准、字幕格式规范 |
| **Video** | video-compositor | G4b: 最终视频确认 | End Card/CTA、片头片尾品牌、缩略图质量、字幕移动端可读性 | 发布元数据策略、UTM追踪、版权声明 |

### 2.3 跨轨道系统性缺口

| 缺口类别 | 描述 | 影响 |
|---------|------|------|
| **目标追溯链断裂** | L0(业务目标) → L2(spec) → L4(plan) 无目标追溯 | 无法验证"产出是否完成了最初目标" |
| **反馈分类缺 PM 类型** | FEEDBACK-OBSERVER 只有 dev 类型 | PM 问题被归类为 "other" |
| **Spec Gap Protocol 缺失** | 实现过程中发现 spec 模糊无升级路径 | 开发者自行决定 → scope drift |
| **Content 无 L0 策略层** | script-writer 没有业务目标和 KPI 输入 | 产出内容无法衡量效果 |
| **Content 无发布层** | video-compositor 后没有分发就绪检查 | 视频产出后不知道怎么发 |
| **release-builder exit-check 空** | 完全没有验证 | 最大安全漏洞 |

### 2.4 State 文件缺失字段

| State 文件 | 当前包含 | 缺失的 PM 字段 |
|-----------|---------|---------------|
| L1-summary.md | 项目目标、核心技术栈 | 项目阶段/状态、关键利益相关方、当前阶段成功标准 |
| L2-spec.md (dev) | Problem/User/Features/Metrics/Scope/Decisions | 业务目标链接、Feature 优先级(P0/P1/P2)、MVP边界定义、假设列表 |
| L2-spec.md (content) | Platform/Mood/Duration | 目标受众、业务目标、KPI定义、核心信息优先级、CTA |
| L3-design.md (dev) | Design tokens (颜色/字体/间距) | 品牌规范引用、可访问性标准、用户画像关联 |
| L3-design.md (content) | Mood/Style/Color/Font | 品牌调性引用、视觉层次结构、可访问性标准 |
| L4-plan.md | Phases/Deliverables/Dependencies | Phase 业务目标、P0/P1/P2 标记、风险标志(含业务风险)、MVP边界 |
| (新增) L0-strategy.md | 不存在 | 目标受众、业务目标、KPI、核心信息、差异化、合规要求 |
| (新增) L6-distribution.md | 不存在 | 发布平台、标题模板、描述/标签、UTM、版权、发布时间表 |
| (新增) L5-validation.md | 不存在 | Metrics baseline、30天目标、GO/PIVOT/KILL 决策框架 |

---

## 三、PM Gate Points 架构设计

### 3.1 三层架构总览

```
Layer 1: PM Gate Points (决策层 — 贯穿全生命周期)
─────────────────────────────────────────────────
     每个 Gate 是一个 PM 决策点，有明确的输入/输出/验收标准

Layer 2: PM Enrichment Skills (知识层 — 从 pm-skills 注入)
─────────────────────────────────────────────────
     从 pm-skills 提取的决策框架，注入到 Layer 1 的 Gate 中

Layer 3: Existing Execution Tracks (执行层 — dev/content 不变)
─────────────────────────────────────────────────
     现有的 Skill 链路不变，但在关键节点加入 PM Gate
```

### 3.2 Dev Track PM Gate Points 完整定义

#### G0: PM Discovery Gate — 产品发现与验证

```
时机: 产品spec生成之前（product-spec-builder 之后）
输入: 用户原始想法
PM 决策:
  1. 问题是否值得解决？→ problem-statement 框架
  2. 用户是谁？→ proto-persona 框架
  3. 成功指标如何量化？→ 务必与业务目标挂钩
  4. 优先级框架？→ prioritization-advisor 框架
  5. MVP 边界在哪里？
pm-skills 注入: problem-statement, proto-persona, prioritization-advisor
Hard Gate: 问题陈述量化、用户画像具体、指标可衡量、Out-of-Scope 存在
Creative Gate: 用户确认方向
产出: L2-spec.md（增强版，含 P0/P1/P2 和 MVP 边界）
```

#### G1: PM Direction Gate — 设计方向确认

```
时机: 设计spec生成时（design-brief-builder 之后）
输入: L2-spec.md
PM 决策:
  1. 设计方向是否与用户画像和业务目标一致？
  2. 配色/交互/动效是否影响性能或可访问性？
  3. 是否有品牌规范需要遵循？
pm-skills 注入: positioning-statement, user-story-mapping
Hard Gate: 设计规格引用了 brand guideline（或明确"无品牌约束"）
Creative Gate: 用户确认视觉方向
产出: L3-design.md（增强版，含品牌规范引用和可访问性声明）
```

#### G2: PM Scope Gate — 规划范围把控

```
时机: 开发计划生成时（dev-planner 之后）
输入: L2-spec + L3-design
PM 决策:
  1. Phase 划分是否反映业务优先级？
  2. MVP 边界在哪里？Phase 0 是否真的是最小可行产品？
  3. 每个 Phase 是否关联到 spec 的具体 feature？
pm-skills 注入: roadmap-planning, epic-hypothesis, lean-ux-canvas
Hard Gate: 每个 Phase 关联到 spec 的 feature + MVP 边界明确 + P0/P1/P2 标记存在
Creative Gate: 用户确认 MVP 范围和 Phase 顺序
产出: L4-plan.md（增强版，含 P0/P1/P2 和 MVP 标记）
```

#### G3: PM Compliance Gate — 实现合规审查

```
时机: 代码审查时（code-review Stage 1）
输入: 实现代码 + L2-spec + L3-design
PM 决策:
  1. 实现是否符合 spec？（Spec Compliance — 当前已有但不完整）
  2. 是否有 scope creep？（实现做了 spec 没有的功能）
  3. Extra scope 如何处理？（PM 决定接受/拒绝/延后）
PM 角色:
  - Stage 1 (Spec Compliance): PM 是 PRIMARY reviewer
  - Stage 2 (Code Quality): PM 不参与
Hard Gate: 每条 spec item 有验证结果 + 无 scope creep + HIGH issue 有 user impact 评估
Creative Gate: PM 确认实现"看起来对了"
产出: Review 通过或修复指示
```

#### G3b: PM Gap Protocol — Spec 缺口处理

```
时机: 实现过程中发现 spec 模糊或遗漏
触发: 开发者/Reviewer 发现 L2-spec 中没有覆盖到的情况
处理流程:
  A. "As intended, just undocumented"
     → PM 决定，文档补全到 L2-spec
  B. "Ambiguous spec"
     → PM + Designer 联合决定解释方式
  C. "Missing requirement"
     → PM 评估影响:
       * 小改（<20% story points）→ PM 在 OKR 内消化
       * 大改（≥20% story points）→ PM 升级到领导层
  D. "Strategic change needed"
     → PM 升级到领导层带推荐方案
记录: 所有缺口记录到 L4-plan.md 的 "Spec Gaps" section
```

#### G4: PM Release Gate — 发布就绪检查

```
时机: 所有 Phases 完成后（release-builder 之前）
输入: 所有 Phases 完成 + Review 通过
PM 决策:
  1. 所有 P0 功能是否已实现？
  2. Smoke test 是否覆盖关键路径？（由 PM 定义什么是"关键路径"）
  3. 回滚标准是什么？（错误率 > X%？用户影响 > Y？）
  4. 谁需要知道发布时间？（Stakeholder 通知）
  5. 监控是否就绪？需要关注哪些指标？
Hard Gate:
  - Smoke test 通过
  - 所有 P0 spec items 已实现
  - 回滚计划存在并已被 PM 确认
  - Monitoring 就绪
Creative Gate: PM 签字 "可以发布"（Go/No-Go 决策）
产出: Release checklist 签字（新增状态文件）
```

#### G5: PM Validation Gate — 效果验证

```
时机: 产品上线后 7 天和 30 天
输入: 产品已上线 + 监控数据 + Success Metrics baseline
PM 决策:
  1. Success Metrics 是否达到 L2-spec 中定义的目标？
  2. 是否需要迭代？
  3. 是否需要 Pivot？
pm-skills 注入: lean-ux-canvas（验证循环）, pol-probe（假设验证）
Hard Gate: 上线后 7/30 天检查 metrics 与 spec 对齐
Creative Gate: PM 决定 GO / PIVOT / KILL
产出: L5-validation.md（新增状态文件，含 metrics 结果和下一步决策）
```

### 3.3 Content Track PM Gate Points 完整定义

#### CG0: PM Content Strategy Gate — 内容策略验证

```
时机: 口播稿/主题输入时（script-writer 之前或内部）
输入: 原始主题/口播稿
PM 决策:
  1. 目标受众是谁？（年龄/兴趣/痛点）
  2. 业务目标是什么？（品牌认知/引流/转化）
  3. 如何衡量成功？（播放量/完播率/互动率/转化率）
  4. 核心信息优先级？（观众最该记住的一件事）
  5. 差异化策略？（与同类内容的区别）
  6. 合规要求？（广告法/行业规范）
Hard Gate: 目标受众 + 业务目标 + KPI 已定义
Creative Gate: 用户确认内容方向
产出: L0-strategy.md（新增状态文件）

补充: 当输入为 topic（无现成文稿）时，script-writer 内部包含 G0a（选题方向确认）和 G0b（平台/风格/力度确认）两个 Creative Gate。此时 CG0 与 G0a/G0b 的关系：
- CG0（pm/content-strategy）负责业务策略（受众、KPI、差异化）
- G0a/G0b（script-writer 内部）负责内容策略（选题、表达风格、平台规格）
- 如 L0-strategy.md 已存在，G0a/G0b 应参考其中的受众和 KPI 假设
```

#### CG1: PM Visual Direction Gate — 视觉方向确认

```
时机: visual-designer 风格选择时
输入: L2-spec (内容方向)
PM 决策:
  1. 视觉风格是否与品牌一致？
  2. 配色是否适合目标受众？
  3. 可访问性是否达标？
Hard Gate: Style Preview 包含品牌关键词引用
Creative Gate: 用户从 3 个预览中选择
产出: L3-design.md（增强版，含品牌规范引用）
```

#### CG2: PM Voice Direction Gate — 声音方向确认

```
时机: tts-engine 风格选择时（当前标记为"可跳过"⚠️，应改为不可跳过）
输入: L2-spec + L3-design
PM 决策:
  1. 声音是否符合品牌调性？
  2. 语速是否适合内容类型？
  3. 背景音乐策略？
Hard Gate: TTS 风格与 Mood 标签对齐
Creative Gate: 用户确认声音（不可跳过）
产出: L5-media.md（增强版，含声音品牌标记）
```

#### CG3: PM Final Review Gate — 最终审核

```
时机: video-compositor 完成后
输入: final-video.mp4
PM 决策:
  1. 最终视频是否传达了核心信息？
  2. CTA 是否有效？
  3. 品牌标识是否正确？
  4. 缩略图是否吸引人？
Hard Gate: 视频技术参数 + 时长合规 + CTA 存在
Creative Gate: 用户最终确认
产出: final-video.mp4（签字版）
```

#### CG4: PM Distribution Gate — 分发就绪检查

```
时机: 视频产出后（当前完全缺失）
输入: final-video.mp4
PM 决策:
  1. 发布平台和最佳时间？
  2. 标题/描述/标签策略？
  3. 是否需要 A/B 测试缩略图？
  4. UTM 追踪参数？
  5. 版权声明？
Hard Gate: 分发元数据完整（标题 + 描述 + 标签 + UTM）
Creative Gate: 用户确认发布时机
产出: L6-distribution.md（新增状态文件）
```

#### CG5: PM Content Validation Gate — 内容效果验证

```
时机: 内容发布后 7 天
输入: 发布数据 + KPI
PM 决策:
  1. KPI 是否达成？
  2. 是否需要修改视频重发？
  3. Steering Loop 反馈是否需要回到 script-writer？
产出: 内容迭代决策
```

---

## 四、PM Enrichment Skills 映射（Layer 2）

### 4.1 pm-skills → Gate 精准映射

| Gate | pm-skills 注入 | 注入方式 | 注入目标 |
|------|---------------|---------|---------|
| **G0: Discovery** | `problem-statement` + `proto-persona` + `prioritization-advisor` | Key Concepts 段落注入 | product-spec-builder SKILL.md |
| **G1: Direction** | `positioning-statement` + `user-story-mapping` | Key Concepts 段落注入 | design-brief-builder SKILL.md |
| **G2: Scope** | `roadmap-planning` + `epic-hypothesis` + `lean-ux-canvas` | Key Concepts 段落注入 | dev-planner SKILL.md |
| **G3: Compliance** | `prd-development`（验收标准段） | exit-check 增加 PM 合规 | code-review SKILL.md + exit-check.py |
| **G3b: Gap Protocol** | `problem-statement`（分析框架） | 新增 "Spec Gap Protocol" 段 | code-review SKILL.md |
| **G4: Release** | `press-release`（沟通模板） | Key Concepts 段落注入 | release-builder SKILL.md |
| **G5: Validation** | `pol-probe` + `lean-ux-canvas`（验证实验） | 新 Skill | pm/validation |
| **CG0: Strategy** | `discovery-interview-prep` + `positioning-workshop` | 新 Skill | pm/content-strategy |
| **CG4: Distribution** | 无直接对应（全新） | 新 Skill | pm/distribution-planner |
| **CG5: Validation** | `business-health-diagnostic`（指标评估） | 新 Skill | pm/content-validation |

### 4.2 注入方式说明

**注入方式不是复制 SKILL.md**，而是提取决策框架的关键要素：

1. **Key Concepts 注入**：将 pm-skills 的决策框架摘要写入对应 harness Skill 的 Key Concepts 段
   - 例如：`prioritization-advisor` 的 RICE/ICE/Kano 框架摘要写入 `product-spec-builder` 的 Key Concepts

2. **exit-check 增强**：在已有 exit-check.py 中增加 PM 决策质量的 warning 级别检查
   - 例如：`product-spec-builder` exit-check 增加 feature priority 检查

3. **Creative Gate 定义**：在 SKILL.md 的 Application 段增加 Creative Gate 说明
   - 例如：`design-brief-builder` 增加 "PM Direction Gate: 确认设计方向与业务目标一致"

4. **State 文件模板增强**：在 L0-L5 模板中增加 PM 相关字段
   - 例如：L2-spec.md 增加"业务目标"和"假设列表"字段

---

## 五、Spec Gap Protocol（Spec 缺口处理协议）

### 5.1 缺口分类

当实现过程中发现 L2-spec 模糊或遗漏时：

| 类型 | 描述 | 决策者 | 处理方式 |
|------|------|--------|---------|
| **A: As Intended** | 功能确实在 spec 中，只是描述不够详细 | PM | 补全文档到 L2-spec |
| **B: Ambiguous** | spec 有相关描述但含义不明确 | PM + Designer | 联合决定解释方式，更新 spec |
| **C: Missing (Small)** | spec 缺少需求，但影响 <20% story points | PM | 在 OKR 范围内消化，更新 spec 和 plan |
| **D: Missing (Large)** | spec 缺少需求，影响 ≥20% story points | PM → 领导层 | 升级到领导层，带推荐方案 |
| **E: Strategic Change** | 实现过程中发现需要战略方向调整 | PM → 领导层 | 升级到领导层 |

### 5.2 缺口记录格式

所有缺口记录到 L4-plan.md 的 "Spec Gaps" section：

```markdown
## Spec Gaps

### GAP-001: {简短描述}
- **Type**: A/B/C/D/E
- **Discovered by**: {Agent/Role}
- **Discovered at**: {Phase/Task}
- **Decision**: {决策内容}
- **Impact**: {影响范围}
- **Status**: Open/Resolved/Deferred
```

---

## 六、FEEDBACK-OBSERVER 增强

### 6.1 新增 PM 反馈类型

当前类型：
```yaml
type: [missing-test | wrong-approach | scope-creep | ui-mismatch | doc-missing | other]
```

增强后类型：
```yaml
type: [
  # 原有 Dev 类型
  missing-test | wrong-approach | scope-creep | ui-mismatch | doc-missing |
  # 新增 PM 类型
  user-persona-change |   # 目标用户变了
  metric-recalibration |   # 指标需要重新定义
  priority-shift |         # 优先级变化
  scope-expansion |        # 范围扩大（vs scope-creep 是失控的扩大）
  spec-gap |               # Spec 缺口（对应 Gap Protocol）
  validation-failure |     # G5/CG5 上线后 metrics 不达标
  other
]
```

### 6.2 PM 反馈毕业阈值

```yaml
# Dev 类型：≥3 次同类反馈 → 生成提案
# PM 类型：≥2 次同类反馈 → 生成提案（PM 决策更敏感，需要更快响应）
# Content 类型：≥5 次同类反馈（当前，保持不变）
```

---

## 七、State 文件模板增强

### 7.1 新增 L0-strategy.md（Content Track）

```markdown
# Content Strategy: {Project Name}

## Business Goal
{这条内容要达成的业务目标：品牌认知/引流/转化}

## Target Audience
{年龄/兴趣/痛点/消费场景}

## Success KPI
{播放量目标/完播率目标/互动率目标/转化率目标}

## Core Message
{最想让观众记住的一件事}

## Differentiation
{与同类内容的区别}

## Compliance
{特殊合规要求：广告法/行业规范/版权}
```

### 7.2 L2-spec.md 增强字段（Dev Track）

在现有模板底部增加：

```markdown
## Business Goal
{本产品/功能要达成的业务目标，与公司战略的关联}

## Assumptions
{列出关键假设，每个假设标注验证状态}

## Feature Priority
### P0 (MVP — Must Have)
- {feature} — {user outcome}

### P1 (Should Have)
- {feature} — {user outcome}

### P2 (Nice to Have)
- {feature} — {user outcome}

## MVP Boundary
**In MVP (Phase 0):** {列出 MVP 必须包含的功能}
**Post MVP (Phase 1+):** {列出 MVP 之后的扩展功能}
```

### 7.3 新增 L5-validation.md（Dev Track）

```markdown
# Validation Report: {Project Name}

## Metrics Baseline (at launch)
| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| {metric1} | {target1} | {actual1} | {status1} |

## 7-Day Check
{上线后 7 天的 metrics 与 target 对齐情况}

## 30-Day Check
{上线后 30 天的 metrics 与 target 对齐情况}

## Decision
- [ ] GO: Metrics 达标，继续当前方向
- [ ] PIVOT: Metrics 部分达标，需要调整
- [ ] KILL: Metrics 未达标，需要停止或重新开始

## Next Steps
{基于决策的下一步行动计划}
```

### 7.4 新增 L6-distribution.md（Content Track）

```markdown
# Distribution Plan: {Video Title}

## Platform & Timing
| Platform | Optimal Time | Account |
|----------|-------------|---------|
| {platform1} | {time1} | {account1} |

## Title & Description
- **Title**: {视频标题}
- **Description**: {视频描述模板}
- **Tags**: {标签列表}

## Tracking
- **UTM Parameter**: {UTM 追踪链接}
- **KPI Tracking**: {KPI 监控方式}

## Compliance
- **Music License**: {音乐版权信息}
- **Image Rights**: {图片版权信息}
- **Content Rating**: {内容分级}

## Thumbnails
- **Option A**: {缩略图描述或文件路径}
- **Option B**: {缩略图描述或文件路径}
- **Option C**: {缩略图描述或文件路径}
```

---

## 八、exit-check.py 增强设计

### 8.1 product-spec-builder/exit-check.py — 增加 PM 决策质量警告

```python
# 新增：PM 决策质量检查（warning 级别，不阻断）

def check_decision_quality(spec_content):
    checks = []
    # 1. Feature 优先级标记
    if not re.search(r'P[0-2]|优先级|priority|MVP|Must Have', spec_content, re.IGNORECASE):
        checks.append(ReportItem(
            code="features_not_prioritized",
            detail="Core Features 缺少优先级排序（P0/P1/P2 或 Must/Should/Nice）",
            level="warning"
        ))
    # 2. 假设标注
    if not re.search(r'假设|assumption|hypothesis', spec_content, re.IGNORECASE):
        checks.append(ReportItem(
            code="no_stated_assumptions",
            detail="Spec 没有标注假设。考虑使用 discovery-interview-prep 验证关键假设",
            level="warning"
        ))
    # 3. MVP 边界
    if not re.search(r'MVP|最小可行|v1|phase.?0|Must Have', spec_content, re.IGNORECASE):
        checks.append(ReportItem(
            code="no_mvp_boundary",
            detail="没有 MVP 边界。Core Features 是否都需要在第一版交付？",
            level="warning"
        ))
    # 4. 业务目标关联
    if not re.search(r'业务目标|business.goal|objective|OKR', spec_content, re.IGNORECASE):
        checks.append(ReportItem(
            code="no_business_goal",
            detail="Spec 缺少业务目标关联。Success Metrics 应与公司战略挂钩",
            level="warning"
        ))
    return checks
```

### 8.2 release-builder/exit-check.py — 从空占位符实现为完整验证

```python
#!/usr/bin/env python3
"""Release Builder Exit Check — PM Release Gate"""

import sys
from pathlib import Path

def check_release_readiness():
    project_root = Path(__file__).resolve().parent.parent.parent.parent
    state_dir = project_root / "state"
    checks = []
    
    # 1. 所有 P0 features 已实现
    l2_spec = state_dir / "L2-spec.md"
    if l2_spec.exists():
        spec_content = l2_spec.read_text()
        p0_features = re.findall(r'P0.*?—.*?$', spec_content, re.MULTILINE | re.IGNORECASE)
        if p0_features and "MVP" in spec_content:
            checks.append(ReportItem(
                code="p0_features_listed",
                detail=f"Found {len(p0_features)} P0 features",
                level="info"
            ))
    
    # 2. Smoke test 通过（需要项目特定命令）
    # TODO: 自动检测项目类型的 smoke test
    
    # 3. 回滚计划存在
    rollback_doc = project_root / "ROLLBACK.md"
    if not rollback_doc.exists():
        # 也检查 L4-plan 中是否有回滚信息
        l4_plan = state_dir / "L4-plan.md"
        if l4_plan.exists():
            plan_content = l4_plan.read_text()
            if not re.search(r'rollback|回滚|revert', plan_content, re.IGNORECASE):
                checks.append(ReportItem(
                    code="no_rollback_plan",
                    detail="No rollback plan found in ROLLBACK.md or L4-plan.md",
                    level="high"
                ))
    
    # 4. 任务历史完整
    task_history = state_dir / "task-history.yaml"
    if not task_history.exists():
        checks.append(ReportItem(
            code="no_task_history",
            detail="task-history.yaml not found — cannot verify all tasks completed",
            level="warning"
        ))
    
    # 检查是否有 high 级别的问题
    high_issues = [c for c in checks if c.level == "high"]
    if high_issues:
        print("❌ Release Gate FAILED:")
        for c in checks:
            print(f"  [{c.level.upper()}] {c.code}: {c.detail}")
        sys.exit(1)
    else:
        print("✅ Release Gate PASSED")
        for c in checks:
            print(f"  [{c.level.upper()}] {c.code}: {c.detail}")
        sys.exit(0)
```

### 8.3 code-review/exit-check.py — 增加 Spec 合规量化检查

```python
# 新增：PM Spec Compliance 量化检查

def check_spec_coverage(review_content, spec_content):
    checks = []
    # 1. 每条 spec item 是否有验证结果
    spec_items = re.findall(r'[-*]\s+\*\*.*?\*\*', spec_content)
    if spec_items and len(spec_items) > 3:
        for item in spec_items:
            if item.strip() not in review_content:
                checks.append(ReportItem(
                    code="spec_item_not_verified",
                    detail=f"Spec item not verified in review: {item[:50]}...",
                    level="warning"
                ))
    # 2. Scope creep 检测
    if re.search(r'[Ee]xtra [Ss]cope|超出规格|额外功能', review_content, re.IGNORECASE):
        checks.append(ReportItem(
            code="potential_scope_creep",
            detail="Review mentions extra scope beyond spec — PM should confirm whether to accept",
            level="warning"
        ))
    # 3. HIGH issue 是否有 user impact 评估
    high_issues = re.findall(r'HIGH.*?(?:\n|$)', review_content, re.IGNORECASE)
    for issue in high_issues:
        if not re.search(r'user.impact|用户影响|frontend|UX', issue, re.IGNORECASE):
            checks.append(ReportItem(
                code="high_issue_no_user_impact",
                detail=f"HIGH issue without user impact assessment: {issue[:80]}...",
                level="warning"
            ))
    return checks
```

---

## 九、CLAUDE.md 增强设计

在 CLAUDE.md 的"不可协商的铁律"之后增加：

```markdown
## PM Decision Points (产品决策点)

以下时刻需要 PM 决策，Orchestrator 必须在此暂停并请求用户确认：

### Dev Track PM 决策点
1. **G0: PM Discovery Gate** — product-spec-builder 输出后
   - Feature 选择、Scope 边界、Metrics 定义、MVP 边界、优先级排序
2. **G1: PM Direction Gate** — design-brief-builder 输出后
   - 设计方向与业务目标一致性确认
3. **G2: PM Scope Gate** — dev-planner 输出后
   - Phase 划分与业务优先级对齐、MVP 范围确认
4. **G3: PM Compliance Gate** — code-review Stage 1
   - Spec 条目验证、scope creep 检测、user impact 评估
5. **G3b: PM Gap Protocol** — 实现过程中发现 spec 缺口时
   - 缺口分类(A/B/C/D/E) → 对应决策和升级路径
6. **G4: PM Release Gate** — release-builder 之前
   - Go/No-Go 决策、Smoke test 范围确认、回滚标准确认
7. **G5: PM Validation Gate** — 上线后 7/30 天
   - Metrics 与 spec 对齐验证、GO/PIVOT/KILL 决策

### Content Track PM 决策点
8. **CG0: PM Content Strategy Gate** — script-writer 之前
   - 目标受众、业务目标、KPI、核心信息差异化
9. **CG1: PM Visual Direction Gate** — visual-designer 风格选择时
   - 品牌调性确认、可访问性
10. **CG2: PM Voice Direction Gate** — tts-engine 风格选择时
    - 声音品牌确认（不可跳过）
11. **CG3: PM Final Review Gate** — video-compositor 之后
    - 最终视频确认、CTA 有效性
12. **CG4: PM Distribution Gate** — 发布前
    - 分发元数据、UTM 追踪、版权
13. **CG5: PM Content Validation Gate** — 发布后 7 天
    - KPI 达标、内容迭代决策

### Spec Gap Protocol
当实现过程中发现 L2-spec 模糊或遗漏时：
- A类（补充文档）: PM 决定，补全 spec
- B类（歧义解释）: PM + Designer 联合决定
- C类小（<20%影响）: PM 在 OKR 内消化
- C类大（≥20%影响）: PM 升级到领导层
- D类（战略变更）: PM 升级到领导层带推荐方案
```

---

## 十、里程碑实施计划

### M1: 基础加固（P0 — 修复安全漏洞 + 显式化 PM 角色）

**目标**: 修复 release-builder 空占位符，显式化所有隐式 PM 决策点

| 任务 | 修改文件 | 验收标准 |
|------|---------|---------|
| 1.1 实现 release-builder/exit-check.py | `exit-check.py` | 运行后能验证 smoke test、回滚计划、task-history |
| 1.2 CLAUDE.md 增加 PM Decision Points 段 | `CLAUDE.md` | 包含完整的 G0-G5 + CG0-CG5 定义 |
| 1.3 FEEDBACK-OBSERVER.md 增加 PM 反馈类型 | `FEEDBACK-OBSERVER.md` | 新增 5 个 PM 类型 + 毕业阈值调整 |
| 1.4 本设计文档写入项目 | `docs/PM-GATE-DESIGN.md` | 文件存在于 `docs/`（开发者文档区，非 `.claude/docs/`） |

**M1 完成后**: harness 仍然能正常运行，但现在已经显式化了所有 PM 决策点。任何新 session 读 CLAUDE.md 就能理解 PM 决策发生在哪里。

### M2: Spec 增强（P1 — 提升 PM 决策质量基础设施）

**目标**: 增强 State 文件和 exit-check，建立目标追溯链

| 任务 | 修改文件 | 验收标准 |
|------|---------|---------|
| 2.1 product-spec-builder 增加 Entry Modes | `SKILL.md` | 支持 Guided/Context dump/Best guess 三种模式 |
| 2.2 L2-spec.md 模板增加 PM 字段 | `L2-spec.md` | 含业务目标、假设列表、P0/P1/P2、MVP边界 |
| 2.3 L3-design.md 模板增加品牌规范引用 | `L3-design.md` | 含品牌规范引用字段、可访问性声明 |
| 2.4 L4-plan.md 模板增加 PM 字段 | `L4-plan.md` | 含业务目标、优先级标记、风险标志 |
| 2.5 product-spec-builder exit-check 增加 PM 警告 | `exit-check.py` | 检测 missing prioritization、no MVP boundary、no business goal |
| 2.6 新增 L0-strategy.md 模板 | `L0-strategy.md` | 内容策略验证模板 |
| 2.7 新增 L6-distribution.md 模板 | `L6-distribution.md` | 分发就绪检查模板 |

**M2 完成后**: PM 决策的数据基础建好了——每个 Gate 都有对应的 State 文件字段承载 PM 决策。

### M3: PM Gate 验证增强（P2 — 让 Gate 真正把关）

**目标**: 安装 PM Gate 的 Hard Gate 检查机制

| 任务 | 修改文件 | 验收标准 |
|------|---------|---------|
| 3.1 code-review exit-check 增加 spec compliance 量化 | `exit-check.py` | 检查每条 spec item 有验证结果、检测 scope creep |
| 3.2 dev-planner exit-check 增加 Phase→Spec 映射 | `exit-check.py` | 每个 Phase 关联到 Spec 的 feature |
| 3.3 design-brief-builder exit-check 增加品牌验证 | `exit-check.py` | 检查品牌规范引用存在（或明确"无品牌约束"） |
| 3.4 Spec Gap Protocol 写入 code-review SKILL.md | `SKILL.md` | 包含 A/B/C/D/E 分类和升级路径 |
| 3.5 Content track L0 Content Strategy Gate 定义 | `CLAUDE.md` | CG0 的输入/输出/验收标准 |
| 3.6 tts-engine Creative Gate 改为不可跳过 | `SKILL.md` | G4a-1 标注为必选 |

**M3 完成后**: PM Gate 不只是"概念上的决策点"了——有 exit-check 在物理上验证每个 Gate 的条件。

### M4: PM Enrichment（P3 — 从 pm-skills 注入决策框架）

**目标**: 将 pm-skills 的 PM 决策框架注入到对应 Skill，创建新 Skill
**状态**: ✅ 已完成

| 任务 | 修改文件 | 验收标准 | 状态 |
|------|---------|---------|------|
| 4.1 product-spec-builder Key Concepts 注入 pm-skills 框架 | `SKILL.md` | 含 problem-statement + proto-persona + prioritization-advisor 框架摘要 | ✅ |
| 4.2 design-brief-builder Key Concepts 注入 pm-skills 框架 | `SKILL.md` | 含 positioning-statement + user-story-mapping 框架摘要 | ✅ |
| 4.3 dev-planner Key Concepts 注入 pm-skills 框架 | `SKILL.md` | 含 roadmap-planning + epic-hypothesis + lean-ux-canvas 框架摘要 | ✅ |
| 4.4 新建 pm/validation Skill | `SKILL.md` + `exit-check.py` | G5 验证 Skill | ✅ |
| 4.5 新建 pm/content-strategy Skill | `SKILL.md` + `exit-check.py` | CG0 内容策略 Skill | ✅ |
| 4.6 新建 pm/distribution-planner Skill | `SKILL.md` + `exit-check.py` | CG4 分发规划 Skill | ✅ |
| 4.7 新建 pm/content-validation Skill | `SKILL.md` + `exit-check.py` | CG5 内容验证 Skill | ✅ |
| 4.8 router.py 增加 pm/ 域路由 | `router.py` | 支持 `--domain pm` 过滤 | ✅ |
| 4.9 check-harness.py 增加 PM 域检查 | `check-harness.py` | 三域健康检查 | ✅ |

**M4 实际交付与设计的差异**：

| 任务 | 设计 | 实际交付 | 差异说明 |
|------|------|---------|---------|
| 4.4 pm/validation | pol-probe + lean-ux-canvas（验证实验） | GO/PIVOT/KILL 决策框架 + Lean UX 验证实验 + pol-probe 结构化探测 | 增加了 GO/PIVOT/KILL 三级决策，更实用 |
| 4.5 pm/content-strategy | discovery-interview-prep + positioning-workshop | Discovery Interview + Positioning Workshop 框架摘要 + 6 战略决策问题 | 合并为统一的 Content Strategy Compass |
| 4.6 pm/distribution-planner | 无直接对应（全新） | 分发计划 5 维框架 + 平台元数据需求表 + UTM 追踪 | 完全新建 |
| 4.7 pm/content-validation | business-health-diagnostic（指标评估） | Iterate/Refresh/Retire 三级决策 + Business Health Diagnostic 表格 + Steering Loop 连接 | 增加了内容专用决策框架 |

**M4 完成后**: PM 决策层完整了——有 pm/ 域的 Skill 提供方法论，有 exit-check 提供验证，有 Gate Points 提供决策点。

---

## 十一、上下文恢复指南（给新 Session）

> **如果你是新 session，正在恢复上下文，请阅读以下步骤：**

1. **阅读本文档** (`docs/PM-GATE-DESIGN.md`) — 这是唯一的事实来源
2. **阅读** `docs/PM-GATE-MILESTONES.md` — 了解当前完成了哪些里程碑
3. **阅读** `.claude/CLAUDE.md` — 确认 PM Decision Points 段是否已写入（M1 完成标志）
4. **检查 State 文件** — 查看 `.claude/state/` 中 L0-L6 模板是否已增强（M2 完成标志）
5. **继续执行** — 从当前里程碑的下一个未完成任务开始

> ⚠️ **角色区分**: `docs/` 是开发者文档（你），`.claude/docs/` 是运行时文档（harness 用户）。不要混淆。

**关键上下文要点**：
- PM 是横切决策层，不是平行执行轨道
- 每个 Gate 有 Hard Gate（格式验证）+ Creative Gate（方向确认）
- pm-skills 的决策框架通过 Key Concepts 注入，不重新发明
- Spec Gap Protocol 有 A/B/C/D/E 五级分类
- FEEDBACK-OBSERVER 增加了 PM 反馈类型
- release-builder/exit-check.py 之前是空占位符，需要实现

---

## 变更日志

| 日期 | 变更 | 作者 |
|------|------|------|
| 2026-04-17 | 初始创建：完整的 PM Gate Points 设计文档 | Session 1 |
| 2026-04-17 | 迁移：从 `.claude/docs/` 移到 `docs/`（区分开发者文档和运行时文档） | Session 1 |
| 2026-04-17 | AGENTS.md 增加角色区分指引（👷开发者 vs 🏃运行时用户） | Session 1 |