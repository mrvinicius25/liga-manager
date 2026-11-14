class Equipe:
    """Representa uma equipe participante do campeonato."""

    def __init__(self, nome, cidade):
        # 1) Limpa os espaços antes de usar
        nome_limpo = nome.strip()
        cidade_limpa = cidade.strip()

        # 2) Valida antes de guardar
        if not nome_limpo:
            raise ValueError("O nome não pode ficar vazio ou conter apenas espaços.")
        if not cidade_limpa:
            raise ValueError("A cidade não pode ficar vazia ou conter apenas espaços.")

        # 3) Guarda nos atributos privados
        self._nome = nome_limpo
        self._cidade = cidade_limpa

        # 4) Toda equipe nova começa com as estatísticas zeradas
        self.zerar_estatisticas()

    # ---------- Propriedades (somente leitura) ----------

    @property
    def nome(self):
        return self._nome

    @property
    def cidade(self):
        return self._cidade

    @property
    def pontos(self):
        return self._pontos

    @property
    def jogos(self):
        return self._jogos

    @property
    def vitorias(self):
        return self._vitorias

    @property
    def empates(self):
        return self._empates

    @property
    def derrotas(self):
        return self._derrotas

    @property
    def gols_pro(self):
        return self._gols_pro

    @property
    def gols_contra(self):
        return self._gols_contra

    @property
    def saldo_gols(self):
        # Calculado na hora: nunca fica desatualizado
        return self._gols_pro - self._gols_contra

    # ---------- Métodos ----------

    def zerar_estatisticas(self):
        self._pontos = 0
        self._jogos = 0
        self._vitorias = 0
        self._empates = 0
        self._derrotas = 0
        self._gols_pro = 0
        self._gols_contra = 0

    def registrar_jogo(self, gols_feitos, gols_sofridos):
        # Sempre acontece, independentemente do resultado
        self._jogos += 1
        self._gols_pro += gols_feitos
        self._gols_contra += gols_sofridos

        # Depende do resultado
        if gols_feitos > gols_sofridos:
            self._vitorias += 1
            self._pontos += 3
        elif gols_feitos == gols_sofridos:
            self._empates += 1
            self._pontos += 1
        else:
            self._derrotas += 1

    def __str__(self):
        return f"{self._nome} ({self._cidade})"