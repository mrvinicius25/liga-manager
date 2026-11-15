
import customtkinter as ctk
from views.equipes import abrir_tela_equipes
from views.partidas_resultados import abir_tela_partida

ctk.set_appearance_mode("Dark")

app = ctk.CTk()

abrir_tela_equipes(app)
abir_tela_partida(app)

app.mainloop()
