# ocr_parser.py
import re

def is_valor_numerico(valor):
    return re.match(r'^[-+]?\d+(?:[\.,]\d+)?$', valor) is not None

def extrair_valores_receita(texto_ocr: str):
    """
    Espera extrair 4 linhas com 3 valores cada:
    OD longe, OE longe, OD perto, OE perto
    Colunas: Esférico, Cilíndrico, Eixo
    """
    valores = {
        "OD_longe_esferico": None, "OD_longe_cilindrico": None, "OD_longe_eixo": None,
        "OE_longe_esferico": None, "OE_longe_cilindrico": None, "OE_longe_eixo": None,
        "OD_perto_esferico": None, "OD_perto_cilindrico": None, "OD_perto_eixo": None,
        "OE_perto_esferico": None, "OE_perto_cilindrico": None, "OE_perto_eixo": None
    }

    linhas = texto_ocr.splitlines()
    linhas = [l.strip().upper() for l in linhas if l.strip()]

    # Extrai apenas linhas que começam com OD ou OE
    linhas_validas = [linha for linha in linhas if linha.startswith("OD") or linha.startswith("OE")]

    # Esperamos 4 linhas (OD, OE) × (longe, perto)
    if len(linhas_validas) >= 4:
        mapas = [
            ("OD_longe_", linhas_validas[0]),
            ("OE_longe_", linhas_validas[1]),
            ("OD_perto_", linhas_validas[2]),
            ("OE_perto_", linhas_validas[3])
        ]

        for prefixo, linha in mapas:
            partes = linha.split()
            if len(partes) >= 4:
                esferico = partes[1]
                cilindrico = partes[2]
                eixo = partes[3]
                if is_valor_numerico(esferico):
                    valores[prefixo + "esferico"] = esferico
                if is_valor_numerico(cilindrico):
                    valores[prefixo + "cilindrico"] = cilindrico
                if is_valor_numerico(eixo):
                    valores[prefixo + "eixo"] = eixo

    return valores
