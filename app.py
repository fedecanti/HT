import streamlit as st
import pandas as pd
import json
import requests
import plotly.express as px

# LEO HABITOS ###############################################################################################################
# ID del archivo en Google Drive
file_id = "10I1cYGKxlXfHH3t_pb6gPKjrdhKQmOp5"  # ← reemplazalo por tu ID real

# URL para descarga directa desde Drive
url = f"https://drive.google.com/uc?export=download&id={file_id}"

# Descargar y cargar JSON desde Google Drive
response = requests.get(url)
data = json.loads(response.text)

#Paso el json a un dataframe
df = pd.DataFrame(data)
habit = df.copy()                   #Uso una copia del df
habit.columns = habit.iloc[0]         
habit.columns=habit.columns.str.replace(r'\[', '', regex=True).str.replace(r'\]', '', regex=True)
habit.columns = habit.columns.str.strip()
habit = habit[1:]
habit = habit.drop(columns=['Marca temporal'])

#Formateo la columna Día
habit['Día'] = pd.to_datetime(habit['Día'], errors='coerce')  # Convierte correctamente
habit.sort_values(by='Día', inplace=True, ascending=False)
habit.reset_index(drop=True, inplace=True)
habit['Día'] = habit['Día'].dt.strftime('%d-%m-%Y')  # Formatea la fecha

# LEO PESAJE ################################################################################################################################
# ID del archivo en Google Drive
file_id = "1B7OfVu4NE1tH7hga0vt-1QWtWkS5kTb6"  # ← reemplazalo por tu ID real
# URL para descarga directa desde Drive
url = f"https://drive.google.com/uc?export=download&id={file_id}"

# Descargar y cargar JSON desde Google Drive
response = requests.get(url)
data = json.loads(response.text)

#Paso el json a un dataframe
df = pd.DataFrame(data)
pesaje = df.copy()                   #Uso una copia del df
pesaje.columns = pesaje.iloc[0]
pesaje = pesaje[1:]
pesaje = pesaje.drop(columns=['Marca temporal'])

#Formateo la columna Fecha
pesaje['Fecha Pesaje'] = pd.to_datetime(pesaje['Fecha Pesaje'], errors='coerce')  # Convierte correctamente
pesaje['Fecha Pesaje'] = pesaje['Fecha Pesaje'].dt.strftime('%d-%m-%Y')  # Formatea la fecha
pesaje.sort_values(by='Fecha Pesaje', inplace=True, ascending=True)
pesaje.reset_index(drop=True, inplace=True)

#Formateo valores
columnas_valores = ['Peso kg', 'BMI', 'BFR %', 'Muscle Rate %']
pesaje[columnas_valores] = pesaje[columnas_valores].apply(pd.to_numeric, errors='coerce')    #paso a número
pesaje[columnas_valores] = pesaje[columnas_valores].fillna(method='ffill')       #Relleno con valor cercano
pesaje[columnas_valores] = pesaje[columnas_valores].fillna(method='bfill')       #Relleno con valor cercano

pesaje = pesaje[['Fecha Pesaje','Peso kg','BMI','BFR %','Muscle Rate %']]
pesaje_tabla = pesaje.copy()
pesaje_tabla.sort_values(by='Fecha Pesaje', inplace=True, ascending=False)

# COMIENZO APP ####################################################################################################################################
# Título de la app
st.title("Seguimiento de Fede CanTi 📊")

# Mostrar tabla de datos hábitos
st.subheader("Datos Registrados Hábitos")
st.dataframe(habit)

#Gráfico de pesaje e índices
fig = px.line(
    pesaje,
    x='Fecha Pesaje',
    y=['Peso kg', 'BMI', 'BFR %', 'Muscle Rate %'],
    markers=True,
    title='Evolución corporal en el tiempo'
)

fig.update_layout(
    xaxis_title='Fecha',
    yaxis_title='Valor',
    legend_title='Indicadores',
    hovermode='x unified'
)

st.plotly_chart(fig)

# Mostrar tabla de pesaje
st.subheader("Datos Registrados Pesaje")
st.dataframe(pesaje_tabla)


st.write("¡Sigue cumpliendo con tus hábitos!")  # Mensaje motivacional

