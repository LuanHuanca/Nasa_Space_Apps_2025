import logging
from pathlib import Path
from functools import lru_cache
from typing import List, Dict, Any, Optional

import joblib
import pandas as pd
import numpy as np
import requests
from fastapi import FastAPI,HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

origins = [
    "http://localhost:3000",
    "http://localhost:5173",
]


# Inicializar FastAPI
app = FastAPI(
    title="Exoplanet Coordinate API",
    description="API para obtener y calcular coordenadas cartesianas de candidatos a exoplanetas (KOI)."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          # Lista de orígenes permitidos
    allow_credentials=True,         # Permitir cookies y encabezados de autenticación
    allow_methods=["*"],            # Permitir todos los métodos (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],            # Permitir todos los encabezados
)

# URLs de datos
KOI_URL = (
    "https://exoplanetarchive.ipac.caltech.edu/TAP/sync?"
    "query=select+kepoi_name,ra,dec,koi_kepmag+from+cumulative&format=json"
)

CANDIDATE_URL = (
    "https://exoplanetarchive.ipac.caltech.edu/cgi-bin/nstedAPI/nph-nstedAPI?"
    "table=cumulative&where=koi_disposition%20like%20%27CANDIDATE%27"
    "&where=koi_period%3E300,koi_prad%3C2&order=koi_period&format=json"
    "&select=kepid,kepoi_name,koi_score,koi_fpflag_nt,koi_fpflag_ss,"
    "koi_fpflag_co,koi_fpflag_ec,koi_period,koi_period_err1,koi_period_err2,"
    "koi_time0bk,koi_time0bk_err1,koi_time0bk_err2,koi_impact,koi_impact_err1,"
    "koi_impact_err2,koi_duration,koi_duration_err1,koi_duration_err2,"
    "koi_depth,koi_depth_err1,koi_depth_err2,koi_prad,koi_prad_err1,"
    "koi_prad_err2,koi_teq,koi_teq_err1,koi_teq_err2,koi_insol,koi_insol_err1,"
    "koi_insol_err2,koi_model_snr,koi_tce_plnt_num,koi_tce_delivname,"
    "koi_steff,koi_steff_err1,koi_steff_err2,koi_slogg,koi_slogg_err1,"
    "koi_slogg_err2,koi_srad,koi_srad_err1,koi_srad_err2,ra,dec,ra_str,dec_str,koi_kepmag"
)

labels = {0: "Candidate", 1: "False Positive"}

# Paths de modelo
MODEL_DIR = Path("./modelo")
MODEL_PATH = MODEL_DIR / "exoplanet_classifier_model.pkl"
PREPROCESSOR_PATH = MODEL_DIR / "exoplanet_preprocessor.pkl"
COLUMNS_PATH = MODEL_DIR / "original_columns.pkl"

model = None
preprocessor = None
required_columns: List[str] = []


def _convert_to_float(value: Any) -> float:
    """Convierte un valor a float o devuelve NaN si falla."""
    try:
        return float(value)
    except (ValueError, TypeError):
        return np.nan


def _calculate_cartesian(ra: float, dec: float, r: float = 1.0) -> Optional[Dict[str, float]]:
    """Convierte coordenadas RA/DEC a coordenadas cartesianas X,Y,Z."""
    if np.isnan(ra) or np.isnan(dec):
        return None
    ra_rad = np.deg2rad(ra)
    dec_rad = np.deg2rad(dec)
    return {
        "X": r * np.cos(dec_rad) * np.cos(ra_rad),
        "Y": r * np.cos(dec_rad) * np.sin(ra_rad),
        "Z": r * np.sin(dec_rad),
    }


@lru_cache(maxsize=1)
def calculate_koi_coordinates() -> pd.DataFrame:
    """Descarga datos KOI y calcula coordenadas cartesianas."""
    logger.info("Descargando datos de candidatos KOI...")
    try:
        response = requests.get(CANDIDATE_URL, timeout=20)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        logger.error(f"Error al obtener datos KOI: {e}")
        return pd.DataFrame()

    df = pd.DataFrame(data)
    df["ra"] = df["ra"].apply(_convert_to_float)
    df["dec"] = df["dec"].apply(_convert_to_float)
    df.dropna(subset=["ra", "dec"], inplace=True)

    coords = df.apply(lambda row: _calculate_cartesian(row["ra"], row["dec"]), axis=1)
    coords_df = pd.DataFrame(list(coords))

    df_result = pd.concat([df[["kepoi_name", "ra", "dec"]].reset_index(drop=True), coords_df], axis=1)
    logger.info("Cálculo de coordenadas completado.")
    return df_result


@app.get(
    "/api/coordenadas-candidatos",
    response_model=List[Dict[str, Any]],
    summary="Obtener coordenadas cartesianas de candidatos a exoplanetas KOI",
)
async def get_koi_coordinates(limit: int = 10) -> List[Dict[str, Any]]:
    df_coordinates = calculate_koi_coordinates()
    return [] if df_coordinates.empty else df_coordinates.head(limit).to_dict(orient="records")


# ==========================
#   CARGA DE MODELO ML
# ==========================

try:
    model = joblib.load(MODEL_PATH)
    preprocessor = joblib.load(PREPROCESSOR_PATH)
    required_columns = joblib.load(COLUMNS_PATH)
    logger.info("✅ Modelo, preprocesador y columnas cargados correctamente")
except FileNotFoundError:
    logger.warning("⚠️ Archivos ML no encontrados en './modelo'. Endpoints ML no estarán disponibles.")
except Exception as e:
    logger.error(f"❌ Error al cargar el modelo ML: {e}")


def predict_with_pipeline(features: dict) -> Dict[str, Any]:
    """Ejecuta predicción ML dado un diccionario de features."""
    if model is None or preprocessor is None:
        return {"prediction": "Modelo no cargado", "probability": None}

    row = {col: _convert_to_float(features.get(col)) for col in required_columns}
    df = pd.DataFrame([row])

    try:
        X_processed = preprocessor.transform(df)
        prediction = model.predict(X_processed)[0]
        prob = model.predict_proba(X_processed).max() if hasattr(model, "predict_proba") else None
    except Exception as e:
        logger.error(f"Error en predicción ML: {e}")
        return {"prediction": "Error en predicción", "probability": None}

    return {"prediction": labels.get(prediction, "Unknown"), "probability": float(prob) if prob else None}


@app.get(
    "/api/exoplanetas-candidatos-ml",
    response_model=List[Dict[str, Any]],
    summary="Exoplanetas candidatos con coordenadas y predicción ML",
)
async def get_exoplanet_candidates_ml(limit: int = 5) -> List[Dict[str, Any]]:
    if model is None or preprocessor is None:
        return [{"error": "Modelo ML no disponible. Verifique los archivos en ./modelo"}]

    try:
        response = requests.get(CANDIDATE_URL, timeout=20)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        logger.error(f"Error al obtener datos de candidatos: {e}")
        return []

    results = []
    for planet in data[:limit]:
        kepoi_name = planet.get("kepoi_name")
        ra = _convert_to_float(planet.get("ra"))
        dec = _convert_to_float(planet.get("dec"))

        coords = _calculate_cartesian(ra, dec) or {"X": None, "Y": None, "Z": None}
        features = {k: v for k, v in planet.items() if k not in ["kepid", "kepoi_name", "ra_str", "dec_str"]}

        ml_result = predict_with_pipeline(features)

        results.append({
            "kepoi_name": kepoi_name,
            **coords,
            "ml_result": ml_result,
        })

    return results

@app.post(
    "/api/predict-exoplanet",
    summary="Realizar predicción de exoplaneta con datos enviados por el cliente",
)
async def predict_exoplanet(data: Dict[str, Any] = Body(...)) -> Dict[str, Any]:
    """
    Recibe datos de entrada en formato JSON, los pasa al modelo ML y devuelve la predicción.
    Ejemplo de entrada:
    {
        "koi_period": 372.53,
        "koi_prad": 1.12,
        "koi_teq": 579.43,
        "koi_insol": 1.0,
        "koi_model_snr": 12.3,
        ...
    }
    """
    # Verificar que el modelo esté cargado
    if model is None or preprocessor is None:
        raise HTTPException(status_code=503, detail="Modelo ML no disponible. Verifique los archivos en ./modelo")

    # Validar que se enviaron datos
    if not data:
        raise HTTPException(status_code=400, detail="No se enviaron datos para la predicción.")

    # Realizar predicción
    result = predict_with_pipeline(data)

    logger.info(f"Predicción realizada: {result}")
    return {
        "prediction": result["prediction"],
        "probability": result["probability"]
    }
