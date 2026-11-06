# 🔍 Sistema Inteligente de Fiscalización Contractual (SEACE) - Auditoría TI

Este proyecto implementa un motor analítico de detección de anomalías y riesgo de fraude en las órdenes de compra estatales menores o iguales a 8 UIT (S/ 41,200) emitidas por entidades municipales. Combina **Ciencia de Redes (Network Science)** y **Aprendizaje No Supervisado** para identificar de forma automatizada patrones de fraccionamiento de contratos y colusión estructurada.

Desarrollado bajo un enfoque híbrido, el modelo matemático fue entrenado en **Google Colab** y desplegado en producción mediante una arquitectura de microservicios con **FastAPI** (Backend) e **HTML/CSS/JS nativo** (Frontend), corriendo sobre servidores **Render**.

---

## 📊 Arquitectura Matemática y Enfoque de ML

El sistema aborda el problema desde el paradigma del **Aprendizaje No Supervisado**, dado que las bases de datos abiertas del SEACE no cuentan con etiquetas históricas de corrupción (*Ground Truth*).

### 1. Ciencia de Redes (Network Science)
Las interacciones contractuales se modelaron utilizando un **Grafo Bipartito No Dirigido** \(G = (V_F, V_P, E)\), donde:
*   \(V_F\) representa el conjunto de nodos de las Entidades/Funcionarios Municipales.
*   \(V_P\) representa el conjunto de nodos de los Proveedores (RUCs).
*   \(E\) representa las aristas, ponderadas por el monto acumulado adjudicado (\(W\)).

Se extrajo la **Centralidad de Grado (Degree Centrality)** para cada nodo en la red:
\[C_D(v) = \frac{deg(v)}{\vert{}V\vert{} - 1}\]
Esta métrica estructural permite identificar cuantitativamente el acaparamiento y la concentración atípica de contratos entre proveedores y municipios específicos.

### 2. Algoritmo de Aislamiento Geométrico (Isolation Forest)
En lugar de perfilar el comportamiento normal, se utilizó un **Isolation Forest** (200 estimadores) para aislar observaciones de forma aleatoria en un espacio hiperdimensional. Las anomalías (contratos fraudulentos) requieren significativamente menos particiones lineales para ser aisladas, quedando en las ramas más cortas de los árboles de decisión.

**Variables numéricas seleccionadas (*Features*):**
*   `monto_adjudicado`: Monto total de la orden de compra.
*   `dias_proceso`: Tiempos transcurridos para la aprobación de la orden.
*   `centralidad_proveedor`: Concentración del RUC en el grafo histórico.
*   `centralidad_funcionario`: Concentración de la entidad en la red.
*   `distancia_limite_uit`: Métrica lineal que mide la proximidad al límite legal de elusión de licitaciones:
    \[\text{Distancia} = \frac{\text{Límite 8 UIT} - \text{Monto Adjudicado}}{\text{Límite 8 UIT}}\]

---

## 🧪 Rendimiento Matemático y Validación

Para auditar el rendimiento del modelo no supervisado en el laboratorio, se inyectaron patrones sintéticos controlados de fraude (fraccionamiento al límite de la UIT y colusión de red). Los resultados de la validación arrojaron las siguientes métricas:

*   **F1-Score (Clase Anomalía):** `0.94` (Precisión: `0.90` / Recall: `1.00`)
*   **Coeficiente de Silueta (Silhouette Score):** `0.4403` (Confirma una separación geométrica saludable de las densidades anómalas fuera del patrón normal).
*   **Eficacia de Captura:** El modelo logró aislar correctamente el **99.56%** del fraude inducido.

---

## 📂 Estructura del Proyecto

```text
📦 fraude-seace-municipal
 ┣ 📂 backend                 # Servidor API construido en FastAPI
 ┃ ┣ 📂 app
 ┃ ┃ ┣ 📂 api                 # Endpoints y validación de esquemas Pydantic
 ┃ ┃ ┣ 📂 core                # Configuraciones dinámicas de entorno y PATHs
 ┃ ┃ ┗ 📂 models              # Deserializador del motor analítico
 ┃ ┗ 📜 requirements.txt      # Dependencias congeladas para producción en Render
 ┣ 📂 frontend                # Interfaz Web del Dashboard de Fiscalización
 ┃ ┣ 📂 css                   # Hojas de estilo y UI semafórica
 ┃ ┣ 📂 js                    # Consumo asíncrono de la API mediante Fetch dinámico
 ┃ ┗ 📜 index.html            # Maquetación del panel de control
 ┣ 📂 notebooks               # Respaldo y apuntes de investigación en Google Colab
 ┣ 📂 serialized_models       # Modelos e inteligencia serializada (.pkl y .json)
 ┣ 📜 .gitignore              # Filtros de exclusión para datos pesados y venv
 ┗ 📜 README.md               # Documentación científica y técnica del portafolio
```

---

## 🛠️ Instalación y Uso Local

1. Clonar el repositorio y acceder a la carpeta raíz:
```bash
git clone https://github.com
cd fraude-seace-municipal
```

2. Crear y activar el entorno virtual de Python:
```bash
python -m venv venv
# En Windows (PowerShell)
.\venv\Scripts\Activate.ps1
```

3. Instalar dependencias del servidor:
```bash
pip install -r backend/requirements.txt
```

4. Lanzar el backend localmente:
```bash
python -m uvicorn backend.app.main:app --reload
```

5. Abrir la interfaz web (`frontend/index.html`) mediante un servidor web local (como la extensión Live Server de VS Code) para interactuar con el modelo a través de `http://127.0.0.1:5500`.
