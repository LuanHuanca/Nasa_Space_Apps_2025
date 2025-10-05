import pandas as pd
import numpy as np
from fastapi import FastAPI
from typing import List, Dict, Any
from functools import lru_cache

# 1️⃣ Inicializar la aplicación FastAPI
app = FastAPI(
    title="Exoplanet Coordinate API",
    description="API para obtener y calcular coordenadas cartesianas de candidatos a exoplanetas (KOI)."
)

# 🌐 URL del archivo CSV de exoplanetas
KOI_URL = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=select+kepoi_name,ra,dec,koi_kepmag+from+cumulative&format=csv"


@lru_cache(maxsize=1)
def calculate_koi_coordinates() -> pd.DataFrame:
    """
    Descarga los datos de KOI, calcula las coordenadas cartesianas (X, Y, Z) 
    y las almacena en caché.
    """
    print("Iniciando descarga y cálculo de coordenadas de KOI...")

    # 1️⃣ Descarga de datos KOI (Cumulative)
    try:
        df = pd.read_csv(KOI_URL)
    except Exception as e:
        print(f"Error al descargar datos: {e}")
        # Retornar un DataFrame vacío o lanzar una excepción de la API si es necesario
        return pd.DataFrame()

    # Eliminar filas con valores nulos en 'ra' o 'dec' para evitar errores de np.deg2rad
    df.dropna(subset=['ra', 'dec'], inplace=True)

    # 2️⃣ Conversión de grados a radianes
    ra_rad = np.deg2rad(df['ra'])
    dec_rad = np.deg2rad(df['dec'])

    # 3️⃣ Asumimos distancia unitaria (r = 1)
    r = 1.0

    # 4️⃣ Cálculo de coordenadas cartesianas
    df['X'] = r * np.cos(dec_rad) * np.cos(ra_rad)
    df['Y'] = r * np.cos(dec_rad) * np.sin(ra_rad)
    df['Z'] = r * np.sin(dec_rad)

    # Seleccionar y renombrar las columnas a devolver (FastAPI las convierte a float por defecto)
    df_result = df[['kepoi_name', 'ra', 'dec', 'X', 'Y', 'Z']].copy()

    print("Cálculo de coordenadas completado.")
    return df_result


@app.get("/api/coordenadas-confirmadas",
         response_model=List[Dict[str, Any]],
         summary="Obtener coordenadas cartesianas de exoplanetas KOI",
         description="Descarga datos de KOI, calcula las coordenadas (X, Y, Z) asumiendo r=1, y devuelve una lista de registros.")
async def get_koi_coordinates(limit: int = 10) -> List[Dict[str, Any]]:
    """
    Endpoint para obtener los datos procesados de KOI.
    - **limit**: Número de registros a devolver (por defecto: 10).
    """
    df_coordinates = calculate_koi_coordinates()

    if df_coordinates.empty:
        return []

    # 5️⃣ Aplica el límite y convierte el DataFrame a formato JSON (lista de diccionarios)
    # df.to_dict(orient="records") es el formato preferido para FastAPI/JSON
    result = df_coordinates.head(limit).to_dict(orient="records")

    return result