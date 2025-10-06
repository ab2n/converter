import streamlit as st
import pandas as pd
from io import BytesIO

st.title("Convertisseur CSV → XLSX")

# Upload du fichier CSV
uploaded_file = st.file_uploader("Choisissez un fichier CSV", type="csv")

if uploaded_file is not None:
    # Lecture du CSV
    df = pd.read_csv(uploaded_file)
    st.write("Aperçu du fichier CSV :")
    st.dataframe(df)
    
    # Fonction pour convertir en Excel
    def to_excel(df):
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Sheet1')
            writer.save()
        processed_data = output.getvalue()
        return processed_data

    # Conversion
    excel_data = to_excel(df)

    # Bouton pour télécharger le fichier Excel
    st.download_button(
        label="Télécharger en XLSX",
        data=excel_data,
        file_name="converted.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
