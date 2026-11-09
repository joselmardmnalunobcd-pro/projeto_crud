"""Fase 1: repositório de Participante em memória (dict)."""
import copy

from repositories.erros import RegistroDuplicadoError


class ParticipanteRepositoryMemory:
    def __init__(self):
        self._registros = {}
        self._proximo_id = 1

    def _garantir_cpf_unico(self, participante):
        for existente in self._registros.values():
            if (
                existente.cpf == participante.cpf
                and existente.id_participante != participante.id_participante
            ):
                raise RegistroDuplicadoError("Já existe um participante com este CPF.")

    def save(self, participante):
        self._garantir_cpf_unico(participante)
        participante.id_participante = self._proximo_id
        self._proximo_id += 1
        self._registros[participante.id_participante] = copy.copy(participante)
        return participante

    def get_all(self):
        return [copy.copy(p) for p in self._registros.values()]

    def find_by_id(self, id_participante):
        encontrado = self._registros.get(id_participante)
        return copy.copy(encontrado) if encontrado else None

    def update(self, participante):
        if participante.id_participante not in self._registros:
            return False
        self._garantir_cpf_unico(participante)
        self._registros[participante.id_participante] = copy.copy(participante)
        return True

    def delete(self, id_participante):
        return self._registros.pop(id_participante, None) is not None
