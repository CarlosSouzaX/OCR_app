# ocr_parser.py
import re

def is_valor_numerico(valor: str) -> bool:
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

    # Etapa 1: encontrar a ordem dos olhos (OD, OE, OD, OE)
    indices_olhos = [i for i, l in enumerate(linhas) if l in ["OD", "O.D", "OE", "O.E"]]
    if len(indices_olhos) != 4:
        return valores  # Não está no padrão esperado

    olhos = ["OD_longe", "OE_longe", "OD_perto", "OE_perto"]

    # Etapa 2: encontrar valores por seção
    def capturar_valores(titulo):
        try:
            idx = linhas.index(titulo)
            return [linhas[idx + 1], linhas[idx + 2], linhas[idx + 3], linhas[idx + 4]]
        except:
            return [None, None, None, None]

    esfericos = capturar_valores("ESFÉRICO")
    cilindricos = capturar_valores("CILINDRO")
    eixos = capturar_valores("EIXO")

    # Etapa 3: montar os campos
    for i in range(4):
        chave_base = olhos[i]
        if esfericos[i] and is_valor_numerico(esfericos[i]):
            valores[f"{chave_base}_esferico"] = esfericos[i]
        if cilindricos[i] and is_valor_numerico(cilindricos[i]):
            valores[f"{chave_base}_cilindrico"] = cilindricos[i]
        if eixos[i] and is_valor_numerico(eixos[i]):
            valores[f"{chave_base}_eixo"] = eixos[i]

    return valores
