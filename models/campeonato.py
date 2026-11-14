from models.equipe import Equipe
from models.partida import Partida

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

    def quantidade_equipes(self):
        return len(self._equipes)

    def buscar_equipe(self, nome):
        nome_procurado = nome.strip().lower()
        for equipe in self._equipes:
            if equipe.nome.lower() == nome_procurado:
                return equipe
        return None
    
    def adicionar_equipe(self, nome, cidade):
        if self.buscar_equipe(nome) is not None:
            raise ValueError(f"Já existe uma equipe chamada '{nome.strip()}'.")
        equipe = Equipe(nome, cidade)
        self._equipes.append(equipe)
        return equipe

    def remover_equipe(self, nome):
        equipe = self.buscar_equipe(nome)
        if equipe is None:
            raise ValueError(f"Não existe uma equipe chamada '{nome.strip()}'.")
        
        for partida in self._partidas:
            if partida.envolve(equipe):
                raise ValueError(f"A equipe está vinculada a partida e não pode ser removida.")
            self._equipes.remove(equipe)

    def adicionar_partida(self, equipe_casa, equipe_visitante, rodada, gols_casa=None, gols_visitante=None):
        if equipe_casa not in self._equipes or equipe_visitante not in self._equipes:
            raise ValueError("As equipes devem estar cadastradas no campeonato.")
        partida = Partida(equipe_casa, equipe_visitante, rodada, gols_casa, gols_visitante)
        self._partidas.append(partida)
        return partida
            