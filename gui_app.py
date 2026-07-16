import customtkinter as ctk
from tkinter import messagebox
from senhas import FilaSenhas
from banco import salvar_dados, carregar_dados
import threading
import time

# Configurar o tema/aparência padrão (escuro ou claro)
ctk.set_appearance_mode("dark")  # Opções: "dark", "light"
ctk.set_default_color_theme("blue")  # Azul padrão

class SistemaSenhasGUI:
    def __init__(self):
        # 1. Carregar dados salvos
        fila, atendidas, contador = carregar_dados()
        
        # 2. Criar a lógica do sistema com os dados carregados
        self.sistema = FilaSenhas()
        self.sistema.fila = fila
        self.sistema.atendidas = atendidas
        self.sistema.contador = contador

        # 3. Criar a Janela Principal (Farmacêuticas)
        self.janela_staff = ctk.CTk()
        self.janela_staff.title("🏥 Painel da Farmácia")
        self.janela_staff.geometry("900x600")
        
        # 4. Criar a Janela de Exibição para Pacientes (segundo monitor)
        self.criar_janela_pacientes()

        # 5. Construir os botões e listas da interface
        self.criar_widgets_staff()

        # 6. Atualizar as telas pela primeira vez
        self.atualizar_tudo()

        # 7. Iniciar o loop da interface
        self.janela_staff.mainloop()

    def criar_janela_pacientes(self):
        """Cria a segunda janela (tela do paciente)."""
        self.janela_pacientes = ctk.CTkToplevel(self.janela_staff)
        self.janela_pacientes.title("📢 Chamada de Senhas")
        self.janela_pacientes.geometry("800x500")
        self.janela_pacientes.attributes('-topmost', True)  # Fica sempre na frente
        
        # Frame principal da tela do paciente
        frame_paciente = ctk.CTkFrame(self.janela_pacientes)
        frame_paciente.pack(fill="both", expand=True, padx=20, pady=20)

        # Label "ÚLTIMA SENHA CHAMADA"
        self.label_titulo_chamada = ctk.CTkLabel(
            frame_paciente, 
            text="🕒 ÚLTIMA CHAMADA", 
            font=ctk.CTkFont(size=30, weight="bold")
        )
        self.label_titulo_chamada.pack(pady=(10, 0))

        # Label com a senha em tamanho GIGANTE
        self.label_senha_atual = ctk.CTkLabel(
            frame_paciente, 
            text="AGUARDE", 
            font=ctk.CTkFont(size=120, weight="bold"),
            text_color="#00FF00"  # Verde
        )
        self.label_senha_atual.pack(pady=20)

        # Label "PRÓXIMOS DA FILA"
        self.label_proximos_titulo = ctk.CTkLabel(
            frame_paciente, 
            text="🔜 PRÓXIMOS", 
            font=ctk.CTkFont(size=25, weight="bold")
        )
        self.label_proximos_titulo.pack(pady=(20, 0))

        # Label para listar os próximos (usaremos texto puro)
        self.label_lista_proximos = ctk.CTkLabel(
            frame_paciente, 
            text="", 
            font=ctk.CTkFont(size=22)
        )
        self.label_lista_proximos.pack(pady=10)

    def criar_widgets_staff(self):
        """Cria todos os botões, listas e campos da tela das farmacêuticas."""
        
        # Grid: Dividir a tela em esquerda (controles) e direita (fila)
        # Coluna 0 (esquerda) e Coluna 1 (direita)
        self.janela_staff.grid_columnconfigure(0, weight=1)
        self.janela_staff.grid_columnconfigure(1, weight=1)
        self.janela_staff.grid_rowconfigure(0, weight=1)

        # --- LADO ESQUERDO: Painel de Controle ---
        frame_controles = ctk.CTkFrame(self.janela_staff)
        frame_controles.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        frame_controles.grid_rowconfigure(4, weight=1)  # Empurra as coisas pra cima

        titulo = ctk.CTkLabel(
            frame_controles, 
            text="🎛️ PAINEL DE CONTROLE", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        titulo.pack(pady=20)

        # Botão Gerar Normal
        btn_normal = ctk.CTkButton(
            frame_controles, 
            text="📌 Gerar Senha Normal", 
            command=self.gerar_normal,
            height=50,
            font=ctk.CTkFont(size=16)
        )
        btn_normal.pack(pady=10, padx=20, fill="x")

        # Botão Gerar Prioritário
        btn_prioritario = ctk.CTkButton(
            frame_controles, 
            text="⭐ Gerar Senha Prioritária", 
            command=self.gerar_prioritario,
            height=50,
            fg_color="#D4770A",  # Laranja
            hover_color="#A85C08",
            font=ctk.CTkFont(size=16)
        )
        btn_prioritario.pack(pady=10, padx=20, fill="x")

        # Botão Chamar Próximo
        btn_chamar = ctk.CTkButton(
            frame_controles, 
            text="📢 Chamar Próximo", 
            command=self.chamar_proximo,
            height=50,
            fg_color="#1F8D4D",  # Verde
            hover_color="#146C3A",
            font=ctk.CTkFont(size=16)
        )
        btn_chamar.pack(pady=10, padx=20, fill="x")

        # Separador
        ctk.CTkLabel(frame_controles, text="", height=10).pack()

        # Estatísticas
        self.label_stats = ctk.CTkLabel(
            frame_controles, 
            text="📊 Aguardando: 0  |  Atendidos: 0", 
            font=ctk.CTkFont(size=18)
        )
        self.label_stats.pack(pady=10)

        # Botão Sair/Salvar
        btn_sair = ctk.CTkButton(
            frame_controles, 
            text="💾 Salvar e Sair", 
            command=self.sair,
            height=40,
            fg_color="#B22222",  # Vermelho escuro
            hover_color="#8B0000",
            font=ctk.CTkFont(size=14)
        )
        btn_sair.pack(pady=20, padx=20, fill="x")

        # --- LADO DIREITO: Visualização da Fila ---
        frame_fila = ctk.CTkFrame(self.janela_staff)
        frame_fila.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        frame_fila.grid_rowconfigure(1, weight=1)
        frame_fila.grid_columnconfigure(0, weight=1)

        label_fila_titulo = ctk.CTkLabel(
            frame_fila, 
            text="📋 FILA DE ESPERA", 
            font=ctk.CTkFont(size=20, weight="bold")
        )
        label_fila_titulo.grid(row=0, column=0, pady=10)

        # Usando uma Textbox para mostrar a fila (rolagem automática)
        self.textbox_fila = ctk.CTkTextbox(frame_fila, font=ctk.CTkFont(size=18))
        self.textbox_fila.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

    # ========== FUNÇÕES DOS BOTÕES ==========

    def gerar_normal(self):
        senha = self.sistema.gerar_senha("Normal")
        messagebox.showinfo("Sucesso", f"Senha {senha} gerada com sucesso!")
        self.atualizar_tudo()

    def gerar_prioritario(self):
        senha = self.sistema.gerar_senha("Prioritário")
        messagebox.showinfo("Sucesso", f"Senha {senha} (Prioritária) gerada com sucesso!")
        self.atualizar_tudo()

    def chamar_proximo(self):
        proximo = self.sistema.chamar_proximo()
        if proximo:
            # Exibe na tela do paciente
            self.label_senha_atual.configure(
                text=proximo['senha'], 
                text_color="#FFD700"  # Dourado
            )
            messagebox.showinfo("Chamada", f"📢 Chamando: {proximo['senha']}")
        else:
            messagebox.showwarning("Atenção", "Nenhum paciente na fila!")
            self.label_senha_atual.configure(text="AGUARDE", text_color="#00FF00")
        self.atualizar_tudo()

    def atualizar_tudo(self):
        """Atualiza a lista da fila, estatísticas e a tela do paciente."""
        # 1. Atualizar Textbox da fila (Staff)
        fila = self.sistema.listar_fila()
        self.textbox_fila.delete("1.0", "end")
        
        if not fila:
            self.textbox_fila.insert("1.0", "📭 Fila vazia.")
        else:
            for i, s in enumerate(fila, 1):
                tipo_icone = "⭐" if s["tipo"] == "Prioritário" else "📌"
                linha = f"{i}º - {s['senha']} ({s['tipo']}) {tipo_icone}  [{s['horario']}]\n"
                self.textbox_fila.insert("end", linha)

        # 2. Atualizar Estatísticas (Staff)
        self.label_stats.configure(
            text=f"📊 Aguardando: {self.sistema.total_aguardando()}  |  Atendidos: {self.sistema.total_atendidos()}"
        )

        # 3. Atualizar Tela do Paciente (Próximos)
        proximos = self.sistema.listar_fila()[:5]  # Mostra só os 5 primeiros
        if not proximos:
            self.label_lista_proximos.configure(text="Nenhum paciente aguardando.")
        else:
            texto_proximos = "  |  ".join([s['senha'] for s in proximos])
            self.label_lista_proximos.configure(text=texto_proximos)

        # 4. Salvar automaticamente os dados no JSON a cada atualização
        salvar_dados(self.sistema.fila, self.sistema.atendidas, self.sistema.contador)

    def sair(self):
        """Salva e fecha o programa."""
        salvar_dados(self.sistema.fila, self.sistema.atendidas, self.sistema.contador)
        self.janela_staff.destroy()

# ========== PONTO DE ENTRADA ==========
if __name__ == "__main__":
    app = SistemaSenhasGUI()