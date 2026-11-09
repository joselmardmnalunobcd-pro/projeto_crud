"""Fase 1: relatórios analíticos calculados em Python sobre as coleções em memória."""


class RelatorioRepositoryMemory:
    def __init__(self, workshop_repo, inscricao_repo):
        self._workshop_repo = workshop_repo
        self._inscricao_repo = inscricao_repo

    def taxa_ocupacao_por_workshop(self):
        linhas = []
        for workshop in self._workshop_repo.get_all():
            inscritos = self._inscricao_repo.count_by_workshop(workshop.id_workshop)
            linhas.append(
                {
                    "id_workshop": workshop.id_workshop,
                    "tema": workshop.tema,
                    "vagas_limite": workshop.vagas_limite,
                    "inscritos": inscritos,
                    "taxa_ocupacao": workshop.taxa_ocupacao(inscritos),
                }
            )
        return sorted(linhas, key=lambda l: (-l["taxa_ocupacao"], l["tema"]))

    def media_notas_por_workshop(self):
        linhas = []
        for workshop in self._workshop_repo.get_all():
            notas = [
                i.nota_avaliacao
                for i in self._inscricao_repo.find_by_workshop(workshop.id_workshop)
                if i.nota_avaliacao is not None
            ]
            media = round(sum(notas) / len(notas), 2) if notas else None
            linhas.append(
                {
                    "id_workshop": workshop.id_workshop,
                    "tema": workshop.tema,
                    "avaliacoes": len(notas),
                    "media_notas": media,
                }
            )
        return sorted(
            linhas,
            key=lambda l: (l["media_notas"] is None, -(l["media_notas"] or 0), l["tema"]),
        )
