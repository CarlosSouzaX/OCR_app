# ocr_parser.py
import re

def is_valor_numerico(valor):
    return re.match(r'^[-+]?\d+(?:[\.,]\d+)?$', valor) is not None

def extrair_valores_receita(texto_ocr: str):
    linhas = texto_ocr.splitlines()
    valores = {
        "OD_longe_esferico": None, "OD_longe_cilindrico": None, "OD_longe_eixo": None,
        "OE_longe_esferico": None, "OE_longe_cilindrico": None, "OE_longe_eixo": None,
        "OD_perto_esferico": None, "OD_perto_cilindrico": None, "OD_perto_eixo": None,
        "OE_perto_esferico": None, "OE_perto_cilindrico": None, "OE_perto_eixo": None
    }

    linhas = [l.strip().upper() for l in linhas if l.strip()]

    bloco_atual = None
    olho_atual = None
    campo_atual = None

    for linha in linhas:
        # Define se estamos no bloco "Longe" ou "Perto"
        if "LONGE" in linha:
            bloco_atual = "longe"
            continue
        elif "PERTO" in linha:
            bloco_atual = "perto"
            continue

        # Identifica o olho
        if any(sig in linha for sig in ["OD", "O.D", "O.D."]):
            olho_atual = "OD"
            continue
        elif any(sig in linha for sig in ["OE", "O.E", "O.E."]):
            olho_atual = "OE"
            continue

        # Identifica o campo
        if "ESFER" in linha:
            campo_atual = "esferico"
            continue
        elif "CIL" in linha:
            campo_atual = "cilindrico"
            continue
        elif "EIX" in linha or "AXIS" in linha:
            campo_atual = "eixo"
            continue

        # Se a linha atual for um número e sabemos onde estamos, atribuímos
        if is_valor_numerico(linha) and bloco_atual and olho_atual and campo_atual:
            chave = f"{olho_atual}_{bloco_atual}_{campo_atual}".lower()
            valores[chave] = linha
            campo_atual = None  # reseta após uso

    return valores
