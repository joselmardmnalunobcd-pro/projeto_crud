"""Regras de negócio de Participante."""
from models.participante import Participante
from services.erros import RegraNegocioError


class ParticipanteService:
    def __init__(self, participante_repo, inscricao_repo):
        self._participantes = participante_repo
        self._inscricoes = inscricao_repo

    def cadastrar(self, nome, cpf, instituicao, email):
        return self._participantes.save(Participante(nome, cpf, instituicao, email))

    def listar(self):
        return self._participantes.get_all()

    def buscar(self, id_participante):
        participante = self._participantes.find_by_id(id_participante)
        if participante is None:
            raise RegraNegocioError("Participante não encontrado.")
        return participante

    def atualizar(self, id_participante, nome=None, cpf=None, instituicao=None, email=None):
        participante = self.buscar(id_participante)
        if nome is not None:
            participante.nome = nome
        if cpf is not None:
            participante.cpf = cpf
        if instituicao is not None:
            participante.instituicao = instituicao
        if email is not None:
            participante.email = email
        self._participantes.update(participante)
        return participante

    def remover(self, id_participante):
        self.buscar(id_participante)
        if self._inscricoes.find_by_participante(id_participante):
            raise RegraNegocioError(
                "Não é possível remover: o participante possui inscrições. "
                "Cancele as inscrições antes."
            )
        return self._participantes.delete(id_participante)
