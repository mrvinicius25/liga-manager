
import customtkinter as ctk
from views.equipes import abrir_tela_equipes

ctk.set_appearance_mode("Dark")

app = ctk.CTk()

abrir_tela_equipes(app)

app.mainloop()
