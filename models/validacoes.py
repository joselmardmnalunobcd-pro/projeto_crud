"""Funções de validação reutilizadas pelos modelos do domínio."""
import re
from datetime import date, datetime

_EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def texto_obrigatorio(valor, campo):
    """Garante que o valor seja um texto não vazio e devolve-o sem espaços nas pontas."""
    if not isinstance(valor, str) or not valor.strip():
        raise ValueError(f"O campo '{campo}' não pode ser vazio.")
    return valor.strip()


def inteiro_positivo(valor, campo):
    """Converte para int e garante que seja maior que zero."""
    try:
        numero = int(str(valor).strip())
    except (TypeError, ValueError):
        raise ValueError(f"O campo '{campo}' deve ser um número inteiro.") from None
    if numero <= 0:
        raise ValueError(f"O campo '{campo}' deve ser maior que zero.")
    return numero


def numero_no_intervalo(valor, campo, minimo, maximo):
    """Converte para float (aceita vírgula decimal) e valida o intervalo."""
    try:
        numero = float(str(valor).strip().replace(",", "."))
    except (TypeError, ValueError):
        raise ValueError(f"O campo '{campo}' deve ser numérico.") from None
    if not minimo <= numero <= maximo:
        raise ValueError(
            f"O campo '{campo}' deve estar entre {minimo:g} e {maximo:g}."
        )
    return numero


def cpf_valido(valor):
    """Remove a pontuação e exige exatamente 11 dígitos."""
    digitos = re.sub(r"\D", "", str(valor))
    if len(digitos) != 11:
        raise ValueError("O CPF deve conter 11 dígitos.")
    return digitos


def email_valido(valor):
    email = texto_obrigatorio(valor, "email")
    if not _EMAIL_REGEX.match(email):
        raise ValueError("E-mail em formato inválido.")
    return email


def data_valida(valor, campo="data_inscricao"):
    """Aceita date, AAAA-MM-DD ou DD/MM/AAAA."""
    if isinstance(valor, datetime):
        return valor.date()
    if isinstance(valor, date):
        return valor
    texto = str(valor).strip()
    try:
        if "/" in texto:
            return datetime.strptime(texto, "%d/%m/%Y").date()
        return date.fromisoformat(texto)
    except ValueError:
        raise ValueError(
            f"O campo '{campo}' deve estar no formato DD/MM/AAAA ou AAAA-MM-DD."
        ) from None
