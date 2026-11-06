# backend/app/core/config.py
import os

class Settings:
    PROJECT_NAME: str = "Sistema de Alertas SEACE - Municipalidad"
    
    # Apunta a la raíz de la carpeta 'backend'
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    # Sube un nivel a la raíz del proyecto para buscar 'serialized_models'
    ROOT_DIR: str = os.path.dirname(BASE_DIR)
    
    # Rutas absolutas finales de los artefactos de Colab
    MODEL_PATH: str = os.path.join(ROOT_DIR, "serialized_models", "isolation_forest.pkl")
    GRAPH_PATH: str = os.path.join(ROOT_DIR, "serialized_models", "graph_features.json")

settings = Settings()
