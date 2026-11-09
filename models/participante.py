"""Entidade Participante."""
from models.validacoes import cpf_valido, email_valido, texto_obrigatorio


class Participante:
    def __init__(self, nome, cpf, instituicao, email, id_participante=None):
        self.id_participante = id_participante
        self.nome = nome
        self.cpf = cpf
        self.instituicao = instituicao
        self.email = email

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, valor):
        self._nome = texto_obrigatorio(valor, "nome")

    @property
    def cpf(self):
        return self._cpf

    @cpf.setter
    def cpf(self, valor):
        self._cpf = cpf_valido(valor)

    @property
    def instituicao(self):
        return self._instituicao

    @instituicao.setter
    def instituicao(self, valor):
        self._instituicao = texto_obrigatorio(valor, "instituicao")

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, valor):
        self._email = email_valido(valor)

    def cpf_formatado(self):
        c = self._cpf
        return f"{c[:3]}.{c[3:6]}.{c[6:9]}-{c[9:]}"

    def __str__(self):
        return (
            f"[{self.id_participante}] {self.nome} | CPF {self.cpf_formatado()} | "
            f"{self.instituicao} | {self.email}"
        )
