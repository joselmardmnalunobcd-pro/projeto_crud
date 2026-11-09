# EventFlow

Sistema de linha de comando (CLI) para administrar inscrições em workshops de conferências e simpósios tecnológicos. Projeto de CRUD em Python com POO, Repository Pattern e persistência em banco relacional (SQLite).

## Minimundo

Participantes se inscrevem em workshops temáticos conduzidos por instrutores, registrando presença e avaliação.

## Entidades

| Entidade | Atributos |
|---|---|
| **Participante** | `id_participante` (PK), nome, cpf, instituicao, email |
| **Workshop** | `id_workshop` (PK), tema, carga_horaria, vagas_limite, instrutor |
| **InscricaoWorkshop** (associativa N:N) | `id_inscricao` (PK), `id_participante` (FK), `id_workshop` (FK), data_inscricao, percentual_presenca, nota_avaliacao |

Participante 1:N Inscrição N:1 Workshop (relacionamento N:N resolvido pela entidade associativa).

## Como executar

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt  # sem dependências externas

python main.py             # Fase 2: banco SQLite (database/eventflow.db)
python main.py --memoria   # Fase 1: coleções em memória
```

## Testes

```bash
python -m unittest discover -v
```

Os mesmos testes rodam contra os repositórios em memória **e** contra os repositórios SQL (prova do desacoplamento). Destaque: o teste de fronteira de vagas confirma que a inscrição é barrada quando o total de inscritos atinge `vagas_limite` (e que a última vaga ainda pode ser ocupada).

## Arquitetura

```
eventflow/
├── database/
│   ├── connection.py      # criar_conexao(): SQLite + chaves estrangeiras ativas
│   └── schema.sql         # DDL com PK, FK, NOT NULL, UNIQUE, CHECK e trigger
├── models/                # Classes do domínio com validação nos setters
├── repositories/          # *_memory_repository.py (Fase 1) e *_database_repository.py (Fase 2)
├── services/              # Regras de negócio e relatórios
├── tests/
├── main.py                # Menu CLI interativo
└── requirements.txt
```

### Padrão Repository (contrato por convenção)

Os repositórios de memória e de SQL têm os mesmos métodos e parâmetros: `save(objeto)`, `get_all()`, `find_by_id(id)`, `update(objeto)` e `delete(id)`. O repositório de inscrições também oferece `find_by_workshop`, `find_by_participante` e `count_by_workshop`, e os repositórios de relatório oferecem `taxa_ocupacao_por_workshop()` e `media_notas_por_workshop()`.

A troca da Fase 1 para a Fase 2 acontece apenas na inicialização dos repositórios em `main()`; o menu e os serviços não mudam.

## Regras de negócio

- Não é possível se inscrever em um workshop cujo total de inscritos já atingiu `vagas_limite`. A regra é validada no serviço e reforçada por um trigger no banco.
- Um participante só pode se inscrever uma vez em cada workshop (`UNIQUE` em `id_participante, id_workshop`).
- Não é possível reduzir `vagas_limite` abaixo do número de inscritos.
- Participante ou workshop com inscrições não pode ser removido (cancele as inscrições antes).
- CPF único, com 11 dígitos; e-mail em formato válido.
- Presença entre 0 e 100; nota entre 0 e 10; textos não vazios; números positivos.

## Consultas analíticas (Fase 2)

Ambas usam `JOIN` e funções de agregação (`COUNT`, `AVG`) com `GROUP BY` (ver `repositories/relatorio_database_repository.py`):

1. **Taxa de ocupação de vagas por workshop**: inscritos ÷ `vagas_limite` × 100.
2. **Média das notas de avaliação por workshop**: ignora inscrições ainda sem nota.

## Robustez

Toda ação do menu é executada dentro de `try/except`: entradas inválidas (texto onde se espera número, campo vazio, valor negativo, ID inexistente) mostram uma mensagem de erro e o programa volta ao menu, sem encerrar.

## Equipe

| Integrantes | Contribuição |
|---|---|
| Joselmar Dourado
 Marciano Pereira | _Renan_ |
