import json
from pathlib import Path

from models.campeonato import Campeonato


class RepositorioJSON:
    """Lê e grava um Campeonato em um arquivo JSON.

    Só cuida da persistência: as regras continuam em Campeonato, Equipe e
    Partida. Por isso, ao carregar, o campeonato é reconstruído pelos próprios
    métodos do modelo, que validam os dados lidos do arquivo.
    """

    def __init__(self, caminho):
        self._caminho = Path(caminho)

    @property
    def caminho(self):
        return self._caminho

    # ---------- Gravação ----------

    def salvar(self, campeonato):
        dados = self._campeonato_para_dicionario(campeonato)

        # Cria a pasta (ex.: data/) na primeira gravação, se ainda não existir
        self._caminho.parent.mkdir(parents=True, exist_ok=True)

        with open(self._caminho, "w", encoding="utf-8") as arquivo:
            # ensure_ascii=False: grava "São Paulo" em vez de "São Paulo"
            json.dump(dados, arquivo, ensure_ascii=False, indent=2)

    def _campeonato_para_dicionario(self, campeonato):
        # O json só sabe gravar tipos básicos (dict, list, str, int, None),
        # então cada objeto vira um dicionário. As estatísticas não são
        # gravadas: elas são recalculadas a partir das partidas.
        equipes = []
        for equipe in campeonato.equipes:
            equipes.append({"nome": equipe.nome, "cidade": equipe.cidade})

        partidas = []
        for partida in campeonato.partidas:
            partidas.append({
                "equipe_casa": partida.equipe_casa.nome,
                "equipe_visitante": partida.equipe_visitante.nome,
                "rodada": partida.rodada,
                "gols_casa": partida.gols_casa,            # None vira null
                "gols_visitante": partida.gols_visitante,
            })

        return {"nome": campeonato.nome, "equipes": equipes, "partidas": partidas}

    # ---------- Leitura ----------

    def carregar(self):
        """Devolve o Campeonato salvo, ou None se o arquivo ainda não existir.

        Lança ValueError se o arquivo estiver corrompido ou com dados
        inválidos. O arquivo nunca é alterado aqui.
        """
        if not self._caminho.exists():
            return None

        try:
            with open(self._caminho, "r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)
            return self._dicionario_para_campeonato(dados)
        except json.JSONDecodeError:
            raise ValueError(
                f"O arquivo '{self._caminho}' não é um JSON válido."
            )
        except (KeyError, TypeError, AttributeError):
            # Campo faltando ou com tipo errado (ex.: "equipes" não é lista)
            raise ValueError(
                f"O arquivo '{self._caminho}' está com a estrutura incorreta."
            )
        except ValueError as erro:
            # Dados que violam as regras do campeonato (ex.: nome duplicado)
            raise ValueError(
                f"O arquivo '{self._caminho}' contém dados inválidos: {erro}"
            )

    def _dicionario_para_campeonato(self, dados):
        campeonato = Campeonato(dados["nome"])

        # Primeiro todas as equipes: as partidas precisam dos objetos Equipe,
        # e a regra 10 bloqueia cadastrar equipes depois que há partidas.
        for dados_equipe in dados["equipes"]:
            campeonato.adicionar_equipe(dados_equipe["nome"], dados_equipe["cidade"])

        # Depois as partidas, recriadas exatamente como foram salvas (mesmas
        # rodadas e placares). Não usamos gerar_partidas(), que recriaria o
        # calendário do zero e perderia os resultados.
        for dados_partida in dados["partidas"]:
            casa = self._equipe_por_nome(campeonato, dados_partida["equipe_casa"])
            visitante = self._equipe_por_nome(campeonato, dados_partida["equipe_visitante"])
            campeonato.adicionar_partida(
                casa,
                visitante,
                dados_partida["rodada"],
                dados_partida["gols_casa"],
                dados_partida["gols_visitante"],
            )

        return campeonato

    def _equipe_por_nome(self, campeonato, nome):
        equipe = campeonato.buscar_equipe(nome)
        if equipe is None:
            raise ValueError(f"a partida cita a equipe '{nome}', que não está cadastrada.")
        return equipe
