# Git 操作记录

本文档记录了项目的主要Git操作步骤，包括仓库初始化、分支管理、标签发布等操作。

## 1. 初始化仓库

```bash
# 添加远程仓库
git remote add origin https://github.com/Zengwenliang0416/12306QueryMaster.git

# 推送代码到main分支
git push -u origin main
```

## 2. 发布第一个版本

```bash
# 创建并推送v1.1.0标签
git tag -a v1.1.0 -m "12306列车查询系统 v1.1.0发布"
git push origin v1.1.0
```

## 3. 分支重命名

```bash
# 查看当前分支
git branch

# 将dev分支重命名为master
git branch -m dev master

# 推送master分支到远程仓库
git push -u origin master --force

# 删除本地main分支
git branch -d main
```

## 4. 清理忽略文件

### 4.1 更新.gitignore文件
确保.gitignore文件包含所有需要忽略的文件和目录：
- Python相关：__pycache__/, *.pyc等
- 虚拟环境：venv/, env/等
- IDE配置：.idea/, .vscode/等
- 临时文件：*.log, *.tmp等
- 项目特定：backend/data/, backend/test_curl.sh等

### 4.2 清理操作

```bash
# 从git缓存中删除所有文件
git rm -r --cached .

# 重新添加所有文件（会应用.gitignore规则）
git add .

# 提交更改
git commit -m "清理忽略的文件"

# 推送到远程仓库
git push
```

## 5. 分支管理最佳实践

1. 使用master作为主分支
2. 功能开发使用feature分支
3. 版本发布使用tag标记
4. 定期清理过时分支

## 6. GitHub仓库设置

1. 将master设置为默认分支
2. 配置分支保护规则
3. 启用Issues和Pull Requests
4. 配置Actions工作流（可选）

## 7. 常用Git命令

```bash
# 分支操作
git branch                    # 查看分支
git branch -a                 # 查看所有分支（包括远程）
git checkout -b feature/xxx   # 创建并切换到新分支
git branch -d xxx            # 删除分支

# 标签操作
git tag                      # 查看标签
git tag -a v1.x.x -m "消息"  # 创建带注释的标签
git push origin v1.x.x       # 推送标签到远程

# 提交操作
git status                   # 查看状态
git add .                    # 添加所有更改
git commit -m "消息"         # 提交更改
git push                     # 推送到远程

# 同步操作
git fetch                    # 获取远程更新
git pull                     # 拉取并合并远程更改
``` 