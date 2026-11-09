"""Testes do EventFlow, executados contra os dois tipos de repositório.

Rodar a partir da raiz do projeto:
    python -m unittest discover -v
"""
import unittest

from database.connection import criar_conexao
from models.inscricao_workshop import InscricaoWorkshop
from models.participante import Participante
from models.workshop import Workshop
from repositories.erros import (
    IntegridadeReferencialError,
    RegistroDuplicadoError,
    RepositorioError,
)
from repositories.inscricao_database_repository import InscricaoRepositorySQL
from repositories.inscricao_memory_repository import InscricaoRepositoryMemory
from repositories.participante_database_repository import ParticipanteRepositorySQL
from repositories.participante_memory_repository import ParticipanteRepositoryMemory
from repositories.relatorio_database_repository import RelatorioRepositorySQL
from repositories.relatorio_memory_repository import RelatorioRepositoryMemory
from repositories.workshop_database_repository import WorkshopRepositorySQL
from repositories.workshop_memory_repository import WorkshopRepositoryMemory
from services.erros import RegraNegocioError, VagasEsgotadasError
from services.inscricao_service import InscricaoService
from services.participante_service import ParticipanteService
from services.relatorio_service import RelatorioService
from services.workshop_service import WorkshopService


class CenarioBase:
    """Testes de contrato: valem para qualquer implementação de repositório."""

    def criar_repositorios(self):
        raise NotImplementedError

    def setUp(self):
        (
            self.participante_repo,
            self.workshop_repo,
            self.inscricao_repo,
            self.relatorio_repo,
        ) = self.criar_repositorios()
        self.participantes = ParticipanteService(self.participante_repo, self.inscricao_repo)
        self.workshops = WorkshopService(self.workshop_repo, self.inscricao_repo)
        self.inscricoes = InscricaoService(
            self.inscricao_repo, self.participante_repo, self.workshop_repo
        )
        self.relatorios = RelatorioService(self.relatorio_repo)

    def novo_participante(self, n):
        return self.participantes.cadastrar(
            f"Pessoa {n}", f"{n:011d}", "UNIFAN", f"pessoa{n}@email.com"
        )

    def novo_workshop(self, vagas, tema="Python Avançado"):
        return self.workshops.cadastrar(tema, 8, vagas, "Profa. Ana")

    # --- fronteira de vagas (requisito obrigatório) ---
    def test_bloqueia_inscricao_quando_atinge_vagas_limite(self):
        workshop = self.novo_workshop(vagas=2)
        p1, p2, p3 = (self.novo_participante(n) for n in (1, 2, 3))

        self.inscricoes.inscrever(p1.id_participante, workshop.id_workshop)
        self.inscricoes.inscrever(p2.id_participante, workshop.id_workshop)  # última vaga

        with self.assertRaises(VagasEsgotadasError):
            self.inscricoes.inscrever(p3.id_participante, workshop.id_workshop)
        self.assertEqual(self.inscricao_repo.count_by_workshop(workshop.id_workshop), 2)

    def test_ultima_vaga_ainda_pode_ser_ocupada(self):
        workshop = self.novo_workshop(vagas=1)
        p1, p2 = self.novo_participante(1), self.novo_participante(2)

        self.inscricoes.inscrever(p1.id_participante, workshop.id_workshop)
        with self.assertRaises(VagasEsgotadasError):
            self.inscricoes.inscrever(p2.id_participante, workshop.id_workshop)

    def test_cancelamento_libera_vaga(self):
        workshop = self.novo_workshop(vagas=1)
        p1, p2 = self.novo_participante(1), self.novo_participante(2)

        inscricao = self.inscricoes.inscrever(p1.id_participante, workshop.id_workshop)
        self.inscricoes.cancelar(inscricao.id_inscricao)
        self.inscricoes.inscrever(p2.id_participante, workshop.id_workshop)
        self.assertEqual(self.inscricao_repo.count_by_workshop(workshop.id_workshop), 1)

    def test_nao_permite_reduzir_vagas_abaixo_dos_inscritos(self):
        workshop = self.novo_workshop(vagas=3)
        for n in (1, 2):
            p = self.novo_participante(n)
            self.inscricoes.inscrever(p.id_participante, workshop.id_workshop)

        with self.assertRaises(RegraNegocioError):
            self.workshops.atualizar(workshop.id_workshop, vagas_limite=1)
        self.workshops.atualizar(workshop.id_workshop, vagas_limite=2)  # igual: permitido

    # --- outras regras ---
    def test_nao_permite_inscricao_duplicada(self):
        workshop = self.novo_workshop(vagas=5)
        p1 = self.novo_participante(1)
        self.inscricoes.inscrever(p1.id_participante, workshop.id_workshop)
        with self.assertRaises(RegraNegocioError):
            self.inscricoes.inscrever(p1.id_participante, workshop.id_workshop)

    def test_inscricao_com_ids_inexistentes(self):
        workshop = self.novo_workshop(vagas=5)
        p1 = self.novo_participante(1)
        with self.assertRaises(RegraNegocioError):
            self.inscricoes.inscrever(999, workshop.id_workshop)
        with self.assertRaises(RegraNegocioError):
            self.inscricoes.inscrever(p1.id_participante, 999)

    def test_cpf_duplicado_e_rejeitado(self):
        self.novo_participante(1)
        with self.assertRaises(RegistroDuplicadoError):
            self.participantes.cadastrar("Outra", "00000000001", "UNIFAN", "x@y.com")

    def test_nao_remove_workshop_ou_participante_com_inscricoes(self):
        workshop = self.novo_workshop(vagas=5)
        p1 = self.novo_participante(1)
        self.inscricoes.inscrever(p1.id_participante, workshop.id_workshop)
        with self.assertRaises(RegraNegocioError):
            self.workshops.remover(workshop.id_workshop)
        with self.assertRaises(RegraNegocioError):
            self.participantes.remover(p1.id_participante)

    def test_contrato_do_repositorio(self):
        self.assertIsNone(self.participante_repo.find_by_id(123))
        self.assertFalse(self.participante_repo.delete(123))
        self.assertFalse(
            self.participante_repo.update(
                Participante("Fulano", "11111111111", "UNIFAN", "f@f.com", id_participante=123)
            )
        )
        salvo = self.participante_repo.save(
            Participante("Fulano", "11111111111", "UNIFAN", "f@f.com")
        )
        self.assertIsNotNone(salvo.id_participante)
        self.assertEqual(len(self.participante_repo.get_all()), 1)
        self.assertTrue(self.participante_repo.delete(salvo.id_participante))

    def test_presenca_e_avaliacao_sao_persistidas(self):
        workshop = self.novo_workshop(vagas=5)
        p1 = self.novo_participante(1)
        inscricao = self.inscricoes.inscrever(p1.id_participante, workshop.id_workshop)
        self.inscricoes.registrar_presenca(inscricao.id_inscricao, "85,5")
        self.inscricoes.registrar_avaliacao(inscricao.id_inscricao, 9)
        lida = self.inscricao_repo.find_by_id(inscricao.id_inscricao)
        self.assertEqual(lida.percentual_presenca, 85.5)
        self.assertEqual(lida.nota_avaliacao, 9.0)

    # --- validações de entrada ---
    def test_validacoes_rejeitam_dados_invalidos(self):
        with self.assertRaises(ValueError):
            Workshop("Tema", 8, -1, "Fulano")
        with self.assertRaises(ValueError):
            Workshop("Tema", 0, 10, "Fulano")
        with self.assertRaises(ValueError):
            Workshop("   ", 8, 10, "Fulano")
        with self.assertRaises(ValueError):
            Workshop("Tema", "abc", 10, "Fulano")
        with self.assertRaises(ValueError):
            Participante("Fulano", "123", "UNIFAN", "f@f.com")
        with self.assertRaises(ValueError):
            Participante("Fulano", "11111111111", "UNIFAN", "email-invalido")
        with self.assertRaises(ValueError):
            InscricaoWorkshop(1, 1, percentual_presenca=101)
        with self.assertRaises(ValueError):
            InscricaoWorkshop(1, 1, nota_avaliacao=11)
        with self.assertRaises(ValueError):
            InscricaoWorkshop(1, 1, data_inscricao="31/02/2026")

    # --- relatórios analíticos ---
    def test_relatorios_analiticos(self):
        w1 = self.novo_workshop(vagas=4, tema="Python")
        w2 = self.novo_workshop(vagas=10, tema="SQL")
        self.novo_workshop(vagas=5, tema="Git")  # sem inscritos
        p1, p2 = self.novo_participante(1), self.novo_participante(2)

        i1 = self.inscricoes.inscrever(p1.id_participante, w1.id_workshop)
        i2 = self.inscricoes.inscrever(p2.id_participante, w1.id_workshop)
        self.inscricoes.inscrever(p1.id_participante, w2.id_workshop)
        self.inscricoes.registrar_avaliacao(i1.id_inscricao, 8)
        self.inscricoes.registrar_avaliacao(i2.id_inscricao, 9)

        ocupacao = {l["tema"]: l for l in self.relatorios.taxa_ocupacao_por_workshop()}
        self.assertEqual(ocupacao["Python"]["taxa_ocupacao"], 50.0)
        self.assertEqual(ocupacao["Python"]["inscritos"], 2)
        self.assertEqual(ocupacao["SQL"]["taxa_ocupacao"], 10.0)
        self.assertEqual(ocupacao["Git"]["taxa_ocupacao"], 0.0)

        medias = {l["tema"]: l for l in self.relatorios.media_notas_por_workshop()}
        self.assertEqual(medias["Python"]["media_notas"], 8.5)
        self.assertEqual(medias["Python"]["avaliacoes"], 2)
        self.assertIsNone(medias["SQL"]["media_notas"])
        self.assertEqual(medias["SQL"]["avaliacoes"], 0)

        # o workshop de maior média aparece primeiro; os sem nota, por último
        ordem = [l["tema"] for l in self.relatorios.media_notas_por_workshop()]
        self.assertEqual(ordem[0], "Python")


class TestRepositoriosEmMemoria(CenarioBase, unittest.TestCase):
    def criar_repositorios(self):
        workshop_repo = WorkshopRepositoryMemory()
        inscricao_repo = InscricaoRepositoryMemory()
        return (
            ParticipanteRepositoryMemory(),
            workshop_repo,
            inscricao_repo,
            RelatorioRepositoryMemory(workshop_repo, inscricao_repo),
        )


class TestRepositoriosSQL(CenarioBase, unittest.TestCase):
    def criar_repositorios(self):
        self.conexao = criar_conexao(":memory:")
        self.addCleanup(self.conexao.close)
        return (
            ParticipanteRepositorySQL(self.conexao),
            WorkshopRepositorySQL(self.conexao),
            InscricaoRepositorySQL(self.conexao),
            RelatorioRepositorySQL(self.conexao),
        )

    def test_banco_barra_estouro_de_vagas_mesmo_sem_o_servico(self):
        """O trigger do schema é a última barreira da regra de fronteira."""
        workshop = self.novo_workshop(vagas=1)
        p1, p2 = self.novo_participante(1), self.novo_participante(2)
        self.inscricao_repo.save(InscricaoWorkshop(p1.id_participante, workshop.id_workshop))
        with self.assertRaises(RepositorioError):
            self.inscricao_repo.save(
                InscricaoWorkshop(p2.id_participante, workshop.id_workshop)
            )
        self.assertEqual(self.inscricao_repo.count_by_workshop(workshop.id_workshop), 1)

    def test_banco_exige_integridade_referencial(self):
        with self.assertRaises(IntegridadeReferencialError):
            self.inscricao_repo.save(InscricaoWorkshop(42, 42))

        workshop = self.novo_workshop(vagas=3)
        p1 = self.novo_participante(1)
        self.inscricoes.inscrever(p1.id_participante, workshop.id_workshop)
        with self.assertRaises(IntegridadeReferencialError):
            self.workshop_repo.delete(workshop.id_workshop)


if __name__ == "__main__":
    unittest.main()
