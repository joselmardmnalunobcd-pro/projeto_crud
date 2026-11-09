"""Relatórios analíticos (delegam o cálculo ao repositório de relatórios)."""


class RelatorioService:
    def __init__(self, relatorio_repo):
        self._relatorios = relatorio_repo

    def taxa_ocupacao_por_workshop(self):
        return self._relatorios.taxa_ocupacao_por_workshop()

    def media_notas_por_workshop(self):
        return self._relatorios.media_notas_por_workshop()
