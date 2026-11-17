import sys
from pathlib import Path
from tkinter import messagebox

import customtkinter as ctk

from models.campeonato import Campeonato
from storage.repositorio_json import RepositorioJSON
from views.inicio import TelaInicio
from views.equipes import TelaEquipes
from views.partidas import TelaPartidas
from views.classificacao import TelaClassificacao

# Caminho a partir da pasta deste arquivo: funciona mesmo se o programa
# for aberto de outra pasta (ex.: python LigaManager/main.py)
CAMINHO_DADOS = Path(__file__).parent / "data" / "campeonato.json"
NOME_PADRAO = "Campeonato da Turma"


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("LigaManager")
        self.geometry("900x550")

        self.repositorio = RepositorioJSON(CAMINHO_DADOS)
        self.campeonato = self._carregar_campeonato()

        # Container onde todas as telas ficam empilhadas no mesmo lugar
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True)
        container.rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)

        self.telas = {
            "inicio": TelaInicio(container, self),
            "equipes": TelaEquipes(container, self),
            "partidas": TelaPartidas(container, self),
            "classificacao": TelaClassificacao(container, self),
        }
        for tela in self.telas.values():
            tela.grid(row=0, column=0, sticky="nsew")
        self.mostrar_tela("inicio")

    def _carregar_campeonato(self):
        try:
            campeonato = self.repositorio.carregar()
        except ValueError as erro:
            # Arquivo com problema: avisa e fecha SEM salvar, para não
            # sobrescrever dados que talvez ainda possam ser recuperados
            self.withdraw()  # esconde a janela vazia atrás da mensagem
            messagebox.showerror(
                "Erro ao abrir dados",
                f"{erro}\n\nO arquivo não foi alterado. Corrija-o ou apague-o "
                "e abra o programa novamente."
            )
            self.destroy()
            sys.exit(1)

        if campeonato is None:  # primeira execução: ainda não há arquivo
            campeonato = Campeonato(NOME_PADRAO)
            self.repositorio.salvar(campeonato)
        return campeonato
        
    def mostrar_tela(self, nome):
        tela = self.telas[nome]
        tela.atualizar()
        tela.tkraise()

    def salvar_dados(self):
        try:
            self.repositorio.salvar(self.campeonato)
        except OSError as erro:
            messagebox.showerror("Erro ao salvar", f"Não foi possível salvar os dados.\n\n{erro}")


if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    App().mainloop()

