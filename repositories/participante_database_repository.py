"""Fase 2: repositório de Participante em banco de dados (SQL)."""
from models.participante import Participante
from repositories.base_sql import executar_escrita

_COLUNAS = "id_participante, nome, cpf, instituicao, email"


def _para_objeto(linha):
    return Participante(
        nome=linha["nome"],
        cpf=linha["cpf"],
        instituicao=linha["instituicao"],
        email=linha["email"],
        id_participante=linha["id_participante"],
    )


class ParticipanteRepositorySQL:
    def __init__(self, conexao):
        self._conexao = conexao

    def save(self, participante):
        cursor = executar_escrita(
            self._conexao,
            "INSERT INTO participante (nome, cpf, instituicao, email) VALUES (?, ?, ?, ?)",
            (participante.nome, participante.cpf, participante.instituicao, participante.email),
        )
        participante.id_participante = cursor.lastrowid
        return participante

    def get_all(self):
        linhas = self._conexao.execute(
            f"SELECT {_COLUNAS} FROM participante ORDER BY id_participante"
        ).fetchall()
        return [_para_objeto(linha) for linha in linhas]

    def find_by_id(self, id_participante):
        linha = self._conexao.execute(
            f"SELECT {_COLUNAS} FROM participante WHERE id_participante = ?",
            (id_participante,),
        ).fetchone()
        return _para_objeto(linha) if linha else None

    def update(self, participante):
        cursor = executar_escrita(
            self._conexao,
            "UPDATE participante SET nome = ?, cpf = ?, instituicao = ?, email = ? "
            "WHERE id_participante = ?",
            (
                participante.nome,
                participante.cpf,
                participante.instituicao,
                participante.email,
                participante.id_participante,
            ),
        )
        return cursor.rowcount > 0

    def delete(self, id_participante):
        cursor = executar_escrita(
            self._conexao,
            "DELETE FROM participante WHERE id_participante = ?",
            (id_participante,),
        )
        return cursor.rowcount > 0
