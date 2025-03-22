import os
import json

# Caminho da pasta onde os arquivos serão salvos
LABELS_DIR = "dataset_receitas/labels"

# Quantidade de arquivos que deseja criar
NUM_RECEITAS = 30  # você pode mudar esse valor

# Template padrão dos campos
TEMPLATE = {
    "OD_longe_esferico": None,
    "OD_longe_cilindrico": None,
    "OD_longe_eixo": None,
    "OE_longe_esferico": None,
    "OE_longe_cilindrico": None,
    "OE_longe_eixo": None,
    "OD_perto_esferico": None,
    "OD_perto_cilindrico": None,
    "OD_perto_eixo": None,
    "OE_perto_esferico": None,
    "OE_perto_cilindrico": None,
    "OE_perto_eixo": None
}

# Garante que o diretório existe
os.makedirs(LABELS_DIR, exist_ok=True)

# Cria os arquivos
for i in range(1, NUM_RECEITAS + 1):
    nome_arquivo = f"receita_{i:03}_labels.json"
    caminho = os.path.join(LABELS_DIR, nome_arquivo)
    
    if not os.path.exists(caminho):  # evita sobrescrever
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(TEMPLATE, f, indent=2, ensure_ascii=False)
        print(f"✅ Criado: {nome_arquivo}")
    else:
        print(f"⚠️ Já existe: {nome_arquivo}")
