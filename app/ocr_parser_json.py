# ocr_parser_json.py
def extrair_receita_estruturada_do_json(ocr_data):
    # Inicializa os campos da receita
    receita = {
        "OD_longe_esferico": None, "OD_longe_cilindrico": None, "OD_longe_eixo": None,
        "OE_longe_esferico": None, "OE_longe_cilindrico": None, "OE_longe_eixo": None,
        "OD_perto_esferico": None, "OD_perto_cilindrico": None, "OD_perto_eixo": None,
        "OE_perto_esferico": None, "OE_perto_cilindrico": None, "OE_perto_eixo": None,
    }

    try:
        linhas = ocr_data['ParsedResults'][0]['TextOverlay']['Lines']

        # Coordenadas aproximadas de linha para cada olho
        mapeamento_linha_top = {
            40: "OD_longe",   # top ≈ 40
            68: "OE_longe",   # top ≈ 68
            95: "OD_perto",   # top ≈ 95
            121: "OE_perto"   # top ≈ 121
        }

        # Coordenadas aproximadas de coluna (Left) para tipo de campo
        def campo_por_left(left):
            if 240 <= left <= 320:
                return "esferico"
            elif 340 <= left <= 420:
                return "cilindrico"
            elif 460 <= left <= 520:
                return "eixo"
            return None

        # Tolerância de comparação (Top pode variar levemente)
        def linha_mais_proxima(top):
            for ref_top in mapeamento_linha_top:
                if abs(top - ref_top) <= 5:
                    return mapeamento_linha_top[ref_top]
            return None

        # Percorre cada linha detectada
        for linha in linhas:
            if "Words" not in linha:
                continue

            for word in linha["Words"]:
                texto = word["WordText"]
                left = word["Left"]
                top = word["Top"]

                linha_ref = linha_mais_proxima(top)
                campo = campo_por_left(left)

                if linha_ref and campo:
                    chave = f"{linha_ref}_{campo}"
                    receita[chave] = texto

        return receita

    except Exception as e:
        print(f"❌ Erro ao processar JSON estruturado: {e}")
        return receita
