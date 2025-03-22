import streamlit as st
import requests

API_URL = "https://api.ocr.space/parse/image"
API_KEY = "SUA_CHAVE_AQUI"  # substitua pela sua chave da API OCR.space

st.title("📄 Leitor de Receita Médica")

uploaded_file = st.file_uploader("Envie sua receita médica (PNG, JPG)", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    files = {"image": uploaded_file}
    data = {"apikey": API_KEY, "language": "por"}

    with st.spinner("Lendo a receita..."):
        response = requests.post(API_URL, files=files, data=data)
    
    if response.status_code == 200:
        result = response.json()
        texto = result["ParsedResults"][0]["ParsedText"]
        st.success("Texto extraído:")
        st.text_area("Resultado do OCR", texto, height=200)
    else:
        st.error("Erro ao processar a imagem.")
