# logger.py
import logging
import os
from banco import obter_caminho_absoluto

def setup_logging():
    """Configura o sistema de logs para gravar em arquivo e no console."""
    pasta = obter_caminho_absoluto()
    arquivo_log = os.path.join(pasta, "app.log")

    # Configuração principal
    logging.basicConfig(
        level=logging.INFO,  # Pode mudar para DEBUG se precisar de mais detalhes
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
            # 1. Salva no arquivo app.log (com codificação UTF-8 para caracteres especiais)
            logging.FileHandler(arquivo_log, encoding='utf-8'),
            # 2. Também exibe no console (terminal) para debug ao vivo
            logging.StreamHandler()
        ]
    )