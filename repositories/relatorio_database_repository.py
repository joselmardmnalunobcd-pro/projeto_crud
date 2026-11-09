"""Fase 2: relatórios analíticos em SQL (JOIN + COUNT/AVG + GROUP BY)."""

_SQL_OCUPACAO = """
SELECT w.id_workshop,
       w.tema,
       w.vagas_limite,
       COUNT(i.id_inscricao) AS inscritos,
       ROUND(COUNT(i.id_inscricao) * 100.0 / w.vagas_limite, 2) AS taxa_ocupacao
FROM workshop AS w
LEFT JOIN inscricao_workshop AS i ON i.id_workshop = w.id_workshop
GROUP BY w.id_workshop, w.tema, w.vagas_limite
ORDER BY taxa_ocupacao DESC, w.tema
"""

_SQL_MEDIA_NOTAS = """
SELECT w.id_workshop,
       w.tema,
       COUNT(i.nota_avaliacao) AS avaliacoes,
       ROUND(AVG(i.nota_avaliacao), 2) AS media_notas
FROM workshop AS w
LEFT JOIN inscricao_workshop AS i ON i.id_workshop = w.id_workshop
GROUP BY w.id_workshop, w.tema
ORDER BY (AVG(i.nota_avaliacao) IS NULL), AVG(i.nota_avaliacao) DESC, w.tema
"""


class RelatorioRepositorySQL:
    def __init__(self, conexao):
        self._conexao = conexao

    def taxa_ocupacao_por_workshop(self):
        return [dict(linha) for linha in self._conexao.execute(_SQL_OCUPACAO).fetchall()]

    def media_notas_por_workshop(self):
        return [dict(linha) for linha in self._conexao.execute(_SQL_MEDIA_NOTAS).fetchall()]
