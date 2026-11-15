
import customtkinter as ctk
from models.equipe import Equipe


def abrir_tela_equipes(app):

    app.title("Cadastro de Equipes")
    app.geometry("300x350")

    def cadastrar_equipe():
        nome = campo_equipe.get()
        cidade = campo_cidade.get()

        try:
            equipe = Equipe(nome, cidade)

            resultado_equipe.configure(
                text=f"Equipe cadastrada: {equipe}",
                text_color="green"
            )

        except ValueError as erro:
            resultado_equipe.configure(
                text=str(erro),
                text_color="red"
            )

    label_equipe = ctk.CTkLabel(app, text="Equipe")
    label_equipe.pack(pady=10)

    campo_equipe = ctk.CTkEntry(
        app, placeholder_text="Digite a sua equipe"
    )
    campo_equipe.pack(pady=10)

    label_cidade = ctk.CTkLabel(app, text="Cidade")
    label_cidade.pack(pady=10)

    campo_cidade = ctk.CTkEntry(
        app, placeholder_text="Digite a sua cidade"
    )
    campo_cidade.pack(pady=10)

    botao_cadastrar = ctk.CTkButton(
        app,
        text="Cadastrar equipe",
        command=cadastrar_equipe
    )
    botao_cadastrar.pack(pady=10)

    resultado_equipe = ctk.CTkLabel(app, text="")
    resultado_equipe.pack(pady=10)
