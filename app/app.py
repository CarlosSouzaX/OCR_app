# app/app.py
import os
import json
import requests
import streamlit as st
from datetime import datetime

# Configurações
OCR_API_KEY = st.secrets["API_KEY"]
OCR_API_URL = "https://api.ocr.space/parse/image"

# Diretórios
DATASET_DIR = "../dataset_receitas"
IMAGES_DIR = os.path.join(DATASET_DIR, "images")
OCR_DIR = os.path.join(DATASET_DIR, "ocr_json")

os.makedirs(IMAGES_DIR, exist_ok=True)
os.makedirs(OCR_DIR, exist_ok=True)

# Função para gerar nome sequencial
def proximo_nome_receita():
    arquivos = os.listdir(IMAGES_DIR)
    indices = [int(f.split("_")[1].split(".")[0]) for f in arquivos if f.startswith("receita_")]
    novo_indice = max(indices) + 1 if indices else 1
    return f"receita_{novo_indice:03}"

# Streamlit app
st.title("📤 Upload de Receita")

uploaded_file = st.file_uploader("Envie uma imagem da receita (.jpg, .png)", type=["jpg", "jpeg", "png"])

if uploaded_file:
    nome_base = proximo_nome_receita()
    extensao = uploaded_file.name.split(".")[-1]
    nome_arquivo = f"{nome_base}.{extensao}"

    caminho_imagem = os.path.join(IMAGES_DIR, nome_arquivo)
    caminho_json = os.path.join(OCR_DIR, f"{nome_base}.json")

    # Salva a imagem
    with open(caminho_imagem, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.image(caminho_imagem, caption="Imagem salva com sucesso 📸")

    # Faz OCR
    with st.spinner("Processando OCR..."):
        response = requests.post(
            OCR_API_URL,
            files={"image": open(caminho_imagem, "rb")},
            data={"apikey": OCR_API_KEY, "language": "por", "isOverlayRequired": True}
        )
    st.write("Status Code:", response.status_code)
    st.write("Resposta:", response.text)


    if response.status_code == 200:
        ocr_result = response.json()

        with open(caminho_json, "w", encoding="utf-8") as f:
            json.dump(ocr_result, f, indent=2, ensure_ascii=False)

        st.success(f"OCR salvo com sucesso ✅ em: {caminho_json}")
        st.code(ocr_result["ParsedResults"][0]["ParsedText"])
    else:
        st.error("Erro ao processar OCR.")
