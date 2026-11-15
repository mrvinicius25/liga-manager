
import customtkinter as ctk
from tkinter import messagebox


def abrir_tela_partida(app):

    app.title("LigaManager - Partidas e Resultados")
    app.geometry("900x600")

    partida_selecionada = None

    # ---------- FRAME DOS CONFRONTOS ----------

    partida_frame = ctk.CTkFrame(
        master=app,
        corner_radius=15
    )
    partida_frame.grid(
        row=0, column=0,
        padx=(15, 7), pady=15,
        sticky="nsew"
    )

    # ---------- FRAME DOS RESULTADOS ----------

    resultado_frame = ctk.CTkFrame(
        master=app,
        corner_radius=15
    )
    resultado_frame.grid(
        row=0, column=1,
        padx=(7, 15), pady=15,
        sticky="nsew"
    )

    app.grid_columnconfigure(0, weight=1)
    app.grid_columnconfigure(1, weight=1)
    app.grid_rowconfigure(0, weight=1)

    # ---------- TÍTULO DOS CONFRONTOS ----------

    titulo_partidas = ctk.CTkLabel(
        partida_frame,
        text="Confrontos",
        font=("Arial", 22, "bold")
    )
    titulo_partidas.pack(pady=15)

    # ---------- LISTA DE PARTIDAS ----------

    lista_partidas = ctk.CTkScrollableFrame(
        partida_frame,
        width=350,
        height=350
    )
    lista_partidas.pack(
        padx=10,
        pady=10,
        fill="both",
        expand=True
    )

    # ---------- TÍTULO DOS RESULTADOS ----------

    titulo_resultado = ctk.CTkLabel(
        resultado_frame,
        text="Registrar resultado",
        font=("Arial", 22, "bold")
    )
    titulo_resultado.pack(pady=15)

    partida_label = ctk.CTkLabel(
        resultado_frame,
        text="Selecione uma partida",
        font=("Arial", 16)
    )
    partida_label.pack(pady=15)

    # ---------- CAMPOS DE GOLS ----------

    gols_casa = ctk.CTkEntry(
        resultado_frame,
        placeholder_text="Gols da equipe da casa"
    )
    gols_casa.pack(pady=10, padx=20)

    gols_visitante = ctk.CTkEntry(
        resultado_frame,
        placeholder_text="Gols da equipe visitante"
    )
    gols_visitante.pack(pady=10, padx=20)

    # ---------- REGISTRAR RESULTADO ----------

    def registrar_resultado():

        if partida_selecionada is None:
            messagebox.showwarning(
                "Atenção",
                "Selecione uma partida primeiro."
            )
            return

        try:
            casa = int(gols_casa.get())
            visitante = int(gols_visitante.get())

            partida_selecionada.registrar_resultado(
                casa,
                visitante
            )

            partida_label.configure(
                text=str(partida_selecionada)
            )

            messagebox.showinfo(
                "Sucesso",
                "Resultado registrado!"
            )

            gols_casa.delete(0, "end")
            gols_visitante.delete(0, "end")

        except ValueError as erro:
            messagebox.showerror("Erro", str(erro))

    botao_registrar = ctk.CTkButton(
        resultado_frame,
        text="Registrar resultado",
        command=registrar_resultado
    )
    botao_registrar.pack(pady=20)

    # ---------- BOTÃO GERAR CONFRONTOS ----------

    botao_gerar = ctk.CTkButton(
        partida_frame,
        text="Gerar confrontos",
        command=lambda: messagebox.showinfo(
            "Confrontos",
            "Aqui será chamado Campeonato.gerar_partidas()."
        )
    )
    botao_gerar.pack(pady=15)

    # ---------- EXEMPLO DE PARTIDAS ----------

    # Dados temporários para testar a interface.
    # Depois serão substituídos pelas partidas do Campeonato.

    partidas = []

    def selecionar_partida(partida):
        nonlocal partida_selecionada

        partida_selecionada = partida

        partida_label.configure(
            text=str(partida)
        )

        gols_casa.delete(0, "end")
        gols_visitante.delete(0, "end")

    # A lista será preenchida quando as partidas forem geradas.
    # Cada partida terá um botão para seleção.

    def atualizar_partidas():
        for widget in lista_partidas.winfo_children():
            widget.destroy()

        rodada_atual = None

        for partida in partidas:

            if partida.rodada != rodada_atual:
                rodada_atual = partida.rodada

                ctk.CTkLabel(
                    lista_partidas,
                    text=f"Rodada {rodada_atual}",
                    font=("Arial", 17, "bold")
                ).pack(pady=8)

            botao_partida = ctk.CTkButton(
                lista_partidas,
                text=str(partida),
                command=lambda p=partida: selecionar_partida(p)
            )
            botao_partida.pack(fill="x", pady=5)

    atualizar_partidas()
