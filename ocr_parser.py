# ocr_parser.py
import re

def is_valor_numerico(valor: str) -> bool:
    valor = valor.replace(" ", "").replace("–", "-").replace("O", "0")
    return re.match(r'^[-+]?\d+(?:[\.,]\d+)?$', valor) is not None

def limpar_valor(valor: str) -> str:
    return valor.replace(" ", "").replace("–", "-").replace("O", "0")

def linha_parecida_com(valor: str, alternativas: list) -> bool:
    return any(alt in valor for alt in alternativas)

def extrair_valores_receita(texto_ocr: str, debug=False):
    valores = {
        "OD_longe_esferico": None, "OD_longe_cilindrico": None, "OD_longe_eixo": None,
        "OE_longe_esferico": None, "OE_longe_cilindrico": None, "OE_longe_eixo": None,
        "OD_perto_esferico": None, "OD_perto_cilindrico": None, "OD_perto_eixo": None,
        "OE_perto_esferico": None, "OE_perto_cilindrico": None, "OE_perto_eixo": None
    }

    linhas = texto_ocr.splitlines()
    linhas = [l.strip().upper() for l in linhas if l.strip()]

    if debug:
        print("🪵 Linhas OCR:")
        for l in linhas:
            print(f"- {l}")

    bloco = None
    index = 0

    while index < len(linhas):
        linha = linhas[index]

        if "LONGE" in linha:
            bloco = "longe"
            index += 1
            continue
        elif "PERTO" in linha:
            bloco = "perto"
            index += 1
            continue

        if bloco and linha_parecida_com(linha, ["OD", "O.D", "0D", "0.D"]):
            valores = preencher_valores(linhas, index, bloco, "OD", valores)
            index += 4
            continue
        elif bloco and linha_parecida_com(linha, ["OE", "O.E", "0E", "0.E"]):
            valores = preencher_valores(linhas, index, bloco, "OE", valores)
            index += 4
            continue

        index += 1

    return valores

def preencher_valores(linhas, index, bloco, olho, valores):
    try:
        esf = limpar_valor(linhas[index + 1])
        cil = limpar_valor(linhas[index + 2])
        eixo = limpar_valor(linhas[index + 3])
        prefixo = f"{olho}_{bloco}_".lower()

        if is_valor_numerico(esf):
            valores[prefixo + "esferico"] = esf
        if is_valor_numerico(cil):
            valores[prefixo + "cilindrico"] = cil
        if is_valor_numerico(eixo):
            valores[prefixo + "eixo"] = eixo
    except IndexError:
        pass

    return valores
