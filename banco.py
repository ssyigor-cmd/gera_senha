import json
import os
import sys
import shutil
import logging

logger = logging.getLogger(__name__)

def obter_caminho_absoluto():
    """Retorna o caminho da pasta onde o programa está sendo executado."""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
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
    
    try:
        with open(temp_path, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=2, ensure_ascii=False)
        
        if os.path.exists(arquivo_path):
            os.remove(arquivo_path)
        os.rename(temp_path, arquivo_path)
        
        logger.info(f"Dados salvos com sucesso. Fila: {len(fila)}, Atendidos: {len(atendidas)}")  # <-- NOVO
    except Exception as e:
        logger.exception(f"ERRO CRÍTICO ao salvar dados: {e}")  # <-- NOVO (guarda o traceback)

def carregar_dados():
    """Carrega os dados. Se o arquivo estiver corrompido, faz backup e começa do zero."""
    pasta = obter_caminho_absoluto()
    arquivo_path = os.path.join(pasta, "dados.json")
    
    if not os.path.exists(arquivo_path):
        logger.info("Arquivo dados.json não encontrado. Iniciando do zero.")  # <-- NOVO
        return [], [], 1, None
    
    try:
        with open(arquivo_path, "r", encoding="utf-8") as f:
            dados = json.load(f)
        logger.info(f"Dados carregados: {len(dados.get('fila', []))} na fila, {len(dados.get('atendidas', []))} atendidos.")  # <-- NOVO
        return (
            dados.get("fila", []),
            dados.get("atendidas", []),
            dados.get("contador", 1),
            dados.get("ultima_chamada")
        )
    except (json.JSONDecodeError, Exception) as e:
        # Se o arquivo quebrou, faz backup e começa do zero
        backup_path = arquivo_path + ".corrompido.backup"
        try:
            shutil.move(arquivo_path, backup_path)
            # Aqui usamos ERROR porque é um problema grave, mas o sistema se recupera
            logger.error(f"Arquivo de dados estava corrompido. Backup salvo como: {backup_path}. Erro: {e}")  # <-- NOVO
        except Exception as e2:
            logger.exception(f"Não foi possível fazer backup do arquivo corrompido: {e2}")  # <-- NOVO
        return [], [], 1, None