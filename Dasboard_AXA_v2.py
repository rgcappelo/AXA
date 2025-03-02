import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime

# Configuración de página Streamlit
st.set_page_config(
    page_title="Dashboard NPS Avanzado AXA",
    page_icon="📊",
    layout="wide"
)

# Título principal
st.title("CONSTRUCCIÓN DEL NUEVO KPI: NET PROMOTER SCORE (NPS) AVANZADO PARA AXA")

# Sección de Introducción
st.markdown("""
### Introducción
Basándonos en el análisis previo del caso de AXA y en las recomendaciones consensuadas en el panel de expertos, 
desarrollaremos un nuevo KPI de Net Promoter Score (NPS) que supere las limitaciones tradicionales 
y se integre con los KPIs normales de AXA.

Este nuevo KPI responderá a tres perspectivas clave:
- **NPS Predictivo y Accionable (dNPS)**: Enfocado en la anticipación en tiempo real mediante machine learning y datos de comportamiento.
- **NPS de Confianza y Viralidad (tNPS + sNPS)**: Reflejando la confianza en la aseguradora y su capacidad de generar recomendaciones orgánicas en redes sociales.
- **NPS Personalizado por Sector**: Adaptando las métricas a seguros, banca o negocios digitales, según la naturaleza del cliente.
""")

st.markdown("---")

# Carga de datos
@st.cache_data
def load_data():
    # Fechas de datos históricos (36 meses) y proyectados (6 meses)
    dates = pd.date_range(start="2022-01-01", periods=37, freq='M')
    future_dates = pd.date_range(start="2025-03-01", periods=6, freq='M')

    # Datos históricos
    dNPS = [62, 58, 65, 67, 70, 72, 68, 60, 64, 69, 73, 75, 78, 76, 74, 70, 68, 71, 69, 72, 74, 76, 77, 78, 80, 82, 85, 83, 81, 79, 78, 80, 82, 85, 88, 86, 84]
    tNPS = [75, 72, 74, 78, 80, 82, 79, 76, 78, 81, 83, 85, 87, 85, 83, 81, 80, 83, 81, 84, 86, 88, 89, 90, 91, 92, 94, 93, 92, 90, 89, 90, 91, 93, 95, 96, 94]
    sNPS = [50, 48, 52, 55, 57, 60, 58, 54, 56, 59, 62, 64, 67, 65, 63, 60, 58, 61, 60, 63, 65, 67, 68, 70, 71, 73, 75, 74, 72, 70, 68, 70, 72, 74, 76, 78, 76]

    # Datos proyectados (6 meses futuros)
    future_dNPS = [85, 87, 89, 90, 92, 94]
    future_tNPS = [96, 97, 98, 99, 99, 100]
    future_sNPS = [78, 80, 82, 83, 85, 87]

    # Creación de DataFrame
    df_nps = pd.DataFrame({'Fecha': dates, 'dNPS': dNPS, 'tNPS': tNPS, 'sNPS': sNPS})
    df_future = pd.DataFrame({'Fecha': future_dates, 'dNPS': future_dNPS, 'tNPS': future_tNPS, 'sNPS': future_sNPS})

    # Unir datos históricos y proyectados
    df_nps_total = pd.concat([df_nps, df_future], ignore_index=True)
    
    return df_nps, df_future, df_nps_total

# Cargar datos
df_nps, df_future, df_nps_total = load_data()

# Fecha de corte (donde terminan los datos históricos y empiezan los proyectados)
fecha_corte = df_future['Fecha'][0]

# Crear selectores para personalizar la visualización
st.sidebar.header("Opciones de Visualización")
show_historical = st.sidebar.checkbox("Mostrar datos históricos", value=True)
show_projected = st.sidebar.checkbox("Mostrar datos proyectados", value=True)
show_cutline = st.sidebar.checkbox("Mostrar línea de corte", value=True)

# Rango de fechas para filtrar
min_date = df_nps['Fecha'].min().date()
max_date = df_future['Fecha'].max().date()

date_range = st.sidebar.date_input(
    "Seleccione rango de fechas",
    [min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

# Comprobar si el usuario ha seleccionado un rango válido
if len(date_range) == 2:
    start_date, end_date = date_range
    start_date = pd.Timestamp(start_date)
    end_date = pd.Timestamp(end_date)
    
    # Filtrar datos según rango seleccionado
    filtered_historical = df_nps[(df_nps['Fecha'] >= start_date) & (df_nps['Fecha'] <= end_date)]
    filtered_projected = df_future[(df_future['Fecha'] >= start_date) & (df_future['Fecha'] <= end_date)]
else:
    filtered_historical = df_nps
    filtered_projected = df_future

# Función para crear gráficos
def create_nps_chart(title, nps_type):
    fig = go.Figure()
    
    # Añadir datos históricos si están activados
    if show_historical:
        fig.add_trace(go.Scatter(
            x=filtered_historical['Fecha'],
            y=filtered_historical[nps_type],
            mode='lines+markers',
            name=f'{nps_type} Histórico',
            line=dict(width=3),
            marker=dict(size=8)
        ))
    
    # Añadir datos proyectados si están activados
    if show_projected:
        fig.add_trace(go.Scatter(
            x=filtered_projected['Fecha'],
            y=filtered_projected[nps_type],
            mode='lines+markers',
            name=f'{nps_type} Proyectado',
            line=dict(width=3, dash='dot'),
            marker=dict(size=8, symbol='diamond')
        ))
    
    # Añadir línea de corte si está activada
    if show_cutline and fecha_corte >= start_date and fecha_corte <= end_date:
        fig.add_vline(
            x=fecha_corte,
            line_width=2,
            line_dash="solid",
            line_color="red"
        )
        fig.add_annotation(
            x=fecha_corte,
            y=max(df_nps_total[nps_type]) + 5,
            text="Inicio de proyecciones",
            showarrow=True,
            arrowhead=1,
            arrowcolor="red",
            ax=50,
            ay=-30
        )
    
    # Actualizar diseño
    fig.update_layout(
        title=title,
        xaxis_title="Fecha",
        yaxis_title=f"Puntuación {nps_type}",
        template="plotly_white",
        height=400,
        hovermode="x unified"
    )
    
    return fig

# Dashboard principal
st.header("Visualización de KPIs de NPS")

# Métricas clave - Mostrar último valor histórico y último proyectado
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="dNPS Actual",
        value=f"{df_nps['dNPS'].iloc[-1]}",
        delta=f"{df_future['dNPS'].iloc[-1] - df_nps['dNPS'].iloc[-1]}"
    )

with col2:
    st.metric(
        label="tNPS Actual",
        value=f"{df_nps['tNPS'].iloc[-1]}",
        delta=f"{df_future['tNPS'].iloc[-1] - df_nps['tNPS'].iloc[-1]}"
    )

with col3:
    st.metric(
        label="sNPS Actual",
        value=f"{df_nps['sNPS'].iloc[-1]}",
        delta=f"{df_future['sNPS'].iloc[-1] - df_nps['sNPS'].iloc[-1]}"
    )

# Gráficos individuales
st.plotly_chart(
    create_nps_chart(
        "¿Estamos logrando satisfacer las necesidades de sus clientes? (dNPS)",
        "dNPS"
    ),
    use_container_width=True
)

st.plotly_chart(
    create_nps_chart(
        "¿Somos capaces de mantener la confianza de los clientes en el largo plazo? (tNPS)",
        "tNPS"
    ),
    use_container_width=True
)

st.plotly_chart(
    create_nps_chart(
        "¿Tenemos fortaleza y buena percepción de los clientes en redes sociales? (sNPS)",
        "sNPS"
    ),
    use_container_width=True
)

# Tabla de datos
with st.expander("Ver datos completos"):
    tab1, tab2 = st.tabs(["Datos Históricos", "Datos Proyectados"])
    
    with tab1:
        st.dataframe(df_nps)
    
    with tab2:
        st.dataframe(df_future)

# Añadir información de ayuda en la barra lateral
with st.sidebar.expander("Información del Dashboard"):
    st.markdown("""
    ### Acerca de los indicadores
    
    - **dNPS**: NPS Predictivo y Accionable, enfocado en la anticipación en tiempo real mediante machine learning y datos de comportamiento.
    
    - **tNPS**: NPS de Confianza, refleja la confianza de los clientes en la aseguradora a largo plazo.
    
    - **sNPS**: NPS de Viralidad, representa la capacidad de generar recomendaciones orgánicas en redes sociales.
    
    ### Cómo usar este dashboard
    
    - Usa los controles en la barra lateral para personalizar la visualización
    - Selecciona el rango de fechas que quieres visualizar
    - Pasa el cursor sobre los gráficos para ver información detallada
    """)

# Footer
st.markdown("---")
st.caption("Dashboard desarrollado para AXA - Análisis de NPS Avanzado")
