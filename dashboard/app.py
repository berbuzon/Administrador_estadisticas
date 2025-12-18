from dash import Dash, dcc, html, Input, Output
import plotly.express as px

from services import get_actividad_detalle

# ----------------------------------------
# Datos
# ----------------------------------------

df = get_actividad_detalle()
df = df.dropna(subset=["actividad", "institucion"])

instituciones = sorted(df["institucion"].unique())

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
    Input("institucion-dropdown", "value")
)
def actualizar_grafico(institucion):

    df_filtrado = df[df["institucion"] == institucion]

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

    return fig


if __name__ == "__main__":
    app.run(debug=True)
