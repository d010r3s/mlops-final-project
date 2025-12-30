# Sentiment MLOps — Product Demo (Docker)

## What you get
- **ML service (FastAPI)** with Hugging Face model: `d010r3s/sbert-large-sentiment`
- **Streamlit UI** with:
  - Live `/predict`
  - Dataset analytics dashboard (offline sample + optional HF dataset `blinoff/kinopoisk`)
  - System status page
- ClickHouse + Kafka + Grafana (optional for extensions)

## Quick start
```bash
docker compose up -d --build
```

Open:
- UI: http://localhost:8501
- ML service: http://localhost:8000/docs
- Grafana: http://localhost:3000 (admin / admin)
- ClickHouse HTTP ping: http://localhost:8123/ping

## Stop
```bash
docker compose down -v
```

## Notes
- UI talks to ML inside the Docker network via `http://ml_service:8000` (not localhost).
- The tokenizer is loaded robustly: first from model repo, then fallback to `ai-forever/sbert_large_nlu_ru`.
