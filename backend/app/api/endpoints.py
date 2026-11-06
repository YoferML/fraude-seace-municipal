# backend/app/api/endpoints.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from backend.app.models.anomaly_detector import detector

router = APIRouter()

# Definir el esquema de validación de los datos de entrada
class ContratoInput(BaseModel):
    monto_adjudicado: float = Field(..., description="Monto del contrato en Soles", gt=0)
    dias_proceso: int = Field(..., description="Días transcurridos para la aprobación de la orden", ge=0)
    ruc_proveedor: str = Field(..., description="RUC de la empresa proveedora")
    ruc_entidad: str = Field(..., description="RUC de la entidad municipal que contrata")

@router.post("/predict")
def evaluar_contrato(datos: ContratoInput):
    try:
        # Enviar las variables validadas al motor analítico cargado del .pkl
        resultado = detector.predict(
            monto=datos.monto_adjudicado,
            dias_proceso=datos.dias_proceso,
            ruc_proveedor=datos.ruc_proveedor,
            ruc_entidad=datos.ruc_entidad
        )
        return resultado
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el procesamiento analítico: {str(e)}")

