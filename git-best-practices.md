# 代码提交与版本管理最佳实践指南

> 目标：通过清晰的提交规范、合理的分支策略与稳健的版本管理，提升团队协作效率与可维护性，降低发布风险。

## 提交（Commit）习惯

### 基本原则

- **小步快跑**：一次提交只做一件清晰的事情，保持原子化（Atomic）提交。
- **先审后提**：在提交前执行 `git status`、`git diff` 审查改动范围与内容。
- **保持工作树干净**：避免临时文件、构建产物、依赖目录进入版本库（使用 .gitignore 约束）。
- **自动化检查**：在提交前运行本地校验（lint、format、tests）。
  - 后端示例：`pytest`
  - 前端示例：`npm run lint && npm test`
- **保密与合规**：避免提交 `.env`、密钥文件、数据库快照等敏感数据；必要时使用 Git LFS 存储大文件。
- **频率适中**：每完成一个可验证的最小增量即提交，避免巨型提交难以审查。

### 提交信息规范（Conventional Commits）

- **格式**：`<type>(scope): <subject>`
- **常见 type**：
  - `feat`：新功能
  - `fix`：修复缺陷
  - `docs`：文档变更
  - `refactor`：重构（非功能变更）
  - `perf`：性能优化
  - `test`：测试相关
  - `build`：构建系统或依赖变更
  - `ci`：CI 配置变更
  - `chore`：其他维护性工作
- **示例**：
  - `feat(api): add regions POST endpoint`
  - `fix(timeline): correct intersection calculation edge cases`
  - `docs(readme): add setup and run instructions`
- **正文与页脚**（可选）：
  - 在正文中描述动机、实现要点与破坏性变更
  - 如有重大改动可添加 `BREAKING CHANGE:` 段落

### 提交前检查清单

- 运行格式化与静态检查：
  - Python：`ruff` 或 `flake8`，`black` 格式化
  - JS/React：`eslint`，`prettier`
- 运行单元测试：`pytest` / `npm test`
- 确认未包含构建产物与依赖：
  - `node_modules/`、`dist/`、`build/`、`__pycache__/` 等
- 更新必要文档：
  - README、接口文档、迁移指南等

## 分支（Branch）策略

### 推荐策略一：Trunk-Based Development（主干开发）

- **要点**：
  - 以 `master` / `main` 为主干，功能分支短生命周期，尽快合并（通常通过 PR）。
  - 强制主干保护：必须通过 CI、代码审查（Review）后才能合并。
  - 对发布管理，使用标签（tag）或轻量 release 分支。
- **适用场景**：迭代快、自动化测试完善的团队。

### 推荐策略二：Git Flow（发布稳定性优先）

- **分支定义**：
  - `main`：稳定发布分支，始终指向生产版本
  - `develop`：日常开发整合分支
  - `feature/*`：功能分支，从 develop 切出
  - `release/*`：发布分支，从 develop 切出，用于发布前收尾
  - `hotfix/*`：热修复分支，从 main 切出，修复生产缺陷
- **适用场景**：版本节奏明确、需要较严谨发布流程的项目。

### 分支命名规范

- `feature/regions-post`
- `fix/timeline-overlap`
- `docs/setup-guide`
- `refactor/state-management`

### 主干保护与合并策略

- **保护主干**：
  - 禁止直接推送到 `master` / `main`
  - 必须通过 PR，且 CI 绿灯、至少一次 Review 通过
- **合并策略选择**：
  - **Squash Merge**：将分支上的多个 commit 压缩为一个，主干历史更简洁（推荐）
  - **Rebase + Merge**：线性历史，便于回溯，但需谨慎避免历史重写影响他人
  - **Merge Commit**：保留完整历史结构，适合需记录分支合流的场景

## 版本管理（Versioning）

### 语义化版本（SemVer）

- **格式**：`MAJOR.MINOR.PATCH`
  - `MAJOR`：不兼容变更
  - `MINOR`：向后兼容的新功能
  - `PATCH`：向后兼容的修复
- **示例**：`v1.2.3`

### 标签（Tags）与发布（Release）

- **使用标签标记版本点**：`git tag -a v1.2.0 -m "release v1.2.0"`
- **推送标签**：`git push origin v1.2.0` 或所有标签 `git push --tags`
- **生成变更日志（Changelog）**：结合 Conventional Commits 自动生成；或遵循 Keep a Changelog 规范。
- **发布说明**：明确新增、修复、破坏性变更、升级指引、回滚方案。

### 回滚与热修复

- **回滚**：`git revert <commit_or_tag>`，创建反向提交避免历史重写。
- **热修复**：从 main 切出 `hotfix/x.y.z`，修复后合回 main 与 develop，打标签发布。

## 常用工作流示例

### 新功能开发（Trunk-Based）

```powershell
# 从主干更新
git checkout master
git pull origin master

# 创建功能分支
git checkout -b feature/regions-post

# 开发与本地验证
# 后端
pytest
# 前端
npm run lint
npm test

# 提交（按规范）
git add -A
git commit -m "feat(api): add regions POST endpoint"

# 同步主干避免冲突（可选择 rebase 或 merge）
git fetch origin
git rebase origin/master  # 或：git merge origin/master

# 推送并创建PR
git push -u origin feature/regions-post
```

### 发布版本（SemVer + 标签）

```powershell
# 合并完成并通过CI后，在主干打标签
git checkout master
git pull origin master
git tag -a v1.2.0 -m "release v1.2.0: regions API, timeline fixes"
git push origin v1.2.0
```

## 提交模板（可选）

```
<type>(scope): <subject>

[body]
- 背景与动机
- 主要改动点
- 风险与迁移建议

[footer]
BREAKING CHANGE: <说明破坏性变更>
Issue: #123
```

## PR 模板建议

- **标题**：清楚表达目的，如 `feat(api): add POST /regions`
- **描述**：动机、主要改动、影响范围、测试覆盖、风险评估
- **勾选检查项**：已通过本地 lint/format/test、更新文档、无敏感信息
- **截图或接口示例**（如前端页面或API响应）

## 钩子与自动化

- **pre-commit**：统一运行 `black`、`ruff`、`eslint`、`prettier` 等
- **commit-msg**：校验提交信息是否符合 Conventional Commits 规范
- **pre-push**：运行快速测试或构建校验

## 文件忽略与大文件

- **忽略策略**（已在 .gitignore 整合）：
  - 后端：`__pycache__/`、`*.py[cod]`、`.venv/`、测试缓存
  - 前端：`node_modules/`、`dist/`、`build/`、缓存与日志
  - 数据库与二进制：`*.db`、`*.sqlite`（若需版本化请评估）
- **Git LFS**：用于版本化超大、二进制文件（如图片、模型文件），避免膨胀仓库体积
- **保留空目录**：使用占位 `.gitkeep`

## 行尾与平台差异

- **Windows CRLF / Unix LF**：为避免反复转换，可设置：
  - `git config core.autocrlf true`（Windows 推荐）
  - 在 CI 统一格式化规则，避免跨平台冲突

## 与远程仓库的协作

- **认证**：平台可能禁用密码推送，使用 PAT（Personal Access Token）
- **远程操作**：
```powershell
git remote -v
git remote set-url origin https://<user>:<token>@gitcode.com/<org>/<repo>.git
```
- **保护分支与权限**：为 master/main 设置保护策略，强制 PR 与 CI

## 问题排查清单

- **子模块误设**：`git submodule status`（确认是否存在子模块导致无法 add）
- **嵌套 .git 目录**：清理子仓库，将其恢复为普通目录（如 app/test/.git）
- **冲突解决**：`git merge` 或 `git rebase` 时处理冲突文件，谨慎保留正确变更
- **Detached HEAD**：确保在分支上提交，不在游离状态

## 团队约定建议

- 统一提交信息规范（Conventional Commits）
- 使用 PR 模板与提交模板进行约束
- 保护主干分支并强制 CI
- 采用标签与语义化版本管理，自动生成发布说明与变更日志
- 制订回滚与热修复流程

---

### 速查命令清单

```powershell
# 查看状态与改动
git status
git diff

# 提交与推送
git add -A
git commit -m "feat(core): ..."
git push -u origin <branch>

# 拉取与同步
git pull origin master
git fetch origin
git rebase origin/master  # 或 git merge origin/master

# 标签
git tag -a v1.0.0 -m "release v1.0.0"
git push origin v1.0.0

# 回滚
git revert <commit>

# 清理远程配置
git remote -v
git remote set-url origin <url>
```

> 提示：当前仓库已配置前后端 .gitignore ，推送时会自动忽略构建与依赖产物（如 node_modules/ , dist/ , build/ , __pycache__/ 等），请只跟踪源码文件与必要配置。