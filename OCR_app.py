# app.py
import streamlit as st
import requests
from ocr_parser import extrair_valores_receita

# API OCR.space
API_URL = "https://api.ocr.space/parse/image"
API_KEY = st.secrets["API_KEY"]

st.set_page_config(page_title="Centro Multifocal - OCR", layout="centered")
st.title("📄 Leitor de Receita Médica - Centro Multifocal")

uploaded_file = st.file_uploader("Envie sua receita médica (PNG, JPG, JPEG)", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    files = {"image": uploaded_file}
    data = {"apikey": API_KEY, "language": "por"}

    with st.spinner("🔍 Lendo a receita..."):
        response = requests.post(API_URL, files=files, data=data)

    if response.status_code == 200:
        try:
            ocr_data = response.json()
            texto = ocr_data["ParsedResults"][0]["ParsedText"]
            texto = texto.replace('\r', '').replace('\x0c', '')

            st.subheader("📝 Texto extraído da imagem:")
            st.text_area("Texto OCR:", texto.encode('utf-8', errors='ignore').decode('utf-8'), height=250)

            dados_receita = extrair_valores_receita(texto)

            st.subheader("📊 Dados estruturados da receita:")
            for campo, valor in dados_receita.items():
                valor_seguro = (valor or "Não encontrado").encode("utf-8", errors="ignore").decode("utf-8")
                st.write(f"**{campo}**: {valor_seguro}")

        except Exception as e:
            st.error("❌ Erro ao interpretar o texto da receita.")
            st.exception(e)

    else:
        st.error("❌ Erro na API do OCR.")
        st.code(response.text)
