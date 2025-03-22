# Centro Multifocal OCR App

Aplicativo Streamlit que lê receitas oftalmológicas, extrai automaticamente os 12 campos estruturados (OD/OE, perto/longe, esférico/cilindro/eixo), e prepara os dados para um modelo de IA.

## Funcionalidades

- Upload de imagem da receita
- OCR via API OCR.space
- Parser baseado em texto ou em posições
- Armazenamento dos dados estruturados para futura IA
- Dataset de exemplos reais (em `dataset_receitas/`)

## Como rodar

```bash
cd app
pip install -r requirements.txt
streamlit run app.py
