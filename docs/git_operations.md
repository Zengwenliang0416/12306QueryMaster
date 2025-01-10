# Git 操作指南

本文档总结了项目中使用的Git操作和最佳实践。

## 基本操作

### 分支管理

```bash
# 查看当前分支
git branch

# 创建并切换到新分支
git checkout -b feature/new-feature

# 切换分支
git checkout master

# 删除本地分支
git branch -D branch-name

# 删除远程分支
git push origin --delete branch-name
```

### 代码同步

```bash
# 获取远程更新
git fetch origin

# 拉取远程更改
git pull

# 推送到远程仓库
git push -u origin branch-name

# 重置本地分支到远程状态
git reset --hard origin/master
```

### 提交更改

```bash
# 添加更改到暂存区
git add .

# 提交更改
git commit -m "type: 提交信息"

# 推送到远程
git push
```

## 提交信息规范

使用语义化的提交信息格式：

- `feat`: 新功能
- `fix`: 修复问题
- `docs`: 文档更改
- `style`: 代码格式修改
- `refactor`: 代码重构
- `test`: 测试用例修改
- `chore`: 其他修改
- `ci`: CI配置修改

示例：
```bash
git commit -m "feat: 添加用户登录功能"
git commit -m "fix: 修复查询缓存问题"
git commit -m "docs: 更新API文档"
```

## 分支命名规范

- 功能分支：`feature/feature-name`
- 修复分支：`fix/bug-name`
- 文档分支：`docs/doc-name`
- 优化分支：`optimize/optimize-name`

## 工作流程

1. 创建功能分支
```bash
git checkout -b feature/new-feature
```

2. 开发并提交更改
```bash
git add .
git commit -m "feat: 添加新功能"
```

3. 推送到远程
```bash
git push -u origin feature/new-feature
```

4. 创建Pull Request
- 访问GitHub仓库
- 创建新的Pull Request
- 选择源分支和目标分支
- 填写PR描述
- 等待审查和合并

5. 合并后清理
```bash
git checkout master
git pull
git branch -D feature/new-feature
git push origin --delete feature/new-feature
```

## 常见问题处理

### 解决合并冲突

1. 切换到主分支并更新
```bash
git checkout master
git pull
```

2. 切换回功能分支
```bash
git checkout feature/branch
```

3. 将主分支合并到功能分支
```bash
git merge master
```

4. 解决冲突后提交
```bash
git add .
git commit -m "fix: 解决合并冲突"
git push
```

### 撤销更改

```bash
# 撤销工作区更改
git checkout -- file-name

# 撤销暂存区更改
git reset HEAD file-name

# 撤销最近一次提交
git reset --soft HEAD^

# 强制重置到远程状态
git reset --hard origin/master
```

## 最佳实践

1. 经常性地同步主分支的更新
2. 保持提交粒度适中，每个提交专注于一个改动
3. 写清晰的提交信息
4. 在提交前进行代码审查
5. 及时清理已合并的分支
6. 不要提交敏感信息
7. 使用.gitignore忽略不需要的文件