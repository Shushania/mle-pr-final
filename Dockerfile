FROM python:3.11-slim
LABEL author=${LABEL}
# Отделяю, чтобы не пересобирать 
COPY requirements.txt ./services/requirements.txt
WORKDIR services 
RUN pip3 install -r requirements.txt

COPY ./service ./service
COPY ./models ./models
COPY ./prometheus ./prometheus

EXPOSE 8000 
# ${MAIN_APP_PORT}
CMD uvicorn service.main:app --reload --port 8000 --host 0.0.0.0