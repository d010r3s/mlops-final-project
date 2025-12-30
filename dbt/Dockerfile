FROM python:3.11-slim
WORKDIR /dbt
COPY requirements.txt /dbt/requirements.txt
RUN pip install --no-cache-dir -r /dbt/requirements.txt
COPY . /dbt
ENV DBT_PROFILES_DIR=/dbt
CMD ["bash", "-lc", "dbt --version"]
