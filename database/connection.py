"""Criação da conexão com o banco de dados (SQLite)."""
import sqlite3
from pathlib import Path

PASTA = Path(__file__).resolve().parent
CAMINHO_BANCO = PASTA / "eventflow.db"
CAMINHO_SCHEMA = PASTA / "schema.sql"


def criar_conexao(caminho=None):
    """Abre a conexão, ativa as chaves estrangeiras e garante que o schema exista.

    Use ":memory:" como caminho para um banco temporário (útil nos testes).
    """
    conexao = sqlite3.connect(str(caminho or CAMINHO_BANCO))
    conexao.row_factory = sqlite3.Row
    conexao.execute("PRAGMA foreign_keys = ON")
    conexao.executescript(CAMINHO_SCHEMA.read_text(encoding="utf-8"))
    return conexao
