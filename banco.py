import json
import os

ARQUIVO = "dados.json"

def salvar_dados(fila, atendidas, contador):
    dados = {
        "fila": fila,
        "atendidas": atendidas,
        "contador": contador
    }
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)

def carregar_dados():
    if not os.path.exists(ARQUIVO):
        return [], [], 1
    
    with open(ARQUIVO, "r", encoding="utf-8") as f:
        dados = json.load(f)
    
    return dados["fila"], dados["atendidas"], dados["contador"]