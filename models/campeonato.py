class Campeonato:
    def __init__(self, nome, equipes, partidas):
        self.nome = nome
        self.equipes = equipes
        self.partidas = partidas

    def adicionar_equipe(self, equipe):
        self.equipes.append(equipe)

    def adicionar_partida(self, partida):
        self.partidas.append(partida)

    def remover_equipe(self, equipe):
        self.equipes.remove(equipe)

    def remover_partida(self, partida):
        self.partidas.remove(partida)