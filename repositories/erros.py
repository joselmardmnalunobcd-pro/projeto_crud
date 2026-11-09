"""Exceções da camada de repositório (iguais para memória e SQL)."""
import sqlite3


class RepositorioError(Exception):
    """Erro genérico de persistência."""


class RegistroDuplicadoError(RepositorioError):
    """Violação de unicidade (ex.: CPF repetido, inscrição repetida)."""


class IntegridadeReferencialError(RepositorioError):
    """Violação de chave estrangeira (registro inexistente ou em uso)."""


def traduzir_erro_integridade(erro: sqlite3.IntegrityError):
    mensagem = str(erro)
    if "UNIQUE" in mensagem:
        return RegistroDuplicadoError(
            "Já existe um registro com esses dados únicos (ex.: CPF ou inscrição repetida)."
        )
    if "FOREIGN KEY" in mensagem:
        return IntegridadeReferencialError(
            "Operação viola a integridade referencial (registro relacionado inexistente ou em uso)."
        )
    return RepositorioError(f"Violação de restrição do banco: {mensagem}")
