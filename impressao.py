from banco import obter_caminho_absoluto
import os
import tempfile
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def imprimir_senha(senha, tipo, config):
    try:
        if config.get("impressora_ativada", False):
            logger.info(f"Tentando imprimir senha {senha} na térmica.")
            return imprimir_na_termica(senha, tipo, config)
        else:
            logger.info(f"Impressora desativada. Salvando arquivo .txt para senha {senha}.")
            return salvar_txt_senha(senha, tipo)
    except Exception as e:
        logger.exception(f"Erro geral na função imprimir_senha: {e}")
        return False

def imprimir_na_termica(senha, tipo, config):
    try:
        import win32print
        import win32ui
        
        linha = "=" * 32
        texto = f"""
{linha}
        FARMÁCIA BASE REGIONAL
        {datetime.now().strftime("%d/%m/%Y %H:%M")}
{linha}
        SENHA: {senha}
        TIPO: {tipo}
{linha}
        AGUARDE SUA VEZ
{linha}
"""
        printer_name = config.get("impressora_nome") or win32print.GetDefaultPrinter()
        logger.info(f"Enviando para impressora: {printer_name}")
        
        hprinter = win32print.OpenPrinter(printer_name)
        try:
            job_id = win32print.StartDocPrinter(hprinter, 1, ("Senha", None, "RAW"))
            win32print.StartPagePrinter(hprinter)
            win32print.WritePrinter(hprinter, texto.encode('utf-8'))
            win32print.EndPagePrinter(hprinter)
            win32print.EndDocPrinter(hprinter)
            logger.info(f"Senha {senha} impressa com sucesso.")
        finally:
            win32print.ClosePrinter(hprinter)
        return True
        
    except ImportError:
        logger.warning("Biblioteca win32print não encontrada. Salvando como .txt.")
        return salvar_txt_senha(senha, tipo)
    except Exception as e:
        logger.exception(f"Falha na impressão térmica para senha {senha}: {e}")
        return salvar_txt_senha(senha, tipo)

def salvar_txt_senha(senha, tipo):
    try:
        pasta = os.path.join(obter_caminho_absoluto(), "comprovantes")
        os.makedirs(pasta, exist_ok=True)
        
        nome_arquivo = f"senha_{senha}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        caminho = os.path.join(pasta, nome_arquivo)
        
        with open(caminho, "w", encoding="utf-8") as f:
            f.write("=" * 30 + "\n")
            f.write("FARMÁCIA BASE REGIONAL\n")
            f.write(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n")
            f.write("=" * 30 + "\n")
            f.write(f"SENHA: {senha}\n")
            f.write(f"TIPO: {tipo}\n")
            f.write("=" * 30 + "\n")
            f.write("AGUARDE SUA VEZ\n")
            f.write("=" * 30 + "\n")
        
        logger.info(f"Arquivo .txt da senha {senha} salvo em: {caminho}")
        return caminho
    except Exception as e:
        logger.exception(f"Erro ao salvar arquivo .txt para senha {senha}: {e}")
        return None