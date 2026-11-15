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
        # Regra 10: uma equipe nova ficaria sem jogos no calendário já gerado
        if self._partidas:
            raise ValueError("Não é possível cadastrar equipes depois que as partidas foram geradas.")
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
                raise ValueError(f"A equipe '{equipe.nome}' está vinculada a partida e não pode ser removida.")
        self._equipes.remove(equipe)

    def adicionar_partida(self, equipe_casa, equipe_visitante, rodada, gols_casa=None, gols_visitante=None):
        if equipe_casa not in self._equipes or equipe_visitante not in self._equipes:
            raise ValueError("As equipes devem estar cadastradas no campeonato.")
        partida = Partida(equipe_casa, equipe_visitante, rodada, gols_casa, gols_visitante)
        self._partidas.append(partida)
        return partida

    def quantidade_partidas(self):
        return len(self._partidas)

    def partidas_realizadas(self):
        cont = 0
        for partida in self._partidas:
            if partida.foi_jogada():
                cont += 1
        return cont
    
    def partidas_pendentes(self):
        return self.quantidade_partidas() - self.partidas_realizadas()

    def gerar_partidas(self):
        if self._partidas:
            raise ValueError("As partidas já foram geradas.")
        if len(self._equipes) < 2:
            raise ValueError("É necessário ter pelo menos duas equipes para gerar as partidas.")

        times = list(self._equipes)     # cópia: girar não pode bagunçar a lista oficial
        if len(times) % 2 == 1:
            times.append(None)          # None = folga
        # times = [1, 2, 3, 4]
        total = len(times)
        novas = []
        for rodada in range(1, total):
            # Emparelha as pontas: 1ª x última, 2ª x penúltima...
            # Com total = 4: i = 0 -> times[0] x times[3]; i = 1 -> times[1] x times[2]
            for i in range(total // 2):
                casa = times[i]
                visitante = times[total - 1 - i]
                if casa is not None and visitante is not None:
                    novas.append(self.adicionar_partida(casa, visitante, rodada))
            # Gira: a primeira fica fixa, a última vai para a posição 1
            times.insert(1, times.pop())
        return novas

    def calcular_classificacao(self):
        for equipe in self._equipes:
            equipe.zerar_estatisticas()

        for partida in self._partidas:
            partida.aplicar_nas_equipes()

        return sorted(
            self._equipes, key=lambda equipe: (
                -equipe.pontos,
                -equipe.vitorias,
                -equipe.saldo_gols,
                -equipe.gols_pro,
                equipe.nome.lower()
            )
        )

