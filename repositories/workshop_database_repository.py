"""Fase 2: repositório de Workshop em banco de dados (SQL)."""
from models.workshop import Workshop
from repositories.base_sql import executar_escrita

_COLUNAS = "id_workshop, tema, carga_horaria, vagas_limite, instrutor"


def _para_objeto(linha):
    return Workshop(
        tema=linha["tema"],
        carga_horaria=linha["carga_horaria"],
        vagas_limite=linha["vagas_limite"],
        instrutor=linha["instrutor"],
        id_workshop=linha["id_workshop"],
    )


class WorkshopRepositorySQL:
    def __init__(self, conexao):
        self._conexao = conexao

    def save(self, workshop):
        cursor = executar_escrita(
            self._conexao,
            "INSERT INTO workshop (tema, carga_horaria, vagas_limite, instrutor) "
            "VALUES (?, ?, ?, ?)",
            (workshop.tema, workshop.carga_horaria, workshop.vagas_limite, workshop.instrutor),
        )
        workshop.id_workshop = cursor.lastrowid
        return workshop

    def get_all(self):
        linhas = self._conexao.execute(
            f"SELECT {_COLUNAS} FROM workshop ORDER BY id_workshop"
        ).fetchall()
        return [_para_objeto(linha) for linha in linhas]

    def find_by_id(self, id_workshop):
        linha = self._conexao.execute(
            f"SELECT {_COLUNAS} FROM workshop WHERE id_workshop = ?", (id_workshop,)
        ).fetchone()
        return _para_objeto(linha) if linha else None

    def update(self, workshop):
        cursor = executar_escrita(
            self._conexao,
            "UPDATE workshop SET tema = ?, carga_horaria = ?, vagas_limite = ?, "
            "instrutor = ? WHERE id_workshop = ?",
            (
                workshop.tema,
                workshop.carga_horaria,
                workshop.vagas_limite,
                workshop.instrutor,
                workshop.id_workshop,
            ),
        )
        return cursor.rowcount > 0

    def delete(self, id_workshop):
        cursor = executar_escrita(
            self._conexao, "DELETE FROM workshop WHERE id_workshop = ?", (id_workshop,)
        )
        return cursor.rowcount > 0
