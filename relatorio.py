from banco import obter_caminho_absoluto
import os
from datetime import datetime
import matplotlib
matplotlib.use('Agg')  # Usa backend não interativo para salvar sem exibir
import matplotlib.pyplot as plt
import numpy as np

def gerar_graficos(atendidas):
    """
    Gera gráficos de barras e pizza com as estatísticas de atendimentos.
    Retorna o caminho do arquivo de imagem salvo.
    """
    if not atendidas:
        return None

    pasta = os.path.join(obter_caminho_absoluto(), "estatisticas")
    os.makedirs(pasta, exist_ok=True)

    nome_arquivo = f"graficos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    caminho = os.path.join(pasta, nome_arquivo)

    # Contar por tipo
    tipos = {}
    for s in atendidas:
        tipo = s.get("tipo", "Normal")
        tipos[tipo] = tipos.get(tipo, 0) + 1

    # Contar por hora (opcional)
    horas = {}
    for s in atendidas:
        horario = s.get("horario_atendimento", "")
        if horario:
            hora = horario[:2]
            horas[hora] = horas.get(hora, 0) + 1

    # Criar figura com 2 subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle(f"Estatísticas de Atendimentos - {datetime.now().strftime('%d/%m/%Y')}", fontsize=16)

    # Gráfico de barras: por tipo
    tipos_ordenados = sorted(tipos.keys())
    valores = [tipos[t] for t in tipos_ordenados]
    cores = ['#1f77b4', '#ff7f0e']  # azul e laranja
    ax1.bar(tipos_ordenados, valores, color=cores[:len(tipos_ordenados)])
    ax1.set_title('Atendimentos por Tipo')
    ax1.set_ylabel('Quantidade')
    for i, v in enumerate(valores):
        ax1.text(i, v + 0.1, str(v), ha='center', va='bottom')

    # Gráfico de pizza: distribuição percentual
    if tipos:
        ax2.pie(valores, labels=tipos_ordenados, autopct='%1.1f%%', startangle=90, colors=cores[:len(tipos_ordenados)])
        ax2.set_title('Distribuição Percentual')

    plt.tight_layout()
    plt.savefig(caminho, dpi=100, bbox_inches='tight')
    plt.close(fig)  # libera memória

    return caminho

def gerar_grafico_atendimentos(atendidas):
    """
    Mantido para compatibilidade com chamadas antigas (se houver).
    Agora chama gerar_graficos.
    """
    return gerar_graficos(atendidas)

def calcular_tempo_medio(atendidas):
    """Calcula o tempo médio de espera em minutos."""
    tempos = []
    for s in atendidas:
        if "horario" in s and "horario_atendimento" in s:
            try:
                h1 = datetime.strptime(s["horario"], "%H:%M:%S")
                h2 = datetime.strptime(s["horario_atendimento"], "%H:%M:%S")
                diff = (h2 - h1).total_seconds() / 60
                if diff >= 0:
                    tempos.append(diff)
            except:
                continue
    if tempos:
        return sum(tempos) / len(tempos)
    return 0