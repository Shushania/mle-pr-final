
import os
import psutil
from fastapi import FastAPI
import random
from prometheus_client import Histogram, Gauge
from dotenv import load_dotenv

from .fast_api_handler import FastApiHandler

load_dotenv()
feature_flag = os.getenv('FLAG', 'False').lower() == 'true'

app = FastAPI()
app.handler = FastApiHandler()
if feature_flag:
    from prometheus_fastapi_instrumentator import Instrumentator
    instrumentator = Instrumentator()
    instrumentator.instrument(app).expose(app)
    product_predictions = Histogram(
            "product_predictions",
            "Histogram of product predictions (0 or 1)",
            buckets=[0, 1]  # Бинарные значения 0 и 1
        )
    CPU_USAGE = Gauge('custom_cpu_usage_percent', 'CPU usage percent')
    DISK_USAGE = Gauge('custom_disk_usage_percent', 'Disk usage percent')
    MEMORY_USAGE = Gauge('custom_memory_usage_percent', 'Memory usage percent')



@app.get("/service-status")
def health_check():
    return {"status": "ok"}

@app.post("/predict")
def get_prediction(model_params: dict, product: str = None):
    """
    Функция для получения предсказаний. Если указано поле product, возвращает предсказание для одного продукта.
    Если product не указано, возвращает предсказания для всех доступных продуктов.
    """
    if product:
        # Предсказание для одного продукта
        result = app.handler.handle(model_params, product)
        if feature_flag:
            product_predictions.observe(result['score'])
            CPU_USAGE.set(psutil.cpu_percent(interval=1))
            DISK_USAGE.set(psutil.disk_usage('/').percent)
            MEMORY_USAGE.set(psutil.virtual_memory().percent)
        return {product: result}
    else:
        # Предсказание для всех продуктов
        all_predictions = app.handler.handle_all(model_params)
        if feature_flag:
            for product_name, prediction in all_predictions.items():
                product_predictions.observe(prediction['score'])
            CPU_USAGE.set(psutil.cpu_percent(interval=1))
            DISK_USAGE.set(psutil.disk_usage('/').percent)
            MEMORY_USAGE.set(psutil.virtual_memory().percent)
        return all_predictions
    return price


@app.get("/test_all")
def get_test():
    random_params = {
        'ind_empleado': random.choice(['N', 'A', 'B', 'F', 'S']),  # Символьные значения
        'sexo': random.choice(['H', 'V']),  # 'H' - мужской, 'V' - женский
        'age': random.uniform(18, 100),  # Возраст от 18 до 100 лет
        'ind_nuevo': random.choice([0, 1]),  # 0 - не новый, 1 - новый
        'antiguedad': random.randint(0, 240),  # Стаж в месяцах (максимум 20 лет = 240 месяцев)
        'indrel': random.choice([1, 99]),  # Отношение клиента с банком, 1 или 99 (например, 99 - не активен)
        'tiprel_1mes': random.choice([1, 2, 3, 4]),  # Тип отношений в первый месяц: 1, 2, 3, 4
        'indresi': random.choice([0, 1]),  # 1 - резидент, 0 - нерезидент
        'indext': random.choice([0, 1]),  # 1 - иностранец, 0 - не иностранец
        'canal_entrada': random.choice(['KHQ', 'KFC', 'KAT', 'KHG']),  # Канал привлечения
        'indfall': random.choice([0, 1]),  # 1 - умерший, 0 - живой
        'tipodom': random.choice([1, 2]),  # Тип дома
        'nomprov': random.choice(['ALICANTE', 'BARCELONA', 'MADRID', 'CASTELLON', 'TOLEDO']),  # Провинция
        'ind_actividad_cliente': random.choice([0, 1]),  # Активный клиент или нет
        'renta': random.uniform(10000, 300000),  # Уровень дохода, случайное значение от 10 000 до 300 000
        'segmento': random.choice(['01 - TOP', '02 - PARTICULARES', '03 - UNIVERSITARIO']),  # Сегмент
        'ind_ahor_fin_ult1': random.choice([0, 1])  # Продукт: 0 - нет, 1 - есть
    }
    prediction = app.handler.handle_all_products(random_params)
    print(prediction)
    if feature_flag:
        product_predictions.observe(prediction['score'])
        CPU_USAGE.set(psutil.cpu_percent(interval=1))
        DISK_USAGE.set(psutil.disk_usage('/').percent)
        MEMORY_USAGE.set(psutil.virtual_memory().percent)

    return str(random_params) +'\n' + str(prediction)
