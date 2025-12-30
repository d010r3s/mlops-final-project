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
Цель (бизнес-задача):

Цель данного проекта - автоматизировать анализ тональности отзывов с помощью модели машинного обучения. Система позволит быстро определить, является ли отзыв положительным, нейтральным или отрицательным, а также оценить уверенность модели в своём предсказании и показать графики с аналитикой по распределению тональности и уверенности модели.
```
Решение может использоваться для:
> мониторинга качества сервиса;
> быстрого выявления негативных отзывов;
> поддержки работы службы поддержки и маркетинга;
> аналитики пользовательского мнения на основе больших массивов текстовых данных.
```
## one-pager
<img width="595" height="842" alt="A4 - 1" src="https://github.com/user-attachments/assets/5d4364e4-8015-4e84-acc6-29d44fa93413" />
## полная презентация
<img width="1920" height="1080" alt="43" src="https://github.com/user-attachments/assets/b90b6049-12c2-4bd8-983e-d5fb698989e1" />
<img width="1920" height="1080" alt="45" src="https://github.com/user-attachments/assets/5fa426d0-e4b0-4a20-ad08-10839cac074f" />
<img width="1920" height="1080" alt="51" src="https://github.com/user-attachments/assets/6c32b4b2-7ea2-4184-939c-f9bc02502395" />
<img width="1920" height="1080" alt="46" src="https://github.com/user-attachments/assets/f6c56dc0-a24e-48b8-b2bd-5201abd30fb4" />
<img width="1920" height="1080" alt="48" src="https://github.com/user-attachments/assets/8ab4b653-172f-4fb0-949b-b28f9c409e83" />
<img width="1920" height="1080" alt="49" src="https://github.com/user-attachments/assets/2aab6d19-ecdf-4148-bc4e-8d37e222280c" />
<img width="1920" height="1080" alt="50" src="https://github.com/user-attachments/assets/6e00d047-8c87-439a-a53a-1f7a8b55ab0a" />
<img width="1920" height="1080" alt="50" src="https://github.com/user-attachments/assets/96112bf4-4ef3-493f-9b84-13ed83794e40" />
<img width="1920" height="1080" alt="52" src="https://github.com/user-attachments/assets/305ae64f-44b2-4a3a-9b7e-53b220bef108" />
<img width="1920" height="1080" alt="58" src="https://github.com/user-attachments/assets/67a4b88e-cdcb-401e-b5bc-01fb37c2c7d1" />
<img width="1920" height="1080" alt="82" src="https://github.com/user-attachments/assets/6bb9424a-8e70-4064-948f-e89f728b8d11" />
<img width="1920" height="1080" alt="83" src="https://github.com/user-attachments/assets/29608072-d3ce-405c-89a3-e2fe6fcf2959" />
<img width="1920" height="1080" alt="84" src="https://github.com/user-attachments/assets/23f040eb-432b-4720-b389-61d8272dff42" />
<img width="1920" height="1080" alt="55" src="https://github.com/user-attachments/assets/98a76897-db8e-48e2-9e71-b101b09f3294" />
<img width="1920" height="1080" alt="68" src="https://github.com/user-attachments/assets/819e0e5e-7c93-4da9-9ce4-11f3017f127d" />
<img width="1920" height="1080" alt="69" src="https://github.com/user-attachments/assets/15231dfb-6479-4617-8d25-e56f36bfbc7a" />
<img width="1920" height="1080" alt="70" src="https://github.com/user-attachments/assets/1f607227-253b-4f7f-a7c9-873afcce6c9c" />
<img width="1920" height="1080" alt="56" src="https://github.com/user-attachments/assets/5858b213-e01f-4eec-8659-50d0167e6c0b" />
<img width="1920" height="1080" alt="71" src="https://github.com/user-attachments/assets/eeeab750-1638-48f0-a8e5-84c9ec6f0573" />
<img width="1920" height="1080" alt="72" src="https://github.com/user-attachments/assets/7237fe59-1fe2-49db-bc74-c1f09fe4a3cd" />
<img width="1920" height="1080" alt="73" src="https://github.com/user-attachments/assets/313bafff-370a-44b8-b4dc-e4baabb9d508" />
<img width="1920" height="1080" alt="57" src="https://github.com/user-attachments/assets/b5cce7ac-c623-43ef-934f-250f3c60c72f" />
<img width="1920" height="1080" alt="74" src="https://github.com/user-attachments/assets/79a80c19-10ac-4367-9deb-609e1979c6d9" />
<img width="1920" height="1080" alt="76" src="https://github.com/user-attachments/assets/58631a71-23f5-4a95-9711-b506091c95cd" />
<img width="1920" height="1080" alt="78" src="https://github.com/user-attachments/assets/bfa8deb1-489a-4495-9e75-539c35c5a1e9" />





















