import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
from datetime import datetime

# Configuración de la página
st.set_page_config(
    page_title="AXA Smart NPS Dashboard",
    page_icon="📊",
    layout="wide"
)

# Introducción del Dashboard
st.title("CONSTRUCCIÓN DEL NUEVO KPI: NET PROMOTER SCORE (NPS) AVANZADO PARA AXA")

st.markdown("""
### Introducción
Basándonos en el análisis previo del caso de AXA y en las recomendaciones consensuadas en el panel de expertos, desarrollaremos un nuevo KPI de Net Promoter Score (NPS) que supere las limitaciones tradicionales y se integre con los KPIs normales de AXA.

Este nuevo KPI responderá a tres perspectivas clave:
- **NPS Predictivo y Accionable (dNPS)**: Enfocado en la anticipación en tiempo real mediante machine learning y datos de comportamiento.
- **NPS de Confianza y Viralidad (tNPS + sNPS)**: Reflejando la confianza en la aseguradora y su capacidad de generar recomendaciones orgánicas en redes sociales.
- **NPS Personalizado por Sector**: Adaptando las métricas a seguros, banca o negocios digitales, según la naturaleza del cliente.
""")

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
    
    return df_nps_total, df_nps, df_future

# Cargar datos
df_nps_total, df_nps, df_future = load_data()

# Fecha de corte (primer fecha de datos proyectados)
cutoff_date = df_future['Fecha'].min()

# Crear gráficos
st.header("Indicadores de Smart NPS")

# Función para crear gráficos interactivos
def create_nps_plot(title, metric):
    fig = go.Figure()
    
    # Datos históricos
    fig.add_trace(go.Scatter(
        x=df_nps['Fecha'], 
        y=df_nps[metric],
        mode='lines+markers',
        name='Datos Históricos',
        line=dict(color='#2E86C1', width=3),
        marker=dict(size=8),
        hovertemplate='<b>Fecha:</b> %{x|%b %Y}<br><b>' + metric + ':</b> %{y}<extra></extra>'
    ))
    
    # Datos proyectados
    fig.add_trace(go.Scatter(
        x=df_future['Fecha'], 
        y=df_future[metric],
        mode='lines+markers',
        name='Datos Proyectados',
        line=dict(color='#2E86C1', width=3, dash='dot'),
        marker=dict(size=8),
        hovertemplate='<b>Fecha:</b> %{x|%b %Y}<br><b>' + metric + ':</b> %{y}<extra></extra>'
    ))
    
    # Línea de corte
    fig.add_vline(
        x=cutoff_date, 
        line=dict(color='red', width=2, dash='dash'),
        annotation_text="Mar 2025: Inicio de proyección",
        annotation_position="top right",
        annotation_font_color="red"
    )
    
    # Configurar diseño
    fig.update_layout(
        title=title,
        title_font=dict(size=20),
        xaxis_title='Fecha',
        yaxis_title=f'{metric} (Puntos)',
        hovermode='x unified',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        height=500,
        margin=dict(l=20, r=20, t=60, b=20),
    )
    
    # Configurar rango del eje Y
    fig.update_yaxes(range=[40, 105])
    
    return fig

# Crear los tres gráficos en columnas
col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(
        create_nps_plot("¿Estamos logrando satisfacer las necesidades de los clientes?", "dNPS"),
        use_container_width=True
    )
    
    st.plotly_chart(
        create_nps_plot("¿Somos capaces de mantener la confianza de los clientes en el largo plazo?", "tNPS"),
        use_container_width=True
    )

with col2:
    st.plotly_chart(
        create_nps_plot("¿Tenemos fortaleza y buena percepción de los clientes en redes sociales?", "sNPS"),
        use_container_width=True
    )
    
    # Gráfico combinado
    fig_combined = go.Figure()
    
    # Añadir cada métrica
    for metric, color in zip(['dNPS', 'tNPS', 'sNPS'], ['#1F618D', '#5DADE2', '#85C1E9']):
        # Datos históricos
        fig_combined.add_trace(go.Scatter(
            x=df_nps['Fecha'], 
            y=df_nps[metric],
            mode='lines',
            name=f'{metric} (Histórico)',
            line=dict(color=color, width=3),
            hovertemplate='<b>Fecha:</b> %{x|%b %Y}<br><b>' + metric + ':</b> %{y}<extra></extra>'
        ))
        
        # Datos proyectados
        fig_combined.add_trace(go.Scatter(
            x=df_future['Fecha'], 
            y=df_future[metric],
            mode='lines',
            name=f'{metric} (Proyectado)',
            line=dict(color=color, width=3, dash='dot'),
            hovertemplate='<b>Fecha:</b> %{x|%b %Y}<br><b>' + metric + ':</b> %{y}<extra></extra>'
        ))
    
    # Línea de corte
    fig_combined.add_vline(
        x=cutoff_date, 
        line=dict(color='red', width=2, dash='dash'),
        annotation_text="Mar 2025: Inicio de proyección",
        annotation_position="top right",
        annotation_font_color="red"
    )
    
    # Configurar diseño
    fig_combined.update_layout(
        title="Comparativa de todos los indicadores Smart NPS",
        title_font=dict(size=20),
        xaxis_title='Fecha',
        yaxis_title='Puntos',
        hovermode='x unified',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        height=500,
        margin=dict(l=20, r=20, t=60, b=20),
    )
    
    # Configurar rango del eje Y
    fig_combined.update_yaxes(range=[40, 105])
    
    st.plotly_chart(fig_combined, use_container_width=True)

# Añadir resumen estadístico
st.header("Resumen Estadístico")

# Función para calcular estadísticas
def calculate_stats(df, metric):
    return {
        'Mínimo': df[metric].min(),
        'Máximo': df[metric].max(),
        'Promedio': round(df[metric].mean(), 1),
        'Tendencia': "↗️ Creciente" if df[metric].iloc[-1] > df[metric].iloc[0] else "↘️ Decreciente"
    }

# Crear tablas de estadísticas
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("dNPS")
    stats_dNPS = calculate_stats(df_nps, 'dNPS')
    stats_future_dNPS = calculate_stats(df_future, 'dNPS')
    
    st.markdown("**Datos Históricos:**")
    for key, value in stats_dNPS.items():
        st.markdown(f"- **{key}:** {value}")
    
    st.markdown("**Datos Proyectados:**")
    for key, value in stats_future_dNPS.items():
        st.markdown(f"- **{key}:** {value}")

with col2:
    st.subheader("tNPS")
    stats_tNPS = calculate_stats(df_nps, 'tNPS')
    stats_future_tNPS = calculate_stats(df_future, 'tNPS')
    
    st.markdown("**Datos Históricos:**")
    for key, value in stats_tNPS.items():
        st.markdown(f"- **{key}:** {value}")
    
    st.markdown("**Datos Proyectados:**")
    for key, value in stats_future_tNPS.items():
        st.markdown(f"- **{key}:** {value}")

with col3:
    st.subheader("sNPS")
    stats_sNPS = calculate_stats(df_nps, 'sNPS')
    stats_future_sNPS = calculate_stats(df_future, 'sNPS')
    
    st.markdown("**Datos Históricos:**")
    for key, value in stats_sNPS.items():
        st.markdown(f"- **{key}:** {value}")
    
    st.markdown("**Datos Proyectados:**")
    for key, value in stats_future_sNPS.items():
        st.markdown(f"- **{key}:** {value}")

# Pie de página
st.markdown("---")
st.markdown("**Dashboard de Smart NPS para AXA** | Datos históricos: Ene 2022 - Feb 2025 | Proyección: Mar 2025 - Ago 2025")
