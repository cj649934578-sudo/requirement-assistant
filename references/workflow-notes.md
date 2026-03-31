# 工作流说明

## Plan-first 策略

当用户提供截图、模糊需求、部分需求材料，或存在多种可能交付物时，优先采用 plan-first 执行方式。

这类情况下不要直接生成完整 PRD。

`assistant-action` 是这个工作流的首选入口提示词。
它应驱动以下内部阶段顺序：
- `intent -> plan -> check -> ask -> confirm -> execute -> verify -> finalize`

这是默认路径。
除非用户明确要求跳过，否则不要跳过 `check`、`ask` 或 `confirm`。

工作流暂停时，助手应汇报当前阶段。
用户不需要手动逐个调用每个阶段提示词。

当工作流暂停时：
- 返回 `run-status.md` 风格的状态信息
- 说明当前阶段、上一个已完成阶段和下一步动作
- 明确说明当前是可以继续，还是正在等待用户确认

当用户稍后回来继续时：
- 默认从最近一个未完成阶段继续
- 只有在新输入显著改变范围、假设或输出物时，才回退到更早阶段
- 如果用户提出新的问题、修正或新增约束，应先回退到最早受影响的阶段，再继续执行

## 完成判定策略

只有满足以下条件，任务才算完成：
- the goal is defined
- an execution plan exists
- must-confirm items are closed or explicitly waived
- required outputs are generated
- validation has passed when required
- the user signed off or allowed auto-finalization

如果以上任一项不成立，应返回 `run-status.md`，而不是直接宣告完成。

## 建议输出策略

提出问题时，始终同时给出建议，不要只抛出没有引导的被动问题。

## 快速草稿例外

只有当用户明确要求“现在先出一个粗稿”，并接受上下文不完整的风险时，才允许进入快速草稿模式。
此时应：
- 明确标注结果为草稿
- 清晰列出假设
- 保留待确认项
