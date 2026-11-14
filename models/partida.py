
from models.equipe import Equipe


class Partida:
    def __init__(self, equipe_casa, equipe_visitante, rodada,
                 gols_casa=None, gols_visitante=None):
        if equipe_casa == equipe_visitante:
            raise ValueError("As equipes da casa e visitante devem ser diferentes.")
        self._equipe_casa = equipe_casa
        self._equipe_visitante = equipe_visitante
        self._rodada = rodada

        self._gols_casa = None
        self._gols_visitante = None

        if gols_casa is not None or gols_visitante is not None:
            self.registrar_resultado(gols_casa, gols_visitante)

    # ---------- PROPRIEDADES ----------

    @property
    def equipe_casa(self):
        return self._equipe_casa

    @property
    def equipe_visitante(self):
        return self._equipe_visitante

    @property
    def rodada(self):
        return self._rodada

    @property
    def gols_casa(self):
        return self._gols_casa

    @property
    def gols_visitante(self):
        return self._gols_visitante

    # ---------- REGISTRAR RESULTADO ----------

    def registrar_resultado(self, gols_casa, gols_visitante):

        if type(gols_casa) is not int or type(gols_visitante) is not int:
            raise ValueError("Informe os gols das duas equipes.")

        if gols_casa < 0 or gols_visitante < 0:
            raise ValueError("Os gols não podem ser negativos.")

        self._gols_casa = gols_casa
        self._gols_visitante = gols_visitante

    # ---------- VERIFICAR SE FOI JOGADA ----------

    def foi_jogada(self):
        return (
            self._gols_casa is not None
            and self._gols_visitante is not None
        )

    # ---------- VERIFICAR EMPATE ----------

    def empate(self):
        if not self.foi_jogada():
            return False

        return self._gols_casa == self._gols_visitante

    # ---------- IDENTIFICAR VENCEDOR ----------

    def vencedor(self):
        if not self.foi_jogada() or self.empate():
            return None

        if self._gols_casa > self._gols_visitante:
            return self._equipe_casa

        return self._equipe_visitante

    # ---------- VERIFICAR PARTICIPAÇÃO ----------

    def envolve(self, equipe):
        return (
            equipe == self._equipe_casa
            or equipe == self._equipe_visitante
        )

    # ---------- ATUALIZAR ESTATÍSTICAS ----------

    def aplicar_nas_equipes(self):
        if not self.foi_jogada():
            return

        self._equipe_casa.registrar_jogo(
            self._gols_casa,
            self._gols_visitante
        )

        self._equipe_visitante.registrar_jogo(
            self._gols_visitante,
            self._gols_casa
        )

    # ---------- REPRESENTAÇÃO DA PARTIDA ----------

    def __str__(self):
        if not self.foi_jogada():
            return (
                f"{self._equipe_casa.nome} x "
                f"{self._equipe_visitante.nome} "
                f"(Sem resultado - Rodada {self._rodada})"
            )

        return (
            f"{self._equipe_casa.nome} "
            f"{self._gols_casa} x {self._gols_visitante} "
            f"{self._equipe_visitante.nome} "
            f"(Rodada {self._rodada})"
        )

