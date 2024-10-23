import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Cargar los datos
df = pd.read_excel("./CARRERAS.xlsx")

# Título de la aplicación
st.title("Participación de Estudiantes por Facultad y Carrera")

# Filtros en la barra lateral
st.sidebar.header("Filtros")

# Filtro de Región
region = st.sidebar.multiselect(
    'Región:',
    options=df['REGION'].unique(),
    default=None,
    help="Selecciona una o más regiones"
)

# Filtro de Financiamiento
financiamiento = st.sidebar.multiselect(
    'Financiamiento:',
    options=df['FINANCIAMIENTO'].unique(),
    default=None,
    help="Selecciona uno o más tipos de financiamiento"
)

# Filtro de Facultad
facultad = st.sidebar.selectbox(
    'Facultad:',
    options=[None] + df['FACULTAD'].unique().tolist(),
    index=0,
    help="Selecciona una facultad"
)

# Filtro de Carrera
carrera = st.sidebar.multiselect(
    'Carrera:',
    options=df['CARRERA'].unique(),
    default=None,
    help="Selecciona una o más carreras"
)

# Filtrar los datos en función de los filtros seleccionados
filtered_df = df.copy()

if region:
    filtered_df = filtered_df[filtered_df['REGION'].isin(region)]
if financiamiento:
    filtered_df = filtered_df[filtered_df['FINANCIAMIENTO'].isin(financiamiento)]
if facultad:
    filtered_df = filtered_df[filtered_df['FACULTAD'] == facultad]
if carrera:
    filtered_df = filtered_df[filtered_df['CARRERA'].isin(carrera)]

# Agrupar por universidad y año
df_agrupado = filtered_df.groupby(['AÑO', 'UNIVERSIDAD']).agg({'TOTAL': 'sum'}).reset_index()

# Calcular la participación para cada universidad en cada año
df_agrupado['PARTICIPACION'] = df_agrupado.groupby('AÑO')['TOTAL'].transform(lambda x: x / x.sum())

# Crear una figura de Plotly
fig = go.Figure()

# Obtener los años únicos
años = df_agrupado['AÑO'].unique()

# Configurar la paleta de colores en tonos de azul (escala continua)
blues = px.colors.sequential.Blues

# Dibujar barras para cada año
for i, año in enumerate(años):
    df_year = df_agrupado[df_agrupado['AÑO'] == año]
    fig.add_trace(go.Bar(
        x=df_year['UNIVERSIDAD'],
        y=df_year['PARTICIPACION'],
        name=f'Año {año}',
        marker_color=blues[i % len(blues)],  # Usar colores de la escala de azules
        text=df_year['PARTICIPACION'].apply(lambda x: f'{x:.2%}'),  # Texto con formato de porcentaje
        textposition='auto'  # Colocar los valores arriba de las barras
    ))

# Configurar el diseño del gráfico
fig.update_layout(
    barmode='group',
    title='Participación por Universidad y Año',
    xaxis_title='Universidades',
    yaxis_title='Participación',
    legend_title='Años',
    xaxis_tickangle=-45,
    template='plotly_white'
)

# Mostrar el gráfico en Streamlit
st.plotly_chart(fig)
