from banco import obter_caminho_absoluto
from config import carregar_config, salvar_config
from tts import falar
from impressao import imprimir_senha
from relatorio import gerar_grafico_atendimentos, calcular_tempo_medio
import customtkinter as ctk
from tkinter import messagebox
from senhas import FilaSenhas
from banco import salvar_dados, carregar_dados
import winsound

# Configuração inicial do tema
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class SistemaSenhasGUI:
    def __init__(self):
        # 1. Carregar configurações
        self.config = carregar_config()

        # 2. Carregar dados salvos
        fila, atendidas, contador, ultima_chamada = carregar_dados()

        # 3. Criar a lógica do sistema
        self.sistema = FilaSenhas(
            fila=fila,
            atendidas=atendidas,
            contador=contador,
            ultima_chamada=ultima_chamada
        )

        # 4. Criar as janelas
        self.janela_staff = ctk.CTk()
        self.janela_staff.title("🏥 Painel da Farmácia")
        self.janela_staff.geometry("1000x700")

        # Janela do Paciente (segunda tela)
        self.criar_janela_pacientes()

        # Construir a interface da staff
        self.criar_widgets_staff()

        # Atualizar tudo pela primeira vez
        self.atualizar_tudo()

        # Iniciar loop
        self.janela_staff.mainloop()

    def criar_janela_pacientes(self):
        self.janela_pacientes = ctk.CTkToplevel(self.janela_staff)
        self.janela_pacientes.title("📢 Chamada de Senhas")
        self.janela_pacientes.geometry("800x500")
        self.janela_pacientes.attributes('-topmost', True)

        frame = ctk.CTkFrame(self.janela_pacientes)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.label_titulo = ctk.CTkLabel(
            frame, text="🕒 ÚLTIMA CHAMADA",
            font=ctk.CTkFont(size=30, weight="bold")
        )
        self.label_titulo.pack(pady=(10, 0))

        self.label_senha_atual = ctk.CTkLabel(
            frame, text="AGUARDE",
            font=ctk.CTkFont(size=120, weight="bold"),
            text_color="#00FF00"
        )
        self.label_senha_atual.pack(pady=20)

        self.label_proximos_titulo = ctk.CTkLabel(
            frame, text="🔜 PRÓXIMOS",
            font=ctk.CTkFont(size=25, weight="bold")
        )
        self.label_proximos_titulo.pack(pady=(20, 0))

        self.label_lista_proximos = ctk.CTkLabel(
            frame, text="",
            font=ctk.CTkFont(size=22)
        )
        self.label_lista_proximos.pack(pady=10)

    def criar_widgets_staff(self):
        self.janela_staff.grid_columnconfigure(0, weight=1)
        self.janela_staff.grid_columnconfigure(1, weight=1)
        self.janela_staff.grid_rowconfigure(0, weight=1)

        # --- LADO ESQUERDO: CONTROLES ---
        frame_controles = ctk.CTkFrame(self.janela_staff)
        frame_controles.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        frame_controles.grid_rowconfigure(8, weight=1)

        titulo = ctk.CTkLabel(
            frame_controles, text="🎛️ PAINEL DE CONTROLE",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        titulo.pack(pady=20)

        # Botões principais
        btn_normal = ctk.CTkButton(
            frame_controles, text="📌 Gerar Senha Normal",
            command=self.gerar_normal, height=50, font=ctk.CTkFont(size=16)
        )
        btn_normal.pack(pady=10, padx=20, fill="x")

        btn_prioritario = ctk.CTkButton(
            frame_controles, text="⭐ Gerar Senha Prioritária",
            command=self.gerar_prioritario, height=50,
            fg_color="#D4770A", hover_color="#A85C08", font=ctk.CTkFont(size=16)
        )
        btn_prioritario.pack(pady=10, padx=20, fill="x")

        btn_chamar = ctk.CTkButton(
            frame_controles, text="📢 Chamar Próximo",
            command=self.chamar_proximo, height=50,
            fg_color="#1F8D4D", hover_color="#146C3A", font=ctk.CTkFont(size=16)
        )
        btn_chamar.pack(pady=10, padx=20, fill="x")

        btn_rechamar = ctk.CTkButton(
            frame_controles, text="🔊 Rechamar Último",
            command=self.rechamar, height=40,
            fg_color="#005A9C", hover_color="#003D6B", font=ctk.CTkFont(size=14)
        )
        btn_rechamar.pack(pady=5, padx=20, fill="x")

        btn_ajustes = ctk.CTkButton(
            frame_controles, text="⚙️ Ajustes",
            command=self.abrir_ajustes, height=40,
            fg_color="#555555", hover_color="#333333"
        )
        btn_ajustes.pack(pady=5, padx=20, fill="x")

        # Frame para remover senha (Entry + Botão)
        frame_remover = ctk.CTkFrame(frame_controles, fg_color="transparent")
        frame_remover.pack(pady=5, padx=20, fill="x")

        self.entry_remover = ctk.CTkEntry(
            frame_remover, placeholder_text="Código (ex: N001)", width=120
        )
        self.entry_remover.pack(side="left", padx=(0, 5), fill="x", expand=True)

        btn_remover = ctk.CTkButton(
            frame_remover, text="❌ Remover",
            command=self.remover_senha, height=40, width=80,
            fg_color="#B22222", hover_color="#8B0000"
        )
        btn_remover.pack(side="right")

        # Botão Resetar Dia
        btn_resetar = ctk.CTkButton(
            frame_controles, text="🔄 Resetar Dia (Limpar Tudo)",
            command=self.resetar_dia, height=40,
            fg_color="#555555", hover_color="#333333", font=ctk.CTkFont(size=14)
        )
        btn_resetar.pack(pady=5, padx=20, fill="x")

        # Botão Relatório
        btn_relatorio = ctk.CTkButton(
            frame_controles, text="📄 Gerar Relatório Diário",
            command=self.exportar_relatorio, height=40,
            fg_color="#8B4513", hover_color="#5C2E0A", font=ctk.CTkFont(size=14)
        )
        btn_relatorio.pack(pady=5, padx=20, fill="x")

        # Botão Estatísticas (Gráficos)
        btn_estatisticas = ctk.CTkButton(
            frame_controles, text="📊 Estatísticas",
            command=self.abrir_estatisticas, height=40,
            fg_color="#6A1B9A", hover_color="#4A148C", font=ctk.CTkFont(size=14)
        )
        btn_estatisticas.pack(pady=5, padx=20, fill="x")

        # Estatísticas
        self.label_stats = ctk.CTkLabel(
            frame_controles, text="📊 Aguardando: 0  |  Atendidos: 0",
            font=ctk.CTkFont(size=18)
        )
        self.label_stats.pack(pady=10)

        # Botão Sair
        btn_sair = ctk.CTkButton(
            frame_controles, text="💾 Salvar e Sair",
            command=self.sair, height=40,
            fg_color="#B22222", hover_color="#8B0000"
        )
        btn_sair.pack(pady=10, padx=20, fill="x")

        # --- LADO DIREITO: FILA ---
        frame_fila = ctk.CTkFrame(self.janela_staff)
        frame_fila.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        frame_fila.grid_rowconfigure(1, weight=1)
        frame_fila.grid_columnconfigure(0, weight=1)

        label_fila_titulo = ctk.CTkLabel(
            frame_fila, text="📋 FILA DE ESPERA",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        label_fila_titulo.grid(row=0, column=0, pady=10)

        self.textbox_fila = ctk.CTkTextbox(frame_fila, font=ctk.CTkFont(size=18))
        self.textbox_fila.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

    # ========== FUNÇÕES DOS BOTÕES ==========

    def gerar_normal(self):
        senha = self.sistema.gerar_senha("Normal", self.config)

        if self.config.get("impressora_ativada", False):
            from impressao import imprimir_senha
            resultado = imprimir_senha(senha, "Normal", self.config)
            if resultado:
                messagebox.showinfo("Impressão", f"Comprovante da senha {senha} enviado para impressão.")

        messagebox.showinfo("Sucesso", f"Senha {senha} gerada com sucesso!")
        self.atualizar_tudo()

    def gerar_prioritario(self):
        senha = self.sistema.gerar_senha("Prioritário", self.config)

        if self.config.get("impressora_ativada", False):
            from impressao import imprimir_senha
            resultado = imprimir_senha(senha, "Prioritário", self.config)
            if resultado:
                messagebox.showinfo("Impressão", f"Comprovante da senha {senha} enviado para impressão.")

        messagebox.showinfo("Sucesso", f"Senha {senha} (Prioritária) gerada!")
        self.atualizar_tudo()

    def chamar_proximo(self):
        proximo = self.sistema.chamar_proximo()
        if proximo:
            if self.config.get("som_ativado", True):
                winsound.Beep(1000, 500)

            if self.config.get("tts_ativado", True):
                from tts import falar
                texto = f"Senha, {proximo['senha']}" 
                falar(texto)

            self.label_senha_atual.configure(text=proximo['senha'], text_color="#FFD700")
            messagebox.showinfo("Chamada", f"📢 Chamando: {proximo['senha']}")
        else:
            messagebox.showwarning("Atenção", "Nenhum paciente na fila!")
            self.label_senha_atual.configure(text="AGUARDE", text_color="#00FF00")
        self.atualizar_tudo()

    def rechamar(self):
                    
        ultimo = self.sistema.rechamar_ultimo()
        if ultimo:
            if self.config.get("som_ativado", True):
                winsound.Beep(800, 300)
            
            if self.config.get("tts_ativado", True):
                from tts import falar
                texto = f"Senha {ultimo['senha']}, favor se dirigir ao balcão"
                falar(texto)
            
            self.label_senha_atual.configure(
                text=ultimo['senha'],
                text_color="#FFD700"
            )
            messagebox.showinfo("Rechamada", f"🔊 Rechamando: {ultimo['senha']}")
        else:
            messagebox.showwarning("Atenção", "Nenhuma senha foi chamada ainda hoje.")
    
         
    def remover_senha(self):
        codigo = self.entry_remover.get().strip().upper()
        if not codigo:
            messagebox.showwarning("Atenção", "Digite o código da senha para remover.")
            return

        removido = self.sistema.remover_por_senha(codigo)
        if removido:
            messagebox.showinfo("Removido", f"Senha {codigo} removida da fila.")
            self.entry_remover.delete(0, "end")
        else:
            messagebox.showerror("Não encontrado", f"Senha {codigo} não está na fila.")
        self.atualizar_tudo()

    def resetar_dia(self):
        if messagebox.askyesno("Confirmar", "Tem certeza que quer resetar o dia?\nTodas as senhas aguardando serão apagadas."):
            self.sistema.resetar_dia()
            self.label_senha_atual.configure(text="AGUARDE", text_color="#00FF00")
            messagebox.showinfo("Resetado", "Fila e contador reiniciados para o novo dia.")
            self.atualizar_tudo()

    def exportar_relatorio(self):
        caminho = self.sistema.exportar_relatorio()
        if caminho:
            messagebox.showinfo("Relatório Gerado", f"Relatório salvo em:\n{caminho}")
        else:
            messagebox.showwarning("Sem dados", "Nenhum atendimento realizado hoje para gerar relatório.")

    def atualizar_tudo(self):
        fila = self.sistema.listar_fila()
        self.textbox_fila.delete("1.0", "end")

        if not fila:
            self.textbox_fila.insert("1.0", "📭 Fila vazia.")
        else:
            for i, s in enumerate(fila, 1):
                tipo_icone = "⭐" if s["tipo"] == "Prioritário" else "📌"
                destaque = ">>> " if i == 1 else "    "
                linha = f"{destaque}{i}º - {s['senha']} ({s['tipo']}) {tipo_icone}  [{s['horario']}]\n"
                self.textbox_fila.insert("end", linha)

        self.label_stats.configure(
            text=f"📊 Aguardando: {self.sistema.total_aguardando()}  |  Atendidos: {self.sistema.total_atendidos()}"
        )

        proximos = self.sistema.listar_fila()[:5]
        if not proximos:
            self.label_lista_proximos.configure(text="Nenhum paciente aguardando.")
        else:
            texto_proximos = "  |  ".join([s['senha'] for s in proximos])
            self.label_lista_proximos.configure(text=texto_proximos)

        salvar_dados(
            self.sistema.fila,
            self.sistema.atendidas,
            self.sistema.contador,
            self.sistema.ultima_chamada
        )

    def sair(self):
        salvar_dados(
            self.sistema.fila,
            self.sistema.atendidas,
            self.sistema.contador,
            self.sistema.ultima_chamada
        )
        self.janela_staff.destroy()

    def abrir_ajustes(self):
        janela = ctk.CTkToplevel(self.janela_staff)
        janela.title("⚙️ Ajustes do Sistema")
        janela.geometry("500x600")
        janela.attributes('-topmost', True)

        ctk.CTkLabel(janela, text="Configurações", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=20)

        # Prefixos
        frame_prefixos = ctk.CTkFrame(janela)
        frame_prefixos.pack(pady=10, padx=20, fill="x")

        ctk.CTkLabel(frame_prefixos, text="Prefixo Normal:", font=ctk.CTkFont(size=14)).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        entry_prefixo_n = ctk.CTkEntry(frame_prefixos, width=80)
        entry_prefixo_n.insert(0, self.config.get("prefixo_normal", "N"))
        entry_prefixo_n.grid(row=0, column=1, padx=5, pady=5)

        ctk.CTkLabel(frame_prefixos, text="Prefixo Prioritário:", font=ctk.CTkFont(size=14)).grid(row=1, column=0, padx=5, pady=5, sticky="w")
        entry_prefixo_p = ctk.CTkEntry(frame_prefixos, width=80)
        entry_prefixo_p.insert(0, self.config.get("prefixo_prioritario", "P"))
        entry_prefixo_p.grid(row=1, column=1, padx=5, pady=5)

        # Som e TTS
        var_som = ctk.BooleanVar(value=self.config.get("som_ativado", True))
        ctk.CTkSwitch(janela, text="Ativar som (beep)", variable=var_som).pack(pady=5, padx=20, anchor="w")

        var_tts = ctk.BooleanVar(value=self.config.get("tts_ativado", True))
        ctk.CTkSwitch(janela, text="Ativar voz (TTS)", variable=var_tts).pack(pady=5, padx=20, anchor="w")

        # Impressora
        var_imp = ctk.BooleanVar(value=self.config.get("impressora_ativada", False))
        ctk.CTkSwitch(janela, text="Ativar impressora térmica", variable=var_imp).pack(pady=5, padx=20, anchor="w")

        ctk.CTkLabel(janela, text="Nome da impressora (deixe vazio para padrão):").pack(pady=(10, 0), padx=20, anchor="w")
        entry_imp = ctk.CTkEntry(janela, width=300)
        entry_imp.insert(0, self.config.get("impressora_nome", ""))
        entry_imp.pack(pady=5, padx=20, fill="x")

        # Tema
        var_tema = ctk.StringVar(value=self.config.get("tema", "dark"))
        ctk.CTkLabel(janela, text="Tema:").pack(pady=(10, 0), padx=20, anchor="w")
        combo_tema = ctk.CTkComboBox(janela, values=["dark", "light"], variable=var_tema, state="readonly")
        combo_tema.pack(pady=5, padx=20, fill="x")

        def salvar_ajustes():
            self.config["prefixo_normal"] = entry_prefixo_n.get().strip() or "N"
            self.config["prefixo_prioritario"] = entry_prefixo_p.get().strip() or "P"
            self.config["som_ativado"] = var_som.get()
            self.config["tts_ativado"] = var_tts.get()
            self.config["impressora_ativada"] = var_imp.get()
            self.config["impressora_nome"] = entry_imp.get().strip()
            self.config["tema"] = var_tema.get()
            salvar_config(self.config)
            ctk.set_appearance_mode(self.config["tema"])
            messagebox.showinfo("Sucesso", "Configurações salvas!")
            janela.destroy()

        ctk.CTkButton(janela, text="💾 Salvar", command=salvar_ajustes, height=40).pack(pady=20)

    def abrir_estatisticas(self):
        from relatorio import gerar_grafico_atendimentos, calcular_tempo_medio

        janela = ctk.CTkToplevel(self.janela_staff)
        janela.title("📊 Estatísticas")
        janela.geometry("800x600")
        janela.attributes('-topmost', True)

        ctk.CTkLabel(janela, text="Painel de Estatísticas", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=20)

        atendidos = self.sistema.atendidas
        info = ctk.CTkFrame(janela)
        info.pack(pady=10, padx=20, fill="x")

        ctk.CTkLabel(info, text=f"Total atendidos: {len(atendidos)}", font=ctk.CTkFont(size=16)).pack(side="left", padx=20)

        tempo_medio = calcular_tempo_medio(atendidos)
        ctk.CTkLabel(info, text=f"Tempo médio de espera: {tempo_medio:.1f} min", font=ctk.CTkFont(size=16)).pack(side="right", padx=20)

        btn_grafico = ctk.CTkButton(
            janela,
            text="📈 Gerar Gráficos",
            command=lambda: self.exibir_grafico(janela, atendidos)
        )
        btn_grafico.pack(pady=10)

        self.label_grafico = ctk.CTkLabel(janela, text="Clique em 'Gerar Gráficos' para visualizar", font=ctk.CTkFont(size=14))
        self.label_grafico.pack(pady=10, padx=20, fill="both", expand=True)

    def exibir_grafico(self, janela, atendidos):
        """Gera e exibe o relatório em texto (sem imagem)."""
        from relatorio import gerar_grafico_atendimentos
        caminho = gerar_grafico_atendimentos(atendidos)
        if caminho:
            # Abre o arquivo e mostra o conteúdo na tela
            with open(caminho, "r", encoding="utf-8") as f:
                conteudo = f.read()
            # Exibe em uma caixa de texto simples
            messagebox.showinfo("Relatório Gerado", f"Relatório salvo em:\n{caminho}\n\nConteúdo:\n{conteudo[:500]}...")  # Mostra só o início
            self.label_grafico.configure(text="Relatório gerado! Verifique a pasta 'estatisticas'.")
        else:
            self.label_grafico.configure(text="Nenhum dado para gerar relatório.") 

if __name__ == "__main__":
    app = SistemaSenhasGUI()