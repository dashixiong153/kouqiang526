# kouqiang526

广西医科大学口腔医学院口腔临床案例思维训练 AI 网页助手。

## 本地打开

直接打开 `index.html` 即可使用。病例图片与数字人资源位于 `assets/`。

## GitHub Pages 发布

如果希望网址为：

```text
https://kouqiang526.github.io/
```

需要满足 GitHub Pages 的用户 / 组织主页规则：

1. GitHub 用户名或组织名必须是 `kouqiang526`
2. 仓库名必须是 `kouqiang526.github.io`
3. 发布分支选择 `main`
4. 发布目录选择 `/root`

如果当前使用的是 `dashixiong153` 账号，则默认项目页只能是：

```text
https://dashixiong153.github.io/kouqiang526/
```

不能直接生成 `https://kouqiang526.github.io/`，除非创建或使用名为 `kouqiang526` 的 GitHub 账号 / 组织。

推荐命令：

```powershell
gh auth login -h github.com
gh repo create kouqiang526.github.io --public --source=. --remote=origin --push
```

然后在 GitHub 仓库 Settings → Pages 中选择 `main` 分支和 `/root` 目录。

## 数据说明

当前版本使用浏览器 IndexedDB `kouqiang526_training_db` 保存学生登录信息与训练记录，同时使用 `localStorage` 保存教师看板所需的本地镜像数据。

这适合参赛演示和单机试用。正式部署到全班或多设备环境时，建议接入后端数据库和账号权限系统。
