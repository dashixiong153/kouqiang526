# kouqiang526

口腔黏膜病学—“黏膜研思”智能体平台。

## 本地打开

直接打开 `index.html` 即可使用。病例图片与数字人资源位于 `assets/`。

## GitHub Pages 发布

当前项目页地址：

```text
https://dashixiong153.github.io/kouqiang526/
```

## 数据说明

当前版本使用浏览器 IndexedDB `kouqiang526_training_db` 保存学生登录信息与训练记录，同时使用 `localStorage` 保存教师看板所需的本地镜像数据。

这适合参赛演示和单机试用。正式部署到全班或多设备环境时，建议接入后端数据库和账号权限系统。
