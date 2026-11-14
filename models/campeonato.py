class Campeonato:
    def __init__(self, nome):
        nome_campeonato = nome.strip()
        if not nome_campeonato:
            raise ValueError("O nome do campeonato não pode ser vazio.")
        self._nome = nome_campeonato
        self._equipes = []
        self._partidas = []

    @property
    def nome(self):
        return self._nome

    @property
    def equipes(self):
        return list(self._equipes)

    @property
    def partidas(self):
        return list(self._partidas)
    