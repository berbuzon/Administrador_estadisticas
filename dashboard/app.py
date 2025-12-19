from dash import Dash, dcc, html, Input, Output
import plotly.express as px

from services import get_actividad_detalle

# ----------------------------------------
# Datos
# ----------------------------------------

df = get_actividad_detalle()
df = df.dropna(subset=["actividad", "institucion"])

instituciones = sorted(df["institucion"].unique())

import pandas as pd

# ----------------------------------------
# PRE-CÁLCULOS GLOBALES
# ----------------------------------------

# Total de adolescentes por institución (global)
conteo_por_institucion = (
    df.groupby("institucion")
      .size()
      .reset_index(name="total_adolescentes")
)

# Cuartiles institucionales
conteo_por_institucion["cuartil"] = pd.qcut(
    conteo_por_institucion["total_adolescentes"],
    4,
    labels=["Q1", "Q2", "Q3", "Q4"]
)

mapa_cuartil = {
    "Q1": "Q1 – menor volumen",
    "Q2": "Q2 – medio bajo",
    "Q3": "Q3 – medio alto",
    "Q4": "Q4 – mayor volumen"
}


# ----------------------------------------
# App
# ----------------------------------------

app = Dash(__name__)

app.layout = html.Div(
    style={"width": "90%", "margin": "auto"},
    children=[

        html.H1(
            "Adolescentes confirmados por actividad",
            style={"textAlign": "center"}
        ),

        # -------- KPIs --------
        html.Div(
            style={
                "display": "flex",
                "justifyContent": "space-between",
                "marginBottom": "20px"
            },
            children=[

                html.Div(
                    id="kpi-total-adolescentes",
                    style={
                        "flex": "1",
                        "padding": "15px",
                        "margin": "5px",
                        "border": "1px solid #ccc",
                        "borderRadius": "8px",
                        "textAlign": "center"
                    }
                ),

                html.Div(
                    id="kpi-cuartil-institucional",
                    style={
                        "flex": "1",
                        "padding": "15px",
                        "margin": "5px",
                        "border": "1px solid #ccc",
                        "borderRadius": "8px",
                        "textAlign": "center"
                    }
                ),

                html.Div(
                    id="kpi-total-talleres",
                    style={
                        "flex": "1",
                        "padding": "15px",
                        "margin": "5px",
                        "border": "1px solid #ccc",
                        "borderRadius": "8px",
                        "textAlign": "center"
                    }
                ),
            ]
        ),

        html.Label("Institución"),
        dcc.Dropdown(
            id="institucion-dropdown",
            options=[{"label": i, "value": i} for i in instituciones],
            value=instituciones[0],
            clearable=False
        ),

        dcc.Graph(id="grafico-actividades")
    ]
)


# ----------------------------------------
# Callback
# ----------------------------------------

@app.callback(
    Output("grafico-actividades", "figure"),
    Output("kpi-total-adolescentes", "children"),
    Output("kpi-cuartil-institucional", "children"),
    Output("kpi-total-talleres", "children"),
    Input("institucion-dropdown", "value")
)
def actualizar_dashboard(institucion):

    df_filtrado = df[df["institucion"] == institucion]

    # KPI 1 — Total adolescentes
    total_adolescentes = len(df_filtrado)
    kpi_total_adolescentes = [
        html.H3(total_adolescentes),
        html.P("Total adolescentes")
    ]

    # KPI 2 — Cuartil institucional
    cuartil = (
        conteo_por_institucion
        .loc[
            conteo_por_institucion["institucion"] == institucion,
            "cuartil"
        ]
        .iloc[0]
    )

    kpi_cuartil = [
        html.H3(mapa_cuartil[str(cuartil)]),
        html.P("Cuartil institucional")
    ]

    # KPI 3 — Total talleres
    total_talleres = len(df_filtrado)
    kpi_total_talleres = [
        html.H3(total_talleres),
        html.P("Total talleres")
    ]

    # Gráfico
    df_plot = (
        df_filtrado
        .groupby("actividad")
        .size()
        .reset_index(name="cantidad")
        .sort_values("cantidad", ascending=False)
    )

    fig = px.bar(
        df_plot,
        x="actividad",
        y="cantidad",
        title=f"Adolescentes confirmados por actividad – {institucion}",
        labels={
            "actividad": "Actividad",
            "cantidad": "Cantidad de adolescentes"
        }
    )

    fig.update_layout(xaxis_tickangle=-45)

    return fig, kpi_total_adolescentes, kpi_cuartil, kpi_total_talleres



if __name__ == "__main__":
    app.run(debug=True)
