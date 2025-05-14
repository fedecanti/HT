import streamlit as st
import pandas as pd
import json
import requests

# ID del archivo en Google Drive
file_id = "10I1cYGKxlXfHH3t_pb6gPKjrdhKQmOp5"  # ← reemplazalo por tu ID real

# URL para descarga directa desde Drive
url = f"https://drive.google.com/uc?export=download&id={file_id}"

# Descargar y cargar JSON desde Google Drive
response = requests.get(url)
data = json.loads(response.text)

df = pd.DataFrame(data)
habit = df.copy()
habit.columns = habit.iloc[0]
habit.columns=habit.columns.str.replace(r'\[', '', regex=True).str.replace(r'\]', '', regex=True)
habit.columns = habit.columns.str.strip()
habit = habit[1:]
habit = habit.drop(columns=['Marca temporal'])

habit['Día'] = pd.to_datetime(habit['Día'], errors='coerce')  # Convierte correctamente
habit.sort_values(by='Día', inplace=True, ascending=False)
habit.reset_index(drop=True, inplace=True)

habit['Día'] = habit['Día'].dt.strftime('%d-%m-%Y')  # Formatea la fecha

# Título de la app
st.title("Seguimiento de Hábitos de Fede CanTi 📊")

# Mostrar tabla de datos
st.subheader("Datos Registrados")
st.dataframe(habit)

# Gráfico de cumplimiento de hábitos
#st.subheader("Cumplimiento de Hábitos")
#habit_counts = df.iloc[:, 1:].apply(pd.value_counts).T
#st.bar_chart(habit_counts)

st.write("¡Sigue cumpliendo con tus hábitos!")  # Mensaje motivacional

