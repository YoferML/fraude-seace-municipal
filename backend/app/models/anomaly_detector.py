# backend/app/models/anomaly_detector.py
import joblib
import json
import numpy as np
from backend.app.core.config import settings

class AnomalyDetector:
    def __init__(self):
        try:
            self.model = joblib.load(settings.MODEL_PATH)
            print("🧠 Modelo Isolation Forest cargado correctamente en producción.")
        except Exception as e:
            print(f"❌ Error crítico al cargar el archivo pkl: {e}")
            self.model = None

        try:
            with open(settings.GRAPH_PATH, 'r') as f:
                self.graph_features = json.load(f)
            print("📊 Características estructurales del grafo mapeadas.")
        except Exception as e:
            print(f"❌ Error crítico al cargar las métricas de red: {e}")
            self.graph_features = {}

    def predict(self, monto: float, dias_proceso: int, ruc_proveedor: str, ruc_entidad: str):
        if not self.model:
            return {"error": "El motor analítico no se encuentra disponible."}

        # Extraer métricas de centralidad del grafo (fallback al promedio en caso de nodos nuevos)
        centralidad_prov = self.graph_features.get(ruc_proveedor, 0.01)
        centralidad_muni = self.graph_features.get(ruc_entidad, 0.01)

        # Replicar la distancia matemática al límite legal (8 UIT = S/ 41,200)
        LIMITE_8_UIT = 5150 * 8
        distancia_limite = (LIMITE_8_UIT - monto) / LIMITE_8_UIT

        # Construir vector de entrada respetando el orden estricto del entrenamiento en Colab
        input_data = np.array([[monto, dias_proceso, centralidad_prov, centralidad_muni, distancia_limite]])

        # Calcular score probabilístico mapeado geométricamente
        raw_score = self.model.decision_function(input_data)[0]
        score_riesgo = 1.0 - (raw_score + 0.5)
        score_riesgo = max(0.0, min(1.0, score_riesgo))

        # Determinar clasificación binaria (-1 es anómalo en scikit-learn)
        prediccion_binaria = self.model.predict(input_data)[0]

        return {
            "score_riesgo": round(float(score_riesgo), 4),
            "es_anomalo": bool(prediccion_binaria == -1),
            "centralidad_proveedor": round(float(centralidad_prov), 4)
        }

detector = AnomalyDetector()
