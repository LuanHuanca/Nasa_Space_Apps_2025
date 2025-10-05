import joblib
import pandas as pd
import numpy as np
import requests
from fastapi import FastAPI
from typing import List, Dict, Any
from functools import lru_cache
from pathlib import Path  # ✅ faltaba importar

# 1️⃣ Inicializar la aplicación FastAPI
app = FastAPI(
    title="Exoplanet Coordinate API",
    description="API para obtener y calcular coordenadas cartesianas de candidatos a exoplanetas (KOI)."
)

# 🌐 URL del archivo CSV de exoplanetas
KOI_URL = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=select+kepoi_name,ra,dec,koi_kepmag+from+cumulative&format=csv"


labels = {0: "Candidate", 1: "False Positive"}  # Ajusta según tu entrenamiento

# 🌐 URL de candidatos
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


@lru_cache(maxsize=1)
def calculate_koi_coordinates() -> pd.DataFrame:
    """Descarga datos de KOI, calcula coordenadas cartesianas (X, Y, Z)."""
    print("Iniciando descarga y cálculo de coordenadas de KOI...")

    try:
        df = pd.read_csv(KOI_URL)
    except Exception as e:
        print(f"Error al descargar datos: {e}")
        return pd.DataFrame()

    df.dropna(subset=['ra', 'dec'], inplace=True)

    ra_rad = np.deg2rad(df['ra'])
    dec_rad = np.deg2rad(df['dec'])
    r = 1.0

    df['X'] = r * np.cos(dec_rad) * np.cos(ra_rad)
    df['Y'] = r * np.cos(dec_rad) * np.sin(ra_rad)
    df['Z'] = r * np.sin(dec_rad)

    df_result = df[['kepoi_name', 'ra', 'dec', 'X', 'Y', 'Z']].copy()
    print("Cálculo de coordenadas completado.")
    return df_result


@app.get("/api/coordenadas-confirmadas",
         response_model=List[Dict[str, Any]],
         summary="Obtener coordenadas cartesianas de exoplanetas KOI")
async def get_koi_coordinates(limit: int = 10) -> List[Dict[str, Any]]:
    df_coordinates = calculate_koi_coordinates()
    if df_coordinates.empty:
        return []
    return df_coordinates.head(limit).to_dict(orient="records")


# 📂 Ruta al modelo entrenado
MODEL_DIR = Path("./modelo")
MODEL_PATH = MODEL_DIR / "exoplanet_classifier_model.pkl"
PREPROCESSOR_PATH = MODEL_DIR / "exoplanet_preprocessor.pkl"
COLUMNS_PATH = MODEL_DIR / "original_columns.pkl"

model = joblib.load(MODEL_PATH)
preprocessor = joblib.load(PREPROCESSOR_PATH)
required_columns = joblib.load(COLUMNS_PATH)

print("✅ Modelo, preprocesador y columnas cargados correctamente")


# 🔮 Función para predecir con el modelo ML
def predict_with_pipeline(features: dict):
    """Preprocesa y predice si un candidato es exoplaneta válido."""
    row = {col: features.get(col, None) for col in required_columns}
    df = pd.DataFrame([row])

    # Preprocesamiento
    X_processed = preprocessor.transform(df)

    # Predicción
    prediction = model.predict(X_processed)[0]

    prob = None
    if hasattr(model, "predict_proba"):
        prob = model.predict_proba(X_processed).max()

    return {
        "prediction": labels[prediction],
        "probability": float(prob) if prob is not None else None
    }


@app.get("/api/exoplanetas-candidatos-ml",
         response_model=List[Dict[str, Any]],
         summary="Exoplanetas candidatos con coordenadas y predicción ML")
async def get_exoplanet_candidates_ml(limit: int = 5) -> List[Dict[str, Any]]:
    try:
        response = requests.get(CANDIDATE_URL)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"Error al obtener datos de candidatos: {e}")
        return []

    results = []

    for planet in data[:limit]:
        kepid = planet.get("kepid")
        kepoi_name = planet.get("kepoi_name")
        ra = planet.get("ra")
        dec = planet.get("dec")

        # --- Calcular coordenadas cartesianas
        if ra is not None and dec is not None:
            ra_rad = np.deg2rad(ra)
            dec_rad = np.deg2rad(dec)
            r = 1.0
            X = r * np.cos(dec_rad) * np.cos(ra_rad)
            Y = r * np.cos(dec_rad) * np.sin(ra_rad)
            Z = r * np.sin(dec_rad)
        else:
            X, Y, Z = None, None, None

        # --- Features para el modelo
        features = {k: v for k, v in planet.items()
                    if k not in ["kepid", "kepoi_name", "ra_str", "dec_str"]}

        # --- Predicción con el modelo
        ml_result = predict_with_pipeline(features)

        results.append({
            "kepid": kepid,
            "kepoi_name": kepoi_name,
            "X": X,
            "Y": Y,
            "Z": Z,
            "ml_result": ml_result
        })

    return results
