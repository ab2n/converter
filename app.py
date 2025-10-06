import streamlit as st
import pandas as pd
from io import BytesIO
import chardet

st.title("Convertisseur CSV → XLSX")

uploaded_file = st.file_uploader("Choisissez un fichier CSV", type="csv")

if uploaded_file is not None:
    # Lire le fichier en mode binaire pour détecter l'encodage
    raw_data = uploaded_file.read()
    result = chardet.detect(raw_data)
    encoding = result['encoding']

    try:
        df = pd.read_csv(BytesIO(raw_data), encoding=encoding)
        st.write(f"Aperçu du fichier CSV (encodage détecté : {encoding}) :")
        st.dataframe(df)

        # Fonction pour convertir en Excel
        def to_excel(df):
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False, sheet_name='Sheet1')
                writer.save()
            return output.getvalue()

        excel_data = to_excel(df)

        st.download_button(
            label="Télécharger en XLSX",
            data=excel_data,
            file_name="converted.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    except Exception as e:
        st.error(f"Impossible de lire le CSV : {e}")
