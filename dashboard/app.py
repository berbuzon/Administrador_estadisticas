import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

from services import get_adolescentes_por_actividad

# ----------------------------------------
# Carga inicial de datos
# ----------------------------------------

df = get_adolescentes_por_actividad()
print("Columnas recibidas:", df.columns.tolist())

# Limpieza mínima defensiva
df = df.dropna(subset=["Actividad", "Institucion"])

# Lista de instituciones para el filtro
instituciones = sorted(df["Institucion"].unique())

# ----------------------------------------
# App Dash
# ----------------------------------------

app = Dash(__name__)

app.layout = html.Div(
    style={"width": "90%", "margin": "auto"},
    children=[

        html.H1(
            "Adolescentes confirmados por actividad",
            style={"textAlign": "center"}
        ),

        html.Hr(),

        # ----------- Filtro -----------
        html.Label("Institución"),
        dcc.Dropdown(
            id="institucion-dropdown",
            options=[{"label": i, "value": i} for i in instituciones],
            value=instituciones[0],  # valor inicial
            clearable=False
        ),

        html.Br(),

        # ----------- Gráfico -----------
        dcc.Graph(id="grafico-actividades")
    ]
)

# ----------------------------------------
# Callback (interactividad)
# ----------------------------------------

@app.callback(
    Output("grafico-actividades", "figure"),
    Input("institucion-dropdown", "value")
)
def actualizar_grafico(institucion_seleccionada):

    df_filtrado = df[df["Institucion"] == institucion_seleccionada]

    df_plot = (
        df_filtrado
        .groupby("Actividad")
        .size()
        .reset_index(name="cantidad")
        .sort_values("cantidad", ascending=False)
    )

    fig = px.bar(
        df_plot,
        x="Actividad",
        y="cantidad",
        title=f"Adolescentes confirmados por actividad – {institucion_seleccionada}",
        labels={
            "Actividad": "Actividad",
            "cantidad": "Cantidad de adolescentes"
        }
    )

    fig.update_layout(
        xaxis_tickangle=-45,
        margin=dict(t=80)
    )

    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
