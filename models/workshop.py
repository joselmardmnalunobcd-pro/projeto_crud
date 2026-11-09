"""Entidade Workshop."""
from models.validacoes import inteiro_positivo, texto_obrigatorio


class Workshop:
    def __init__(self, tema, carga_horaria, vagas_limite, instrutor, id_workshop=None):
        self.id_workshop = id_workshop
        self.tema = tema
        self.carga_horaria = carga_horaria
        self.vagas_limite = vagas_limite
        self.instrutor = instrutor

    @property
    def tema(self):
        return self._tema

    @tema.setter
    def tema(self, valor):
        self._tema = texto_obrigatorio(valor, "tema")

    @property
    def carga_horaria(self):
        return self._carga_horaria

    @carga_horaria.setter
    def carga_horaria(self, valor):
        self._carga_horaria = inteiro_positivo(valor, "carga_horaria")

    @property
    def vagas_limite(self):
        return self._vagas_limite

    @vagas_limite.setter
    def vagas_limite(self, valor):
        self._vagas_limite = inteiro_positivo(valor, "vagas_limite")

    @property
    def instrutor(self):
        return self._instrutor

    @instrutor.setter
    def instrutor(self, valor):
        self._instrutor = texto_obrigatorio(valor, "instrutor")

    def vagas_disponiveis(self, inscritos):
        return max(self._vagas_limite - inscritos, 0)

    def tem_vaga(self, inscritos):
        return inscritos < self._vagas_limite

    def taxa_ocupacao(self, inscritos):
        """Percentual de vagas ocupadas (0 a 100)."""
        return round(inscritos * 100 / self._vagas_limite, 2)

    def __str__(self):
        return (
            f"[{self.id_workshop}] {self.tema} | {self.carga_horaria}h | "
            f"{self.vagas_limite} vagas | Instrutor: {self.instrutor}"
        )
