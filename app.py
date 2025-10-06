import streamlit as st
import pandas as pd
from io import BytesIO

st.title("Convertisseur CSV → XLSX")

uploaded_file = st.file_uploader("Choisissez un fichier CSV", type="csv")

if uploaded_file is not None:
    # Essayons différents encodages
    encodings = ["utf-8", "latin-1", "ISO-8859-1"]
    for enc in encodings:
        try:
            df = pd.read_csv(uploaded_file, encoding=enc)
            break
        except Exception as e:
            df = None

    if df is None:
        st.error("Impossible de lire le CSV. Essayez un autre encodage.")
    else:
        st.write("Aperçu du fichier CSV :")
        st.dataframe(df)

        # Conversion en Excel
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
