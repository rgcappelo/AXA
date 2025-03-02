import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt

# Cargar el contenido del documento Word en la introducción
intro_text = """
## CONSTRUCCIÓN DEL NUEVO KPI: NET PROMOTER SCORE (NPS) AVANZADO PARA AXA

### Introducción

Basándonos en el análisis previo del caso de AXA y en las recomendaciones consensuadas en el panel de expertos, desarrollaremos un nuevo KPI de Net Promoter Score (NPS) que supere las limitaciones tradicionales y se integre con los KPIs normales de AXA.

Este nuevo KPI responderá a tres perspectivas clave:

- **NPS Predictivo y Accionable (dNPS):** Enfocado en la anticipación en tiempo real mediante machine learning y datos de comportamiento.
- **NPS de Confianza y Viralidad (tNPS + sNPS):** Reflejando la confianza en la aseguradora y su capacidad de generar recomendaciones orgánicas en redes sociales.
- **NPS Personalizado por Sector:** Adaptando las métricas a seguros, banca o negocios digitales, según la naturaleza del cliente.
"""

# Generación de datos simulados
np.random.seed(42)
dates = pd.date_range(start="2022-01-01", periods=37, freq='M')
dNPS = np.clip(np.random.normal(loc=60, scale=10, size=len(dates)), 40, 90)
tNPS = np.clip(np.random.normal(loc=70, scale=8, size=len(dates)), 50, 95)
sNPS = np.clip(np.random.normal(loc=55, scale=12, size=len(dates)), 30, 85)
smart_NPS = (0.5 * dNPS) + (0.3 * tNPS) + (0.2 * sNPS)

df_nps = pd.DataFrame({
    'Fecha': dates,
    'dNPS': dNPS,
    'tNPS': tNPS,
    'sNPS': sNPS,
    'Smart_NPS': smart_NPS
})

# Proyección de los próximos 6 meses
future_dates = pd.date_range(start="2025-03-01", periods=6, freq='M')
future_dNPS = np.linspace(dNPS[-1], dNPS[-1] + 5, 6)
future_tNPS = np.linspace(tNPS[-1], tNPS[-1] + 5, 6)
future_sNPS = np.linspace(sNPS[-1], sNPS[-1] + 5, 6)
future_smart_NPS = np.linspace(smart_NPS[-1], smart_NPS[-1] + 5, 6)

df_future = pd.DataFrame({
    'Fecha': future_dates,
    'dNPS': future_dNPS,
    'tNPS': future_tNPS,
    'sNPS': future_sNPS,
    'Smart_NPS': future_smart_NPS
})

# Unir datos históricos y proyectados
df_nps_total = pd.concat([df_nps, df_future], ignore_index=True)

# Convertir las fechas a tipo datetime para visualización
df_nps_total['Fecha'] = pd.to_datetime(df_nps_total['Fecha'])

# Función para graficar dinámicamente
def plot_nps(df, variable, title, color):
    plt.figure(figsize=(10, 5))
    plt.plot(df['Fecha'], df[variable], marker='o', linestyle='-', color=color, label=title)
    plt.axvline(x=df[df['Fecha'] < "2025-03-01"].Fecha.max(), color='red', linestyle='--', label="Inicio de Predicción")
    plt.xlabel("Fecha")
    plt.ylabel("Puntuación")
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.show()

# Mostrar gráficos dinámicos
print(intro_text)
plot_nps(df_nps_total, 'dNPS', "Estamos logrando satisfacer las necesidades de sus clientes?", "blue")
plot_nps(df_nps_total, 'tNPS', "Somos capaces de mantener la confianza de los clientes en el largo plazo?", "orange")
plot_nps(df_nps_total, 'sNPS', "Tenemos fortaleza y buena percepción de los clientes en redes sociales?", "green")
plot_nps(df_nps_total, 'Smart_NPS', "Logramos satisfacer las necesidades del cliente, manteniendo su confianza en el largo plazo y con fuerte percepción en redes?", "red")
