import os
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A6, landscape
from reportlab.lib.units import mm
from banco import obter_caminho_absoluto

def gerar_pdf_senha(senha, tipo, nome_farmacia="Farmácia Base Regional"):
    """Gera um PDF com a senha para impressão"""
    pasta = obter_caminho_absoluto()
    data_hora = datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_arquivo = f"senha_{senha}_{data_hora}.pdf"
    caminho = os.path.join(pasta, "impressos", nome_arquivo)
    
    # Criar pasta se não existir
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    
    # Configurar página (formato A6 paisagem)
    c = canvas.Canvas(caminho, pagesize=landscape(A6))
    largura, altura = landscape(A6)
    
    # Título
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(largura/2, altura-10*mm, nome_farmacia)
    
    # Tipo
    c.setFont("Helvetica", 10)
    c.drawCentredString(largura/2, altura-18*mm, f"Senha {tipo}")
    
    # Senha em tamanho grande
    c.setFont("Helvetica-Bold", 40)
    c.drawCentredString(largura/2, altura-32*mm, senha)
    
    # Data/hora
    c.setFont("Helvetica", 8)
    c.drawCentredString(largura/2, 8*mm, datetime.now().strftime("%d/%m/%Y %H:%M"))
    
    c.save()
    return caminho

def imprimir_senha(senha, tipo):
    """Função principal chamada pela GUI: gera PDF e imprime (se houver impressora configurada)"""
    # Por enquanto só gera PDF
    caminho = gerar_pdf_senha(senha, tipo)
    # Aqui você pode adicionar código para enviar para impressora térmica via win32print
    # Exemplo:
    # import win32print
    # import win32ui
    # ... (requer pywin32)
    return caminho