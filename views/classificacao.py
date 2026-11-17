from tkinter import ttk

import customtkinter as ctk

# (chave interna, título exibido, largura em pixels)
COLUNAS = [
    ("pos", "Pos", 50),
    ("equipe", "Equipe", 220),
    ("pts", "PTS", 60),
    ("j", "J", 50),
    ("v", "V", 50),
    ("e", "E", 50),
    ("d", "D", 50),
    ("gp", "GP", 50),
    ("gc", "GC", 50),
    ("sg", "SG", 50),
]


class TelaClassificacao(ctk.CTkFrame):
    """Tabela de classificação. Só exibe: o cálculo é do Campeonato."""

    def __init__(self, master, app):
        super().__init__(master, fg_color="transparent")
        self.app = app

        ctk.CTkLabel(self, text="Classificação",
                     font=ctk.CTkFont(size=24, weight="bold")).pack(pady=(25, 15))

        self._configurar_estilo()

        moldura = ctk.CTkFrame(self)
        moldura.pack(fill="both", expand=True, padx=30)

        self.tabela = ttk.Treeview(
            moldura,
            columns=[chave for chave, _, _ in COLUNAS],
            show="headings",
            style="Classificacao.Treeview",
        )
        for chave, titulo, largura in COLUNAS:
            self.tabela.heading(chave, text=titulo)
            alinhamento = "w" if chave == "equipe" else "center"
            self.tabela.column(chave, width=largura, anchor=alinhamento,
                               stretch=(chave == "equipe"))

        barra_rolagem = ctk.CTkScrollbar(moldura, command=self.tabela.yview)
        self.tabela.configure(yscrollcommand=barra_rolagem.set)

        barra_rolagem.pack(side="right", fill="y", pady=10, padx=(0, 5))
        self.tabela.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)

        botoes = ctk.CTkFrame(self, fg_color="transparent")
        botoes.pack(pady=20)
        ctk.CTkButton(botoes, text="Início",
                      command=lambda: self.app.mostrar_tela("inicio")).pack(side="left", padx=8)
        ctk.CTkButton(botoes, text="Partidas",
                      command=lambda: self.app.mostrar_tela("partidas")).pack(side="left", padx=8)

    def _configurar_estilo(self):
        estilo = ttk.Style()
        estilo.theme_use("clam")
        estilo.configure("Classificacao.Treeview",
                         background="#2b2b2b", fieldbackground="#2b2b2b",
                         foreground="white", rowheight=28, borderwidth=0)
        estilo.configure("Classificacao.Treeview.Heading",
                         background="#1f538d", foreground="white",
                         font=("Arial", 11, "bold"), relief="flat")
        estilo.map("Classificacao.Treeview", background=[("selected", "#1f538d")])
        estilo.map("Classificacao.Treeview.Heading", background=[("active", "#14375e")])

    def atualizar(self):
        self.tabela.delete(*self.tabela.get_children())
        classificacao = self.app.campeonato.calcular_classificacao()
        for posicao, equipe in enumerate(classificacao, start=1):
            self.tabela.insert("", "end", values=(
                posicao, equipe.nome, equipe.pontos, equipe.jogos,
                equipe.vitorias, equipe.empates, equipe.derrotas,
                equipe.gols_pro, equipe.gols_contra, equipe.saldo_gols,
            ))
