# app.py
import streamlit as st
import requests
from ocr_parser import extrair_receita_estruturada_do_json

# API
API_URL = "https://api.ocr.space/parse/image"
API_KEY = st.secrets["API_KEY"]  # 🔒 Use secrets.toml

# Layout do app
st.set_page_config(page_title="Centro Multifocal - OCR", layout="centered")
st.title("📄 Leitor de Receita Médica - Centro Multifocal")

# Upload
uploaded_file = st.file_uploader("📤 Envie sua receita médica (PNG, JPG, JPEG)", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    files = {"image": uploaded_file}
    data = {
        "apikey": API_KEY,
        "language": "por",
        "isOverlayRequired": True  # 🔍 Necessário para pegar as posições
    }

    with st.spinner("🧠 Processando a imagem..."):
        response = requests.post(API_URL, files=files, data=data)

    if response.status_code == 200:
        try:
            ocr_data = response.json()

            st.subheader("🧾 JSON completo (OCR.space):")
            st.json(ocr_data)

            texto_ocr = ocr_data["ParsedResults"][0]["ParsedText"]
            st.subheader("📝 Texto extraído (OCR):")
            st.text_area("Texto OCR:", texto_ocr, height=200)

            # 🔍 Extração baseada em posição (JSON)
            dados_receita = extrair_receita_estruturada_do_json(ocr_data)

            st.subheader("📊 Dados estruturados da receita:")
            for campo, valor in dados_receita.items():
                valor_exibido = valor if valor else "Não encontrado"
                st.write(f"**{campo}**: {valor_exibido}")

        except Exception as e:
            st.error("❌ Erro ao processar resposta da API.")
            st.exception(e)

    else:
        st.error("❌ Erro na API OCR:")
        st.code(response.text)
