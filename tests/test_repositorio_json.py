"""Testes do RepositorioJSON (Etapa 4), sem interface gráfica.

Cada teste usa uma pasta temporária, apagada no final, para não mexer no
data/campeonato.json de verdade.
"""

import json
import tempfile
import unittest
from pathlib import Path

from models.campeonato import Campeonato
from storage.repositorio_json import RepositorioJSON


class TestRepositorioJSON(unittest.TestCase):

    def setUp(self):
        self.pasta_temporaria = tempfile.TemporaryDirectory()
        # Subpasta que ainda não existe: testa a criação automática da pasta
        self.caminho = Path(self.pasta_temporaria.name) / "data" / "campeonato.json"
        self.repositorio = RepositorioJSON(self.caminho)

    def tearDown(self):
        # Roda depois de CADA teste, mesmo se ele falhar: apaga a pasta
        self.pasta_temporaria.cleanup()

    def criar_campeonato_exemplo(self):
        campeonato = Campeonato("Campeonato da Turma")
        campeonato.adicionar_equipe("Flamengo", "Rio de Janeiro")
        campeonato.adicionar_equipe("Palmeiras", "São Paulo")
        campeonato.adicionar_equipe("Grêmio", "Porto Alegre")
        partidas = campeonato.gerar_partidas()
        partidas[0].registrar_resultado(2, 1)  # uma realizada, as outras pendentes
        return campeonato

    def escrever_arquivo(self, texto):
        """Auxiliar: grava um conteúdo qualquer no arquivo, para testar leituras ruins."""
        self.caminho.parent.mkdir(parents=True, exist_ok=True)
        self.caminho.write_text(texto, encoding="utf-8")

    # ---------- Casos normais ----------

    def test_carregar_sem_arquivo_devolve_none(self):
        self.assertIsNone(self.repositorio.carregar())

    def test_salvar_cria_a_pasta_e_o_arquivo(self):
        self.repositorio.salvar(Campeonato("Teste"))

        self.assertTrue(self.caminho.exists())

    def test_salvar_e_carregar_mantem_os_dados(self):
        original = self.criar_campeonato_exemplo()

        self.repositorio.salvar(original)
        carregado = self.repositorio.carregar()

        self.assertEqual(carregado.nome, original.nome)
        self.assertEqual(
            [(e.nome, e.cidade) for e in carregado.equipes],
            [(e.nome, e.cidade) for e in original.equipes],
        )
        # Compara cada partida: equipes, rodada e placar (None nas pendentes)
        self.assertEqual(
            [self.resumo(p) for p in carregado.partidas],
            [self.resumo(p) for p in original.partidas],
        )

    def resumo(self, partida):
        return (partida.equipe_casa.nome, partida.equipe_visitante.nome,
                partida.rodada, partida.gols_casa, partida.gols_visitante)

    def test_partidas_carregadas_apontam_para_as_equipes_carregadas(self):
        # Se a partida apontasse para outro objeto, a classificação não funcionaria
        self.repositorio.salvar(self.criar_campeonato_exemplo())
        carregado = self.repositorio.carregar()

        for partida in carregado.partidas:
            self.assertIn(partida.equipe_casa, carregado.equipes)
            self.assertIn(partida.equipe_visitante, carregado.equipes)

    def test_classificacao_funciona_depois_de_carregar(self):
        self.repositorio.salvar(self.criar_campeonato_exemplo())
        carregado = self.repositorio.carregar()

        lider = carregado.calcular_classificacao()[0]

        self.assertEqual(lider.pontos, 3)

    def test_arquivo_segue_o_formato_da_especificacao(self):
        self.repositorio.salvar(self.criar_campeonato_exemplo())

        dados = json.loads(self.caminho.read_text(encoding="utf-8"))

        self.assertEqual(dados["nome"], "Campeonato da Turma")
        self.assertEqual(dados["equipes"][1], {"nome": "Palmeiras", "cidade": "São Paulo"})
        pendente = dados["partidas"][1]
        self.assertIsNone(pendente["gols_casa"])       # null no arquivo
        self.assertIsNone(pendente["gols_visitante"])
        self.assertNotIn("pontos", dados["equipes"][0])  # estatística não é salva

    def test_acentos_ficam_legiveis_no_arquivo(self):
        self.repositorio.salvar(self.criar_campeonato_exemplo())

        texto = self.caminho.read_text(encoding="utf-8")

        self.assertIn("São Paulo", texto)

    # ---------- Arquivos com problema ----------

    def test_json_corrompido_gera_erro_e_nao_altera_o_arquivo(self):
        conteudo_ruim = '{"nome": "Campeonato", "equipes": ['
        self.escrever_arquivo(conteudo_ruim)

        with self.assertRaises(ValueError):
            self.repositorio.carregar()
        self.assertEqual(self.caminho.read_text(encoding="utf-8"), conteudo_ruim)

    def test_campo_faltando_gera_erro(self):
        self.escrever_arquivo('{"nome": "Campeonato"}')  # sem "equipes" e "partidas"

        with self.assertRaises(ValueError):
            self.repositorio.carregar()

    def test_dados_que_violam_as_regras_geram_erro(self):
        dados = {
            "nome": "Campeonato",
            "equipes": [
                {"nome": "Flamengo", "cidade": "Rio"},
                {"nome": "FLAMENGO", "cidade": "Rio"},  # nome duplicado
            ],
            "partidas": [],
        }
        self.escrever_arquivo(json.dumps(dados))

        with self.assertRaises(ValueError):
            self.repositorio.carregar()

    def test_partida_com_equipe_inexistente_gera_erro(self):
        dados = {
            "nome": "Campeonato",
            "equipes": [{"nome": "Flamengo", "cidade": "Rio"}],
            "partidas": [{
                "equipe_casa": "Flamengo", "equipe_visitante": "Vasco",
                "rodada": 1, "gols_casa": None, "gols_visitante": None,
            }],
        }
        self.escrever_arquivo(json.dumps(dados))

        with self.assertRaises(ValueError):
            self.repositorio.carregar()


if __name__ == "__main__":
    unittest.main()
