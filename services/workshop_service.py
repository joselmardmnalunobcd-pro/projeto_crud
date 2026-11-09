"""Regras de negócio de Workshop."""
from models.workshop import Workshop
from services.erros import RegraNegocioError


class WorkshopService:
    def __init__(self, workshop_repo, inscricao_repo):
        self._workshops = workshop_repo
        self._inscricoes = inscricao_repo

    def cadastrar(self, tema, carga_horaria, vagas_limite, instrutor):
        return self._workshops.save(Workshop(tema, carga_horaria, vagas_limite, instrutor))

    def listar(self):
        return self._workshops.get_all()

    def listar_com_ocupacao(self):
        """Lista de tuplas (workshop, total_de_inscritos)."""
        return [
            (w, self._inscricoes.count_by_workshop(w.id_workshop))
            for w in self._workshops.get_all()
        ]

    def buscar(self, id_workshop):
        workshop = self._workshops.find_by_id(id_workshop)
        if workshop is None:
            raise RegraNegocioError("Workshop não encontrado.")
        return workshop

    def atualizar(
        self, id_workshop, tema=None, carga_horaria=None, vagas_limite=None, instrutor=None
    ):
        workshop = self.buscar(id_workshop)
        if tema is not None:
            workshop.tema = tema
        if carga_horaria is not None:
            workshop.carga_horaria = carga_horaria
        if instrutor is not None:
            workshop.instrutor = instrutor
        if vagas_limite is not None:
            workshop.vagas_limite = vagas_limite
            inscritos = self._inscricoes.count_by_workshop(id_workshop)
            if workshop.vagas_limite < inscritos:
                raise RegraNegocioError(
                    f"O novo limite ({workshop.vagas_limite}) é menor que o número "
                    f"de inscritos atuais ({inscritos})."
                )
        self._workshops.update(workshop)
        return workshop

    def remover(self, id_workshop):
        self.buscar(id_workshop)
        if self._inscricoes.count_by_workshop(id_workshop) > 0:
            raise RegraNegocioError(
                "Não é possível remover: o workshop possui inscrições. "
                "Cancele as inscrições antes."
            )
        return self._workshops.delete(id_workshop)
