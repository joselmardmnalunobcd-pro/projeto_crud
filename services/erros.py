"""Exceções das regras de negócio."""


class RegraNegocioError(Exception):
    """Violação de uma regra de negócio."""


class VagasEsgotadasError(RegraNegocioError):
    """O workshop já atingiu o limite de vagas."""
