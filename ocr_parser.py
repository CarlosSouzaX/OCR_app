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

    try:
        idx_pwr = linhas.index("PWR")
        if is_valor_numerico(linhas[idx_pwr + 1]):
            valores["OD_perto_esferico"] = linhas[idx_pwr + 1]
        if is_valor_numerico(linhas[idx_pwr + 2]):
            valores["OE_perto_esferico"] = linhas[idx_pwr + 2]
    except:
        pass

    try:
        idx_cyl = linhas.index("CYL")
        if is_valor_numerico(linhas[idx_cyl + 1]):
            valores["OD_perto_cilindrico"] = linhas[idx_cyl + 1]
        if is_valor_numerico(linhas[idx_cyl + 2]):
            valores["OE_perto_cilindrico"] = linhas[idx_cyl + 2]
    except:
        pass

    try:
        idx_axis = linhas.index("AXIS")
        if is_valor_numerico(linhas[idx_axis + 1]):
            valores["OD_perto_eixo"] = linhas[idx_axis + 1]
        if is_valor_numerico(linhas[idx_axis + 2]):
            valores["OE_perto_eixo"] = linhas[idx_axis + 2]
    except:
        pass

    regex_valores = re.findall(r'[-+]?\d+(?:[\.,]\d+)?', texto_ocr)
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
