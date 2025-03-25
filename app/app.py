import os
import json
import requests
import streamlit as st
from datetime import datetime

# Título principal
st.title("Teste de Conexão e Upload de Receita")

# Bloco para testar a conexão com OCR.space
if st.button("Testar conexão com OCR.space"):
    try:
        r = requests.get("https://api.ocr.space", timeout=5)
        st.write("Conexão com OCR.space bem-sucedida! Status code:", r.status_code)
    except requests.exceptions.RequestException as e:
        st.write("Falha ao conectar com OCR.space:", e)

st.markdown("---")  # Linha separadora

# Configurações da API OCR.space
OCR_API_KEY = st.secrets["API_KEY"]
OCR_API_URL = "https://api.ocr.space/parse/image"

# Diretórios para salvar imagens e JSON de saída
DATASET_DIR = "../dataset_receitas"
IMAGES_DIR = os.path.join(DATASET_DIR, "images")
OCR_DIR = os.path.join(DATASET_DIR, "ocr_json")

os.makedirs(IMAGES_DIR, exist_ok=True)
os.makedirs(OCR_DIR, exist_ok=True)

# Função para gerar um nome sequencial para a receita
def proximo_nome_receita():
    arquivos = os.listdir(IMAGES_DIR)
    indices = [int(f.split("_")[1].split(".")[0]) for f in arquivos if f.startswith("receita_")]
    novo_indice = max(indices) + 1 if indices else 1
    return f"receita_{novo_indice:03}"

# Seção de upload de receita
st.subheader("📤 Upload de Receita")

uploaded_file = st.file_uploader("Envie uma imagem da receita (.jpg, .png)", type=["jpg", "jpeg", "png"])

if uploaded_file:
    nome_base = proximo_nome_receita()
    extensao = uploaded_file.name.split(".")[-1]
    nome_arquivo = f"{nome_base}.{extensao}"

    caminho_imagem = os.path.join(IMAGES_DIR, nome_arquivo)

    # Salva a imagem localmente
    with open(caminho_imagem, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.image(caminho_imagem, caption="Imagem salva com sucesso 📸")

    # Realiza o OCR com a API
    with st.spinner("Processando OCR..."):
        with open(caminho_imagem, "rb") as image_file:
            response = requests.post(
                OCR_API_URL,
                files={"file": image_file},  # Usando 'file' conforme documentação
                data={"apikey": OCR_API_KEY, "language": "por", "isOverlayRequired": True},
                timeout=30  # Timeout aumentado para 30 segundos
            )

    st.write("Status Code:", response.status_code)
    st.write("Resposta:", response.text)

    if response.status_code == 200:
        ocr_result = response.json()
        st.success("OCR processado com sucesso!")
        
        # Exibe o texto extraído
        st.subheader("Texto Extraído")
        st.code(ocr_result["ParsedResults"][0]["ParsedText"], language="text")

        # Exibe o JSON completo retornado pela API
        st.subheader("JSON Completo")
        st.json(ocr_result)

        # Botão para baixar o JSON manualmente
        st.download_button(
            label="Baixar JSON",
            data=json.dumps(ocr_result, indent=2, ensure_ascii=False),
            file_name=f"{nome_base}.json",
            mime="application/json"
        )
    else:
        st.error("Erro ao processar OCR.")
