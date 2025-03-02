
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
from datetime import datetime

# 1. Carga de datos
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

# 2. Visualización con Plotly
# Crear figura con subplots
fig = make_subplots(rows=3, cols=1, 
                   subplot_titles=("¿Estamos logrando satisfacer las necesidades de sus clientes? (dNPS)",
                                  "¿Somos capaces de mantener la confianza de los clientes en el largo plazo? (tNPS)",
                                  "¿Tenemos fortaleza y buena percepción de los clientes en redes sociales? (sNPS)"),
                   vertical_spacing=0.15,
                   specs=[[{"type": "scatter"}], [{"type": "scatter"}], [{"type": "scatter"}]])

# Fecha de corte (donde terminan los datos históricos y empiezan los proyectados)
fecha_corte = future_dates[0]

# Gráfico 1: dNPS
# Datos históricos
fig.add_trace(
    go.Scatter(
        x=df_nps['Fecha'], 
        y=df_nps['dNPS'],
        mode='lines+markers',
        name='dNPS Histórico',
        line=dict(color='royalblue', width=3),
        marker=dict(size=6)
    ),
    row=1, col=1
)

# Datos proyectados
fig.add_trace(
    go.Scatter(
        x=df_future['Fecha'], 
        y=df_future['dNPS'],
        mode='lines+markers',
        name='dNPS Proyectado',
        line=dict(color='royalblue', width=3, dash='dot'),
        marker=dict(size=6, symbol='diamond')
    ),
    row=1, col=1
)

# Gráfico 2: tNPS
# Datos históricos
fig.add_trace(
    go.Scatter(
        x=df_nps['Fecha'], 
        y=df_nps['tNPS'],
        mode='lines+markers',
        name='tNPS Histórico',
        line=dict(color='green', width=3),
        marker=dict(size=6)
    ),
    row=2, col=1
)

# Datos proyectados
fig.add_trace(
    go.Scatter(
        x=df_future['Fecha'], 
        y=df_future['tNPS'],
        mode='lines+markers',
        name='tNPS Proyectado',
        line=dict(color='green', width=3, dash='dot'),
        marker=dict(size=6, symbol='diamond')
    ),
    row=2, col=1
)

# Gráfico 3: sNPS
# Datos históricos
fig.add_trace(
    go.Scatter(
        x=df_nps['Fecha'], 
        y=df_nps['sNPS'],
        mode='lines+markers',
        name='sNPS Histórico',
        line=dict(color='purple', width=3),
        marker=dict(size=6)
    ),
    row=3, col=1
)

# Datos proyectados
fig.add_trace(
    go.Scatter(
        x=df_future['Fecha'], 
        y=df_future['sNPS'],
        mode='lines+markers',
        name='sNPS Proyectado',
        line=dict(color='purple', width=3, dash='dot'),
        marker=dict(size=6, symbol='diamond')
    ),
    row=3, col=1
)

# Añadir líneas de corte verticales en cada gráfico
for i in range(1, 4):
    fig.add_vline(x=fecha_corte, line_width=2, line_dash="solid", line_color="red", row=i, col=1)
    # Añadir anotación para indicar la línea de corte
    fig.add_annotation(
        x=fecha_corte,
        y=100 if i == 2 else 95,  # Ajustar posición vertical según el gráfico
        text="Inicio de proyecciones",
        showarrow=True,
        arrowhead=1,
        arrowcolor="red",
        ax=50,
        ay=-30,
        row=i, 
        col=1
    )

# Actualizar diseño de la figura
fig.update_layout(
    title_text="CONSTRUCCIÓN DEL NUEVO KPI: NET PROMOTER SCORE (NPS) AVANZADO PARA AXA",
    height=900,
    width=1200,
    template="plotly_white",
    legend_title_text="Tipo de Datos",
    showlegend=True,
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.2,
        xanchor="center",
        x=0.5
    )
)

# Actualizar ejes x e y
fig.update_xaxes(title_text="Fecha", showgrid=True, gridwidth=0.5, gridcolor='lightgray')
fig.update_yaxes(title_text="Puntuación NPS", showgrid=True, gridwidth=0.5, gridcolor='lightgray', range=[45, 105])

# Añadir texto de introducción como anotación en la parte superior
fig.add_annotation(
    text="""Introducción<br>
    Basándonos en el análisis previo del caso de AXA y en las recomendaciones consensuadas en el panel de expertos, 
    desarrollaremos un nuevo KPI de Net Promoter Score (NPS) que supere las limitaciones tradicionales 
    y se integre con los KPIs normales de AXA.<br><br>
    Este nuevo KPI responderá a tres perspectivas clave:<br>
    • NPS Predictivo y Accionable (dNPS): Enfocado en la anticipación en tiempo real mediante machine learning y datos de comportamiento.<br>
    • NPS de Confianza y Viralidad (tNPS + sNPS): Reflejando la confianza en la aseguradora y su capacidad de generar recomendaciones orgánicas en redes sociales.<br>
    • NPS Personalizado por Sector: Adaptando las métricas a seguros, banca o negocios digitales, según la naturaleza del cliente.""",
    xref="paper", yref="paper",
    x=0, y=1.15,
    showarrow=False,
    font=dict(size=12),
    align="left",
    bordercolor="black",
    borderwidth=1,
    borderpad=10,
    bgcolor="white",
)

# Mostrar la figura
fig.show()

# También se puede guardar la figura como HTML para interacción
# fig.write_html("dashboard_nps_axa.html")

# Si se prefiere usar Matplotlib en lugar de Plotly, aquí está el código alternativo:
'''
plt.figure(figsize=(15, 12))

# Configuración de estilo
plt.style.use('ggplot')

# Introducción (como texto en lugar de gráfico)
plt.figtext(0.5, 0.95, "CONSTRUCCIÓN DEL NUEVO KPI: NET PROMOTER SCORE (NPS) AVANZADO PARA AXA", 
            fontsize=14, ha="center", fontweight='bold')
plt.figtext(0.1, 0.90, """Introducción
Basándonos en el análisis previo del caso de AXA y en las recomendaciones consensuadas en el panel de expertos, 
desarrollaremos un nuevo KPI de Net Promoter Score (NPS) que supere las limitaciones tradicionales 
y se integre con los KPIs normales de AXA.

Este nuevo KPI responderá a tres perspectivas clave:
• NPS Predictivo y Accionable (dNPS): Enfocado en la anticipación en tiempo real mediante machine learning y datos de comportamiento.
• NPS de Confianza y Viralidad (tNPS + sNPS): Reflejando la confianza en la aseguradora y su capacidad de generar recomendaciones orgánicas en redes sociales.
• NPS Personalizado por Sector: Adaptando las métricas a seguros, banca o negocios digitales, según la naturaleza del cliente.""", 
            fontsize=10, ha="left")

# Gráfico 1: dNPS
plt.subplot(3, 1, 1)
plt.plot(df_nps['Fecha'], df_nps['dNPS'], 'b-', linewidth=2, label='Histórico')
plt.plot(df_future['Fecha'], df_future['dNPS'], 'b--', linewidth=2, label='Proyectado')
plt.axvline(x=fecha_corte, color='red', linestyle='-', linewidth=2)
plt.text(fecha_corte, max(df_nps['dNPS']) + 5, "Inicio de proyecciones", color='red', ha='left')
plt.title('¿Estamos logrando satisfacer las necesidades de sus clientes? (dNPS)')
plt.ylabel('Puntuación dNPS')
plt.grid(True)
plt.legend()

# Gráfico 2: tNPS
plt.subplot(3, 1, 2)
plt.plot(df_nps['Fecha'], df_nps['tNPS'], 'g-', linewidth=2, label='Histórico')
plt.plot(df_future['Fecha'], df_future['tNPS'], 'g--', linewidth=2, label='Proyectado')
plt.axvline(x=fecha_corte, color='red', linestyle='-', linewidth=2)
plt.text(fecha_corte, max(df_nps['tNPS']) + 5, "Inicio de proyecciones", color='red', ha='left')
plt.title('¿Somos capaces de mantener la confianza de los clientes en el largo plazo? (tNPS)')
plt.ylabel('Puntuación tNPS')
plt.grid(True)
plt.legend()

# Gráfico 3: sNPS
plt.subplot(3, 1, 3)
plt.plot(df_nps['Fecha'], df_nps['sNPS'], 'm-', linewidth=2, label='Histórico')
plt.plot(df_future['Fecha'], df_future['sNPS'], 'm--', linewidth=2, label='Proyectado')
plt.axvline(x=fecha_corte, color='red', linestyle='-', linewidth=2)
plt.text(fecha_corte, max(df_nps['sNPS']) + 5, "Inicio de proyecciones", color='red', ha='left')
plt.title('¿Tenemos fortaleza y buena percepción de los clientes en redes sociales? (sNPS)')
plt.ylabel('Puntuación sNPS')
plt.xlabel('Fecha')
plt.grid(True)
plt.legend()

plt.tight_layout(rect=[0, 0, 1, 0.85])
plt.show()
'''
Made with
Artifacts are user-generated and may contain unverified or potentially unsafe content.
Report
Remix Artifact

