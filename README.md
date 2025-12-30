# Аналитика отзывов

## Запуск
```bash
docker compose up -d --build
```

Сервисы:
- UI: http://localhost:8501
- ML service: http://localhost:8000/docs
- ClickHouse HTTP ping: http://localhost:8123/ping
- 
Архитектура:
```
Пользователь
     ↓
Streamlit (UI)
     ↓ HTTP
ML-сервис (модель тональности)
     ↓
ClickHouse (хранение результатов)
```
