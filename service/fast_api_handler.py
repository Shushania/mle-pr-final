# coding: utf-8
"""Класс FastApiHandler, который обрабатывает запросы API."""
import os
import pickle as pkl
import pandas as pd

REQUIRED_PARAMS = [
            'ind_empleado', 'sexo', 'age', 'ind_nuevo', 'antiguedad', 'indrel', 
            'tiprel_1mes', 'indresi', 'indext', 'canal_entrada', 'indfall', 
            'tipodom', 'nomprov', 'ind_actividad_cliente', 'renta', 
            'segmento', 'ind_ahor_fin_ult1' 
        ]
MODEL_PATH = os.path.join(os.getcwd(), 'models')


class FastApiHandler:
    """Class to handle multiple models for FastAPI requests and return predictions."""

    def __init__(self, model_dir=MODEL_PATH):
        """Initialize the class by loading all models and setting the required parameters."""
        self.model_dir = model_dir
        self.models = self.load_all_models()  
        self.required_model_params = self.load_required_params() 

    def load_all_models(self):
        """Loads all models from the directory and stores them in a dictionary."""
        models = {}
        try:
            print(os.listdir(self.model_dir))
            for model_file in os.listdir(self.model_dir):
                if model_file.endswith('_model.pkl'):
                    product_name = model_file.replace('_model.pkl', '')
                    model_path = os.path.join(self.model_dir, model_file)
                    with open(model_path, 'rb') as f:
                        models[product_name] = pkl.load(f)
            print(f"Loaded {len(models)} models successfully.")
        except Exception as e:
            print(f"Failed to load models: {e}")
        return models

    def load_required_params(self):
        """Sets the required features for the models."""
        return REQUIRED_PARAMS

    def product_predict(self, product: str, model_params: dict) -> float:
        """Make a prediction using the appropriate model for the given product."""
        if product not in self.models:
            raise ValueError(f"Model for product '{product}' not found.")
        
        df_sample = pd.DataFrame(model_params, index=[0])
        return self.models[product].predict(df_sample)[0]

    def validate_params(self, params: dict) -> bool:
        """Validate the request parameters."""
        if set(params.keys()) == set(self.required_model_params):
            print("All required parameters are present.")
            return True
        else:
            print("Missing or incorrect parameters.")
            return False

    def handle(self, product: str, params: dict) -> dict:
        """Handle API requests for a specific product and return prediction."""
        try:
            if not self.validate_params(params):
                return {"Error": "Invalid or missing parameters"}

            predicted_value = self.product_predict(product, params)
            return {"product": product, "score": predicted_value}

        except Exception as e:
            print(f"Error while handling request for product '{product}': {e}")
            return {"Error": f"Problem with request: {e}"}

    def handle_all_products(self, params: dict) -> dict:
        """Method to return predictions for all products."""
        try:
            if not self.validate_params(params):
                return {"Error": "Invalid or missing parameters"}

            # Iterate over all products and collect predictions
            predictions = {}
            for product in self.models.keys():
                predicted_value = self.product_predict(product, params)
                print(product, predicted_value)
                predictions[product] = predicted_value
            return {"predictions": predictions}

        except Exception as e:
            print(f"Error while handling request: {e}")
            return {"Error": f"Problem with request: {e}"}


# Пример использования
if __name__ == "__main__":

    # Тестовый запрос
    test_params = {
        'ind_empleado': 'N',
        'sexo': 'V',
        'age': 30,
        'ind_nuevo': 0,
        'antiguedad': 60,
        'indrel': 1,
        'tiprel_1mes': 'A',
        'indresi': 1,
        'indext': 1,
        'canal_entrada': 'KHE',
        'indfall': 1,
        'tipodom': 1,
        'nomprov': 'MADRID',
        'ind_actividad_cliente': 1,
        'renta': 45000,
        'segmento': '02 - PARTICULARES',
        'ind_ahor_fin_ult1': 0
    }

    # Создаем обработчик запросов для API
    handler = FastApiHandler(model_dir="../models")

    # Делаем предсказание для всех продуктов сразу
    response = handler.handle_all_products(test_params)
    print(f"Response: {response}")
