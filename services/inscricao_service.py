"""Regras de negócio de InscricaoWorkshop."""
from models.inscricao_workshop import InscricaoWorkshop
from services.erros import RegraNegocioError, VagasEsgotadasError


class InscricaoService:
    def __init__(self, inscricao_repo, participante_repo, workshop_repo):
        self._inscricoes = inscricao_repo
        self._participantes = participante_repo
        self._workshops = workshop_repo

    def inscrever(self, id_participante, id_workshop, data_inscricao=None):
        """Inscreve o participante, respeitando o limite de vagas do workshop."""
        if self._participantes.find_by_id(id_participante) is None:
            raise RegraNegocioError("Participante não encontrado.")
        workshop = self._workshops.find_by_id(id_workshop)
        if workshop is None:
            raise RegraNegocioError("Workshop não encontrado.")

        ja_inscritos = self._inscricoes.find_by_workshop(id_workshop)
        if any(i.id_participante == id_participante for i in ja_inscritos):
            raise RegraNegocioError("O participante já está inscrito neste workshop.")

        # Fronteira de vagas: com inscritos == vagas_limite, a inscrição é barrada.
        if len(ja_inscritos) >= workshop.vagas_limite:
            raise VagasEsgotadasError(
                f"Vagas esgotadas: '{workshop.tema}' já tem "
                f"{len(ja_inscritos)}/{workshop.vagas_limite} inscritos."
            )

        inscricao = InscricaoWorkshop(id_participante, id_workshop, data_inscricao)
        return self._inscricoes.save(inscricao)

    def listar(self):
        return self._inscricoes.get_all()

    def listar_detalhado(self):
        """Inscrições com o nome do participante e o tema do workshop."""
        detalhadas = []
        for inscricao in self._inscricoes.get_all():
            participante = self._participantes.find_by_id(inscricao.id_participante)
            workshop = self._workshops.find_by_id(inscricao.id_workshop)
            detalhadas.append(
                {
                    "id_inscricao": inscricao.id_inscricao,
                    "participante": participante.nome if participante else "?",
                    "workshop": workshop.tema if workshop else "?",
                    "data_inscricao": inscricao.data_inscricao,
                    "percentual_presenca": inscricao.percentual_presenca,
                    "nota_avaliacao": inscricao.nota_avaliacao,
                }
            )
        return detalhadas

    def buscar(self, id_inscricao):
        inscricao = self._inscricoes.find_by_id(id_inscricao)
        if inscricao is None:
            raise RegraNegocioError("Inscrição não encontrada.")
        return inscricao

    def registrar_presenca(self, id_inscricao, percentual):
        inscricao = self.buscar(id_inscricao)
        inscricao.registrar_presenca(percentual)
        self._inscricoes.update(inscricao)
        return inscricao

    def registrar_avaliacao(self, id_inscricao, nota):
        inscricao = self.buscar(id_inscricao)
        inscricao.registrar_avaliacao(nota)
        self._inscricoes.update(inscricao)
        return inscricao

    def cancelar(self, id_inscricao):
        self.buscar(id_inscricao)
        return self._inscricoes.delete(id_inscricao)
