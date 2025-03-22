# app.py
import streamlit as st
import requests
from ocr_parser import extrair_valores_receita

# Configurações da API OCR.space
API_URL = "https://api.ocr.space/parse/image"
API_KEY = st.secrets["API_KEY"]  # Configure em .streamlit/secrets.toml

st.set_page_config(page_title="Centro Multifocal - OCR", layout="centered")
st.title("\ud83d\udcc4 Leitor de Receita Médica - Centro Multifocal")

uploaded_file = st.file_uploader("Envie sua receita médica (PNG, JPG, JPEG)", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    files = {"image": uploaded_file}
    data = {"apikey": API_KEY, "language": "por"}

    with st.spinner("\ud83d\udd0d Lendo a receita..."):
        response = requests.post(API_URL, files=files, data=data)

    if response.status_code == 200:
        ocr_data = response.json()
        try:
            texto = ocr_data["ParsedResults"][0]["ParsedText"]
            st.subheader("\ud83d\udcdd Texto extraído da imagem")
            st.text_area("Texto completo:", texto, height=250)

            dados_receita = extrair_valores_receita(texto)

            st.subheader("\ud83d\udcca Dados estruturados da receita:")
            for campo, valor in dados_receita.items():
                st.write(f"**{campo}**: {valor or 'Não encontrado'}")

        except Exception as e:
            st.error("\u274c Não foi possível interpretar o texto da receita.")
            st.exception(e)
    else:
        st.error("\u274c Erro ao processar a imagem.")
        st.code(response.text)
