import matplotlib.pyplot as plt
from datetime import datetime
import os
from banco import obter_caminho_absoluto

def gerar_grafico_atendimentos(atendidas, salvar=True):
    """Gera gráfico de barras com atendimentos por hora"""
    if not atendidas:
        return None
    
    # Extrair horas
    horas = []
    for s in atendidas:
        if 'horario_atendimento' in s:
            h = datetime.strptime(s['horario_atendimento'], "%H:%M:%S").hour
            horas.append(h)
    
    if not horas:
        return None
    
    # Contar frequência por hora
    from collections import Counter
    contagem = Counter(horas)
    horas_ordenadas = sorted(contagem.keys())
    valores = [contagem[h] for h in horas_ordenadas]
    
    # Criar gráfico
    plt.figure(figsize=(10, 5))
    plt.bar(horas_ordenadas, valores, color='#1F8D4D')
    plt.xlabel('Hora do dia')
    plt.ylabel('Número de atendimentos')
    plt.title('Atendimentos por hora')
    plt.xticks(range(min(horas_ordenadas), max(horas_ordenadas)+1))
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    if salvar:
        pasta = obter_caminho_absoluto()
        caminho = os.path.join(pasta, "relatorios")
        os.makedirs(caminho, exist_ok=True)
        data = datetime.now().strftime("%Y%m%d")
        arquivo = os.path.join(caminho, f"grafico_{data}.png")
        plt.savefig(arquivo, dpi=100, bbox_inches='tight')
        plt.close()
        return arquivo
    else:
        plt.show()
        return None

def calcular_tempo_medio(atendidas):
    """Calcula o tempo médio de espera (minutos) entre geração e atendimento"""
    tempos = []
    for s in atendidas:
        if 'horario' in s and 'horario_atendimento' in s:
            try:
                h_geracao = datetime.strptime(s['horario'], "%H:%M:%S")
                h_atend = datetime.strptime(s['horario_atendimento'], "%H:%M:%S")
                diff = (h_atend - h_geracao).total_seconds() / 60.0
                tempos.append(diff)
            except:
                continue
    if tempos:
        return sum(tempos) / len(tempos)
    return 0