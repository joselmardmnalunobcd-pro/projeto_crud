"""Entidade associativa InscricaoWorkshop (Participante N:N Workshop)."""
from datetime import date

from models.validacoes import data_valida, inteiro_positivo, numero_no_intervalo


class InscricaoWorkshop:
    def __init__(
        self,
        id_participante,
        id_workshop,
        data_inscricao=None,
        percentual_presenca=0.0,
        nota_avaliacao=None,
        id_inscricao=None,
    ):
        self.id_inscricao = id_inscricao
        self.id_participante = id_participante
        self.id_workshop = id_workshop
        self.data_inscricao = date.today() if data_inscricao is None else data_inscricao
        self.percentual_presenca = percentual_presenca
        self.nota_avaliacao = nota_avaliacao

    @property
    def id_participante(self):
        return self._id_participante

    @id_participante.setter
    def id_participante(self, valor):
        self._id_participante = inteiro_positivo(valor, "id_participante")

    @property
    def id_workshop(self):
        return self._id_workshop

    @id_workshop.setter
    def id_workshop(self, valor):
        self._id_workshop = inteiro_positivo(valor, "id_workshop")

    @property
    def data_inscricao(self):
        return self._data_inscricao

    @data_inscricao.setter
    def data_inscricao(self, valor):
        self._data_inscricao = data_valida(valor)

    @property
    def percentual_presenca(self):
        return self._percentual_presenca

    @percentual_presenca.setter
    def percentual_presenca(self, valor):
        self._percentual_presenca = numero_no_intervalo(
            valor, "percentual_presenca", 0, 100
        )

    @property
    def nota_avaliacao(self):
        return self._nota_avaliacao

    @nota_avaliacao.setter
    def nota_avaliacao(self, valor):
        if valor is None:
            self._nota_avaliacao = None
        else:
            self._nota_avaliacao = numero_no_intervalo(valor, "nota_avaliacao", 0, 10)

    def registrar_presenca(self, percentual):
        self.percentual_presenca = percentual

    def registrar_avaliacao(self, nota):
        self.nota_avaliacao = nota

    def __str__(self):
        nota = "sem nota" if self.nota_avaliacao is None else f"{self.nota_avaliacao:.1f}"
        return (
            f"[{self.id_inscricao}] participante {self.id_participante} -> "
            f"workshop {self.id_workshop} | {self.data_inscricao:%d/%m/%Y} | "
            f"presença {self.percentual_presenca:.0f}% | {nota}"
        )
