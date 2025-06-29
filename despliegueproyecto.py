# -*- coding: utf-8 -*-
"""DespliegueProyecto.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1lVSh4bFWsUVcY1syOMCPXTT7KpIGejo9
"""

import streamlit as st
import pandas as pd
import pickle
import os

# ----------------------------
# Cargar modelo y scaler
# ----------------------------

try:
    with open("saved_models/standard_scaler.pkl", "rb") as f:
        scaler = pickle.load(f)

    with open("saved_models/svr_model.pkl", "rb") as f:  # Cambia si usas otro modelo
        model = pickle.load(f)
except FileNotFoundError:
    st.error("❌ Archivos del modelo no encontrados. Verifica la carpeta 'saved_models'.")
    st.stop()

# ----------------------------
# Título de la aplicación
# ----------------------------
st.title("💰 Predicción de Ingreso Anual")
st.write("Esta aplicación predice el ingreso anual estimado de nuevos clientes con base en su experiencia laboral y tamaño familiar.")

# ----------------------------
# Subida del archivo .csv
# ----------------------------
uploaded_file = st.file_uploader("📤 Sube tu archivo .CSV con columnas: Work Experience, Family Size", type=["csv"])

if uploaded_file is not None:
    try:
        # Leer CSV
        df = pd.read_csv(uploaded_file)

        st.subheader("📄 Vista previa de los datos cargados")
        st.write(df.head())

        # Validar columnas necesarias
        required_cols = ['Work Experience', 'Family Size']
        if not all(col in df.columns for col in required_cols):
            st.error(f"El archivo debe contener estas columnas: {required_cols}")
        else:
            # Escalar datos
            X = df[required_cols]
            X_scaled = scaler.transform(X)

            # Hacer predicción
            predictions = model.predict(X_scaled)

            # Agregar al dataframe
            df['Predicted Annual Income ($)'] = predictions

            # Mostrar predicciones
            st.subheader("📊 Resultados de la predicción")
            st.write(df[['Work Experience', 'Family Size', 'Predicted Annual Income ($)']])

            # Descargar archivo
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("⬇️ Descargar resultados", data=csv, file_name="predicciones_ingresos.csv", mime='text/csv')

    except Exception as e:
        st.error(f"❌ Error procesando el archivo: {e}")