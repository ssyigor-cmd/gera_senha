from banco import obter_caminho_absoluto
import os
from datetime import datetime

def gerar_grafico_atendimentos(atendidas):
    """
    Gera um relatório em .txt com as estatísticas.
    (Versão simplificada, sem dependências de imagem)
    """
    if not atendidas:
        return None

    pasta = os.path.join(obter_caminho_absoluto(), "estatisticas")
    os.makedirs(pasta, exist_ok=True)

    nome_arquivo = f"relatorio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    caminho = os.path.join(pasta, nome_arquivo)

    # Contar por tipo
    tipos = {}
    for s in atendidas:
        tipo = s.get("tipo", "Normal")
        tipos[tipo] = tipos.get(tipo, 0) + 1

    # Contar por hora
    horas = {}
    for s in atendidas:
        horario = s.get("horario_atendimento", "")
        if horario:
            hora = horario[:2]
            horas[hora] = horas.get(hora, 0) + 1

    with open(caminho, "w", encoding="utf-8") as f:
        f.write("=" * 40 + "\n")
        f.write("RELATÓRIO DE ATENDIMENTOS\n")
        f.write(f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
        f.write("=" * 40 + "\n\n")

        f.write(f"Total de atendimentos: {len(atendidas)}\n\n")

        f.write("Por tipo:\n")
        for tipo, qtd in tipos.items():
            f.write(f"  - {tipo}: {qtd} ({qtd/len(atendidas)*100:.1f}%)\n")

        if horas:
            f.write("\nAtendimentos por hora:\n")
            for hora, qtd in sorted(horas.items()):
                f.write(f"  - {hora}:00h → {qtd} atendimentos\n")

        if atendidas:
            primeiro = atendidas[0]
            ultimo = atendidas[-1]
            f.write(f"\nPrimeiro atendimento: {primeiro.get('senha')} às {primeiro.get('horario_atendimento', 'N/A')}\n")
            f.write(f"Último atendimento: {ultimo.get('senha')} às {ultimo.get('horario_atendimento', 'N/A')}\n")

    return caminho

def calcular_tempo_medio(atendidas):
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