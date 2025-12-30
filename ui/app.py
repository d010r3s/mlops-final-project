import os
import time
from dataclasses import dataclass
from typing import Dict, Optional

import numpy as np
import pandas as pd
import requests
import streamlit as st
import plotly.express as px

try:
    from datasets import load_dataset
except Exception:
    load_dataset = None


ML_URL = os.getenv("ML_SERVICE_URL", "http://ml_service:8000")
DATA_DIR = os.getenv("DATA_DIR", "data")
LOCAL_SAMPLE = os.path.join(DATA_DIR, "sample_reviews_ru.csv")


@dataclass
class ApiResult:
    ok: bool
    data: Optional[dict] = None
    err: Optional[str] = None


def _get(path: str, timeout: float = 5.0) -> ApiResult:
    try:
        r = requests.get(f"{ML_URL}{path}", timeout=timeout)
        r.raise_for_status()
        return ApiResult(True, r.json(), None)
    except Exception as e:
        return ApiResult(False, None, str(e))


def _post(path: str, payload: dict, timeout: float = 10.0) -> ApiResult:
    try:
        r = requests.post(f"{ML_URL}{path}", json=payload, timeout=timeout)
        r.raise_for_status()
        return ApiResult(True, r.json(), None)
    except Exception as e:
        return ApiResult(False, None, str(e))


@st.cache_data(show_spinner=False)
def load_local_sample() -> pd.DataFrame:
    df = pd.read_csv(LOCAL_SAMPLE)
    df["text"] = df["text"].astype(str)
    return df


@st.cache_data(show_spinner=False)
def load_kinopoisk(limit: int = 5000) -> pd.DataFrame:
    if load_dataset is None:
        raise RuntimeError("Библиотека datasets недоступна в этом окружении")
    ds = load_dataset("blinoff/kinopoisk", split="train")
    df = ds.to_pandas()
    df = df.rename(columns={"content": "text", "grade3": "label_raw"})
    df = df[["text", "label_raw", "movie_name"]].copy()
    df["text"] = df["text"].astype(str)
    df = df.sample(min(limit, len(df)), random_state=42)
    return df.reset_index(drop=True)


def page_live():
    st.header("Онлайн-предсказание тональности")
    st.caption(f"ML-сервис: {ML_URL}")

    col1, col2 = st.columns([2, 1])
    with col1:
        text = st.text_area(
            "Текст отзыва",
            "Мне очень понравилось! Доставка быстрая, качество отличное.",
            height=160,
        )
        c1, c2 = st.columns(2)
        with c1:
            do_pred = st.button("Определить тональность", use_container_width=True)
        with c2:
            do_health = st.button("Проверить сервис", use_container_width=True)

    with col2:
        if do_health:
            res = _get("/health")
            if res.ok:
                st.success("Сервис доступен")
                st.json(res.data)
            else:
                st.error(res.err)

        if do_pred:
            res = _post("/predict", {"text": text})
            if res.ok:
                st.success(
                    f"Тональность: {res.data['label']} "
                    f"(уверенность = {res.data['score']:.3f})"
                )
                probs = res.data.get("probs", {})
                if probs:
                    dfp = pd.DataFrame(
                        {"Тональность": list(probs.keys()), "Вероятность": list(probs.values())}
                    ).sort_values("Вероятность", ascending=False)
                    st.plotly_chart(
                        px.bar(dfp, x="Тональность", y="Вероятность"),
                        use_container_width=True,
                    )
            else:
                st.error(res.err)


def _batch_predict(texts: pd.Series, max_rows: int = 300) -> pd.DataFrame:
    texts = texts.dropna().astype(str).head(max_rows)
    labels, scores = [], []
    prog = st.progress(0)
    for i, t in enumerate(texts):
        res = _post("/predict", {"text": t}, timeout=15.0)
        if res.ok:
            labels.append(res.data["label"])
            scores.append(res.data["score"])
        else:
            labels.append("ОШИБКА")
            scores.append(0.0)
        prog.progress((i + 1) / len(texts))
        time.sleep(0.02)
    prog.empty()
    return pd.DataFrame(
        {"Текст": texts.tolist(), "Тональность": labels, "Уверенность": scores}
    )


def page_dataset():
    st.header("Датасет русскоязычных отзывов и аналитика")
    st.caption(
        "Загружаем готовый датасет и прогоняем модель анализа тональности "
        "по подвыборке, строим продуктовый дашборд"
    )

    source = st.radio(
        "Источник датасета",
        [
            "Локальный пример (офлайн)",
            "Hugging Face: blinoff/kinopoisk (36,6 тыс.)",
        ],
        index=0,
    )
    limit = st.slider(
        "Количество отзывов для аналитики",
        50,
        500,
        200,
        step=50,
    )

    if source.startswith("Локальный"):
        df = load_local_sample()
        st.info(f"Загружен локальный пример: {len(df)} строк")
    else:
        with st.spinner("Загрузка датасета с HF..."):
            df = load_kinopoisk(limit=5000)
        st.info(f"Загружено с HF: {len(df)} строк (случайная выборка)")

    st.subheader("Предварительный просмотр данных")
    st.dataframe(df.head(20), use_container_width=True, height=280)

    st.subheader("Аналитика тональности на основе модели")
    st.write(
        "Нажмите, чтобы запустить инференс "
        "и построить аналитические графики."
    )

    if st.button("Запустить анализ", type="primary"):
        with st.spinner("Выполняется инференс..."):
            pred = _batch_predict(df["text"], max_rows=limit)

        st.success("Анализ завершён")
        st.dataframe(pred.head(20), use_container_width=True, height=260)

        dist = pred["Тональность"].value_counts().reset_index()
        dist.columns = ["Тональность", "Количество"]
        st.plotly_chart(
            px.pie(dist, names="Тональность", values="Количество",
                   title="Распределение тональностей"),
            use_container_width=True,
        )

        st.plotly_chart(
            px.histogram(pred, x="Уверенность", nbins=20,
                         title="Распределение уверенности модели"),
            use_container_width=True,
        )

        st.subheader("Ключевые инсайты")
        pos = pred[pred["Тональность"].str.contains("POS", case=False, na=False)]
        neg = pred[pred["Тональность"].str.contains("NEG", case=False, na=False)]
        neu = pred[pred["Тональность"].str.contains("NEU", case=False, na=False)]

        kpi1, kpi2, kpi3 = st.columns(3)
        kpi1.metric("Доля позитивных", f"{len(pos)/len(pred):.0%}")
        kpi2.metric("Доля негативных", f"{len(neg)/len(pred):.0%}")
        kpi3.metric("Средняя уверенность", f"{pred['Уверенность'].mean():.3f}")

        st.write("Топ уверенных негативных отзывов (очередь поддержки):")
        st.dataframe(
            neg.sort_values("Уверенность", ascending=False).head(10),
            use_container_width=True,
            height=260,
        )

        st.write("Топ уверенных позитивных отзывов (маркетинг и витрина):")
        st.dataframe(
            pos.sort_values("Уверенность", ascending=False).head(10),
            use_container_width=True,
            height=260,
        )


def page_status():
    st.header("Статус системы")
    st.caption("Быстрые проверки для демо")

    cols = st.columns(3)
    with cols[0]:
        st.write("ML-сервис")
        res = _get("/health")
        st.success("Доступен") if res.ok else st.error("Недоступен")
        if res.ok:
            st.json(res.data)
        else:
            st.code(res.err)

    with cols[1]:
        st.write("ClickHouse")
        try:
            r = requests.get("http://clickhouse:8123/ping", timeout=3)
            st.success("Доступен") if r.status_code == 200 else st.error(f"HTTP {r.status_code}")
            st.code(r.text)
        except Exception as e:
            st.error(str(e))

    with cols[2]:
        st.write("Kafka")


def main():
    st.set_page_config(
        page_title="Аналитика отзывов // финальный проект MLOps",
        page_icon="📊",
        layout="wide",
    )
    st.title("Аналитика отзывов // финальный проект MLOps, Торговкина Мария")

    with st.sidebar:
        st.subheader("Навигация")
        page = st.radio(
            "Перейти к разделу",
            ["Онлайн-предсказание", "Аналитика датасета", "Статус системы"],
            index=1,
        )
        st.divider()
        st.caption(
            "Интерфейс обращается к ML-сервису внутри Docker по адресу "
            "`http://ml_service:8000`."
        )

    if page == "Онлайн-предсказание":
        page_live()
    elif page == "Аналитика датасета":
        page_dataset()
    else:
        page_status()


if __name__ == "__main__":
    main()
