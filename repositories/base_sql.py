"""Utilitário comum aos repositórios SQL: escrita com commit/rollback."""
import sqlite3

from repositories.erros import RepositorioError, traduzir_erro_integridade


def executar_escrita(conexao, sql, parametros=()):
    """Executa INSERT/UPDATE/DELETE com gestão de transação (commit e rollback)."""
    try:
        cursor = conexao.execute(sql, parametros)
        conexao.commit()
        return cursor
    except sqlite3.IntegrityError as erro:
        conexao.rollback()
        raise traduzir_erro_integridade(erro) from erro
    except sqlite3.Error as erro:
        conexao.rollback()
        raise RepositorioError(f"Erro no banco de dados: {erro}") from erro
