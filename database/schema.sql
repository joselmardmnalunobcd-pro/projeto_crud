-- EventFlow: script DDL (SQLite)
-- Pode ser executado várias vezes (IF NOT EXISTS).

CREATE TABLE IF NOT EXISTS participante (
    id_participante INTEGER PRIMARY KEY AUTOINCREMENT,
    nome            TEXT NOT NULL CHECK (length(trim(nome)) > 0),
    cpf             TEXT NOT NULL UNIQUE CHECK (length(cpf) = 11),
    instituicao     TEXT NOT NULL CHECK (length(trim(instituicao)) > 0),
    email           TEXT NOT NULL CHECK (email LIKE '%_@_%._%')
);

CREATE TABLE IF NOT EXISTS workshop (
    id_workshop   INTEGER PRIMARY KEY AUTOINCREMENT,
    tema          TEXT    NOT NULL CHECK (length(trim(tema)) > 0),
    carga_horaria INTEGER NOT NULL CHECK (carga_horaria > 0),
    vagas_limite  INTEGER NOT NULL CHECK (vagas_limite > 0),
    instrutor     TEXT    NOT NULL CHECK (length(trim(instrutor)) > 0)
);

-- Entidade associativa (N:N entre participante e workshop) com atributos próprios.
CREATE TABLE IF NOT EXISTS inscricao_workshop (
    id_inscricao        INTEGER PRIMARY KEY AUTOINCREMENT,
    id_participante     INTEGER NOT NULL,
    id_workshop         INTEGER NOT NULL,
    data_inscricao      TEXT    NOT NULL,
    percentual_presenca REAL    NOT NULL DEFAULT 0
                        CHECK (percentual_presenca BETWEEN 0 AND 100),
    nota_avaliacao      REAL
                        CHECK (nota_avaliacao IS NULL OR nota_avaliacao BETWEEN 0 AND 10),
    UNIQUE (id_participante, id_workshop),
    FOREIGN KEY (id_participante) REFERENCES participante (id_participante)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_workshop) REFERENCES workshop (id_workshop)
        ON DELETE RESTRICT ON UPDATE CASCADE
);

-- Última barreira da regra de fronteira: impede inscrição quando o total de
-- inscritos já atingiu vagas_limite (a camada de serviço valida antes).
CREATE TRIGGER IF NOT EXISTS trg_inscricao_limite_vagas
BEFORE INSERT ON inscricao_workshop
WHEN (SELECT COUNT(*) FROM inscricao_workshop WHERE id_workshop = NEW.id_workshop)
     >= (SELECT vagas_limite FROM workshop WHERE id_workshop = NEW.id_workshop)
BEGIN
    SELECT RAISE(ABORT, 'Vagas esgotadas para este workshop.');
END;
