import streamlit as st
import pandas as pd
import json

# Cargar datos desde el JSON (asegúrate de que está en la misma carpeta)
with open('datos_habitos.json', 'r') as f:
    data = json.load(f)

df = pd.DataFrame(data)
habit = df.copy()
habit.columns = habit.iloc[0]
habit.columns=habit.columns.str.replace(r'\[', '', regex=True).str.replace(r'\]', '', regex=True)
habit.columns = habit.columns.str.strip()
habit = habit[1:]
habit = habit.drop(columns=['Marca temporal'])
#habit['Día']=pd.to_datetime(habit['Día'],format='%d/%m/%Y')
habit.sort_values(by='Día', inplace=True, ascending= False)
habit.reset_index(drop=True, inplace=True)

# Título de la app
st.title("Seguimiento de Hábitos 📊")

# Mostrar tabla de datos
st.subheader("Datos Registrados")
st.dataframe(habit)

# Gráfico de cumplimiento de hábitos
#st.subheader("Cumplimiento de Hábitos")
#habit_counts = df.iloc[:, 1:].apply(pd.value_counts).T
#st.bar_chart(habit_counts)

st.write("¡Sigue cumpliendo con tus hábitos!")  # Mensaje motivacional

