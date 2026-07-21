from banco import obter_caminho_absoluto
import json
import os
from datetime import datetime

import config

class FilaSenhas:
    def __init__(self, fila=None, atendidas=None, contador=1, ultima_chamada=None):
        self.fila = fila if fila is not None else []
        self.atendidas = atendidas if atendidas is not None else []
        self.contador = contador
        self.ultima_chamada = ultima_chamada  # Guarda a última senha chamada
    
    def gerar_senha(self, tipo="Normal", config=None):
        """
        Gera uma nova senha.
        - Prioritário: insere no início da fila, mas depois de outros prioritários (ordem de chegada).
        - Normal: insere no final da fila.
        """
        if config:
            prefixo_normal = config.get("prefixo_normal", "N")
            prefixo_prioritario = config.get("prefixo_prioritario", "P")
        else:
            prefixo_normal = "N"
            prefixo_prioritario = "P"

        prefixo = prefixo_prioritario if tipo == "Prioritário" else prefixo_normal
        numero = str(self.contador).zfill(3)
        senha = f"{prefixo}{numero}"

        nova_senha = {
            "senha": senha,
            "tipo": tipo,
            "horario": datetime.now().strftime("%H:%M:%S"),
            "status": "Aguardando"
        }

        # Lógica de prioridade
        if tipo == "Prioritário":
            # Insere na posição: depois do último prioritário existente, mas antes dos normais
            insert_index = 0
            for i, s in enumerate(self.fila):
                if s["tipo"] == "Prioritário":
                    insert_index = i + 1  # Vai para depois do último prioritário
            self.fila.insert(insert_index, nova_senha)
        else:
            # Senha normal: vai para o final
            self.fila.append(nova_senha)

        self.contador += 1
        return senha    
    
    def chamar_proximo(self):
        """Remove e retorna a primeira senha da fila."""
        if not self.fila:
            return None
        
        senha = self.fila.pop(0)
        senha["status"] = "Atendido"
        senha["horario_atendimento"] = datetime.now().strftime("%H:%M:%S")
        self.atendidas.append(senha)
        self.ultima_chamada = senha  # Guarda para re-chamar
        return senha
    
    def rechamar_ultimo(self):
        """Retorna a última senha chamada (sem removê-la da fila, pois já foi atendida)."""
        return self.ultima_chamada
    
    def remover_por_senha(self, codigo_senha):
        """Remove uma senha específica da fila (ex: paciente desistiu)."""
        for i, s in enumerate(self.fila):
            if s["senha"] == codigo_senha:
                return self.fila.pop(i)
        return None
    
    def resetar_dia(self):
        """Reseta a fila, o histórico e o contador para 1."""
        self.fila = []
        self.atendidas = []
        self.contador = 1
        self.ultima_chamada = None
    
    def listar_fila(self):
        return self.fila
    
    def total_aguardando(self):
        return len(self.fila)
    
    def total_atendidos(self):
        return len(self.atendidas)
    
    def exportar_relatorio(self):
        """Gera um arquivo .txt com o relatório do dia (senhas atendidas)."""
        if not self.atendidas:
            return None
        
        data_atual = datetime.now().strftime("%Y-%m-%d")
        nome_arquivo = f"relatorio_atendidos_{data_atual}.txt"
        
        pasta = obter_caminho_absoluto()
        nome_arquivo = f"relatorio_atendidos_{data_atual}.txt"
        caminho_completo = os.path.join(pasta, nome_arquivo)
        
        with open(caminho_completo, "w", encoding="utf-8") as f:
            f.write(f"RELATÓRIO DE ATENDIMENTOS - {data_atual}\n")
            f.write("=" * 40 + "\n\n")
            for idx, s in enumerate(self.atendidas, 1):
                f.write(f"{idx}º - Senha: {s['senha']} | Tipo: {s['tipo']} | Atendido às: {s.get('horario_atendimento', 'N/A')}\n")
            f.write(f"\nTotal de atendimentos: {len(self.atendidas)}")
        
        return caminho_completo