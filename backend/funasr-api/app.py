import os
import tempfile
from functools import lru_cache

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from funasr import AutoModel


APP_NAME = "mucosa-funasr-api"
HOTWORDS = "主诉 口腔 黏膜 牙龈 颊黏膜 舌部 白斑 白纹 红斑 糜烂 扁平苔藓 苔藓样 活检 病理 随访"

app = FastAPI(title=APP_NAME)

allowed_origins = os.getenv("ALLOWED_ORIGINS", "*")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in allowed_origins.split(",")] if allowed_origins != "*" else ["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@lru_cache(maxsize=1)
def get_model():
    return AutoModel(
        model=os.getenv("FUNASR_MODEL", "paraformer-zh"),
        vad_model=os.getenv("FUNASR_VAD_MODEL", "fsmn-vad"),
        punc_model=os.getenv("FUNASR_PUNC_MODEL", "ct-punc"),
        disable_update=True,
    )


def normalize_dental_terms(text: str) -> str:
    replacements = {
        "朴素": "主诉",
        "仆诉": "主诉",
        "朴诉": "主诉",
        "主速": "主诉",
        "主素": "主诉",
        "年膜": "黏膜",
        "黏莫": "黏膜",
        "粘膜": "黏膜",
        "脸膜": "黏膜",
        "牙引": "牙龈",
        "牙银": "牙龈",
        "白文": "白纹",
        "白问": "白纹",
        "白班": "白斑",
        "红班": "红斑",
        "糜乱": "糜烂",
        "迷烂": "糜烂",
        "舔部": "舌部",
        "蛇部": "舌部",
        "夹黏膜": "颊黏膜",
        "假黏膜": "颊黏膜",
        "扁平太鲜": "扁平苔藓",
        "扁平苔鲜": "扁平苔藓",
        "扁平台藓": "扁平苔藓",
        "苔鲜样": "苔藓样",
        "活捡": "活检",
        "病里": "病理",
        "随房": "随访",
    }
    value = text or ""
    for source, target in replacements.items():
        value = value.replace(source, target)
    return value.strip()


@app.get("/health")
def health():
    return {"ok": True, "service": APP_NAME}


@app.post("/v1/audio/transcriptions")
async def transcribe_audio(
    file: UploadFile = File(...),
    model: str = Form("paraformer-zh"),
    hotword: str = Form(HOTWORDS),
):
    suffix = os.path.splitext(file.filename or "")[1] or ".webm"
    if suffix.lower() not in {".wav", ".mp3", ".m4a", ".webm", ".ogg", ".flac"}:
        raise HTTPException(status_code=400, detail="Unsupported audio format")

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    try:
        result = get_model().generate(input=tmp_path, hotword=hotword)
        if isinstance(result, list) and result:
            text = result[0].get("text", "")
        elif isinstance(result, dict):
            text = result.get("text", "")
        else:
            text = str(result or "")
        text = normalize_dental_terms(text)
        return {"text": text, "model": model}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"ASR failed: {exc}") from exc
    finally:
        try:
            os.remove(tmp_path)
        except OSError:
            pass
