import streamlit as st
import requests
import re

# 📌 API OCR.space
API_URL = "https://api.ocr.space/parse/image"
API_KEY = st.secrets["API_KEY"]  # 🔐 configure via .streamlit/secrets.toml

# 📌 Função para extrair os dados da receita médica
def extrair_valores_receita(texto_ocr: str):
    linhas = texto_ocr.splitlines()
    valores = {
        "OD_longe_esferico": None, "OD_longe_cilindrico": None, "OD_longe_eixo": None,
        "OE_longe_esferico": None, "OE_longe_cilindrico": None, "OE_longe_eixo": None,
        "OD_perto_esferico": None, "OD_perto_cilindrico": None, "OD_perto_eixo": None,
        "OE_perto_esferico": None, "OE_perto_cilindrico": None, "OE_perto_eixo": None
    }

    # 🔍 Etapa 1: Normaliza e remove linhas vazias
    linhas = [l.strip().upper() for l in linhas if l.strip()]

    # 🔍 Etapa 2: Busca por palavras-chave (posição)
    try:
        idx_pwr = linhas.index("PWR")
        valores["OD_perto_esferico"] = linhas[idx_pwr + 1]
        valores["OE_perto_esferico"] = linhas[idx_pwr + 2]
    except:
        pass

    try:
        idx_cyl = linhas.index("CYL")
        valores["OD_perto_cilindrico"] = linhas[idx_cyl + 1]
        valores["OE_perto_cilindrico"] = linhas[idx_cyl + 2]
    except:
        pass

    try:
        idx_axis = linhas.index("AXIS")
        valores["OD_perto_eixo"] = linhas[idx_axis + 1]
        valores["OE_perto_eixo"] = linhas[idx_axis + 2]
    except:
        pass

    # 🔍 Etapa 3: Expressões regulares como fallback
    regex_valores = re.findall(r'[-+]?[\d]+(?:[\.,]\d+)?', texto_ocr)
    if len(regex_valores) >= 6:
        valores["OD_longe_esferico"] = regex_valores[0]
        valores["OD_longe_cilindrico"] = regex_valores[1]
        valores["OD_longe_eixo"] = regex_valores[2]
        valores["OE_longe_esferico"] = regex_valores[3]
        valores["OE_longe_cilindrico"] = regex_valores[4]
        valores["OE_longe_eixo"] = regex_valores[5]
    if len(regex_valores) >= 12:
        valores["OD_perto_esferico"] = valores["OD_perto_esferico"] or regex_valores[6]
        valores["OD_perto_cilindrico"] = valores["OD_perto_cilindrico"] or regex_valores[7]
        valores["OD_perto_eixo"] = valores["OD_perto_eixo"] or regex_valores[8]
        valores["OE_perto_esferico"] = valores["OE_perto_esferico"] or regex_valores[9]
        valores["OE_perto_cilindrico"] = valores["OE_perto_cilindrico"] or regex_valores[10]
        valores["OE_perto_eixo"] = valores["OE_perto_eixo"] or regex_valores[11]

    return valores

# 📱 Interface Streamlit
st.set_page_config(page_title="Centro Multifocal - OCR", layout="centered")
st.title("📄 Leitor de Receita Médica - Centro Multifocal")

uploaded_file = st.file_uploader("Envie sua receita médica (PNG, JPG, JPEG)", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    files = {"image": uploaded_file}
    data = {"apikey": API_KEY, "language": "por"}

    with st.spinner("🔍 Lendo a receita..."):
        response = requests.post(API_URL, files=files, data=data)

    if response.status_code == 200:
        ocr_data = response.json()
        try:
            texto = ocr_data["ParsedResults"][0]["ParsedText"]
            st.subheader("📝 Texto extraído da imagem")
            st.text_area("Texto completo:", texto, height=250)

            dados_receita = extrair_valores_receita(texto)

            st.subheader("📊 Dados estruturados da receita:")
            for campo, valor in dados_receita.items():
                st.write(f"**{campo}**: {valor or 'Não encontrado'}")

        except Exception as e:
            st.error("❌ Não foi possível interpretar o texto da receita.")
            st.exception(e)
    else:
        st.error("❌ Erro ao processar a imagem.")
        st.code(response.text)
