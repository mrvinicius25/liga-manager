from tkinter import messagebox

import customtkinter as ctk


class TelaEquipes(ctk.CTkFrame):
    """Cadastro, listagem e remoção de equipes."""

    def __init__(self, master, app):
        super().__init__(master, fg_color="transparent")
        self.app = app

        ctk.CTkLabel(self, text="Equipes",
                     font=ctk.CTkFont(size=24, weight="bold")).pack(pady=(25, 15))

        # ---------- Formulário de cadastro ----------
        formulario = ctk.CTkFrame(self, fg_color="transparent")
        formulario.pack(pady=5)

        self.campo_nome = ctk.CTkEntry(formulario, placeholder_text="Nome da equipe", width=220)
        self.campo_nome.pack(side="left", padx=5)

        self.campo_cidade = ctk.CTkEntry(formulario, placeholder_text="Cidade", width=180)
        self.campo_cidade.pack(side="left", padx=5)

        ctk.CTkButton(formulario, text="Cadastrar",
                      command=self.cadastrar).pack(side="left", padx=5)

        # ---------- Lista de equipes ----------
        self.lista = ctk.CTkScrollableFrame(self, label_text="Equipes cadastradas")
        self.lista.pack(fill="both", expand=True, padx=30, pady=15)

        # ---------- Navegação ----------
        ctk.CTkButton(self, text="Voltar ao início",
                      command=lambda: self.app.mostrar_tela("inicio")).pack(pady=(0, 20))

    def atualizar(self):
        # Apaga as linhas antigas e redesenha a partir do Campeonato
        for widget in self.lista.winfo_children():
            widget.destroy()

        equipes = self.app.campeonato.equipes
        if not equipes:
            ctk.CTkLabel(self.lista, text="Nenhuma equipe cadastrada.").pack(pady=10)
            return

        for equipe in equipes:
            linha = ctk.CTkFrame(self.lista, fg_color="transparent")
            linha.pack(fill="x", pady=3)
            ctk.CTkLabel(linha, text=str(equipe), anchor="w").pack(side="left", padx=10)
            ctk.CTkButton(
                linha, text="Remover", width=90,
                fg_color="#a83232", hover_color="#7a2424",
                # nome=nome "congela" o nome de cada equipe nesta volta do for
                command=lambda nome=equipe.nome: self.remover(nome),
            ).pack(side="right", padx=10)

    def cadastrar(self):
        try:
            equipe = self.app.campeonato.adicionar_equipe(
                self.campo_nome.get(), self.campo_cidade.get()
            )
        except ValueError as erro:
            messagebox.showerror("Erro ao cadastrar", str(erro))
            return

        self.app.salvar_dados()
        self.campo_nome.delete(0, "end")
        self.campo_cidade.delete(0, "end")
        self.atualizar()
        messagebox.showinfo("Equipe cadastrada", f"{equipe} foi cadastrada com sucesso.")

    def remover(self, nome):
        if not messagebox.askyesno("Remover equipe", f"Deseja remover a equipe {nome}?"):
            return
        try:
            self.app.campeonato.remover_equipe(nome)
        except ValueError as erro:
            messagebox.showerror("Erro ao remover", str(erro))
            return

        self.app.salvar_dados()
        self.atualizar()
