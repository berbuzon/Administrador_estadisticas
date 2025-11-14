from fastapi import FastAPI
from src.routers import actividades, instituciones, sedes

app = FastAPI(
    title="API Estadísticas Programa Adolescencia",
    version="1.0",
)

app.include_router(actividades.router)
app.include_router(instituciones.router)
app.include_router(sedes.router)

@app.get("/")
def raiz():
    return {"mensaje": "API funcionando correctamente"}

