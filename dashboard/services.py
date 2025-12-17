import requests
import pandas as pd

API_BASE_URL = "http://127.0.0.1:8000"
TIMEOUT = 15

def get_adolescentes_por_actividad() -> pd.DataFrame:
    r = requests.get(f"{API_BASE_URL}/reportes/actividad/", timeout=TIMEOUT)
    r.raise_for_status()
    return pd.DataFrame(r.json())
