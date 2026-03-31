# 计划模板

以下固定模板用于 plan-first 执行方式。

`assistant-action` 是推荐的工作流入口提示词。
它应先产出 `intent-summary.md` 和 `execution-plan.md`，然后以 `run-status.md` 风格汇报当前状态；当任务还不能安全继续时，应停下来等待用户确认。
默认内部阶段顺序：
- `intent -> plan -> check -> ask -> confirm -> execute -> verify -> finalize`

推荐文件落盘位置：
- `docs/requirement-assistant/intent/YYYY-MM-DD-<topic>-intent-summary.md`
- `docs/requirement-assistant/plan/YYYY-MM-DD-<topic>-execution-plan.md`
- `docs/requirement-assistant/status/YYYY-MM-DD-<topic>-run-status.md`

## intent-summary.md

```md
# 意图摘要

## 元数据
- 日期: [YYYY-MM-DD]
- 主题: [stable-topic-slug]
- 入口提示词: [assistant-action / assistant-plan / assistant-check / assistant-analyze / assistant-ask / assistant-confirm / assistant-execute]

## 用户目标
[一句话描述]

## 请求产物
[列出请求的输出物]

## 范围判断
[页面优化 / 逻辑改动 / 仅检查 / 混合]

## 输入清单
- 截图:
- 说明笔记:
- 流程描述:
- 现有 PRD:
- 模板要求:

## 已知事实
- 

## 未明确点
- 

## 推荐模式
[plan / analyze / check / ask / confirm / execute]

## 当前阶段
[intent]
```

## execution-plan.md

```md
# 执行计划

## 元数据
- 日期: [YYYY-MM-DD]
- 主题: [stable-topic-slug]
- 来源: [intent-summary 文件或请求摘要]

## 用户目标
[简要总结]

## 当前判断
- 材料完整度: [high / medium / low]
- 是否适合直接执行: [yes / no]
- 推荐模式: [plan / analyze / check / ask / confirm / execute]
- 当前工作流阶段: [plan]
- 跳过阶段: [none / 用户指定跳过的阶段]

## 输入清单
- 截图:
- 说明笔记:
- 流程描述:
- 现有 PRD:
- 模板要求:

## 已识别内容
- 页面/模块:
- 关键字段:
- 关键动作:
- 初始规则:
- 初始风险:

## 计划步骤
1.
2.
3.
4.

## 待确认项
### 必须确认项
1. [会影响范围、正确性或执行安全的问题]
   - 建议选项:
     - [选项 A]
     - [选项 B]

### 建议优化项
1. [会影响质量、一致性或可维护性，但未必阻塞执行的问题]
   - 建议选项:
     - [选项 A]
     - [选项 B]

### 可后续确认项
1. [如有需要可延后确认的问题]
   - 建议选项:
     - [选项 A]
     - [选项 B]

## 已完成步骤
- [已完成 intent 阶段]

## 建议
- 
- 

## 下一步动作
[继续检查 / 追问必须确认项 / 等待确认 / 按用户认可的假设继续]
```

## run-status.md

```md
# 运行状态

## 元数据
- 日期: [YYYY-MM-DD]
- 主题: [stable-topic-slug]
- 状态文件: [当前文件路径]

## 当前阶段
[intent / plan / check / ask / confirm / execute / verify / finalize]

## 上一个完成阶段
[intent / plan / check / ask / confirm / execute / verify / none]

## 目标状态
[defined / unclear]

## 计划状态
[not started / ready / approved]

## 待确认项统计
- 必须确认项: [number]
- 建议优化项: [number]
- 可后续确认项: [number]

## 执行状态
[not started / in progress / complete / blocked]

## 校验状态
[not applicable / pending / passed / failed]

## 恢复起点
[阶段名称]

## 回退触发条件
[none / new question / new correction / new scope input / new dependency]

## 是否可结束
[yes / no]

## 下一步动作
[一句话描述]

## 备注
- [已完成内容]
- [当前卡点]
- [需要用户确认的内容]
```

格式规则：
- 仅对每个分区中的顶层问题使用编号列表。
- 每个问题下的建议选项必须使用缩进的无序列表，不要继续使用编号。
