from tkinter import messagebox

import customtkinter as ctk


class TelaPartidas(ctk.CTkFrame):
    """Geração de confrontos, lista por rodada e registro de resultados."""

    def __init__(self, master, app):
        super().__init__(master, fg_color="transparent")
        self.app = app
        self.partida_selecionada = None

        # Duas colunas do mesmo tamanho; a linha 0 ocupa a altura disponível
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        # ---------- Coluna da esquerda: confrontos ----------
        partida_frame = ctk.CTkFrame(self, corner_radius=15)
        partida_frame.grid(row=0, column=0, padx=(15, 7), pady=15, sticky="nsew")

        ctk.CTkLabel(partida_frame, text="Confrontos",
                     font=("Arial", 22, "bold")).pack(pady=15)

        self.lista_partidas = ctk.CTkScrollableFrame(partida_frame)
        self.lista_partidas.pack(padx=10, pady=10, fill="both", expand=True)

        self.botao_gerar = ctk.CTkButton(partida_frame, text="Gerar confrontos",
                                         command=self.gerar_confrontos)
        self.botao_gerar.pack(pady=15)

        # ---------- Coluna da direita: registrar resultado ----------
        resultado_frame = ctk.CTkFrame(self, corner_radius=15)
        resultado_frame.grid(row=0, column=1, padx=(7, 15), pady=15, sticky="nsew")

        ctk.CTkLabel(resultado_frame, text="Registrar resultado",
                     font=("Arial", 22, "bold")).pack(pady=15)

        self.partida_label = ctk.CTkLabel(resultado_frame, text="Selecione uma partida pendente",
                                          font=("Arial", 16))
        self.partida_label.pack(pady=15)

        self.label_gols_casa = ctk.CTkLabel(resultado_frame, text="Gols da casa")
        self.label_gols_casa.pack()
        self.gols_casa = ctk.CTkEntry(resultado_frame, placeholder_text="0")
        self.gols_casa.pack(pady=(0, 10), padx=20)

        self.label_gols_visitante = ctk.CTkLabel(resultado_frame, text="Gols do visitante")
        self.label_gols_visitante.pack()
        self.gols_visitante = ctk.CTkEntry(resultado_frame, placeholder_text="0")
        self.gols_visitante.pack(pady=(0, 10), padx=20)

        ctk.CTkButton(resultado_frame, text="Registrar resultado",
                      command=self.registrar_resultado).pack(pady=20)

        # ---------- Navegação ----------
        navegacao = ctk.CTkFrame(self, fg_color="transparent")
        navegacao.grid(row=1, column=0, columnspan=2, pady=(0, 15))
        ctk.CTkButton(navegacao, text="Início",
                      command=lambda: self.app.mostrar_tela("inicio")).pack(side="left", padx=8)
        ctk.CTkButton(navegacao, text="Classificação",
                      command=lambda: self.app.mostrar_tela("classificacao")).pack(side="left", padx=8)

    # ---------- Atualização da tela ----------

    def atualizar(self):
        self._limpar_selecao()

        for widget in self.lista_partidas.winfo_children():
            widget.destroy()

        partidas = sorted(self.app.campeonato.partidas, key=lambda partida: partida.rodada)

        # Depois de gerar, o botão fica desativado (regra: não gerar duas vezes)
        self.botao_gerar.configure(state="disabled" if partidas else "normal")

        if not partidas:
            ctk.CTkLabel(self.lista_partidas,
                         text="Nenhum confronto gerado ainda.").pack(pady=10)
            return

        rodada_atual = None
        for partida in partidas:
            if partida.rodada != rodada_atual:
                rodada_atual = partida.rodada
                ctk.CTkLabel(self.lista_partidas, text=f"Rodada {rodada_atual}",
                             font=("Arial", 17, "bold")).pack(pady=8)

            ctk.CTkButton(
                self.lista_partidas,
                text=str(partida),
                # Partida já realizada aparece, mas não pode ser selecionada
                state="disabled" if partida.foi_jogada() else "normal",
                command=lambda p=partida: self.selecionar_partida(p),
            ).pack(fill="x", pady=5)

    def _limpar_selecao(self):
        self.partida_selecionada = None
        self.partida_label.configure(text="Selecione uma partida pendente")
        self.label_gols_casa.configure(text="Gols da casa")
        self.label_gols_visitante.configure(text="Gols do visitante")
        self.gols_casa.delete(0, "end")
        self.gols_visitante.delete(0, "end")

    # ---------- Ações ----------

    def gerar_confrontos(self):
        if not messagebox.askyesno(
            "Gerar confrontos",
            "Depois de gerar os confrontos não será possível cadastrar ou remover "
            "equipes. Deseja continuar?",
        ):
            return
        try:
            novas = self.app.campeonato.gerar_partidas()
        except ValueError as erro:
            messagebox.showerror("Erro ao gerar confrontos", str(erro))
            return

        self.app.salvar_dados()
        self.atualizar()
        messagebox.showinfo("Confrontos gerados", f"{len(novas)} partidas foram geradas.")

    def selecionar_partida(self, partida):
        self.partida_selecionada = partida
        casa = partida.equipe_casa.nome
        visitante = partida.equipe_visitante.nome
        self.partida_label.configure(text=f"{casa} x {visitante}")
        self.label_gols_casa.configure(text=f"Gols do {casa}")
        self.label_gols_visitante.configure(text=f"Gols do {visitante}")
        self.gols_casa.delete(0, "end")
        self.gols_visitante.delete(0, "end")

    def registrar_resultado(self):
        if self.partida_selecionada is None:
            messagebox.showwarning("Atenção", "Selecione uma partida primeiro.")
            return

        texto_casa = self.gols_casa.get().strip()
        texto_visitante = self.gols_visitante.get().strip()
        if not texto_casa or not texto_visitante:
            messagebox.showerror("Erro", "Informe os gols das duas equipes.")
            return

        # Converter texto em número é papel da tela; validar o placar é da Partida
        try:
            gols_casa = int(texto_casa)
            gols_visitante = int(texto_visitante)
        except ValueError:
            messagebox.showerror("Erro", "Digite apenas números inteiros.")
            return

        try:
            self.partida_selecionada.registrar_resultado(gols_casa, gols_visitante)
        except ValueError as erro:
            messagebox.showerror("Erro", str(erro))
            return

        self.app.salvar_dados()
        self.atualizar()
        messagebox.showinfo("Resultado registrado", "Resultado registrado com sucesso.")
