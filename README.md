# kouqiang526

广西医科大学口腔医学院口腔临床案例思维训练 AI 网页助手。

## 本地打开

直接打开 `index.html` 即可使用。病例图片与数字人资源位于 `assets/`。

## GitHub Pages 发布

建议将仓库命名为 `kouqiang526`，发布分支选择 `main`，目录选择 `/root`。

发布后的默认访问地址为：

```text
https://<你的GitHub用户名>.github.io/kouqiang526/
```

如果需要自定义域名，需要先注册真实域名并在 GitHub Pages 中配置 DNS。仅 `kouqiang526` 不是一个可解析的公网域名。

## 数据说明

当前版本使用浏览器 IndexedDB `kouqiang526_training_db` 保存学生登录信息与训练记录，同时使用 `localStorage` 保存教师看板所需的本地镜像数据。

这适合参赛演示和单机试用。正式部署到全班或多设备环境时，建议接入后端数据库和账号权限系统。
