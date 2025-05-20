# modules/visualizations.py
import plotly.express as px
import pandas as pd

def plot_timeline(stages):
    df = pd.DataFrame({
        "fase": stages["etapa"],
        "inicio": [0] + [sum(stages["duración (meses)"][:i+1]) for i in range(len(stages)-1)],
        "fin": stages["duración (meses)"].cumsum()
    })
    fig = px.timeline(df, x_start="inicio", x_end="fin", y="fase", title="hoja de ruta")
    return fig

def plot_menu(menu):
    fig = px.bar(menu, x="Plato", y=["Costo", "Precio Sugerido"], title="costos vs precios del menú", barmode="group")
    return fig

def plot_scenarios(df):
    fig = px.bar(df, x="escenario", y=["ingresos", "opex", "beneficio"], title="comparación de escenarios", barmode="group")
    return fig

def plot_swot():
    df = pd.DataFrame({
        "categoría": ["fortalezas", "debilidades", "oportunidades", "amenazas"],
        "valor": [8, 5, 7, 6]
    })
    fig = px.bar(df, x="categoría", y="valor", title="análisis swot", color="categoría")
    return fig

def plot_competitors(competitors):
    fig = px.bar(competitors, x="Restaurante", y="Combo", title="precios de competencia")
    return fig
