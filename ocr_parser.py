# ocr_parser.py
import re

def is_valor_numerico(valor):
    return re.match(r'^[-+]?\d+(?:[\.,]\d+)?$', valor) is not None

def extrair_valores_receita(texto_ocr: str):
    valores = {
        "OD_longe_esferico": None, "OD_longe_cilindrico": None, "OD_longe_eixo": None,
        "OE_longe_esferico": None, "OE_longe_cilindrico": None, "OE_longe_eixo": None,
        "OD_perto_esferico": None, "OD_perto_cilindrico": None, "OD_perto_eixo": None,
        "OE_perto_esferico": None, "OE_perto_cilindrico": None, "OE_perto_eixo": None
    }

    linhas = texto_ocr.splitlines()
    linhas = [l.strip().upper() for l in linhas if l.strip()]

    # Filtra linhas que comecem com OD ou OE e tenham pelo menos 3 valores
    linhas_validas = []
    for linha in linhas:
        if linha.startswith(("OD", "O.D")) or linha.startswith(("OE", "O.E")):
            partes = linha.split()
            if len(partes) >= 4 and all(is_valor_numerico(p) or p == '-' for p in partes[1:4]):
                linhas_validas.append(partes)

    if len(linhas_validas) >= 4:
        campos = [
            ("OD_longe_", linhas_validas[0]),
            ("OE_longe_", linhas_validas[1]),
            ("OD_perto_", linhas_validas[2]),
            ("OE_perto_", linhas_validas[3]),
        ]

        for prefixo, partes in campos:
            esf, cil, eixo = partes[1], partes[2], partes[3]
            if is_valor_numerico(esf):
                valores[prefixo + "esferico"] = esf
            if is_valor_numerico(cil):
                valores[prefixo + "cilindrico"] = cil
            if is_valor_numerico(eixo):
                valores[prefixo + "eixo"] = eixo

    return valores
