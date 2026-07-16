import json
import os
import sys
import shutil

def obter_caminho_absoluto():
    """Retorna o caminho da pasta onde o programa está sendo executado."""
    if getattr(sys, 'frozen', False):
        # Se for o executável (.exe) gerado pelo PyInstaller
        return os.path.dirname(sys.executable)
    else:
        # Se for o script .py rodando no VS Code
        return os.path.dirname(os.path.abspath(__file__))

def salvar_dados(fila, atendidas, contador, ultima_chamada):
    """Salva os dados com segurança (primeiro em um .tmp, depois renomeia)."""
    dados = {
        "fila": fila,
        "atendidas": atendidas,
        "contador": contador,
        "ultima_chamada": ultima_chamada
    }
    
    pasta = obter_caminho_absoluto()
    arquivo_path = os.path.join(pasta, "dados.json")
    temp_path = arquivo_path + ".tmp"
    
    # Salva no arquivo temporário
    with open(temp_path, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)
    
    # Substitui o principal pelo temporário (se der erro de energia, o original fica intacto)
    if os.path.exists(arquivo_path):
        os.remove(arquivo_path)
    os.rename(temp_path, arquivo_path)

def carregar_dados():
    """Carrega os dados. Se o arquivo estiver corrompido, faz backup e começa do zero."""
    pasta = obter_caminho_absoluto()
    arquivo_path = os.path.join(pasta, "dados.json")
    
    if not os.path.exists(arquivo_path):
        return [], [], 1, None  # Nenhum dado salvo ainda
    
    try:
        with open(arquivo_path, "r", encoding="utf-8") as f:
            dados = json.load(f)
        return (
            dados.get("fila", []),
            dados.get("atendidas", []),
            dados.get("contador", 1),
            dados.get("ultima_chamada")  # Pode ser None
        )
    except (json.JSONDecodeError, Exception) as e:
        # Se o arquivo quebrou, faz backup e começa do zero
        backup_path = arquivo_path + ".corrompido.backup"
        shutil.move(arquivo_path, backup_path)
        print(f"⚠️ Arquivo de dados estava corrompido. Backup salvo como: {backup_path}")
        return [], [], 1, None