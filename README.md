# requirement-assistant

一个“需求分析助手”skill 资源包：把截图/原型/会议纪要/PRD 片段等混合需求材料，按 **plan-first**（先意图→再计划→问阻塞问题→确认→执行→校验）流程整理成结构化需求产物，并提供 **严格 JSON Schema + 本地校验脚本**，方便给 GPT/Codex 或下游自动化管道使用。

> 这不是一个可直接运行的产品（没有内置模型调用、没有 Web UI/服务端）；它提供的是 **流程规范、模板、schema 和校验工具**。

---

## 功能介绍（What it does）

### 1) Plan-first 需求工作流（skill）

入口：`SKILL.md`

核心原则：
- **先澄清意图与范围**：目标产物是什么（PRD / issue-report / 功能清单 / 测试点 / 严格 JSON）
- **先出执行计划**：列输入清单、识别结果、步骤、阻塞问题、推荐动作
- **只问阻塞问题**：不一次性问太多，确保问题会影响结构/范围/正确性
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

## 目录结构（Repository layout）

- `SKILL.md`：skill 定义（plan-first 工作流）
- `references/`：模板与清单（plan、输出模板、checklist 等）
- `schemas/`：严格 JSON Schema
- `examples/`：最小合法 JSON 样例
- `scripts/`：bootstrap/validate 脚本
- `evals/`：最小 eval 基线（固定样例 + 期望检查）
- `ra.ps1`：Windows 最小 CLI wrapper
- `.planning/`：GSD 项目化文件与代码库地图（可选，用于项目推进/体检）

---

## FAQ

### Q: 作为 skill 一定要有 CLI 吗？
不必须。skill 本身只需要规范与模板即可；CLI 的价值在于**可重复执行、可自动化校验、便于集成**。

### Q: 我如何把截图/纪要“变成” issue-report？
把材料提供给对话式助手，让它按 `issue-report` schema 产出 JSON；然后用 `.\ra.ps1 validate issue-report <file>` 做本地校验。
