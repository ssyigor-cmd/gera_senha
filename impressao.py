from banco import obter_caminho_absoluto
import os
import tempfile
from datetime import datetime


def imprimir_senha(senha, tipo, config):
    """
    Imprime um comprovante com a senha.
    Se a impressora estiver configurada, envia direto.
    Caso contrário, salva um arquivo .txt na pasta.
    """
    try:
        if config.get("impressora_ativada", False):
            # Tenta imprimir na impressora térmica
            return imprimir_na_termica(senha, tipo, config)
        else:
            # Salva um arquivo .txt
            return salvar_txt_senha(senha, tipo)
    except Exception as e:
        print(f"Erro na impressão: {e}")
        return False

def imprimir_na_termica(senha, tipo, config):
    """Envia o texto para a impressora térmica (Windows)"""
    try:
        # Texto formatado para impressora térmica (80mm)
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
        # Tenta enviar para a impressora padrão
        import win32print
        import win32ui
        
        printer_name = config.get("impressora_nome") or win32print.GetDefaultPrinter()
        hprinter = win32print.OpenPrinter(printer_name)
        try:
            # Cria um job de impressão
            job_id = win32print.StartDocPrinter(hprinter, 1, ("Senha", None, "RAW"))
            win32print.StartPagePrinter(hprinter)
            win32print.WritePrinter(hprinter, texto.encode('utf-8'))
            win32print.EndPagePrinter(hprinter)
            win32print.EndDocPrinter(hprinter)
        finally:
            win32print.ClosePrinter(hprinter)
        
        return True
    except ImportError:
        # Se não tiver win32print, salva como arquivo de texto
        return salvar_txt_senha(senha, tipo)
    except Exception as e:
        print(f"Erro na impressão térmica: {e}")
        return salvar_txt_senha(senha, tipo)

def salvar_txt_senha(senha, tipo):
    """Salva um arquivo .txt com a senha na pasta 'comprovantes'"""
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
    
    return caminho