
# ==========================================
# EVENTFLOW - DEMONSTRAÇÃO DE FUNCIONAMENTO
# ==========================================

print("=" * 45)
print("       SISTEMA EVENTFLOW")
print("       DEMONSTRAÇÃO PRÁTICA")
print("=" * 45)

# Lista de workshops
workshops = []

# Lista de participantes
participantes = []

# Lista de inscrições
inscricoes = []


# 1. CADASTRAR WORKSHOP
def cadastrar_workshop(nome, vagas):
    workshop = {
        "id": len(workshops) + 1,
        "nome": nome,
        "vagas": vagas
    }

    workshops.append(workshop)
    print(f"\n[OK] Workshop '{nome}' cadastrado!")


# 2. CADASTRAR PARTICIPANTE
def cadastrar_participante(nome, email):
    participante = {
        "id": len(participantes) + 1,
        "nome": nome,
        "email": email
    }

    participantes.append(participante)
    print(f"[OK] Participante '{nome}' cadastrado!")


# 3. REALIZAR INSCRIÇÃO
def realizar_inscricao(participante_id, workshop_id):
    workshop = next(
        (w for w in workshops if w["id"] == workshop_id), None
    )

    participante = next(
        (p for p in participantes if p["id"] == participante_id), None
    )

    if not workshop or not participante:
        print("[ERRO] Participante ou workshop não encontrado!")
        return

    ocupadas = sum(
        1 for i in inscricoes
        if i["workshop_id"] == workshop_id
    )

    if ocupadas >= workshop["vagas"]:
        print("[ERRO] Workshop sem vagas disponíveis!")
        return

    inscricoes.append({
        "participante_id": participante_id,
        "workshop_id": workshop_id
    })

    print(f"[OK] Inscrição de {participante['nome']} realizada!")


# 4. LISTAR WORKSHOPS
def listar_workshops():
    print("\n--- WORKSHOPS CADASTRADOS ---")

    for workshop in workshops:
        ocupadas = sum(
            1 for i in inscricoes
            if i["workshop_id"] == workshop["id"]
        )

        disponiveis = workshop["vagas"] - ocupadas

        print(f"\nWorkshop: {workshop['nome']}")
        print(f"Vagas totais: {workshop['vagas']}")
        print(f"Vagas ocupadas: {ocupadas}")
        print(f"Vagas disponíveis: {disponiveis}")


# 5. CANCELAR INSCRIÇÃO
def cancelar_inscricao(participante_id, workshop_id):
    for inscricao in inscricoes:
        if (
            inscricao["participante_id"] == participante_id
            and inscricao["workshop_id"] == workshop_id
        ):
            inscricoes.remove(inscricao)
            print("[OK] Inscrição cancelada!")
            return

    print("[ERRO] Inscrição não encontrada!")


# ==========================================
# EXECUÇÃO DOS EXEMPLOS
# ==========================================

print("\n1. CADASTRANDO WORKSHOP")
cadastrar_workshop("Workshop de Python", 2)

print("\n2. CADASTRANDO PARTICIPANTES")
cadastrar_participante("João", "joao@email.com")
cadastrar_participante("Maria", "maria@email.com")
cadastrar_participante("Pedro", "pedro@email.com")

print("\n3. REALIZANDO INSCRIÇÕES")
realizar_inscricao(1, 1)
realizar_inscricao(2, 1)

print("\n4. TESTANDO LIMITE DE VAGAS")
realizar_inscricao(3, 1)

print("\n5. CONSULTANDO WORKSHOPS")
listar_workshops()

print("\n6. CANCELANDO INSCRIÇÃO")
cancelar_inscricao(1, 1)

print("\n7. CONSULTANDO VAGAS APÓS CANCELAMENTO")
listar_workshops()

print("\n" + "=" * 45)
print("       DEMONSTRAÇÃO FINALIZADA")
print("=" * 45)
