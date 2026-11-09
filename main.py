"""EventFlow - gestão de inscrições em workshops (menu CLI).

Uso:
    python main.py             # Fase 2: persistência em SQLite
    python main.py --memoria   # Fase 1: coleções em memória
"""
import sys

from database.connection import criar_conexao
from repositories.erros import RepositorioError
from repositories.inscricao_database_repository import InscricaoRepositorySQL
from repositories.inscricao_memory_repository import InscricaoRepositoryMemory
from repositories.participante_database_repository import ParticipanteRepositorySQL
from repositories.participante_memory_repository import ParticipanteRepositoryMemory
from repositories.relatorio_database_repository import RelatorioRepositorySQL
from repositories.relatorio_memory_repository import RelatorioRepositoryMemory
from repositories.workshop_database_repository import WorkshopRepositorySQL
from repositories.workshop_memory_repository import WorkshopRepositoryMemory
from services.erros import RegraNegocioError
from services.inscricao_service import InscricaoService
from services.participante_service import ParticipanteService
from services.relatorio_service import RelatorioService
from services.workshop_service import WorkshopService


# ----------------------------------------------------------------------
# Funções de entrada de dados
# ----------------------------------------------------------------------
def pedir(rotulo, atual=None):
    """Lê um texto. Em atualizações, Enter vazio mantém o valor atual (retorna None)."""
    dica = f" [{atual}]" if atual is not None else ""
    valor = input(f"{rotulo}{dica}: ").strip()
    if atual is not None and valor == "":
        return None
    return valor


def pedir_id(rotulo):
    texto = input(f"{rotulo}: ").strip()
    try:
        return int(texto)
    except ValueError:
        raise ValueError(f"'{texto}' não é um ID válido (use um número inteiro).") from None


def formatar_data(data):
    return data.strftime("%d/%m/%Y")


def linha_inscricao(d):
    nota = "sem nota" if d["nota_avaliacao"] is None else f"{d['nota_avaliacao']:.1f}"
    return (
        f"[{d['id_inscricao']}] {d['participante']} -> {d['workshop']} | "
        f"inscrito em {formatar_data(d['data_inscricao'])} | "
        f"presença {d['percentual_presenca']:.0f}% | nota {nota}"
    )


# ----------------------------------------------------------------------
# Aplicação CLI
# ----------------------------------------------------------------------
class EventFlowCLI:
    def __init__(self, participantes, workshops, inscricoes, relatorios):
        self._participantes = participantes
        self._workshops = workshops
        self._inscricoes = inscricoes
        self._relatorios = relatorios

    # --- infraestrutura de menus ---
    @staticmethod
    def _executar(acao):
        """Executa uma ação sem permitir que erros derrubem o programa."""
        try:
            acao()
        except (ValueError, RepositorioError, RegraNegocioError) as erro:
            print(f"\n[ERRO] {erro}")
        except (KeyboardInterrupt, EOFError):
            raise
        except Exception as erro:  # rede de segurança: o CLI nunca fecha por engano
            print(f"\n[ERRO INESPERADO] {type(erro).__name__}: {erro}")

    def _submenu(self, titulo, opcoes):
        while True:
            print(f"\n=== {titulo} ===")
            for chave, (texto, _) in opcoes.items():
                print(f"{chave} - {texto}")
            print("0 - Voltar")
            escolha = input("Escolha uma opção: ").strip()
            if escolha == "0":
                return
            if escolha in opcoes:
                self._executar(opcoes[escolha][1])
            else:
                print("Opção inválida.")

    def executar(self):
        principal = {
            "1": ("Participantes", self.menu_participantes),
            "2": ("Workshops", self.menu_workshops),
            "3": ("Inscrições", self.menu_inscricoes),
            "4": ("Relatórios analíticos", self.menu_relatorios),
        }
        while True:
            print("\n=== EventFlow ===")
            for chave, (texto, _) in principal.items():
                print(f"{chave} - {texto}")
            print("0 - Sair")
            escolha = input("Escolha uma opção: ").strip()
            if escolha == "0":
                print("Até logo!")
                return
            if escolha in principal:
                principal[escolha][1]()
            else:
                print("Opção inválida.")

    # --- participantes ---
    def menu_participantes(self):
        self._submenu(
            "Participantes",
            {
                "1": ("Cadastrar", self._cadastrar_participante),
                "2": ("Listar", self._listar_participantes),
                "3": ("Buscar por ID", self._buscar_participante),
                "4": ("Atualizar", self._atualizar_participante),
                "5": ("Remover", self._remover_participante),
            },
        )

    def _cadastrar_participante(self):
        participante = self._participantes.cadastrar(
            pedir("Nome"),
            pedir("CPF (11 dígitos)"),
            pedir("Instituição"),
            pedir("E-mail"),
        )
        print(f"\nParticipante cadastrado (ID {participante.id_participante}).")

    def _listar_participantes(self):
        lista = self._participantes.listar()
        if not lista:
            print("\nNenhum participante cadastrado.")
        for participante in lista:
            print(participante)

    def _buscar_participante(self):
        print(self._participantes.buscar(pedir_id("ID do participante")))

    def _atualizar_participante(self):
        atual = self._participantes.buscar(pedir_id("ID do participante"))
        print("Enter mantém o valor atual.")
        atualizado = self._participantes.atualizar(
            atual.id_participante,
            nome=pedir("Nome", atual.nome),
            cpf=pedir("CPF", atual.cpf),
            instituicao=pedir("Instituição", atual.instituicao),
            email=pedir("E-mail", atual.email),
        )
        print(f"\nAtualizado: {atualizado}")

    def _remover_participante(self):
        id_participante = pedir_id("ID do participante")
        self._participantes.remover(id_participante)
        print("\nParticipante removido.")

    # --- workshops ---
    def menu_workshops(self):
        self._submenu(
            "Workshops",
            {
                "1": ("Cadastrar", self._cadastrar_workshop),
                "2": ("Listar", self._listar_workshops),
                "3": ("Buscar por ID", self._buscar_workshop),
                "4": ("Atualizar", self._atualizar_workshop),
                "5": ("Remover", self._remover_workshop),
            },
        )

    def _cadastrar_workshop(self):
        workshop = self._workshops.cadastrar(
            pedir("Tema"),
            pedir("Carga horária (horas)"),
            pedir("Limite de vagas"),
            pedir("Instrutor"),
        )
        print(f"\nWorkshop cadastrado (ID {workshop.id_workshop}).")

    def _listar_workshops(self):
        lista = self._workshops.listar_com_ocupacao()
        if not lista:
            print("\nNenhum workshop cadastrado.")
        for workshop, inscritos in lista:
            print(f"{workshop} | inscritos: {inscritos}/{workshop.vagas_limite}")

    def _buscar_workshop(self):
        print(self._workshops.buscar(pedir_id("ID do workshop")))

    def _atualizar_workshop(self):
        atual = self._workshops.buscar(pedir_id("ID do workshop"))
        print("Enter mantém o valor atual.")
        atualizado = self._workshops.atualizar(
            atual.id_workshop,
            tema=pedir("Tema", atual.tema),
            carga_horaria=pedir("Carga horária", atual.carga_horaria),
            vagas_limite=pedir("Limite de vagas", atual.vagas_limite),
            instrutor=pedir("Instrutor", atual.instrutor),
        )
        print(f"\nAtualizado: {atualizado}")

    def _remover_workshop(self):
        self._workshops.remover(pedir_id("ID do workshop"))
        print("\nWorkshop removido.")

    # --- inscrições ---
    def menu_inscricoes(self):
        self._submenu(
            "Inscrições",
            {
                "1": ("Inscrever participante em workshop", self._inscrever),
                "2": ("Listar inscrições", self._listar_inscricoes),
                "3": ("Registrar presença", self._registrar_presenca),
                "4": ("Registrar avaliação", self._registrar_avaliacao),
                "5": ("Cancelar inscrição", self._cancelar_inscricao),
            },
        )

    def _inscrever(self):
        id_participante = pedir_id("ID do participante")
        id_workshop = pedir_id("ID do workshop")
        data = pedir("Data da inscrição (DD/MM/AAAA, Enter = hoje)") or None
        inscricao = self._inscricoes.inscrever(id_participante, id_workshop, data)
        print(f"\nInscrição realizada (ID {inscricao.id_inscricao}).")

    def _listar_inscricoes(self):
        lista = self._inscricoes.listar_detalhado()
        if not lista:
            print("\nNenhuma inscrição registrada.")
        for item in lista:
            print(linha_inscricao(item))

    def _registrar_presenca(self):
        id_inscricao = pedir_id("ID da inscrição")
        percentual = pedir("Percentual de presença (0 a 100)")
        self._inscricoes.registrar_presenca(id_inscricao, percentual)
        print("\nPresença registrada.")

    def _registrar_avaliacao(self):
        id_inscricao = pedir_id("ID da inscrição")
        nota = pedir("Nota da avaliação (0 a 10)")
        self._inscricoes.registrar_avaliacao(id_inscricao, nota)
        print("\nAvaliação registrada.")

    def _cancelar_inscricao(self):
        self._inscricoes.cancelar(pedir_id("ID da inscrição"))
        print("\nInscrição cancelada.")

    # --- relatórios ---
    def menu_relatorios(self):
        self._submenu(
            "Relatórios analíticos",
            {
                "1": ("Taxa de ocupação de vagas por workshop", self._rel_ocupacao),
                "2": ("Média das notas por workshop", self._rel_media_notas),
            },
        )

    def _rel_ocupacao(self):
        linhas = self._relatorios.taxa_ocupacao_por_workshop()
        if not linhas:
            print("\nNenhum workshop cadastrado.")
            return
        print(f"\n{'Workshop':<32}{'Inscritos':>10}{'Vagas':>8}{'Ocupação':>11}")
        for l in linhas:
            print(
                f"{l['tema'][:30]:<32}{l['inscritos']:>10}{l['vagas_limite']:>8}"
                f"{l['taxa_ocupacao']:>10.2f}%"
            )

    def _rel_media_notas(self):
        linhas = self._relatorios.media_notas_por_workshop()
        if not linhas:
            print("\nNenhum workshop cadastrado.")
            return
        print(f"\n{'Workshop':<32}{'Avaliações':>11}{'Média':>8}")
        for l in linhas:
            media = "—" if l["media_notas"] is None else f"{l['media_notas']:.2f}"
            print(f"{l['tema'][:30]:<32}{l['avaliacoes']:>11}{media:>8}")


# ----------------------------------------------------------------------
# Inicialização: é AQUI que a Fase 1 vira Fase 2 (o menu não muda).
# ----------------------------------------------------------------------
def main():
    conexao = None
    if "--memoria" in sys.argv[1:]:
        # --- Fase 1: coleções em memória ---
        participante_repo = ParticipanteRepositoryMemory()
        workshop_repo = WorkshopRepositoryMemory()
        inscricao_repo = InscricaoRepositoryMemory()
        relatorio_repo = RelatorioRepositoryMemory(workshop_repo, inscricao_repo)
        print("[Modo memória: os dados serão perdidos ao sair]")
    else:
        # --- Fase 2: banco de dados relacional ---
        conexao = criar_conexao()
        participante_repo = ParticipanteRepositorySQL(conexao)
        workshop_repo = WorkshopRepositorySQL(conexao)
        inscricao_repo = InscricaoRepositorySQL(conexao)
        relatorio_repo = RelatorioRepositorySQL(conexao)

    cli = EventFlowCLI(
        ParticipanteService(participante_repo, inscricao_repo),
        WorkshopService(workshop_repo, inscricao_repo),
        InscricaoService(inscricao_repo, participante_repo, workshop_repo),
        RelatorioService(relatorio_repo),
    )
    try:
        cli.executar()
    except (KeyboardInterrupt, EOFError):
        print("\nEncerrando...")
    finally:
        if conexao is not None:
            conexao.close()


if __name__ == "__main__":
    main()
