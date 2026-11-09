"""Fase 1: repositório de InscricaoWorkshop em memória (dict)."""
import copy

from repositories.erros import RegistroDuplicadoError


class InscricaoRepositoryMemory:
    def __init__(self):
        self._registros = {}
        self._proximo_id = 1

    def _garantir_par_unico(self, inscricao):
        for existente in self._registros.values():
            if (
                existente.id_participante == inscricao.id_participante
                and existente.id_workshop == inscricao.id_workshop
                and existente.id_inscricao != inscricao.id_inscricao
            ):
                raise RegistroDuplicadoError(
                    "O participante já está inscrito neste workshop."
                )

    def save(self, inscricao):
        self._garantir_par_unico(inscricao)
        inscricao.id_inscricao = self._proximo_id
        self._proximo_id += 1
        self._registros[inscricao.id_inscricao] = copy.copy(inscricao)
        return inscricao

    def get_all(self):
        return [copy.copy(i) for i in self._registros.values()]

    def find_by_id(self, id_inscricao):
        encontrado = self._registros.get(id_inscricao)
        return copy.copy(encontrado) if encontrado else None

    def update(self, inscricao):
        if inscricao.id_inscricao not in self._registros:
            return False
        self._garantir_par_unico(inscricao)
        self._registros[inscricao.id_inscricao] = copy.copy(inscricao)
        return True

    def delete(self, id_inscricao):
        return self._registros.pop(id_inscricao, None) is not None

    # --- consultas auxiliares (mesmos nomes no repositório SQL) ---
    def find_by_workshop(self, id_workshop):
        return [
            copy.copy(i) for i in self._registros.values() if i.id_workshop == id_workshop
        ]

    def find_by_participante(self, id_participante):
        return [
            copy.copy(i)
            for i in self._registros.values()
            if i.id_participante == id_participante
        ]

    def count_by_workshop(self, id_workshop):
        return sum(1 for i in self._registros.values() if i.id_workshop == id_workshop)
