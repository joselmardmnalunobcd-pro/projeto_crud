# Projeto Profissional: Aplicação CRUD com Arquitetura em Camadas e Persistência de Dados

**Disciplina:** Estruturação, Modelagem e Persistência de Dados  
**Curso:** Engenharia de Software  
**Docente:** Prof. Renan Felipe Brito Dantas  

---

## 1. Visão Geral do Projeto

Este projeto tem como objetivo consolidar competências em **Engenharia de Software**, **Programação Orientada a Objetos (POO)** e **Estrutura de Dados**. As equipes desenvolverão uma aplicação completa de linha de comando (CLI) baseada nas operações fundamentais de **CRUD** (*Create, Read, Update, Delete*).

A evolução técnica do software ocorrerá em duas fases pedagógicas estratégicas:
1. **Fase 1 (Coleções em Memória):** Implementação inicial estruturada em memória volátil através de coleções nativas do Python (`list`, `dict`), com forte aplicação do padrão arquitetural **Repository Pattern** para abstração da fonte de dados.
2. **Fase 2 (Persistência em Banco de Dados Relacional):** Migração transparente do armazenamento para um SGBD relacional via linguagem SQL (DDL e DML), demonstrando a eficácia do baixo acoplamento obtido com a camada de repositório.

> **Atenção:** A especificação do domínio de negócio de cada equipe (entidades específicas, atributos, minimundo e regras de negócio obrigatórias) está documentada na pasta compartilhada da turma no Google Drive.

---

## 2. Escopo do Domínio e Entidades

Cada projeto deverá contemplar **pelo menos 3 entidades de domínio correlacionadas**, contendo:
* Entidades Fortes e Fracas;
* Relacionamentos do tipo $1:N$ e pelo menos um relacionamento $N:N$ resolvido por uma Entidade Associativa com atributos próprios;
* Chaves identificadoras claras (Chave Primária - PK e Chave Estrangeira - FK).

---

## 3. Arquitetura e Padrões de Software

O código deve seguir estritamente o princípio da **Separação de Responsabilidades (SoC)**, organizado na seguinte estrutura em pacotes:

```text
projeto_crud/
│
├── database/
│   ├── connection.py                # Criação da conexão com o banco de dados
│   └── schema.sql                   # Script DDL (CREATE TABLE com constraints)
│
├── models/                          # Classes do domínio (POO com __init__ e atributos)
│   ├── cliente.py
│   ├── veiculo.py
│   └── ...
│
├── repositories/                      # Camada responsável pelo armazenamento e consultas
│   ├── cliente_memory_repository.py   # Fase 1: CRUD manipulando listas e dicionários
│   └── cliente_database_repository.py # Fase 2: CRUD executando comandos SQL
│
├── services/                          # Regras de negócio, cálculos analíticos e validações
│   └── ...
│
│
├── requirements.txt                   # Dependências da aplicação
├── main.py                            # Menu CLI interativo do sistema
└── README.md                          # Documentação do projeto da equipe
```

---

## 4. O Padrão Repository (Convenção de Métodos)

Em vez de bibliotecas complexas de abstração, a turma aplicará o **contrato por convenção**: os repositórios em memória e os repositórios em banco de dados devem possuir **exatamente os mesmos nomes de métodos e parâmetros**.

### Convenção Padrão de Nomenclatura:
* `save(objeto)`: Adiciona um novo registro na coleção ou executa `INSERT INTO`.
* `get_all()`: Retorna todos os registros armazenados.
* `find_by_id(id)`: Retorna a entidade correspondente ou `None` caso não exista.
* `update(objeto)`: Aplica as alterações no registro correspondente.
* `delete(id)`: Exclui o registro com base no identificador (retorna `True` ou `False`).

### A Troca no `main.py`:
Durante a transição da Fase 1 para a Fase 2, a aplicação deve manter seu funcionamento normal apenas alterando a inicialização do repositório:

```python
# --- Fase 1 (Semanas 1 e 2) ---
# cliente_repo = ClienteRepositoryMemory()

# --- Fase 2 (Semanas 3 e 4) ---
conexao = criar_conexao()
cliente_repo = ClienteRepositorySQL(conexao)

# O restante do menu CLI permanece 100% inalterado:
clientes = cliente_repo.get_all()
```

---

## 5. Cronograma de Entregas e Fases

### Fase 1: CRUD em Memória e Padrão Repositório (Semanas 1 e 2)
* Modelagem das entidades em classes (`models/`) com construtor `__init__`, atributos e métodos de domínio.
* Menu CLI interativo (`main.py`) para executar operações completas de CRUD.
* Armazenamento encapsulado nos repositórios em memória (`repositories/memory/`) com listas e dicionários.
* Validações de entrada via `try/except` para impedir valores negativos, campos vazios ou formatos inválidos.

### Fase 2: Persistência em Banco de Dados e Consultas Analíticas (Semanas 3 e 4)
* Criação do script `schema.sql` contendo `CREATE TABLE` com restrições (`PRIMARY KEY`, `FOREIGN KEY`, `NOT NULL`, `UNIQUE`, `CHECK`).
* Implementação dos repositórios SQL (`repositories/sql/`) com comandos DML (`INSERT`, `SELECT`, `UPDATE`, `DELETE`) e gestão de transações (`commit` e `rollback`).
* Transição de repositórios no `main.py` comprovando o desacoplamento arquitetural.
* Implementação de no mínimo **2 relatórios analíticos** utilizando consultas com `JOIN` e funções de agregação (`COUNT`, `SUM`, `AVG`, `GROUP BY`).

---

## 6. Requisitos de Qualidade e Boas Práticas

1. **Robustez de Software:** A aplicação CLI não pode travar ou fechar inesperadamente diante de dados incorretos digitados pelo usuário.
2. **Convenções de Código (PEP 8):** Nomenclatura em `snake_case` para variáveis e funções, `PascalCase` para classes e imports organizados.
3. **Ambiente Virtual:** Execução isolada em `venv` com arquivos dependentes especificados no `requirements.txt`.
4. **Git e Commits Semânticos:** Repositório com contribuições equilibradas e commits objetivos de todos os membros do grupo.

---

## 7. Critérios de Avaliação

| Critério | Peso | Descrição |
| :--- | :---: | :--- |
| **Funcionalidade do CRUD** | 30% | Operações de Create, Read, Update e Delete funcionais em todas as entidades do sistema. |
| **Desacoplamento e Padrão Repository** | 25% | Correta separação entre a interface CLI e a persistência, mantendo métodos padronizados entre memória e SQL. |
| **Modelagem e SQL** | 20% | Aplicação adequada de constraints, integridade referencial, consultas `JOIN` e funções agregadoras. |
| **Robustez e Validação** | 15% | Tratamento defensivo com `try/except`, impedindo encerramentos abruptos e inconsistências nos dados. |
| **Engenharia e PEP 8** | 10% | Organização das pastas, uso de `venv`, commits colaborativos e código limpo. |

---

## 8. Identificação do Grupo

* **Nome do Sistema:** `[EventFlow — Gestão de Congressos e Workshops]`
* **Link da Atividade (Google Drive):** [Propostas de Projetos CRUD - Engenharia de Software](https://docs.google.com/document/d/13PCZjxVaOd-qq50ej_Bu1DkNeEINvOH17ZgtNX_fxKE/edit)
* **Tema Escolhido:** `[EventFlow — Gestão de Congressos e Workshops]`
* **Equipe de Desenvolvimento:**
  - `[Marciano Pereira da Silva]`
  - `[Joselmar Dourado Moitinho Neto]`
