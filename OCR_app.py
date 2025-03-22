# app.py
import streamlit as st
import requests
from ocr_parser import extrair_valores_receita

API_URL = "https://api.ocr.space/parse/image"
API_KEY = st.secrets["API_KEY"]

st.set_page_config(page_title="Centro Multifocal - OCR", layout="centered")
st.title("📄 Leitor de Receita Médica - Centro Multifocal")

uploaded_file = st.file_uploader("Envie sua receita médica (PNG, JPG, JPEG)", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    files = {"image": uploaded_file}
    data = {"apikey": API_KEY, "language": "por", "isOverlayRequired": True}  # ativa o retorno do TextOverlay

    with st.spinner("🔍 Lendo a receita..."):
        response = requests.post(API_URL, files=files, data=data)

    if response.status_code == 200:
        try:
            ocr_data = response.json()

            st.subheader("🧾 JSON bruto da API OCR.space:")
            st.json(ocr_data)  # Exibe o JSON formatado

            # Opcional: extrair texto puro
            texto = ocr_data["ParsedResults"][0]["ParsedText"]
            texto = texto.replace('\r', '').replace('\x0c', '')

            st.subheader("📝 Texto extraído (OCR):")
            st.text_area("Texto OCR:", texto, height=200)

            # Dados estruturados
            dados_receita = extrair_valores_receita(texto, debug=True)

            st.subheader("📊 Dados estruturados:")
            for campo, valor in dados_receita.items():
                valor_seguro = (valor or "Não encontrado")
                st.write(f"**{campo}**: {valor_seguro}")

        except Exception as e:
            st.error("❌ Erro ao processar a resposta da API.")
            st.exception(e)

    else:
        st.error("❌ Erro ao processar a imagem.")
        st.code(response.text)
