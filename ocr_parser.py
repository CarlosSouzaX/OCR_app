# ocr_parser.py
import re

def is_valor_numerico(valor):
    return re.match(r'^[-+]?\d+(?:[\.,]\d+)?$', valor) is not None

def extrair_valores_receita(texto_ocr: str):
    """
    Extrai os valores da receita a partir do texto OCR, assumindo que a estrutura é:
    Para longe / Para perto
    OD <esf> <cil> <eixo>
    OE <esf> <cil> <eixo>
    """
    valores = {
        "OD_longe_esferico": None, "OD_longe_cilindrico": None, "OD_longe_eixo": None,
        "OE_longe_esferico": None, "OE_longe_cilindrico": None, "OE_longe_eixo": None,
        "OD_perto_esferico": None, "OD_perto_cilindrico": None, "OD_perto_eixo": None,
        "OE_perto_esferico": None, "OE_perto_cilindrico": None, "OE_perto_eixo": None
    }

    linhas = texto_ocr.splitlines()
    linhas = [l.strip().upper() for l in linhas if l.strip()]

    bloco_atual = None  # "longe" ou "perto"

    for linha in linhas:
        if "LONGE" in linha:
            bloco_atual = "longe"
        elif "PERTO" in linha:
            bloco_atual = "perto"
        elif bloco_atual and linha.startswith("OD"):
            partes = linha.split()
            if len(partes) >= 4:
                if is_valor_numerico(partes[1]):
                    valores[f"OD_{bloco_atual}_esferico"] = partes[1]
                if is_valor_numerico(partes[2]):
                    valores[f"OD_{bloco_atual}_cilindrico"] = partes[2]
                if is_valor_numerico(partes[3]):
                    valores[f"OD_{bloco_atual}_eixo"] = partes[3]
        elif bloco_atual and linha.startswith("OE"):
            partes = linha.split()
            if len(partes) >= 4:
                if is_valor_numerico(partes[1]):
                    valores[f"OE_{bloco_atual}_esferico"] = partes[1]
                if is_valor_numerico(partes[2]):
                    valores[f"OE_{bloco_atual}_cilindrico"] = partes[2]
                if is_valor_numerico(partes[3]):
                    valores[f"OE_{bloco_atual}_eixo"] = partes[3]

    return valores
