# FunASR 云端语音识别接口

这个目录提供一个可部署到云服务器的 FastAPI + FunASR 语音识别服务，用于替代浏览器自带 Web Speech API，提高中文口腔黏膜病学术语识别稳定性。

## 接口

- `GET /health`：健康检查
- `POST /v1/audio/transcriptions`：上传音频并返回转写文本

请求示例：

```bash
curl -X POST "https://你的后端域名/v1/audio/transcriptions" \
  -F "file=@answer.webm" \
  -F "hotword=主诉 口腔 黏膜 牙龈 白斑 白纹 扁平苔藓 活检 病理 随访"
```

返回示例：

```json
{
  "text": "主诉是左侧颊黏膜白纹三个月",
  "model": "paraformer-zh"
}
```

## 本地运行

需要 Python 3.8+。首次运行会下载模型，耗时较长。

```bash
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8000
```

## Docker 部署

```bash
docker build -t mucosa-funasr-api .
docker run -p 8000:8000 mucosa-funasr-api
```

## 云端部署建议

FunASR 依赖 PyTorch 和语音模型，不适合部署在 GitHub Pages 或 Supabase Edge Function。建议使用支持 Docker/Python 的云服务：

- 有 GPU：阿里云 ECS、腾讯云 CVM、AutoDL、火山引擎、RunPod 等。
- CPU 轻量试用：Render、Railway、Fly.io 等，但首次加载和识别会慢。

生产环境建议配置：

- Python 3.10
- 内存不少于 4GB，推荐 8GB+
- GPU 推荐 8GB 显存以上
- 环境变量 `ALLOWED_ORIGINS` 设置为前端页面域名，避免任意网页调用

## 可配置环境变量

- `ALLOWED_ORIGINS`：允许跨域访问的前端域名，默认 `*`
- `FUNASR_MODEL`：默认 `paraformer-zh`
- `FUNASR_VAD_MODEL`：默认 `fsmn-vad`
- `FUNASR_PUNC_MODEL`：默认 `ct-punc`
