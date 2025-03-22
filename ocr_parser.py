# ocr_parser.py
import re

def is_valor_numerico(valor):
    return re.match(r'^[-+]?\d+(?:[\.,]\d+)?$', valor) is not None

def extrair_valores_receita(texto_ocr: str):
    # Inicializa os campos esperados
    valores = {
        "OD_longe_esferico": None, "OD_longe_cilindrico": None, "OD_longe_eixo": None,
        "OE_longe_esferico": None, "OE_longe_cilindrico": None, "OE_longe_eixo": None,
        "OD_perto_esferico": None, "OD_perto_cilindrico": None, "OD_perto_eixo": None,
        "OE_perto_esferico": None, "OE_perto_cilindrico": None, "OE_perto_eixo": None
    }

    linhas = texto_ocr.splitlines()
    linhas = [l.strip().upper() for l in linhas if l.strip()]

    bloco_atual = None  # "longe" ou "perto"

    try:
        for i, linha in enumerate(linhas):
            if "LONGE" in linha:
                bloco_atual = "longe"
                continue
            elif "PERTO" in linha:
                bloco_atual = "perto"
                continue

            if bloco_atual and linha in ["OD", "O.D", "O.D."]:
                esf = linhas[i+1] if i+1 < len(linhas) else ""
                cil = linhas[i+2] if i+2 < len(linhas) else ""
                eixo = linhas[i+3] if i+3 < len(linhas) else ""

                if is_valor_numerico(esf):
                    valores[f"OD_{bloco_atual}_esferico"] = esf
                if is_valor_numerico(cil):
                    valores[f"OD_{bloco_atual}_cilindrico"] = cil
                if is_valor_numerico(eixo):
                    valores[f"OD_{bloco_atual}_eixo"] = eixo

            elif bloco_atual and linha in ["OE", "O.E", "O.E."]:
                esf = linhas[i+1] if i+1 < len(linhas) else ""
                cil = linhas[i+2] if i+2 < len(linhas) else ""
                eixo = linhas[i+3] if i+3 < len(linhas) else ""

                if is_valor_numerico(esf):
                    valores[f"OE_{bloco_atual}_esferico"] = esf
                if is_valor_numerico(cil):
                    valores[f"OE_{bloco_atual}_cilindrico"] = cil
                if is_valor_numerico(eixo):
                    valores[f"OE_{bloco_atual}_eixo"] = eixo

        # Se nada foi preenchido, tenta modo flexível
        if all(v is None for v in valores.values()):
            valores = fallback_regex(texto_ocr, valores)

    except Exception as e:
        print("Erro durante parsing estruturado:", e)
        valores = fallback_regex(texto_ocr, valores)

    return valores

def fallback_regex(texto: str, valores_dict: dict):
    numeros = re.findall(r'[-+]?\d+(?:[\.,]\d+)?', texto)
    if len(numeros) >= 2:
        valores_dict["OD_perto_esferico"] = numeros[0]
        valores_dict["OE_perto_esferico"] = numeros[1]
    return valores_dict
