import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime
from modules.financials import calculate_roi, monte_carlo_simulation
from modules.visualizations import plot_timeline, plot_menu, plot_scenarios

# Configuración de la página
st.set_page_config(page_title="Miami Food Truck: Análisis Financiero", layout="wide")
st.markdown('<style>' + open('assets/style.css').read() + '</style>', unsafe_allow_html=True)

# Sidebar para navegación
st.sidebar.title("Miami Food Truck")
st.sidebar.markdown("**Modelo Financiero Interactivo**")
page = st.sidebar.selectbox("Sección", ["Introducción", "Etapas", "Finanzas", "Operaciones", "Menú", "Comparación de Escenarios", "Conclusiones"])

# Cargar datos iniciales
proyecciones = pd.read_csv("data/proyecciones.csv")
menu = pd.read_csv("data/menu.csv")
competitors = pd.read_csv("data/competitors.csv")

# Etapas iniciales (editable)
stages = pd.DataFrame({
    "Etapa": ["Previa", "Inicial", "Desarrollo", "Crecimiento"],
    "Duración (meses)": [1, 3, 6, 27],
    "Pedidos_Dia": [0, 40, 50, 60]  # Escenario Normal
})

# Página: Introducción
if page == "Introducción":
    st.title("Miami Food Truck: Análisis Financiero")
    project_name = st.text_input("Nombre del Proyecto", value="Miami Food Truck")
    start_date = st.date_input("Fecha de Inicio", value=datetime(2025, 6, 1))
    st.markdown(f"""
        **Objetivo**: Evaluar la rentabilidad de {project_name}.  
        **Fecha de inicio**: {start_date.strftime('%d/%m/%Y')}.
    """)
    try:
        st.image("assets/logo.png", caption=project_name, width=400)
    except:
        st.write("(Añade un logo en assets/logo.png)")

# Página: Etapas
elif page == "Etapas":
    st.header("Etapas del Negocio")
    edited_stages = st.data_editor(stages, num_rows="dynamic")
    st.plotly_chart(plot_timeline(edited_stages))

# Página: Finanzas
elif page == "Finanzas":
    st.header("Finanzas")
    tabs = st.tabs(["CAPEX", "OPEX", "Proyecciones", "Monte Carlo"])
    
    with tabs[0]:  # CAPEX
        st.subheader("CAPEX (Inversión Inicial)")
        capex_items = st.data_editor(pd.DataFrame({
            "Ítem": ["Food Truck", "Equipos", "Permisos", "Marketing Inicial"],
            "Costo": [53000, 6950, 1000, 1500]
        }), num_rows="dynamic")
        total_capex = capex_items["Costo"].sum()
        st.write(f"**Total CAPEX**: ${total_capex:,.2f}")

    with tabs[1]:  # OPEX
        st.subheader("OPEX (Costos Operativos Mensuales)")
        opex_items = st.data_editor(pd.DataFrame({
            "Ítem": ["Empleados", "Alquiler", "Marketing", "Servicios"],
            "Costo": [5625, 4000, 3000, 500]
        }), num_rows="dynamic")
        food_cost_pct = st.slider("Food Cost (%)", 20, 40, 30)
        total_opex_base = opex_items["Costo"].sum()

    with tabs[2]:  # Proyecciones
        st.subheader("Proyecciones Financieras")
        scenario = st.selectbox("Escenario", ["Flojo", "Normal", "Fuerte"])
        pedidos_diarios = {"Flojo": 20, "Normal": 40, "Fuerte": 60}[scenario]
        precio_combo = st.number_input("Precio Combo ($)", value=17.5)
        dias_operativos = st.slider("Días Operativos/Semana", 3, 5, 4)
        ingresos_mensuales = pedidos_diarios * precio_combo * dias_operativos * 4
        food_cost = ingresos_mensuales * (food_cost_pct / 100)
        total_opex = total_opex_base + food_cost
        beneficio_mensual = ingresos_mensuales - total_opex
        roi = calculate_roi(ingresos_mensuales, total_opex)
        st.write(f"**Ingresos Mensuales**: ${ingresos_mensuales:,.2f}")
        st.write(f"**OPEX Total**: ${total_opex:,.2f}")
        st.write(f"**Beneficio Mensual**: ${beneficio_mensual:,.2f}")
        st.write(f"**ROI**: {roi:.2f}%")
        if beneficio_mensual > 0:
            st.write(f"**Punto de Equilibrio**: {total_capex / beneficio_mensual:.1f} meses")
        else:
            st.write("**Punto de Equilibrio**: No alcanzable con pérdidas")

    with tabs[3]:  # Monte Carlo
        st.subheader("Simulación Monte Carlo")
        sim_results = monte_carlo_simulation(pedidos_diarios, precio_combo, total_opex_base, dias_operativos, food_cost_pct)
        fig = px.histogram(sim_results, x="Ingresos", title="Distribución de Ingresos Mensuales")
        st.plotly_chart(fig)
        st.write(f"Percentil 10%: ${np.percentile(sim_results['Ingresos'], 10):,.2f}")
        st.write(f"Percentil 50%: ${np.percentile(sim_results['Ingresos'], 50):,.2f}")
        st.write(f"Percentil 90%: ${np.percentile(sim_results['Ingresos'], 90):,.2f}")

# Página: Operaciones
elif page == "Operaciones":
    st.header("Operaciones")
    st.subheader("Estructura de Empleados")
    num_empleados = st.selectbox("Número de Empleados", [2, 3])
    if num_empleados == 2:
        roles = ["Encargado", "Cocinero"]
        costos_hora = [25, 18]
    else:
        roles = ["Encargado", "Cocinero", "Asistente"]
        costos_hora = [25, 18, 15]
    horas_dia = st.slider("Horas por Día", 4, 10, 6)
    dias_semana = st.slider("Días por Semana", 3, 5, 4)
    costo_mensual = sum(costos_hora) * horas_dia * dias_semana * 4
    st.write(f"**Costo Mensual Empleados**: ${costo_mensual:,.2f}")

# Página: Menú
elif page == "Menú":
    st.header("Menú y Recetas")
    edited_menu = st.data_editor(menu, num_rows="dynamic")
    st.plotly_chart(plot_menu(edited_menu))

# Página: Comparación de Escenarios
elif page == "Comparación de Escenarios":
    st.header("Comparación de Escenarios")
    escenarios = ["Flojo", "Normal", "Fuerte"]
    datos = []
    for esc in escenarios:
        pedidos = {"Flojo": 20, "Normal": 40, "Fuerte": 60}[esc]
        ingresos = pedidos * precio_combo * dias_operativos * 4
        food_cost = ingresos * (food_cost_pct / 100)
        total_opex = opex_items["Costo"].sum() + food_cost
        beneficio = ingresos - total_opex
        datos.append([esc, pedidos, ingresos, total_opex, beneficio])
    df = pd.DataFrame(datos, columns=["Escenario", "Pedidos/Día", "Ingresos", "OPEX", "Beneficio"])
    st.table(df)
    st.plotly_chart(plot_scenarios(df))

# Página: Conclusiones
elif page == "Conclusiones":
    st.header("Conclusiones")
    if beneficio_mensual > 0:
        meses_equilibrio = total_capex / beneficio_mensual
        st.write(f"**Retorno de Inversión**: En {meses_equilibrio:.1f} meses.")
    else:
        st.write("**Retorno de Inversión**: No alcanzable con pérdidas.")
    st.write("**Recomendaciones**:")
    if pedidos_diarios < 30:
        st.write("- Aumentar marketing para incrementar pedidos.")
    if food_cost_pct > 35:
        st.write("- Optimizar costos de insumos para reducir food cost.")
