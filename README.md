# requirement-assistant

一个“需求分析助手”skill 资源包：把截图/原型/会议纪要/PRD 片段等混合需求材料，按 **plan-first**（先意图→再计划→整理待确认项→确认→执行→校验）流程整理成结构化需求产物，并提供 **严格 JSON Schema + 本地校验脚本**，方便给 GPT/Codex 或下游自动化管道使用。

> 这不是一个可直接运行的产品（没有内置模型调用、没有 Web UI/服务端）；它提供的是 **流程规范、模板、schema 和校验工具**。

安装说明见 [INSTALL.md](INSTALL.md)。

---

## 功能介绍（What it does）

### 1) Plan-first 需求工作流（skill）

入口：`SKILL.md`

核心原则：
- **先澄清意图与范围**：目标产物是什么（PRD / issue-report / 功能清单 / 测试点 / 严格 JSON）
- **先出执行计划**：列输入清单、识别结果、步骤、待确认项、推荐动作
- **分层整理待确认项**：优先区分“必须确认项”“建议优化项”“可后续确认项”，避免把所有问题都当成同级阻塞
- **确认闸门**：用户确认后才生成长文/结构化产物
- **可校验**：需要机器可读时输出严格 JSON，并本地校验

### 2) 三类严格输出 Schema（machine-readable）

位置：`schemas/`

- `issue-report`：适合“扫描/检查/风险识别”，输出缺失/冲突/歧义/覆盖缺口
- `prd-bundle`：适合“生成型交付物”，输出 PRD 草稿 + 功能点 + 测试点 + 用例草稿
- `requirement-package`：适合“全量分析包”，包含识别摘要、结构化模型、问题清单、待确认项、以及可选产物

最小合法样例：`examples/*.min.json`

### 3) 本地工具：bootstrap & validate

位置：`scripts/`
- `scripts/bootstrap_output.py`：生成各 schema 的“空骨架”JSON
- `scripts/validate_output.py`：对 JSON 做本地校验（实现的是 JSON Schema 的子集校验器）

### 4) Windows 最小命令入口（CLI wrapper）

入口：`ra.ps1`

它是对现有 `scripts/*.py` 的薄封装，提供统一命令与退出码，便于本地/CI 使用。

---

## 当前支持的情况（Supported）

### 支持的输入材料类型（作为 skill 使用时）

- 原型/页面截图、交互截图
- 页面说明、字段说明、流程描述
- PRD 片段、会议纪要、需求碎片化文本
- 中英混合材料（默认以中文输出更自然）

> 注意：仓库本身不包含“截图解析器”或“模型调用器”，通常由对话式助手（GPT/Codex）来读图/读文并按 schema 输出。

### 支持的输出产物类型

- `issue-report`（结构化问题扫描：missing/conflict/ambiguous/coverage-gap）
- `prd-bundle`（结构化 PRD 草稿 + 功能点 + 测试点 + 用例草稿）
- `requirement-package`（全量分析包）

### 校验支持

- 支持对上述三类 JSON 输出做本地校验（见“Quick Start”）

---

## 限制与已知风险（Limitations）

- `scripts/validate_output.py` 是 **JSON Schema 子集**校验器：它覆盖常用的 `type/enum/required/items/$ref` 等，但不等同于完整 Draft 2020-12 实现。
- 本仓库不内置：
  - OpenAI API 调用
  - 线上服务部署
  - UI（Web/桌面）
  - 需求知识库/持久化存储

---

## Quick Start（Windows）

### 环境要求

- PowerShell
- Python 3（命令为 `python`）

## 安装为 Codex Skill

### 方式 1：直接从仓库使用

在当前仓库根目录直接运行：

```powershell
.\ra.ps1 check-examples
.\ra.ps1 run-evals
```

然后把材料交给助手，默认先产出 `issue-report`。

### 方式 2：通过 npm / npx 安装

发布到 npm 后，可直接安装到 Codex skills 目录：

```powershell
npx @chaidd/requirement-assistant-skill@latest install
```

默认安装到：

```text
%USERPROFILE%\.codex\skills\requirement-assistant
```

安装到当前项目：

```powershell
npx @chaidd/requirement-assistant-skill@latest install --target project
```

安装到指定目录：

```powershell
npx @chaidd/requirement-assistant-skill@latest install --dir C:\Users\you\.codex\skills
```

安装后建议验证：

```powershell
.\ra.ps1 check-examples
.\ra.ps1 run-evals
```

如果已经安装过旧版本，重新执行同一条 `install` 命令即可覆盖更新到最新版，例如：

```powershell
npx @chaidd/requirement-assistant-skill@latest install
```

### 1) 校验仓库自带最小样例

```powershell
.\ra.ps1 check-examples
```

期望输出：
- `VALID` x3

### 2) 生成一个空骨架 JSON（bootstrap）

```powershell
.\ra.ps1 bootstrap issue-report out.issue-report.json
```

### 3) 校验一个 JSON（validate）

```powershell
.\ra.ps1 validate issue-report out.issue-report.json
```

### 4) 运行最小 eval 基线

```powershell
.\ra.ps1 run-evals
```

只跑单个基线样例：

```powershell
.\ra.ps1 run-evals issue-report-gdyd-202603
```

运行失败型基线（用于验证 eval runner 能抓到格式或语义退化）：

```powershell
python scripts/run_evals.py --manifest evals/negative.json
```

---

## Schema 选择指南（Schema guide）

你想做什么 → 选哪个 schema：

- “我想先找问题/补全需求/扫描风险” → `issue-report`
- “我想生成 PRD/功能点/测试点/用例草稿” → `prd-bundle`
- “我想把识别、结构化模型、问题、待确认项、产物都打包” → `requirement-package`

---

## 作为 Skill 的正确使用方式

`requirement-assistant` 是一个 **plan-first** 的需求工作流 skill。助手内部应严格按阶段顺序推进，但不要求用户手动逐条输入每个阶段命令。

正确理解方式：

- 助手内部应遵守顺序化流程：`intent -> plan -> check -> ask -> confirm -> execute -> verify -> finalize`
- 正常使用时，你可以直接用自然语言描述目标，由助手驱动内部流程，而不是要求用户手动逐条输入命令
- 如果你希望使用一个统一入口提示词，推荐使用 `assistant-action`
- 默认情况下，助手应按顺序执行，不应主动跳过 `check`、`ask` 或 `confirm`
- 只有用户明确要求跳过某一步时，助手才可以跳过对应阶段
- 每次暂停时，助手都应明确告知当前执行到了哪一步、已完成什么、还缺什么、下一步建议是什么
- 后续继续时，助手应默认从上一次未完成的阶段继续，而不是重新从头分析
- 如果用户提出新的问题、纠正、补充约束或新材料，助手应回退到受影响的最早阶段，再继续往后执行

### 推荐用法

大多数情况下，不需要手动输入：

- `assistant-action`
- `assistant-plan`
- `assistant-check`
- `assistant-analyze`
- `assistant-ask`
- `assistant-confirm`
- `assistant-execute`

你更推荐直接这样使用：

- `assistant-action，先生成计划并告诉我当前判断，等我确认后再继续`
- `assistant-action，请帮我分析梳理功能点，并编写测试用例；先告知我当前判断、缺失信息和建议，待我确认后再继续输出`
- `assistant-action，继续上一次未完成的需求分析，从当前阶段往后执行，并先告诉我现在卡在哪一步`
- `帮我根据这批截图先分析需求，并给执行计划`
- `先检查这份 PRD 有没有歧义、冲突和遗漏`
- `帮我拆这个页面的功能点、状态和流程`
- `这些范围已经确认了，直接输出功能清单和测试点`
- `如果有必须确认项先问我，不要直接生成 PRD`

上面这些自然语言请求，会由助手驱动内部阶段顺序执行；如果中途有必须确认项或等待确认，会暂停并汇报当前阶段状态。

### `assistant-action` 是什么

`assistant-action` 是推荐的统一入口提示词，适合你希望助手先整理计划步骤文档，再由你确认是否继续的场景。

它的默认行为是：

- 先输出 `intent summary`
- 再输出 `execution plan`
- 明确当前判断、输入清单、识别结果、计划步骤、待确认项分层、建议动作
- 用 `run-status` 风格总结当前状态
- 明确当前执行阶段，以及后续如何从该阶段继续
- 明确告知用户下一步需要确认什么

它**不会**默认直接生成 PRD、功能清单、测试点或 JSON 成果，除非你在后续确认继续执行。

### 各阶段的定位

- `assistant-action`：统一入口；先生成计划并告知当前情况，等待用户确认
- `assistant-plan`：先理解目标，给执行计划，先不生成正文
- `assistant-check`：查缺失、冲突、歧义、覆盖漏洞
- `assistant-analyze`：拆页面、流程、规则、状态
- `assistant-ask`：把不清楚的地方整理成分层待确认项
- `assistant-confirm`：锁定范围、假设、输出物
- `assistant-execute`：在确认后生成交付物

### 测试用例输出规范

如果输出包含测试用例，推荐至少包含以下字段：

- 测试用例标题
- 前置条件
- 测试用例步骤
- 测试用例期望结果

约束建议：

- 测试用例标题应以功能模块作为前缀，例如：`登录模块-手机号登录成功`
- 测试用例步骤应尽量详细，能够直接指导测试执行，而不是只写笼统动作
- 前置条件应尽量说明账号状态、权限、测试数据和页面进入条件
- 期望结果应尽量覆盖页面反馈、状态变化、校验结果和错误提示

这些阶段的关系应理解为：

- 它们构成一个内部顺序工作流
- 不要求用户必须手动依次调用每个阶段命令
- 助手需要明确当前处于哪一阶段，并在暂停后支持继续执行
- 默认路径应按顺序执行，除非用户明确提出跳过某一步
- 其中 `assistant-action` 更适合作为默认起点

### 常见使用场景

#### 场景 1：只有截图或原型

用户输入：

```text
assistant-action，帮我根据这些截图整理需求
```

推荐行为：

- 先输出 `intent summary` 和 `execution plan`
- 必要时列出分层待确认项
- 等用户确认后再进入后续阶段

#### 场景 2：已有较完整 PRD，想做质量检查

用户输入：

```text
帮我检查这份 PRD 有没有歧义、遗漏和覆盖漏洞
```

推荐行为：

- 可直接进入 `assistant-check`

#### 场景 3：只想拆解页面或流程

用户输入：

```text
帮我拆这个页面的功能点、状态和交互流程
```

推荐行为：

- 可直接进入 `assistant-analyze`

#### 场景 4：范围已经确认，只要产出物

用户输入：

```text
范围已确认，直接输出功能清单和测试点；如果有必要假设请明确列出
```

推荐行为：

- 先快速确认假设是否可接受
- 条件满足后进入 `assistant-execute`

### 一句话原则

**助手内部应按 `intent -> plan -> check -> ask -> confirm -> execute -> verify -> finalize` 顺序执行，并持续汇报当前阶段状态；只有用户明确要求时才可跳过某一步。**

---

## 过程文档与落盘规则

为了支持“知道当前执行到哪一步”以及“后续从上一次阶段继续执行”，推荐把过程文档落盘保存。

### 三类过程文档分别做什么

- `intent-summary.md`：记录用户目标、范围判断、输入清单、已知事实和未明确点，用来确认“要做什么”
- `execution-plan.md`：记录当前判断、识别结果、计划步骤、待确认项分层、建议动作和下一步，用来确认“准备怎么做”
- `run-status.md`：记录当前阶段、完成情况、阻塞状态、验证状态和下一步，用来确认“现在做到哪了”

### 推荐目录结构

```text
docs/requirement-assistant/
  intent/
  plan/
  status/
```

### 推荐命名规则

- `docs/requirement-assistant/intent/YYYY-MM-DD-<topic>-intent-summary.md`
- `docs/requirement-assistant/plan/YYYY-MM-DD-<topic>-execution-plan.md`
- `docs/requirement-assistant/status/YYYY-MM-DD-<topic>-run-status.md`

说明：

- `YYYY-MM-DD` 用于标记本次运行日期
- `<topic>` 使用稳定、可读的主题标识，例如 `login-flow`、`refund-process`、`member-center`
- 同一轮 workflow 尽量复用相同的 `<topic>`
- `run-status.md` 更适合在同一轮任务中持续更新，而不是每暂停一次就新建一份

### 为什么这样更合理

- 按文档类型分目录，便于查找和归档
- 文件名带日期和主题，便于追踪历史记录
- 可以清楚区分“目标定义”“执行计划”“当前状态”
- 当任务中断后，可以根据 `run-status.md` 直接从上一次阶段继续

---

## 目录结构（Repository layout）

- `SKILL.md`：skill 定义（plan-first 工作流）
- `references/`：模板与清单（plan、输出模板、checklist 等）
- `schemas/`：严格 JSON Schema
- `examples/`：最小合法 JSON 样例
- `scripts/`：bootstrap/validate 脚本
- `evals/`：最小 eval 基线（固定样例 + 期望检查）
- `bin/install.js`：npm / npx 安装器入口
- `package.json`：npm 分发元数据
- `ra.ps1`：Windows 最小 CLI wrapper
- `.planning/`：GSD 项目化文件与代码库地图（可选，用于项目推进/体检）

---

## FAQ

说明：以下 `assistant-action`、`assistant-check`、`assistant-analyze` 等是与助手对话时使用的工作模式提示词，不是 `ra.ps1` 的本地 CLI 子命令。

### Q: 测试人员如何使用这个 skill 辅助工作？
推荐从 `assistant-action` 或 `assistant-check` 开始。

- 如果材料还比较散，先用 `assistant-action`，让助手先整理目标、范围、待确认项和建议
- 如果需求文档已经比较完整，直接用 `assistant-check` 检查缺失、冲突、歧义和覆盖漏洞
- 如果你要产出测试点或测试用例，可以在确认范围后再让助手进入 `assistant-execute`

示例：

```text
assistant-action，请帮我分析这批需求材料，先告诉我当前判断、风险点和缺失信息，确认后再输出测试点和测试用例
```

### Q: 开发人员如何使用这个 skill 辅助工作？
开发更适合用它做“需求拆解”和“实现前澄清”。

- 如果需求范围还没理清，也可以先用 `assistant-action` 作为统一入口，让助手先输出计划、风险判断和待确认项
- 用 `assistant-analyze` 拆页面、流程、规则、状态和边界条件
- 用 `assistant-check` 提前发现需求冲突、遗漏和不明确的地方
- 用 `assistant-confirm` 在实现前锁定范围、假设和输出物，减少返工

示例：

```text
assistant-action，请帮我拆解这个需求的功能点、业务规则、状态流转和依赖关系，先给我计划和风险判断
```

### Q: 产品人员如何使用这个 skill 辅助工作？
产品更适合把它当成“需求梳理和确认助手”。

- 用 `assistant-action` 先让助手整理目标、范围、输入材料和建议动作
- 用 `assistant-ask` 把模糊点转成明确的分层待确认项，并优先突出必须确认项
- 用 `assistant-confirm` 锁定范围、假设和交付物
- 在确认后，再让助手输出 PRD 草稿、功能清单、测试点等结果

示例：

```text
assistant-action，请根据这些截图、流程说明和会议纪要整理需求，先给出执行计划、待确认项和建议，不要直接生成 PRD
```
