import json
import os
from datetime import datetime

class FilaSenhas:
    def __init__(self):
        self.fila = []
        self.atendidas = []
        self.contador = 1
    
    def gerar_senha(self, tipo="Normal"):
        prefixo = "P" if tipo == "Prioritário" else "N"
        numero = str(self.contador).zfill(3)
        senha = f"{prefixo}{numero}"
        
        self.fila.append({
            "senha": senha,
            "tipo": tipo,
            "horario": datetime.now().strftime("%H:%M:%S"),
            "status": "Aguardando"
        })
        self.contador += 1
        return senha
    
    def chamar_proximo(self):
        if not self.fila:
            return None
        
        prioritarios = [s for s in self.fila if s["tipo"] == "Prioritário"]
        normais = [s for s in self.fila if s["tipo"] == "Normal"]
        self.fila = prioritarios + normais
        
        senha = self.fila.pop(0)
        senha["status"] = "Atendido"
        senha["horario_atendimento"] = datetime.now().strftime("%H:%M:%S")
        self.atendidas.append(senha)
        return senha
    
    def listar_fila(self):
        return self.fila
    
    def total_aguardando(self):
        return len(self.fila)
    
    def total_atendidos(self):
        return len(self.atendidas)