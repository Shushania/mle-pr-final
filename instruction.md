# Инструкция по запуску приложения

## 1. Создание файла `.env`

Для настройки окружения создайте файл `.env` в корневой директории вашего проекта и добавьте в него следующие переменные:

```
MAIN_APP_PORT=8000
APP_VM_PORT=4601
AUTHOR="mle-student"
FLAG='false' # для локального запуска
GRAFANA_USER='admin'
GRAFANA_PASS='admin'
PROMETHEUS_PORT=9090
GRAFANA_PORT=3000```


```plaintext
MAIN_APP_PORT: Порт, на котором будет доступен ваш FastAPI сервис.
APP_VM_PORT: Порт для взаимодействия с виртуальной машиной (если используется).
AUTHOR: Имя автора проекта.
FLAG: Флаг для локального запуска. Установите 'false' для отключения дополнительных фич (например, метрик).
GRAFANA_USER: Имя пользователя для Grafana.
GRAFANA_PASS: Пароль для Grafana.
PROMETHEUS_PORT: Порт для Prometheus.
GRAFANA_PORT: Порт для Grafana.
```
## 2. Запуск локально

Для запуска FastAPI приложения локально используйте Uvicorn. Выполните следующую команду:
`uvicorn service.main:app`
## 3. Запуск из Docker

Для запуска приложения и связанных сервисов (Prometheus, Grafana) с использованием Docker, выполните:

`docker-compose up`
Эта команда запустит все сервисы, определенные в вашем docker-compose.yml файле. 

## 4. Проверка работоспособности

После запуска приложения вы можете проверить его работоспособность, отправив запрос на ручку /test_all. 

Пример запроса с использованием curl:
`curl http://localhost:8000/test_all `
