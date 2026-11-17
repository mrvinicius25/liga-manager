from tkinter import messagebox

import customtkinter as ctk


class TelaInicio(ctk.CTkFrame):
    """Dashboard: resumo do campeonato e atalhos para as outras telas."""

    def __init__(self, master, app):
        super().__init__(master, fg_color="transparent")
        self.app = app

        ctk.CTkLabel(self, text="LigaManager",
                     font=ctk.CTkFont(size=28, weight="bold")).pack(pady=(30,5))

        # Começa vazio: o texto é preenchido em atualizar()
        self.label_nome = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=18))
        self.label_nome.pack(pady=(0,25))

        # Grade 2x2 com os indicadores
        grade = ctk.CTkFrame(self, fg_color="transparent")
        grade.pack()
        self.valor_equipes = self._criar_cartao(grade, "Equipes", 0, 0)
        self.valor_total = self._criar_cartao(grade, "Total de partidas", 0, 1)
        self.valor_realizadas = self._criar_cartao(grade, "Realizadas", 1, 0)
        self.valor_pendentes = self._criar_cartao(grade, "Pendentes", 1, 1)

        # Navegação
        botoes = ctk.CTkFrame(self, fg_color="transparent")
        botoes.pack(pady=30)
        ctk.CTkButton(botoes, text="Equipes",
                      command=lambda: self.app.mostrar_tela("equipes")).pack(side="left", padx=8)
        ctk.CTkButton(botoes, text="Partidas",
                      command=lambda: self.app.mostrar_tela("partidas")).pack(side="left", padx=8)
        ctk.CTkButton(botoes, text="Classificação",
                      command=lambda: self.app.mostrar_tela("classificacao")).pack(side="left", padx=8)

        # Ação destrutiva: separada da navegação e em vermelho
        ctk.CTkButton(self, text="Novo campeonato",
                      fg_color="#a83232", hover_color="#7a2424",
                      command=self.novo_campeonato).pack(pady=(0, 20))

    def _criar_cartao(self, grade, titulo, linha, coluna):
        """Cria um cartão com título e número; devolve o label do número."""
        cartao = ctk.CTkFrame(grade, corner_radius=12)
        cartao.grid(row=linha, column=coluna, padx=10, pady=10, sticky="nsew")
        ctk.CTkLabel(cartao, text=titulo, width=180).pack(pady=(15, 0))
        valor = ctk.CTkLabel(cartao, text="0", font=ctk.CTkFont(size=32, weight="bold"))
        valor.pack(pady=(0, 15))
        return valor

    def atualizar(self):
        campeonato = self.app.campeonato
        self.label_nome.configure(text=campeonato.nome)
        self.valor_equipes.configure(text=str(campeonato.quantidade_equipes()))
        self.valor_total.configure(text=str(campeonato.quantidade_partidas()))
        self.valor_realizadas.configure(text=str(campeonato.partidas_realizadas()))
        self.valor_pendentes.configure(text=str(campeonato.partidas_pendentes()))

    def novo_campeonato(self):
        confirmar = messagebox.askyesno(
            "Novo campeonato",
            "Isso apaga todas as equipes, partidas e resultados do campeonato atual.\n\n"
            "Essa ação não pode ser desfeita. Deseja continuar?",
            icon="warning",
        )
        if not confirmar:
            return

        self.app.novo_campeonato()
        messagebox.showinfo("Novo campeonato", "Um novo campeonato foi criado.")
