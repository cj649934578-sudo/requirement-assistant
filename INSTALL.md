# INSTALL

本文件只说明三件事：
- 怎么安装这个 skill
- 怎么验证安装成功
- 安装失败时先检查什么

## 适用对象

适合：
- 想在 Codex 中安装 `requirement-assistant` skill 的用户
- 想通过 `npx` 一键安装到用户目录或项目目录的用户

不适合：
- 想把本仓库当作 Web 应用直接运行的用户

## 方式 1：通过 npm / npx 安装

已发布包：

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

此时会安装到：

```text
<current-project>\.codex\skills\requirement-assistant
```

安装到指定目录：

```powershell
npx @chaidd/requirement-assistant-skill@latest install --dir C:\Users\you\.codex\skills
```

## 方式 2：直接从仓库使用

如果你已经拿到了这个仓库，也可以不经过 npm，直接在仓库根目录使用：

```powershell
.\ra.ps1 check-examples
.\ra.ps1 run-evals
```

然后把原型、截图、需求说明等材料交给助手，默认先产出 `issue-report`。

## 安装后验证

进入安装后的目录，执行：

```powershell
.\ra.ps1 check-examples
.\ra.ps1 run-evals
```

期望结果：
- `check-examples` 输出 `VALID` x3
- `run-evals` 输出 `EVAL PASS`

## 安装成功后怎么用

这个 skill 的默认工作方式是：
- 输入需求材料（截图、原型链接、PRD 片段、会议纪要、流程说明等）
- 默认先做 `issue-report`
- 需要时再导出 `prd-bundle` 或 `requirement-package`

更完整的使用说明见：
- `README.md`
- `SKILL.md`

## 常见问题

### 1. `npx` 安装报错

先检查：
- Node.js 是否可用：`node -v`
- npm 是否可用：`npm -v`
- 网络是否能访问 npm registry

### 2. 安装后找不到 skill

先确认安装目标目录：
- 用户级：`%USERPROFILE%\.codex\skills\requirement-assistant`
- 项目级：`<project>\.codex\skills\requirement-assistant`

如果 Codex 已经在运行，重启一次会话。

### 3. 安装后验证失败

先检查：
- Python 3 是否可用：`python --version`
- 是否在 skill 根目录执行了 `.\ra.ps1 ...`

### 4. npm 发布相关

如果你是维护者而不是使用者，发布前至少要确认：
- `npm login`
- `npm whoami`
- `npm pack --dry-run`

