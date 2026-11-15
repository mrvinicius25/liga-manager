"""Testes da classe Campeonato (Etapa 3 do plano), sem interface gráfica.

Como rodar, a partir da pasta raiz do projeto:
    python -m unittest discover -s tests -v
"""

import unittest

from models.campeonato import Campeonato


class TestCadastroEquipes(unittest.TestCase):

    def setUp(self):
        # Roda antes de CADA teste: cada um começa com um campeonato novo,
        # então um teste nunca interfere no outro.
        self.campeonato = Campeonato("Campeonato Teste")

    def test_campeonato_comeca_vazio(self):
        self.assertEqual(self.campeonato.quantidade_equipes(), 0)
        self.assertEqual(self.campeonato.quantidade_partidas(), 0)

    def test_nome_do_campeonato_vazio_e_rejeitado(self):
        with self.assertRaises(ValueError):
            Campeonato("   ")

    def test_adicionar_equipe_aumenta_quantidade(self):
        equipe = self.campeonato.adicionar_equipe("Flamengo", "Rio de Janeiro")

        self.assertEqual(self.campeonato.quantidade_equipes(), 1)
        self.assertEqual(equipe.nome, "Flamengo")

    def test_nome_duplicado_e_bloqueado_ignorando_maiusculas(self):
        self.campeonato.adicionar_equipe("Flamengo", "Rio de Janeiro")

        with self.assertRaises(ValueError):
            self.campeonato.adicionar_equipe("FLAMENGO", "Outra Cidade")
        self.assertEqual(self.campeonato.quantidade_equipes(), 1)

    def test_campos_vazios_sao_rejeitados(self):
        with self.assertRaises(ValueError):
            self.campeonato.adicionar_equipe("", "Rio de Janeiro")
        with self.assertRaises(ValueError):
            self.campeonato.adicionar_equipe("Flamengo", "   ")
        self.assertEqual(self.campeonato.quantidade_equipes(), 0)

    def test_buscar_equipe_ignora_maiusculas_e_espacos(self):
        equipe = self.campeonato.adicionar_equipe("Flamengo", "Rio de Janeiro")

        # assertIs confere que é o MESMO objeto, não só um igual
        self.assertIs(self.campeonato.buscar_equipe("  fLaMeNgO "), equipe)

    def test_buscar_equipe_inexistente_devolve_none(self):
        self.assertIsNone(self.campeonato.buscar_equipe("Vasco"))

    def test_propriedade_equipes_devolve_copia(self):
        self.campeonato.adicionar_equipe("Flamengo", "Rio de Janeiro")

        copia = self.campeonato.equipes
        copia.clear()  # mexer na cópia não pode afetar o campeonato

        self.assertEqual(self.campeonato.quantidade_equipes(), 1)


class TestRemocaoEquipes(unittest.TestCase):

    def setUp(self):
        self.campeonato = Campeonato("Campeonato Teste")
        self.flamengo = self.campeonato.adicionar_equipe("Flamengo", "Rio de Janeiro")
        self.palmeiras = self.campeonato.adicionar_equipe("Palmeiras", "Sao Paulo")
        self.santos = self.campeonato.adicionar_equipe("Santos", "Santos")

    def test_remover_equipe_sem_partidas(self):
        self.campeonato.remover_equipe("Santos")

        self.assertEqual(self.campeonato.quantidade_equipes(), 2)
        self.assertIsNone(self.campeonato.buscar_equipe("Santos"))

    def test_remover_equipe_com_partidas_de_outras_equipes(self):
        # Caso que pegou o bug do remove dentro do for
        self.campeonato.adicionar_partida(self.flamengo, self.palmeiras, 1)
        self.campeonato.adicionar_partida(self.palmeiras, self.flamengo, 2)

        self.campeonato.remover_equipe("Santos")

        self.assertEqual(self.campeonato.quantidade_equipes(), 2)

    def test_remover_equipe_vinculada_a_partida_pendente_e_bloqueado(self):
        self.campeonato.adicionar_partida(self.flamengo, self.palmeiras, 1)

        with self.assertRaises(ValueError):
            self.campeonato.remover_equipe("Flamengo")
        self.assertEqual(self.campeonato.quantidade_equipes(), 3)

    def test_remover_equipe_inexistente_e_rejeitado(self):
        with self.assertRaises(ValueError):
            self.campeonato.remover_equipe("Vasco")


class TestAdicionarPartida(unittest.TestCase):

    def setUp(self):
        self.campeonato = Campeonato("Campeonato Teste")
        self.flamengo = self.campeonato.adicionar_equipe("Flamengo", "Rio de Janeiro")
        self.palmeiras = self.campeonato.adicionar_equipe("Palmeiras", "Sao Paulo")

    def test_partida_nasce_pendente(self):
        partida = self.campeonato.adicionar_partida(self.flamengo, self.palmeiras, 1)

        self.assertFalse(partida.foi_jogada())
        self.assertEqual(partida.rodada, 1)

    def test_mesma_equipe_nos_dois_lados_e_rejeitado(self):
        with self.assertRaises(ValueError):
            self.campeonato.adicionar_partida(self.flamengo, self.flamengo, 1)

    def test_equipe_nao_cadastrada_e_rejeitada(self):
        # Equipe criada em OUTRO campeonato, com nome repetido de propósito
        outro = Campeonato("Outro")
        intrusa = outro.adicionar_equipe("Flamengo", "Rio de Janeiro")

        with self.assertRaises(ValueError):
            self.campeonato.adicionar_partida(intrusa, self.palmeiras, 1)


class TestGerarPartidas(unittest.TestCase):

    def criar_campeonato(self, quantidade):
        """Auxiliar: cria um campeonato com 'quantidade' equipes já cadastradas."""
        campeonato = Campeonato("Campeonato Teste")
        for numero in range(1, quantidade + 1):
            campeonato.adicionar_equipe(f"Equipe {numero}", "Cidade")
        return campeonato

    def test_quantidade_de_partidas_segue_a_formula(self):
        for n in range(2, 9):
            # subTest: se falhar, o relatório diz para qual n falhou
            with self.subTest(equipes=n):
                campeonato = self.criar_campeonato(n)
                partidas = campeonato.gerar_partidas()
                self.assertEqual(len(partidas), n * (n - 1) // 2)

    def test_nenhum_confronto_repetido_nem_contra_si_mesmo(self):
        for n in range(2, 9):
            with self.subTest(equipes=n):
                partidas = self.criar_campeonato(n).gerar_partidas()

                confrontos = set()
                for partida in partidas:
                    self.assertIsNot(partida.equipe_casa, partida.equipe_visitante)
                    # frozenset: "A x B" e "B x A" contam como o mesmo par
                    par = frozenset((partida.equipe_casa.nome, partida.equipe_visitante.nome))
                    self.assertNotIn(par, confrontos)
                    confrontos.add(par)

    def test_equipe_joga_no_maximo_uma_vez_por_rodada(self):
        for n in range(2, 9):
            with self.subTest(equipes=n):
                partidas = self.criar_campeonato(n).gerar_partidas()

                jogaram = {}  # rodada -> nomes das equipes que já jogaram nela
                for partida in partidas:
                    nomes = jogaram.setdefault(partida.rodada, [])
                    self.assertNotIn(partida.equipe_casa.nome, nomes)
                    self.assertNotIn(partida.equipe_visitante.nome, nomes)
                    nomes.append(partida.equipe_casa.nome)
                    nomes.append(partida.equipe_visitante.nome)

    def test_quantidade_de_rodadas(self):
        # Par: n - 1 rodadas. Ímpar: n rodadas (uma folga por rodada).
        self.assertEqual(len({p.rodada for p in self.criar_campeonato(4).gerar_partidas()}), 3)
        self.assertEqual(len({p.rodada for p in self.criar_campeonato(5).gerar_partidas()}), 5)

    def test_partidas_geradas_sao_pendentes(self):
        campeonato = self.criar_campeonato(4)
        campeonato.gerar_partidas()

        self.assertEqual(campeonato.partidas_pendentes(), 6)
        self.assertEqual(campeonato.partidas_realizadas(), 0)

    def test_gerar_duas_vezes_e_bloqueado(self):
        campeonato = self.criar_campeonato(4)
        campeonato.gerar_partidas()

        with self.assertRaises(ValueError):
            campeonato.gerar_partidas()
        self.assertEqual(campeonato.quantidade_partidas(), 6)

    def test_gerar_com_menos_de_duas_equipes_e_bloqueado(self):
        with self.assertRaises(ValueError):
            self.criar_campeonato(1).gerar_partidas()

    def test_cadastrar_equipe_depois_da_geracao_e_bloqueado(self):
        campeonato = self.criar_campeonato(4)
        campeonato.gerar_partidas()

        with self.assertRaises(ValueError):
            campeonato.adicionar_equipe("Atrasada", "Cidade")


class TestResultadosEContadores(unittest.TestCase):

    def setUp(self):
        self.campeonato = Campeonato("Campeonato Teste")
        self.flamengo = self.campeonato.adicionar_equipe("Flamengo", "Rio de Janeiro")
        self.palmeiras = self.campeonato.adicionar_equipe("Palmeiras", "Sao Paulo")
        self.partida = self.campeonato.adicionar_partida(self.flamengo, self.palmeiras, 1)

    def test_registrar_placar_torna_partida_realizada(self):
        self.partida.registrar_resultado(2, 1)

        self.assertEqual(self.campeonato.partidas_realizadas(), 1)
        self.assertEqual(self.campeonato.partidas_pendentes(), 0)

    def test_placar_invalido_e_rejeitado(self):
        for gols_casa, gols_visitante in [(-1, 0), (1.5, 0), ("2", 1), (None, 1)]:
            with self.subTest(placar=(gols_casa, gols_visitante)):
                with self.assertRaises(ValueError):
                    self.partida.registrar_resultado(gols_casa, gols_visitante)

        # Nenhuma tentativa inválida pode ter deixado a partida "meio registrada"
        self.assertEqual(self.campeonato.partidas_pendentes(), 1)


class TestClassificacao(unittest.TestCase):

    def setUp(self):
        self.campeonato = Campeonato("Campeonato Teste")
        self.alfa = self.campeonato.adicionar_equipe("alfa", "Cidade")
        self.bravo = self.campeonato.adicionar_equipe("Bravo", "Cidade")
        self.charlie = self.campeonato.adicionar_equipe("Charlie", "Cidade")
        self.delta = self.campeonato.adicionar_equipe("Delta", "Cidade")

    def jogo(self, casa, visitante, gols_casa, gols_visitante):
        """Auxiliar: cria uma partida já com placar."""
        self.campeonato.adicionar_partida(casa, visitante, 1, gols_casa, gols_visitante)

    def test_pontuacao_vitoria_empate_derrota(self):
        self.jogo(self.alfa, self.bravo, 2, 0)     # alfa vence
        self.jogo(self.charlie, self.delta, 1, 1)  # empate

        self.campeonato.calcular_classificacao()

        self.assertEqual(self.alfa.pontos, 3)
        self.assertEqual(self.bravo.pontos, 0)
        self.assertEqual(self.charlie.pontos, 1)
        self.assertEqual(self.delta.pontos, 1)

    def test_estatisticas_completas(self):
        self.jogo(self.alfa, self.bravo, 3, 1)
        self.jogo(self.charlie, self.alfa, 2, 2)

        self.campeonato.calcular_classificacao()

        self.assertEqual(self.alfa.jogos, 2)
        self.assertEqual(self.alfa.vitorias, 1)
        self.assertEqual(self.alfa.empates, 1)
        self.assertEqual(self.alfa.derrotas, 0)
        self.assertEqual(self.alfa.gols_pro, 5)
        self.assertEqual(self.alfa.gols_contra, 3)
        self.assertEqual(self.alfa.saldo_gols, 2)

    def test_partidas_pendentes_nao_contam(self):
        self.campeonato.adicionar_partida(self.alfa, self.bravo, 1)  # sem placar

        self.campeonato.calcular_classificacao()

        self.assertEqual(self.alfa.jogos, 0)
        self.assertEqual(self.alfa.pontos, 0)

    def test_recalcular_varias_vezes_nao_duplica(self):
        self.jogo(self.alfa, self.bravo, 2, 0)

        for _ in range(5):
            self.campeonato.calcular_classificacao()

        self.assertEqual(self.alfa.pontos, 3)
        self.assertEqual(self.alfa.jogos, 1)

    def test_desempate_por_vitorias(self):
        # alfa: 1 vitória + 1 derrota = 3 pts. bravo: 3 empates = 3 pts.
        self.jogo(self.alfa, self.charlie, 1, 0)
        self.jogo(self.delta, self.alfa, 1, 0)
        self.jogo(self.bravo, self.charlie, 0, 0)
        self.jogo(self.bravo, self.delta, 0, 0)
        self.jogo(self.charlie, self.bravo, 0, 0)

        ordem = self.campeonato.calcular_classificacao()

        self.assertLess(ordem.index(self.alfa), ordem.index(self.bravo))

    def test_desempate_por_saldo_de_gols(self):
        # Ambos com 1 vitória; alfa tem saldo +3, bravo +1.
        self.jogo(self.alfa, self.charlie, 3, 0)
        self.jogo(self.bravo, self.delta, 1, 0)

        ordem = self.campeonato.calcular_classificacao()

        self.assertLess(ordem.index(self.alfa), ordem.index(self.bravo))

    def test_desempate_por_gols_pro(self):
        # Ambos com 1 vitória e saldo +1; bravo marcou mais gols.
        self.jogo(self.alfa, self.charlie, 1, 0)
        self.jogo(self.bravo, self.delta, 3, 2)

        ordem = self.campeonato.calcular_classificacao()

        self.assertLess(ordem.index(self.bravo), ordem.index(self.alfa))

    def test_desempate_por_ordem_alfabetica_ignorando_maiusculas(self):
        # Tudo igual entre alfa e Bravo. Sem o .lower(), "Bravo" viria antes
        # de "alfa", porque no Python maiúsculas vêm antes das minúsculas.
        self.jogo(self.alfa, self.bravo, 1, 1)

        ordem = self.campeonato.calcular_classificacao()

        self.assertEqual(ordem[0], self.alfa)
        self.assertEqual(ordem[1], self.bravo)

    def test_classificacao_nao_altera_ordem_de_cadastro(self):
        self.jogo(self.delta, self.alfa, 5, 0)

        self.campeonato.calcular_classificacao()

        nomes = [equipe.nome for equipe in self.campeonato.equipes]
        self.assertEqual(nomes, ["alfa", "Bravo", "Charlie", "Delta"])


if __name__ == "__main__":
    unittest.main()
