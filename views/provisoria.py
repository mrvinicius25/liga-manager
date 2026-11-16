import customtkinter as ctk

class TelaProvisoria(ctk.CTkFrame):
    """Tela temporária, usada até a tela real ficar pronta"""

    def __init__(self, master, app, titulo):
        super().__init__(master)
        self.app = app

        ctk.CTkLabel(self, text=titulo, font=ctk.CTkFont(size=24, weight="bold")).pack(pady=(40,10))
        ctk.CTkLabel(self, text="Tela em construção.").pack(pady=10)

        barra = ctk.CTkFrame(self, fg_color="transparent")
        barra.pack(pady=20)
        for texto, nome in [("Início", "inicio"), ("Equipes", "equipes"),
                            ("Partidas", "partidas"), ("Classificação", "classificacao")]:
            botao = ctk.CTkButton(
                barra, text=texto,
                # nome=nome "congela" o valor de cada volta do for (ver explicação)
                command=lambda nome=nome: self.app.mostrar_tela(nome),
            )
            botao.pack(side="left", padx=5)

    def atualizar(self):
        pass  # não tem dados para atualizar