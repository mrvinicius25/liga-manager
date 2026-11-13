# LigaManager — Especificação geral atualizada do projeto
## Documento de referência para desenvolvimento com Claude Code

**Objetivo deste documento:** explicar o projeto como um todo, registrar os requisitos e a arquitetura combinada pela equipe, descrever as classes e telas e orientar o desenvolvimento da parte de responsabilidade do colega que ficará com `Campeonato`, a janela principal, a tela inicial e a tabela de classificação.

> Use este documento como referência durante o desenvolvimento. Antes de alterar nomes de classes, métodos, parâmetros ou responsabilidades compartilhadas, confirme a mudança com o colega e atualize o contrato da equipe.

---

# 1. Visão geral

O **LigaManager** é um aplicativo desktop simples, desenvolvido em Python com Tkinter, para gerenciar um campeonato de futebol em turno único.

O sistema permitirá cadastrar equipes, organizar os confrontos, registrar resultados e acompanhar automaticamente a classificação.

O projeto tem finalidade acadêmica e deve demonstrar principalmente:
- Programação Orientada a Objetos (POO);
- classes e objetos;
- encapsulamento por atributos privados e propriedades (`@property`);
- relacionamento entre objetos;
- separação entre regras de negócio e interface gráfica;
- organização do código em módulos.

## 1.1 Escopo

O projeto deve permanecer simples e concentrado nas funcionalidades essenciais.

**Incluído no escopo:**
- criar um campeonato;
- cadastrar e remover equipes;
- gerar os confrontos de um turno único;
- visualizar partidas;
- registrar placares;
- identificar partidas realizadas e pendentes;
- calcular e exibir a classificação;
- navegar entre as telas.

**Fora do escopo nesta versão:**
- login e controle de usuários;
- APIs ou integração com serviços externos;
- funcionalidades online;
- pagamentos;
- mata-mata ou segunda fase;
- cadastro completo de jogadores e escalações;
- estatísticas avançadas além das necessárias para a classificação.

**Persistência:** o sistema utilizará arquivos JSON para manter os dados entre execuções. O arquivo principal será `data/campeonato.json`. A leitura será feita na inicialização e a gravação ocorrerá após operações que alterem os dados, como cadastrar/remover equipes, gerar partidas e registrar resultados.

---

# 2. Tecnologias e execução

- Linguagem: Python 3.
- Interface gráfica: Tkinter e `tkinter.ttk`.
- Paradigma: Programação Orientada a Objetos.
- Dependências externas: nenhuma prevista para a versão básica.

O programa deve ser executado a partir da pasta raiz:

```bash
python main.py
```

---

# 3. Organização de pastas

Estrutura acordada no contrato da equipe:

```text
LigaManager/
├── main.py
├── data/
│   └── campeonato.json       # criado automaticamente na primeira gravação
├── storage/
│   ├── __init__.py
│   └── repositorio_json.py   # leitura e gravação dos dados em JSON
├── models/
│   ├── __init__.py
│   ├── equipe.py
│   ├── partida.py
│   └── campeonato.py
└── views/
    ├── __init__.py
    ├── inicio.py
    ├── equipes.py
    ├── partidas.py
    └── classificacao.py
```

Responsabilidades:

- `models/`: regras de negócio e entidades do sistema. Não deve importar Tkinter.
- `views/`: interface gráfica. Deve chamar os métodos das classes de negócio, sem duplicar regras ou calcular pontos diretamente.
- `main.py`: inicialização do aplicativo, criação do campeonato e navegação entre telas.

Os imports devem partir da pasta raiz, por exemplo:

```python
from models.equipe import Equipe
from models.partida import Partida
from models.campeonato import Campeonato
from storage.repositorio_json import RepositorioJSON
from views.inicio import TelaInicio
```

---

# 4. Divisão de responsabilidades

| Entrega | Responsável | Arquivo |
|---|---|---|
| Classe `Equipe` | Vitor | `models/equipe.py` |
| Classe `Partida` | Vitor | `models/partida.py` |
| Tela de cadastro de equipes | Vitor | `views/equipes.py` |
| Tela de partidas e resultados | Vitor | `views/partidas.py` |
| Classe `Campeonato` | Colega | `models/campeonato.py` |
| Janela principal e navegação (`App`) | Colega | `main.py` |
| Tela inicial / Dashboard | Colega | `views/inicio.py` |
| Tela independente de classificação | Colega | `views/classificacao.py` |
| Persistência JSON | A combinar (sugestão: colega) | `storage/repositorio_json.py` |

A integração e os testes finais devem ser feitos em conjunto.

---

# 5. Requisitos funcionais

## RF01 — Criar o campeonato
Ao iniciar o programa, o sistema deve criar um objeto `Campeonato` com um nome padrão, por exemplo, “Campeonato da Turma”.

## RF02 — Cadastrar equipes
O usuário deve poder informar nome e cidade da equipe. O sistema deve impedir campos vazios e nomes duplicados, ignorando diferenças entre letras maiúsculas e minúsculas.

## RF03 — Listar equipes
O sistema deve apresentar as equipes cadastradas.

## RF04 — Remover equipes
O usuário deve poder remover uma equipe que não esteja vinculada a nenhuma partida. Se a equipe já estiver em algum confronto, a remoção deve ser impedida para preservar a consistência do campeonato.

## RF05 — Gerar confrontos
O sistema deve gerar automaticamente os confrontos de turno único: cada equipe enfrenta cada uma das outras equipes uma única vez, sem jogar contra si mesma. Os confrontos são criados inicialmente como partidas pendentes, sem placar, e recebem um número de rodada.

A quantidade esperada de partidas é:

```text
n * (n - 1) / 2
```

Em que `n` é a quantidade de equipes. Para gerar partidas, deve haver pelo menos duas equipes.

A geração deve evitar duplicar confrontos caso o usuário acione a funcionalidade mais de uma vez. A distribuição por rodadas é obrigatória nesta versão: cada partida deve guardar o número da rodada em que será disputada. Se a quantidade de equipes for ímpar, uma equipe ficará sem jogar em cada rodada (folga), sem criar partida fictícia.

## RF06 — Exibir partidas
O sistema deve listar os confrontos gerados e seus placares, quando já registrados.

## RF07 — Registrar resultado
O usuário deve informar os gols da equipe da casa e da equipe visitante. Os valores devem ser números inteiros maiores ou iguais a zero. Não deve ser permitido registrar apenas um dos dois gols.

## RF08 — Identificar situação da partida
Uma partida sem placar deve ser considerada pendente. Uma partida com os dois gols registrados deve ser considerada realizada.

## RF09 — Calcular classificação
O sistema deve calcular automaticamente os dados das equipes com base nos resultados registrados.

## RF10 — Exibir Dashboard
A tela inicial deve apresentar o nome do campeonato, os indicadores gerais e os atalhos de navegação.

## RF11 — Navegar entre telas
O usuário deve conseguir acessar quatro telas independentes: Início, Equipes, Partidas e Classificação.

---

# 6. Regras de negócio

1. Uma equipe precisa ter nome e cidade preenchidos.
2. Não pode haver duas equipes com o mesmo nome, desconsiderando maiúsculas e minúsculas.
3. Uma partida não pode colocar a mesma equipe nos dois lados.
4. O placar deve conter dois números inteiros não negativos.
5. Uma partida só é considerada realizada quando os dois gols estiverem registrados.
6. Uma partida sem resultado é pendente.
7. Em turno único, cada par de equipes deve se enfrentar uma única vez.
8. Não se deve gerar novamente os mesmos confrontos.
9. Uma equipe vinculada a uma partida não deve ser removida, mesmo que a partida ainda esteja pendente.
10. Depois que os confrontos forem gerados, não se deve adicionar ou remover equipes sem antes definir um procedimento explícito para regenerar o calendário; para a versão simples, bloquear alterações no conjunto de equipes após a geração é a opção mais segura.
11. A classificação deve ser recalculada a partir das partidas, sem acumular estatísticas repetidas a cada atualização.

## 6.1 Pontuação

- Vitória: 3 pontos.
- Empate: 1 ponto para cada equipe.
- Derrota: 0 ponto.

## 6.2 Estatísticas da classificação

- `jogos`: partidas realizadas pela equipe;
- `vitorias`: vitórias;
- `empates`: empates;
- `derrotas`: derrotas;
- `gols_pro`: gols marcados;
- `gols_contra`: gols sofridos;
- `saldo_gols`: gols pró menos gols contra;
- `pontos`: pontuação total.

Partidas pendentes não entram nas estatísticas.

## 6.3 Critérios de desempate

A classificação deve ser ordenada nesta sequência:
1. maior número de pontos;
2. maior número de vitórias;
3. maior saldo de gols;
4. maior número de gols pró;
5. ordem alfabética do nome da equipe.

---

# 7. Classes de negócio (`models/`)

## 7.1 Classe `Equipe` — responsabilidade de Vitor

**Arquivo:** `models/equipe.py`

Representa uma equipe participante.

### Construtor

```python
Equipe(nome, cidade)
```

Deve validar nome e cidade e iniciar as estatísticas em zero.

### Propriedades públicas previstas

- `nome`
- `cidade`
- `pontos`
- `jogos`
- `vitorias`
- `empates`
- `derrotas`
- `gols_pro`
- `gols_contra`
- `saldo_gols`

Os atributos internos devem usar `_`, por exemplo, `self._nome`, e ser expostos por propriedades.

### Métodos previstos

| Método | Responsabilidade |
|---|---|
| `zerar_estatisticas()` | Zera todos os indicadores da equipe. |
| `registrar_jogo(gols_feitos, gols_sofridos)` | Atualiza jogos, gols, resultado e pontos conforme o placar. |
| `__str__()` | Retorna uma representação legível, por exemplo `Flamengo (Rio de Janeiro)`. |

### Regra importante para a integração

A classe `Equipe` não deve calcular a classificação geral do campeonato. Ela apenas mantém suas próprias estatísticas. A classe `Campeonato` coordena o recálculo de todas as equipes.

---

## 7.2 Classe `Partida` — responsabilidade de Vitor

**Arquivo:** `models/partida.py`

Representa um confronto entre dois objetos `Equipe`.

### Construtor definido no contrato

```python
Partida(
    equipe_casa,
    equipe_visitante,
    rodada,
    gols_casa=None,
    gols_visitante=None
)
```

Os dois gols devem ser `None` quando a partida ainda não tiver resultado. Se o placar for informado, os dois valores devem ser validados.

### Propriedades previstas

- `equipe_casa`
- `equipe_visitante`
- `gols_casa`
- `gols_visitante`

### Métodos previstos

| Método | Responsabilidade |
|---|---|
| `registrar_resultado(gols_casa, gols_visitante)` | Valida e registra o placar. |
| `foi_jogada()` | Retorna `True` se já houver resultado. |
| `empate()` | Informa se a partida terminou empatada. |
| `vencedor()` | Retorna a equipe vencedora ou `None` em empate/partida pendente. |
| `envolve(equipe)` | Informa se a equipe participa do confronto. |
| `aplicar_nas_equipes()` | Aplica o resultado às estatísticas das duas equipes, se a partida tiver sido realizada. |
| `__str__()` | Retorna o confronto e o placar ou indica que está sem resultado. |

### Rodada

A equipe decidiu que toda partida terá uma rodada. Portanto, a classe deve expor a propriedade `rodada`, recebida no construtor. A assinatura combinada deve ser semelhante a:

```python
Partida(equipe_casa, equipe_visitante, rodada, gols_casa=None, gols_visitante=None)
```

Vitor e o colega devem confirmar a ordem final dos parâmetros e manter a mesma assinatura nos dois lados do projeto.

---

## 7.3 Classe `Campeonato` — responsabilidade do colega

**Arquivo:** `models/campeonato.py`

É a classe central das regras do campeonato. Ela mantém a lista de equipes e a lista de partidas e coordena cadastro, geração de confrontos, remoção e classificação.

### Construtor

```python
Campeonato(nome)
```

Deve inicializar:
- `self._nome`;
- `self._equipes = []`;
- `self._partidas = []`.

### Propriedades

| Propriedade | Retorno | Regra |
|---|---|---|
| `nome` | `str` | Nome do campeonato. |
| `equipes` | `list[Equipe]` | Deve devolver uma cópia da lista interna. |
| `partidas` | `list[Partida]` | Deve devolver uma cópia da lista interna. |

### Métodos definidos no contrato atualizado

| Método | Retorno | Responsabilidade |
|---|---|---|
| `quantidade_equipes()` | `int` | Informa quantas equipes estão cadastradas. |
| `adicionar_equipe(nome, cidade)` | `Equipe` | Cria e adiciona uma equipe, impedindo nome duplicado. |
| `buscar_equipe(nome)` | `Equipe` ou `None` | Busca equipe pelo nome, sem diferenciar maiúsculas/minúsculas. |
| `remover_equipe(nome)` | — | Remove equipe existente que não esteja vinculada a partidas. |
| `adicionar_partida(equipe_casa, equipe_visitante, rodada, gols_casa=None, gols_visitante=None)` | `Partida` | Cria e guarda uma partida; por padrão, cria uma partida pendente. |

### Métodos obrigatórios para atender aos requisitos

A classe deve implementar os seguintes métodos:

| Método recomendado | Retorno | Finalidade |
|---|---|---|
| `gerar_partidas()` | `list[Partida]` | Gera todos os confrontos de turno único, distribuídos em rodadas e sem duplicatas. |
| `quantidade_partidas()` | `int` | Total de confrontos cadastrados. |
| `partidas_realizadas()` | `int` | Quantidade de partidas com resultado. |
| `partidas_pendentes()` | `int` | Quantidade de partidas sem resultado. |
| `calcular_classificacao()` | `list[Equipe]` | Recalcula e devolve as equipes ordenadas. |

**Criação e resultado são operações separadas.** `gerar_partidas()` ou `adicionar_partida()` cria o confronto com `gols_casa=None` e `gols_visitante=None`. Depois, a tela de partidas chama `partida.registrar_resultado(gols_casa, gols_visitante)` para registrar o placar. Os dois gols devem estar preenchidos juntos; não se aceita placar parcial.

### Recálculo da classificação

A estratégia acordada no contrato é:

1. zerar as estatísticas de todas as equipes;
2. percorrer as partidas;
3. aplicar às equipes somente os resultados das partidas realizadas;
4. ordenar as equipes pelos critérios de desempate;
5. devolver a lista ordenada.

O recálculo deve poder ser executado várias vezes sem duplicar pontos ou estatísticas.

Exemplo conceitual:

```python
def calcular_classificacao(self):
    for equipe in self._equipes:
        equipe.zerar_estatisticas()

    for partida in self._partidas:
        partida.aplicar_nas_equipes()

    return sorted(
        self._equipes,
        key=lambda equipe: (
            -equipe.pontos,
            -equipe.vitorias,
            -equipe.saldo_gols,
            -equipe.gols_pro,
            equipe.nome.lower()
        )
    )
```

Esse método depende de `Equipe` e `Partida` implementarem exatamente os métodos e propriedades descritos neste documento.

---

# 8. Persistência em JSON

**Arquivo sugerido:** `storage/repositorio_json.py`  
**Arquivo de dados:** `data/campeonato.json`  
**Responsável:** ainda deve ser confirmado entre os integrantes. Como o colega cuida da inicialização e integração, recomenda-se que ele implemente ou coordene esta parte.

O JSON deve armazenar os dados necessários para reconstruir o campeonato:
- nome do campeonato;
- equipes, com nome e cidade;
- partidas, com nome da equipe da casa, nome da equipe visitante, rodada, gols da casa e gols do visitante;
- partidas pendentes devem guardar `null` nos dois campos de gols.

Não é necessário salvar as estatísticas da classificação. Elas devem ser recalculadas a partir dos resultados das partidas, evitando divergências.

### Exemplo conceitual do arquivo JSON

```json
{
  "nome": "Campeonato da Turma",
  "equipes": [
    {"nome": "Flamengo", "cidade": "Rio de Janeiro"},
    {"nome": "Palmeiras", "cidade": "Sao Paulo"}
  ],
  "partidas": [
    {
      "equipe_casa": "Flamengo",
      "equipe_visitante": "Palmeiras",
      "rodada": 1,
      "gols_casa": null,
      "gols_visitante": null
    }
  ]
}
```

### Como carregar

1. Verificar se `data/campeonato.json` existe.
2. Se não existir, iniciar um campeonato vazio com o nome padrão.
3. Se existir, ler o JSON e criar o objeto `Campeonato`.
4. Recriar primeiro as equipes.
5. Recriar as partidas usando os nomes das equipes para recuperar os objetos correspondentes.
6. Recalcular a classificação quando a tela de classificação for atualizada.

### Como salvar

Após uma operação bem-sucedida que altere os dados, salvar novamente o campeonato:
- cadastrar ou remover equipe;
- gerar os confrontos;
- registrar um resultado.

A gravação deve converter os objetos em dicionários, listas, textos, números e valores `null`. Não se deve tentar gravar diretamente objetos Python no JSON.

### Interface sugerida para o repositório

```python
RepositorioJSON(caminho)
repositorio.carregar()  # devolve um Campeonato ou None se o arquivo ainda não existir
repositorio.salvar(campeonato)
```

O repositório deve cuidar somente da leitura e gravação. As regras do campeonato permanecem em `Campeonato`, `Equipe` e `Partida`. Se o JSON estiver inválido, apresentar um erro claro e não sobrescrever silenciosamente o arquivo.

---

# 8. Interface gráfica (`views/` e `main.py`)

## 9.1 Janela principal e classe `App`

**Arquivo:** `main.py`  
**Responsável:** colega.

A classe `App` deve herdar de `tk.Tk`, criar a janela principal, instanciar um único objeto `Campeonato` e controlar a navegação.

### Interface pública obrigatória

| Membro | Responsabilidade |
|---|---|
| `app.campeonato` | Referência ao único objeto `Campeonato` usado pelas telas. |
| `app.mostrar_tela(nome)` | Atualiza e exibe a tela solicitada. |

Nomes de tela previstos:
- `"inicio"`
- `"equipes"`
- `"partidas"`
- `"classificacao"`

Cada tela deve ter um método `atualizar()` para reler os dados do campeonato antes de ser exibida.

### Esqueleto de referência

```python
import tkinter as tk

from models.campeonato import Campeonato
from storage.repositorio_json import RepositorioJSON
from views.inicio import TelaInicio
from views.equipes import TelaEquipes
from views.partidas import TelaPartidas
from views.classificacao import TelaClassificacao


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("LigaManager")
        self.geometry("900x550")

        self.repositorio = RepositorioJSON("data/campeonato.json")
        self.campeonato = self.repositorio.carregar()
        if self.campeonato is None:
            self.campeonato = Campeonato("Campeonato da Turma")
            self.repositorio.salvar(self.campeonato)

        container = tk.Frame(self)
        container.pack(fill="both", expand=True)
        container.rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)

        self.telas = {
            "inicio": TelaInicio(container, self),
            "equipes": TelaEquipes(container, self),
            "partidas": TelaPartidas(container, self),
            "classificacao": TelaClassificacao(container, self),
        }

        for tela in self.telas.values():
            tela.grid(row=0, column=0, sticky="nsew")

        self.mostrar_tela("inicio")

    def mostrar_tela(self, nome):
        tela = self.telas[nome]
        tela.atualizar()
        tela.tkraise()

    def salvar_dados(self):
        self.repositorio.salvar(self.campeonato)


if __name__ == "__main__":
    App().mainloop()
```

O esqueleto é uma referência de integração. Ajustes visuais podem ser feitos sem alterar a interface pública usada pelas outras telas.

---

## 9.2 Padrão das telas

As telas devem herdar de `tk.Frame` ou de um componente `ttk.Frame`, receber `master` e `app` no construtor e manter uma referência a `app`.

Padrão:

```python
class TelaExemplo(tk.Frame):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app
        # Construção dos componentes visuais.

    def atualizar(self):
        # Atualiza a interface com os dados de self.app.campeonato.
        pass
```

As telas não devem manter cópias independentes das equipes e partidas. A fonte dos dados é `self.app.campeonato`.

---

## 9.3 Tela inicial / Dashboard

**Arquivo:** `views/inicio.py`  
**Classe:** `TelaInicio`  
**Responsável:** colega.

A tela inicial é o resumo do campeonato e o ponto de entrada para as demais funcionalidades.

### Informações obrigatórias

1. Nome do campeonato.
2. Quantidade de equipes cadastradas.
3. Total de partidas.
4. Partidas realizadas.
5. Partidas pendentes.

### Navegação

Deve oferecer acesso às telas:
- Equipes;
- Partidas;
- Classificação.

A classificação será acessada pela opção própria na navegação principal.

### Atualização dos indicadores

Os números não devem ser digitados manualmente. Devem ser obtidos do objeto `self.app.campeonato` sempre que a tela for exibida ou atualizada.

Para isso, a classe `Campeonato` precisa fornecer métodos ou propriedades que retornem as quantidades. Os métodos recomendados estão descritos na seção 7.3.

### Exemplo visual conceitual

```text
+--------------------------------------------------+
|                    LigaManager                   |
|                                                  |
|              Campeonato da Turma                |
|                                                  |
|   Equipes          Total de partidas             |
|      8                     28                    |
|                                                  |
|   Realizadas       Pendentes                     |
|      12                 16                       |
|                                                  |
|   [ Equipes ]       [ Partidas ]                 |
+--------------------------------------------------+
```

Os números acima são apenas ilustrativos.

---

## 9.4 Tela de equipes

**Arquivo:** `views/equipes.py`  
**Classe:** `TelaEquipes`  
**Responsável:** Vitor.

Funcionalidades:
- campo para nome;
- campo para cidade;
- botão para cadastrar;
- lista das equipes;
- botão para remover;
- botão para voltar à tela inicial;
- mensagens de validação e erro.

A tela deve chamar os métodos de `self.app.campeonato`, em vez de manter uma lista própria de equipes.

---

## 9.5 Tela de partidas e resultados

**Arquivo:** `views/partidas.py`  
**Classe:** `TelaPartidas`  
**Responsável:** Vitor.

Funcionalidades:
- exibir os confrontos agrupados ou identificados por rodada;
- oferecer uma ação para gerar os confrontos do campeonato, se ainda não tiverem sido gerados;
- mostrar partidas pendentes e realizadas;
- permitir selecionar uma partida pendente e registrar seu placar;
- oferecer navegação para Início e Classificação;
- chamar `app.salvar_dados()` após uma alteração bem-sucedida.

A tela não deve calcular pontos por conta própria. A criação do calendário é responsabilidade de `Campeonato.gerar_partidas()`.

Após cadastrar/remover equipe, gerar confrontos ou registrar um resultado, a tela deve chamar `self.app.salvar_dados()` depois que a operação for concluída com sucesso.

---

## 9.6 Tela independente `TelaClassificacao`

**Arquivo:** `views/classificacao.py`  
**Classe:** `TelaClassificacao`  
**Responsável:** colega.

É uma tela independente, registrada na navegação principal da classe `App`. Ela apresenta a tabela de classificação completa.

### Colunas previstas

| Coluna | Significado |
|---|---|
| Pos | Posição |
| Equipe | Nome da equipe |
| PTS | Pontos |
| J | Jogos realizados |
| V | Vitórias |
| E | Empates |
| D | Derrotas |
| GP | Gols pró |
| GC | Gols contra |
| SG | Saldo de gols |

### Interface pública

```python
TelaClassificacao(master, app)
```

A tela deve ter o método `atualizar()` e consultar `self.app.campeonato.calcular_classificacao()`. Deve exibir as colunas Pos, Equipe, PTS, J, V, E, D, GP, GC e SG. Pode usar `ttk.Treeview`.

A tela apenas apresenta os dados. O cálculo pertence à classe `Campeonato`. Deve oferecer um botão para voltar ao Início e/ou navegar para as demais telas.

---

# 10. Padrões de implementação

1. Classes em `PascalCase`, por exemplo, `Campeonato`.
2. Métodos e variáveis em `snake_case`, por exemplo, `calcular_classificacao`.
3. Nomes em português, sem acentos nos identificadores.
4. Atributos internos iniciados por `_`.
5. Propriedades públicas implementadas com `@property`.
6. Classes de `models/` não importam Tkinter.
7. As telas não duplicam regras de negócio.
8. Erros de regra de negócio devem lançar `ValueError` com mensagens em português.
9. As telas devem capturar `ValueError` e apresentar a mensagem com `messagebox.showerror`.


---

# 11. Contrato de integração atualizado

As decisões abaixo já foram tomadas pela equipe:

- [x] A classe `Campeonato` terá `gerar_partidas()`.
- [x] Os confrontos serão criados inicialmente sem placar; o resultado será registrado depois.
- [x] A classe `Partida` terá o atributo `rodada`.
- [x] A classificação será recalculada a partir das partidas, zerando antes as estatísticas.
- [x] Os dados serão persistidos em JSON.
- [x] A classificação terá uma tela independente.

Ainda é necessário alinhar com Vitor a assinatura exata do construtor de `Partida`, incluindo a posição do parâmetro `rodada`, e confirmar quem implementará `RepositorioJSON`. Não alterem assinaturas compartilhadas sem atualizar o contrato.

---

# 12. Plano de trabalho para a parte do colega

Esta é a sequência recomendada para desenvolver e aprender gradualmente, sem tentar construir tudo de uma vez.

## Etapa 1 — Entender o contrato de integração
- Ler este documento.
- Confirmar com Vitor os métodos e parâmetros de `Equipe` e `Partida`.
- Não inventar atributos ou métodos que ainda não estejam combinados.

## Etapa 2 — Implementar `Campeonato`
- Criar `models/campeonato.py`.
- Implementar o construtor e as propriedades.
- Implementar cadastro, busca e remoção de equipes.
- Implementar `gerar_partidas()` com turno único e distribuição por rodadas.
- Implementar os indicadores necessários ao Dashboard.
- Implementar o cálculo da classificação.

## Etapa 3 — Testar `Campeonato` sem interface
Testar pelo terminal:
- cadastro de equipes;
- bloqueio de nomes repetidos;
- busca;
- remoção permitida e bloqueada;
- quantidade de partidas;
- geração sem confrontos repetidos;
- partidas pendentes e realizadas;
- cálculo da classificação;
- recálculo repetido sem duplicação de estatísticas.

## Etapa 4 — Criar a persistência JSON e a janela principal
- Implementar ou integrar `RepositorioJSON` em `storage/repositorio_json.py` (responsável a confirmar).
- Criar/carregar um único objeto `Campeonato` na inicialização.
- Salvar após operações que alterem os dados.
- Implementar a classe `App` em `main.py`.
- Criar o container de quatro telas.
- Implementar `mostrar_tela(nome)`.
- Testar carregamento, gravação e navegação.

## Etapa 5 — Criar a tela inicial
- Implementar `TelaInicio` em `views/inicio.py`.
- Mostrar o nome do campeonato e os quatro indicadores.
- Criar botões de navegação para Equipes e Partidas.
- Atualizar os dados sempre que a tela for exibida.

## Etapa 6 — Criar a tela independente de classificação
- Implementar `TelaClassificacao` em `views/classificacao.py`.
- Criar o `Treeview` e suas colunas.
- Implementar `atualizar()` consultando `self.app.campeonato`.
- Adicionar a tela à navegação do `App`.
- Testar com equipes e resultados fictícios.

## Etapa 7 — Integrar com a parte de Vitor
- Receber as classes `Equipe` e `Partida`.
- Verificar se os nomes e assinaturas coincidem com este contrato.
- Integrar as telas.
- Testar o fluxo completo.

---

# 13. Critérios de aceitação e testes finais

O projeto será considerado funcional quando os seguintes cenários forem atendidos:

- [ ] `python main.py` abre a janela principal sem erro.
- [ ] A tela inicial mostra o nome do campeonato.
- [ ] Cadastrar quatro equipes atualiza o indicador para quatro.
- [ ] Tentar cadastrar equipe com nome repetido apresenta erro.
- [ ] Tentar cadastrar equipe com campos vazios apresenta erro.
- [ ] Uma equipe sem partidas pode ser removida.
- [ ] Uma equipe vinculada a uma partida não pode ser removida.
- [ ] A geração de turno único cria `n * (n - 1) / 2` partidas.
- [ ] Nenhuma equipe enfrenta a si mesma.
- [ ] Nenhum par de equipes aparece duas vezes.
- [ ] Uma partida sem placar é contada como pendente.
- [ ] Registrar um placar válido transforma a partida em realizada.
- [ ] Placar com texto inválido, valor negativo ou valor não inteiro é rejeitado.
- [ ] A tela inicial atualiza total, realizadas e pendentes.
- [ ] A classificação abre em uma tela independente.
- [ ] Os dados continuam disponíveis após fechar e abrir o programa, por meio do JSON.
- [ ] O arquivo JSON contém equipes, partidas, rodadas e placares (incluindo `null` para partidas pendentes).
- [ ] A classificação apresenta pontos e estatísticas corretos.
- [ ] Os critérios de desempate são respeitados.
- [ ] Atualizar a classificação várias vezes não duplica estatísticas.
- [ ] A navegação entre Início, Equipes, Partidas e Classificação funciona sem travamentos.

---

# 14. Orientações para usar o Claude Code como tutor de programação

O objetivo é que o Claude Code ajude a desenvolver a parte do colega **lado a lado**, explicando o raciocínio e não apenas entregando arquivos prontos.

Instruções sugeridas para o Claude Code:

1. Leia este documento inteiro antes de sugerir alterações.
2. Respeite a divisão de responsabilidades e a estrutura de pastas.
3. Trabalhe principalmente nas partes atribuídas ao colega:
   - `models/campeonato.py`;
   - `main.py`;
   - `views/inicio.py`;
   - `views/classificacao.py`.
   - `storage/repositorio_json.py`, somente após confirmar que essa responsabilidade ficará com o colega.
4. Não implemente as partes atribuídas a Vitor, salvo se for necessário criar um mock temporário para testes. Não sobrescreva os arquivos dele.
5. Antes de codificar, confira os arquivos que já existem no projeto. Não presuma que estejam vazios.
6. Não altere silenciosamente o contrato das classes `Equipe` e `Partida`. Se encontrar incompatibilidade ou falta de método, explique o problema e proponha uma alteração para aprovação antes de modificar a interface.
7. Desenvolva uma etapa por vez. Explique o que será feito, por que será feito e como testar.
8. Prefira exemplos pequenos e código simples, adequado a um projeto acadêmico introdutório de POO.
9. Não acrescente bibliotecas, banco de dados SQL, autenticação ou funcionalidades fora do escopo sem autorização. A persistência definida é JSON.
10. Após cada etapa, execute ou proponha testes objetivos e explique os resultados.
11. Preserve o código já existente. Não apague nem reescreva arquivos sem necessidade e sem explicar o motivo.
12. Se houver mais de uma solução, apresente a opção mais simples e explique brevemente as alternativas.
13. Ao terminar cada etapa, informe quais arquivos foram criados ou modificados, o que foi implementado e qual é o próximo passo.

**Primeira solicitação ao Claude Code:**

> Analise a estrutura atual do projeto e este documento. Não altere nenhum arquivo ainda. Primeiro, apresente um diagnóstico da estrutura existente, identifique o que já está implementado e aponte incompatibilidades com o contrato atualizado. Verifique especialmente a integração de `Campeonato` com `Equipe` e `Partida`, o atributo `rodada`, a geração de partidas pendentes, a tela independente de classificação e a persistência JSON. Não invente nem altere assinaturas compartilhadas sem sinalizar. Depois, proponha uma sequência de implementação da minha parte, começando pela classe `Campeonato`, para que possamos desenvolver e testar cada etapa juntos.

---

# 15. Resumo da arquitetura

```text
main.py
  |
  +-- App
       |
       +-- Campeonato  <---- fonte central dos dados e regras
       |     |
       |     +-- lista de Equipe
       |     |
       |     +-- lista de Partida
       |     |
       |     +-- cálculo da classificação
       |
       +-- TelaInicio
       |     +-- nome do campeonato
       |     +-- quantidade de equipes
       |     +-- total de partidas
       |     +-- realizadas e pendentes
       |     +-- navegação
       |
       +-- TelaEquipes (Vitor)
       |
       +-- TelaPartidas (Vitor)
       |
       +-- TelaClassificacao

storage/repositorio_json.py
  +-- salva e carrega o estado do Campeonato em data/campeonato.json
```

**Ideia central:** `Campeonato` coordena as entidades e as regras. As telas consultam e chamam essa classe para executar operações. A interface não deve duplicar a lógica de cadastro, partidas ou classificação. O repositório JSON cuida da persistência, sem misturar leitura e gravação de arquivos com as regras de negócio.


---

# 16. Nota de sincronização entre os integrantes

Esta versão substitui a versão anterior da especificação. Ela registra as decisões confirmadas pela equipe nesta revisão: geração automática dos confrontos, partidas inicialmente pendentes, atributo `rodada`, persistência em JSON e tela independente de classificação.

Antes de começar a implementação compartilhada, Vitor e o colega devem conferir se os arquivos `models/equipe.py` e `models/partida.py` seguem as propriedades e assinaturas deste documento. Em especial, confirmem a assinatura final de `Partida` e quem ficará responsável pelo repositório JSON. O Claude Code deve primeiro analisar o projeto existente e não sobrescrever código do colega.
