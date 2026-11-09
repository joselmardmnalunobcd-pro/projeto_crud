"""Fase 1: repositório de Workshop em memória (dict)."""
import copy


class WorkshopRepositoryMemory:
    def __init__(self):
        self._registros = {}
        self._proximo_id = 1

    def save(self, workshop):
        workshop.id_workshop = self._proximo_id
        self._proximo_id += 1
        self._registros[workshop.id_workshop] = copy.copy(workshop)
        return workshop

    def get_all(self):
        return [copy.copy(w) for w in self._registros.values()]

    def find_by_id(self, id_workshop):
        encontrado = self._registros.get(id_workshop)
        return copy.copy(encontrado) if encontrado else None

    def update(self, workshop):
        if workshop.id_workshop not in self._registros:
            return False
        self._registros[workshop.id_workshop] = copy.copy(workshop)
        return True

    def delete(self, id_workshop):
        return self._registros.pop(id_workshop, None) is not None
