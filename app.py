import streamlit as st
import pandas as pd
import json
import requests

# LEO HABITOS
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

# LEO PESAJE
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

# COMIENZO APP
# Título de la app
st.title("Seguimiento de Fede CanTi 📊")

# Mostrar tabla de datos hábitos
st.subheader("Datos Registrados Hábitos")
st.dataframe(habit)

#Mostrar tabla de pesaje
st.subheader("Datos Registrados Peso")
st.dataframe(pesaje)


# Gráfico de cumplimiento de hábitos
#st.subheader("Cumplimiento de Hábitos")
#habit_counts = df.iloc[:, 1:].apply(pd.value_counts).T
#st.bar_chart(habit_counts)

st.write("¡Sigue cumpliendo con tus hábitos!")  # Mensaje motivacional

