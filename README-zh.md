# Reliable Dev Harness

双轨道产品开发框架，融合**规格驱动的 Skill 设计**与**硬门工程纪律**。同时支持软件开发和内容生产（口播视频）。

[English](README.md)

## 核心理念

> Vibe Coding 失败的原因不是模型不够聪明，而是**模型周围没有系统**。

这套 Harness 提供：
- **引导（前馈控制）**：在 Agent 行动之前，注入方法论、验收标准和反模式
- **传感（反馈控制）**：确定性脚本（exit-check.py）在行动之后物理阻断不合格输出
- **方向盘（进化层）**：反馈积累成提案，但**必须人类确认**才能改规则
- **上下文防火墙（执行隔离）**：每个 Sub-Agent 都是全新实例，不继承历史

## 快速上手

### 第一步：安装到你的项目

```bash
# 方式 A：直接复制（推荐给已有项目）
cp -r /path/to/harness-video-generator/.claude /your/project/

# 方式 B：用初始化脚本
cd /your/project
/path/to/harness-video-generator/scripts/init-harness.sh .

# 验证安装
python3 .claude/check-harness.py
# → ✅ Harness health check passed. Both dev/ and content/ domains are intact.
```

### 第二步：使用开发轨道（软件开发）

在你的项目里跟 Claude Code 对话。Orchestrator 会读取 `CLAUDE.md` 并自动路由：

```text
你说: "我要做一个用户认证系统"

Claude 自动执行：
  1. 路由到 dev/product-spec-builder → 写需求规格 → 运行 exit-check.py
  2. exit-check 不通过 → 阻断，必须修复
  3. exit-check 通过 → Creative Gate：你确认需求规格
  4. 路由到 dev/design-brief-builder → 写设计简报 → exit-check
  5. → 设计稿 → 开发计划 → 实现 → 代码审查 → 发布
  6. 每步 exit-check.py 不通过 = 物理阻断
```

**你做**：确认规格、做设计决策、审查质量。
**Harness 做**：强制执行流程、运行验证、阻断不合格的工作。

### 第三步：使用内容轨道（口播视频生产）

```text
你说: "帮我把这个口播稿做成短视频"

Claude 自动执行：
  1. 路由到 content/script-writer → 解析文稿 → scenes.json
  2. Hard Gate：验证 JSON 结构（文件存在、字段完整、场景数量 2-15）
  3. Creative Gate：你确认平台（9:16/16:9/4:5）、Mood、场景拆分
  4. 路由到 content/visual-designer → 生成 HTML 幻灯片
  5. Creative Gate：你在 3 个 Style Preview 中选择
  6. 路由到 content/tts-engine → 生成音频 + 字幕
  7. 路由到 content/video-compositor → 渲染最终视频
  8. Creative Gate：你确认最终视频质量
```

**你做**：选平台/风格、确认场景、批准质量。
**Harness 做**：生成资产、验证输出、确保流水线一致性。

### 第四步：CLI 工具（可选）

```bash
# 看看请求会路由到哪个 Skill
python3 .claude/router.py "做登录页面"
# → dev/dev-builder

python3 .claude/router.py "制作口播视频" --domain content
# → content/script-writer

# 验证某个 content skill 的产出
python3 .claude/skills/content/script-writer/exit-check.py
# → ❌ [file_missing] scenes.json does not exist
# → ✅ script-writer exit check passed

# 健康检查
python3 .claude/check-harness.py
# → ✅ Harness health check passed
```

## 目录结构

📊 [查看架构图](architecture.svg) | [交互式版本](architecture.html)

```
.claude/
├── CLAUDE.md                          # 调度协议（双域路由 + PM 决策门）
├── router.py                          # Skill 匹配器（--domain 过滤）
├── check-harness.py                   # 双轨健康检查
│
├── skills/
│   ├── dev/                           # 软件开发域
│   │   ├── product-spec-builder/      #   需求 → L2-spec [G0 PM 发现门]
│   │   ├── design-brief-builder/      #   设计简报 → L3-design [G1 PM 方向门]
│   │   ├── design-maker/              #   设计稿生成
│   │   ├── dev-planner/               #   开发规划 → L4-plan [G2 PM 范围门]
│   │   ├── dev-builder/               #   代码实现
│   │   ├── bug-fixer/                 #   缺陷修复
│   │   ├── code-review/               #   两阶段代码审查 [G3 PM 合规门 + Spec缺口协议]
│   │   └── release-builder/           #   发布打包 [G4 PM 发布门]
│   │
│   └── content/                        # 内容生产域
│       ├── script-writer/             #   口播文稿 → scenes.json + L2-spec [CG0]
│       ├── visual-designer/           #   场景 → HTML 幻灯片 [CG1 视觉方向门]
│       ├── tts-engine/                #   语音合成 → audio/ + subtitles.json [CG2 声音方向门 - 不可跳过]
│       └── video-compositor/          #   视频合成 → final-video.mp4 [CG3 最终审核门]
│
├── hooks/                              # 传感层
│   ├── pre-commit-check.sh            #   开发域
│   ├── stop-gate.sh                   #   开发域
│   └── content-validator.sh           #   内容域
│
├── state/                              # 层级上下文（L0-L6）
│   ├── L0-strategy.md                #   内容策略（业务目标、受众、KPI）
│   ├── L1-summary.md                  #   项目概览（共享）
│   ├── L2-spec.md                     #   开发: 需求规格 / 内容: 内容规格
│   ├── L3-design.md                   #   开发: 设计简报 / 内容: 视觉规格
│   ├── L4-plan.md                     #   开发: 开发计划 / 内容: 流水线进度
│   ├── L5-media.md                   #   内容: 媒体资产清单
│   └── L6-distribution.md             #   分发计划（平台、时间、UTM、合规）
│
├── feedback/                           # 方向盘输入
├── agents/                             # Sub-Agent 角色定义
│   ├── IMPLEMENTER.md
│   ├── REVIEWER.md
│   ├── FEEDBACK-OBSERVER.md           #   PM/内容/开发 反馈类型（三域毕业阈值）
│   └── EVOLUTION-RUNNER.md
│
└── docs/
    ├── HARNESS-ARCHITECTURE.md         #   架构文档（双轨）
    ├── EVOLUTION-PROTOCOL.md           #   方向盘协议
    └── CONTENT-PIPELINE.md             #   内容生产流程
```

## 双轨道系统

### 开发轨道（软件开发）

```
想法 → product-spec-builder → design-brief-builder → design-maker
  → dev-planner → dev-builder → code-review → release-builder
  [Hard Gate: exit-check.py 每步验证]
  [PM 决策门: G0→G1→G2→G3+G3b→G4→G5 每步需要人类决策]
```

### 内容轨道（口播视频）

```
口播稿 → script-writer → visual-designer → tts-engine → video-compositor
  [Hard Gate: exit-check.py] + [Creative Gate: 人类确认]
  [PM 决策门: CG0→CG1→CG2→CG3→CG4→CG5 每步需要人类决策]
```

内容轨道使用**双网关**：确定性脚本验证（Hard Gate）+ 人类判断点（Creative Gate）。

## 关键设计决策

1. **每个 Skill 都有 exit-check.py**
   自然语言规则不可靠。`exit-check.py` 是物理门。

2. **方向盘有 Human Gate**
   `evolution-runner` 只能生成提案，不能直接改规则文件。

3. **设计图 > 设计简报 > 需求规格**（开发轨道）
   视觉歧义杀死 UI 质量。设计稿是唯一无歧义的 Source of Truth。

4. **Hard Gate + Creative Gate**（内容轨道）
   确定性检查（文件存在、JSON 有效）+ 人类判断（好看吗？）。Creative Gate 默认不可跳过。

5. **Sub-Agent 上下文防火墙**
   每个任务是全新实例。状态只通过 `.claude/state/` 文件传递。

6. **领域感知路由**
   `router.py` 支持 `--domain dev|content` 限制路由到特定领域。领域不确定时，Orchestrator 会问你。

## 不可协商的规则

- Exit Code ≠ 0 = **停**。没有例外。
- 代码变更必须经过 `code-review` 才能提交。
- 规则升级必须人类确认。
- UI 变更必须同步设计稿。
- 内容轨道的 Creative Gate 默认不可跳过。
- 内容 Steering Loop 毕业阈值：≥5 次同类反馈（开发 ≥3 次）。

## 致谢

- **Product-Manager-Skills** (deanpeters) - 规格驱动的 Skill 设计和标准化
- **self-media-video** - 内容流水线逻辑（已迁移到 content/ skills）
