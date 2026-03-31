# 严格 JSON 输出与校验

当用户需要面向 GPT、Codex、下游 API 或自动化流水线的机器可读输出时，使用本说明。

## 支持的 schema

### 1. requirement-package
适用于完整分析输出，包含识别结果、需求建模、问题发现、待确认项以及可选生成产物。

Schema 文件：
- `schemas/requirement-package.schema.json`

生成骨架命令：
```bash
scripts/bootstrap_output.py requirement-package /tmp/requirement-package.json
```

校验命令：
```bash
scripts/validate_output.py requirement-package /tmp/requirement-package.json
```

### 2. issue-report
适用于检查、扫描、风险识别类输出。

Schema 文件：
- `schemas/issue-report.schema.json`

生成骨架命令：
```bash
scripts/bootstrap_output.py issue-report /tmp/issue-report.json
```

校验命令：
```bash
scripts/validate_output.py issue-report /tmp/issue-report.json
```

### 3. prd-bundle
适用于用户需要机器可读的需求交付物生成结果时。

Schema 文件：
- `schemas/prd-bundle.schema.json`

生成骨架命令：
```bash
scripts/bootstrap_output.py prd-bundle /tmp/prd-bundle.json
```

校验命令：
```bash
scripts/validate_output.py prd-bundle /tmp/prd-bundle.json
```

## Schema 选择规则

- 完整分析或混合型请求，优先选 `requirement-package`。
- 检查 / 评审 / 扫描类请求，优先选 `issue-report`。
- 生成 / 草稿类请求，优先选 `prd-bundle`。
- 如果用户明确要求 JSON schema 输出，优先使用这些 schema，而不是自由 markdown。

## 输出约束

输出严格 JSON 时：
- 不要在 JSON 对象内部混入解释性文字。
- key 必须严格与 schema 定义一致。
- 可行时优先使用空数组，而不是省略可选列表字段。
- 不确定内容应放入 `assumptions`、`limitations` 或 `pending_confirmations`，不要编造事实。
- 在有文件系统上下文时，应使用 `scripts/validate_output.py` 做校验。

## 最小合法示例文件
当 GPT 或 Codex 需要每个 schema 的最小合法载荷，或需要测试内置校验器时，使用以下文件：

- `examples/requirement-package.min.json`
- `examples/issue-report.min.json`
- `examples/prd-bundle.min.json`

推荐校验命令：

```bash
python scripts/validate_output.py requirement-package examples/requirement-package.min.json
python scripts/validate_output.py issue-report examples/issue-report.min.json
python scripts/validate_output.py prd-bundle examples/prd-bundle.min.json
```
