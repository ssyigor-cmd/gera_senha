import json
import os
from banco import obter_caminho_absoluto

CONFIG_FILE = "config.json"

def carregar_config():
    """Carrega as configurações do arquivo config.json"""
    pasta = obter_caminho_absoluto()
    caminho = os.path.join(pasta, CONFIG_FILE)
    
    padrao = {
        "prefixo_normal": "N",
        "prefixo_prioritario": "P",
        "som_ativado": True,
        "volume": 0.5,
        "cor_tela": "#000000",  # fundo da tela paciente
        "cor_texto": "#00FF00", # cor da senha
        "fonte_tamanho": 120
    }
    
    if not os.path.exists(caminho):
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(padrao, f, indent=2, ensure_ascii=False)
        return padrao
    
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return padrao

def salvar_config(config):
    pasta = obter_caminho_absoluto()
    caminho = os.path.join(pasta, CONFIG_FILE)
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)