import streamlit as st
import requests

# Configurações da API OCR.space
API_URL = "https://api.ocr.space/parse/image"
API_KEY = st.secrets["API_KEY"]  # usa segredo do Streamlit Cloud

st.title("📄 Leitor de Receita Médica - Centro Multifocal")

uploaded_file = st.file_uploader("Envie sua receita médica (PNG, JPG)", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    files = {"image": uploaded_file}
    data = {"apikey": API_KEY, "language": "por"}

    with st.spinner("Lendo a receita..."):
        response = requests.post(API_URL, files=files, data=data)

    st.subheader("🔍 Resposta da API OCR")
    st.write("Status Code:", response.status_code)

    if response.status_code == 200:
        result = response.json()

        try:
            texto = result["ParsedResults"][0]["ParsedText"]
            st.text_area("📝 Texto extraído da receita:", texto, height=200)

            # Quebra o texto em linhas
            linhas = texto.splitlines()

            # Inicializa variáveis
            grau_esf_od_perto = None
            grau_esf_oe_perto = None

            # Procura por "PWR" (campo do Esférico) e extrai os próximos dois valores
            for i, linha in enumerate(linhas):
                if linha.strip().upper() == "PWR":
                    try:
                        grau_esf_od_perto = linhas[i + 1].strip()
                        grau_esf_oe_perto = linhas[i + 2].strip()
                    except IndexError:
                        pass
                    break

            st.subheader("🔢 Valores extraídos:")
            st.write("Esférico OD (perto):", grau_esf_od_perto or "Não encontrado")
            st.write("Esférico OE (perto):", grau_esf_oe_perto or "Não encontrado")

        except (KeyError, IndexError):
            st.warning("❗ Não foi possível interpretar o texto da receita.")
    else:
        st.error("Erro ao processar a imagem.")
        st.code(response.text)
