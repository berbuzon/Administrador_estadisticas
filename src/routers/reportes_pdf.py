from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle,
    Paragraph, Spacer, Image
)
from reportlab.lib.units import inch

from src.reports.adolescentes import top10_instituciones, top10_actividades

import io

# --- FIX PARA EL ERROR DE TKINTER ---
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
# -------------------------------------

from src.database.conexiones import get_db
from src.reports.adolescentes import (
    total_adolescentes,
    adolescentes_por_categoria,
    adolescentes_por_institucion,
    adolescentes_por_actividad,
    adolescentes_por_tramo_edad,
    adolescentes_por_genero
)

router = APIRouter(prefix="/reportes-pdf", tags=["PDF"])


# ---------------------------------------------------------
# Gráfico de barras
# ---------------------------------------------------------
def generar_grafico(titulo, etiquetas, valores):
    fig, ax = plt.subplots(figsize=(10, 5))  # tamaño grande
    plt.title(titulo, fontsize=14)
    ax.bar(etiquetas, valores)
    plt.xticks(rotation=45, ha='right', fontsize=8)

    buffer = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buffer, format="png", dpi=150)
    plt.close(fig)
    buffer.seek(0)
    return buffer


# ---------------------------------------------------------
# Gráfico de torta
# ---------------------------------------------------------
def generar_torta(titulo, etiquetas, valores):
    fig, ax = plt.subplots(figsize=(7, 7))  # torta grande
    plt.title(titulo, fontsize=14)
    ax.pie(valores, labels=etiquetas, autopct='%1.1f%%')

    buffer = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buffer, format="png", dpi=150)
    plt.close(fig)
    buffer.seek(0)
    return buffer


# ---------------------------------------------------------
# ENDPOINT PRINCIPAL
# ---------------------------------------------------------
@router.get("/general")
def reporte_general(db: Session = Depends(get_db)):

    buffer = io.BytesIO()
    pdf = SimpleDocTemplate(buffer, pagesize=letter)
    elementos = []
    styles = getSampleStyleSheet()

    # TÍTULO
    elementos.append(Paragraph("<b>Reporte General de Adolescentes</b>", styles["Title"]))
    elementos.append(Spacer(1, 12))

    total = total_adolescentes(db)
    elementos.append(Paragraph(f"<b>Total de adolescentes:</b> {total}", styles["Heading2"]))
    elementos.append(Spacer(1, 12))

    # ---------------------------------------------------------
    # FUNCIÓN INTERNA PARA TABLAS
    # ---------------------------------------------------------
    def tabla_desde_resultados(titulo, data):
        elementos.append(Paragraph(f"<b>{titulo}</b>", styles["Heading3"]))

        total_global = total or 1

        tabla = [["Categoría", "Cantidad", "Porcentaje"]]
        for nombre, cantidad in data:
            porcentaje = (cantidad / total_global) * 100
            tabla.append([nombre, cantidad, f"{porcentaje:.2f}%"])

        t = Table(tabla)
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.lightgrey]),
        ]))

        elementos.append(t)
        elementos.append(Spacer(1, 14))

    # ---------------------------------------------------------
    # TABLAS
    # ---------------------------------------------------------
    tabla_desde_resultados("Adolescentes por Categoría", adolescentes_por_categoria(db))
    tabla_desde_resultados("Adolescentes por Institución", adolescentes_por_institucion(db))
    tabla_desde_resultados("Adolescentes por Actividad", adolescentes_por_actividad(db))
    tabla_desde_resultados("Adolescentes por Tramo de Edad", adolescentes_por_tramo_edad(db))
    tabla_desde_resultados("Adolescentes por Género", adolescentes_por_genero(db))

    # ---------------------------------------------------------
    # GRÁFICOS
    # ---------------------------------------------------------
    def insertar_grafico(titulo, funcion):
        datos = funcion(db)
        etiquetas = [d[0] for d in datos]
        valores = [d[1] for d in datos]

        img_buffer = generar_grafico(titulo, etiquetas, valores)
        img = Image(img_buffer, width=6 * inch, height=3.5 * inch)
        elementos.append(img)
        elementos.append(Spacer(1, 20))

    # Gráficos TOP 10
    insertar_grafico("TOP 10 Instituciones", top10_instituciones)
    insertar_grafico("TOP 10 Actividades", top10_actividades)

    # ---------------------------------------------------------
    # TORTA GÉNERO AGRUPADA
    # ---------------------------------------------------------
    genero = adolescentes_por_genero(db)

    conteo = {"mujer": 0, "varon": 0, "otros": 0}

    for etiqueta, valor in genero:
        e = (etiqueta or "").strip().lower()

        # mujer
        if any(x in e for x in ["mujer", "femenin", "fem", "chica", "f"]):
            conteo["mujer"] += valor

        # varón
        elif any(x in e for x in ["varon", "hombre", "masculin", "masc", "m"]):
            conteo["varon"] += valor

        # otros
        else:
            conteo["otros"] += valor

    etiquetas = list(conteo.keys())
    valores = list(conteo.values())

    img_buffer = generar_torta("Género (agrupado)", etiquetas, valores)
    elementos.append(Image(img_buffer, width=5 * inch, height=5 * inch))
    elementos.append(Spacer(1, 20))

    # ---------------------------------------------------------
    # GENERAR PDF
    # ---------------------------------------------------------
    pdf.build(elementos)
    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": "attachment; filename=reporte_general.pdf"
        }
    )
