"""Fase 2: repositório de InscricaoWorkshop em banco de dados (SQL)."""
from models.inscricao_workshop import InscricaoWorkshop
from repositories.base_sql import executar_escrita

_COLUNAS = (
    "id_inscricao, id_participante, id_workshop, data_inscricao, "
    "percentual_presenca, nota_avaliacao"
)


def _para_objeto(linha):
    return InscricaoWorkshop(
        id_participante=linha["id_participante"],
        id_workshop=linha["id_workshop"],
        data_inscricao=linha["data_inscricao"],
        percentual_presenca=linha["percentual_presenca"],
        nota_avaliacao=linha["nota_avaliacao"],
        id_inscricao=linha["id_inscricao"],
    )


class InscricaoRepositorySQL:
    def __init__(self, conexao):
        self._conexao = conexao

    def save(self, inscricao):
        cursor = executar_escrita(
            self._conexao,
            "INSERT INTO inscricao_workshop (id_participante, id_workshop, data_inscricao, "
            "percentual_presenca, nota_avaliacao) VALUES (?, ?, ?, ?, ?)",
            (
                inscricao.id_participante,
                inscricao.id_workshop,
                inscricao.data_inscricao.isoformat(),
                inscricao.percentual_presenca,
                inscricao.nota_avaliacao,
            ),
        )
        inscricao.id_inscricao = cursor.lastrowid
        return inscricao

    def get_all(self):
        linhas = self._conexao.execute(
            f"SELECT {_COLUNAS} FROM inscricao_workshop ORDER BY id_inscricao"
        ).fetchall()
        return [_para_objeto(linha) for linha in linhas]

    def find_by_id(self, id_inscricao):
        linha = self._conexao.execute(
            f"SELECT {_COLUNAS} FROM inscricao_workshop WHERE id_inscricao = ?",
            (id_inscricao,),
        ).fetchone()
        return _para_objeto(linha) if linha else None

    def update(self, inscricao):
        cursor = executar_escrita(
            self._conexao,
            "UPDATE inscricao_workshop SET id_participante = ?, id_workshop = ?, "
            "data_inscricao = ?, percentual_presenca = ?, nota_avaliacao = ? "
            "WHERE id_inscricao = ?",
            (
                inscricao.id_participante,
                inscricao.id_workshop,
                inscricao.data_inscricao.isoformat(),
                inscricao.percentual_presenca,
                inscricao.nota_avaliacao,
                inscricao.id_inscricao,
            ),
        )
        return cursor.rowcount > 0

    def delete(self, id_inscricao):
        cursor = executar_escrita(
            self._conexao,
            "DELETE FROM inscricao_workshop WHERE id_inscricao = ?",
            (id_inscricao,),
        )
        return cursor.rowcount > 0

    # --- consultas auxiliares (mesmos nomes no repositório em memória) ---
    def find_by_workshop(self, id_workshop):
        linhas = self._conexao.execute(
            f"SELECT {_COLUNAS} FROM inscricao_workshop WHERE id_workshop = ? "
            "ORDER BY id_inscricao",
            (id_workshop,),
        ).fetchall()
        return [_para_objeto(linha) for linha in linhas]

    def find_by_participante(self, id_participante):
        linhas = self._conexao.execute(
            f"SELECT {_COLUNAS} FROM inscricao_workshop WHERE id_participante = ? "
            "ORDER BY id_inscricao",
            (id_participante,),
        ).fetchall()
        return [_para_objeto(linha) for linha in linhas]

    def count_by_workshop(self, id_workshop):
        linha = self._conexao.execute(
            "SELECT COUNT(*) AS total FROM inscricao_workshop WHERE id_workshop = ?",
            (id_workshop,),
        ).fetchone()
        return linha["total"]
