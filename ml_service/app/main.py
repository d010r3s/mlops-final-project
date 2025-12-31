import os
from typing import Any, Dict, List, Optional

import torch
from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoModelForSequenceClassification, AutoTokenizer

MODEL_NAME = os.getenv("MODEL_NAME", "cointegrated/rubert-tiny-sentiment-balanced")
DEVICE = os.getenv("DEVICE", "cpu")

app = FastAPI(title="Sentiment MLOps ML Service", version="1.0.0")

tokenizer = None
model = None
id2label = None


def _load() -> None:
    global tokenizer, model, id2label
    try:
        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, use_fast=True)
    except Exception:
        for fallback in [
            "ai-forever/sbert_large_nlu_ru",
            "DeepPavlov/rubert-base-cased",
        ]:
            try:
                tokenizer = AutoTokenizer.from_pretrained(fallback, use_fast=True)
                break
            except Exception:
                continue
        if tokenizer is None:
            raise

    model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
    model.eval()

    if DEVICE.lower() == "cuda" and torch.cuda.is_available():
        model.to("cuda")
    else:
        model.to("cpu")

    cfg = getattr(model, "config", None)
    id2label = getattr(cfg, "id2label", None) or {0: "NEGATIVE", 1: "NEUTRAL", 2: "POSITIVE"}
    def _normalize_label(lbl: str) -> str:
        s = str(lbl).strip().lower()
        if "neg" in s:
            return "negative"
        if "pos" in s:
            return "positive"
        if "neu" in s:
            return "neutral"
        return s or "unknown"

    _tmp = {}
    for k, v in dict(id2label).items():
        try:
            kk = int(k)
        except Exception:
            continue
        _tmp[kk] = _normalize_label(v)
    if _tmp:
        id2label = _tmp



@app.on_event("startup")
def startup_event() -> None:
    _load()


class PredictRequest(BaseModel):
    text: str


class PredictResponse(BaseModel):
    label: str
    score: float
    probs: Dict[str, float]


@app.get("/health")
def health() -> Dict[str, Any]:
    return {
        "status": "ok",
        "model": MODEL_NAME,
        "tokenizer": getattr(tokenizer, "name_or_path", None),
        "device": str(next(model.parameters()).device) if model is not None else None,
        "dummy": False,
    }


@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest) -> PredictResponse:
    inputs = tokenizer(
        req.text,
        return_tensors="pt",
        truncation=True,
        max_length=256,
        padding=True,
    )
    device = next(model.parameters()).device
    inputs = {k: v.to(device) for k, v in inputs.items()}

    with torch.no_grad():
        logits = model(**inputs).logits
        probs = torch.softmax(logits, dim=-1).squeeze(0)

    probs_dict = {id2label[i]: float(probs[i].cpu()) for i in range(probs.shape[-1])}
    best_i = int(torch.argmax(probs).cpu())
    return PredictResponse(label=id2label[best_i], score=float(probs[best_i].cpu()), probs=probs_dict)
