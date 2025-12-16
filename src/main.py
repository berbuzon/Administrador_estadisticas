from fastapi import FastAPI
from dotenv import load_dotenv

# Cargar .env
load_dotenv()
print(">> Variables de entorno cargadas")

# Importar routers correctamente
from src.routers.actividades import router as actividades_router
from src.routers.instituciones import router as instituciones_router
from src.routers.sedes import router as sedes_router
from src.routers.reportes import router as reportes_router
from src.routers.reportes_excel import router as reportes_excel_router
from src.routers.reportes_pdf import router as reportes_pdf_router

app = FastAPI(
    title="API Estadísticas Programa Adolescencia",
    version="1.0",
)

# Incluir routers
app.include_router(actividades_router)
app.include_router(instituciones_router)
app.include_router(sedes_router)
app.include_router(reportes_router)
app.include_router(reportes_excel_router)
app.include_router(reportes_pdf_router)


@app.get("/")
def raiz():
    return {"mensaje": "API funcionando correctamente"}
