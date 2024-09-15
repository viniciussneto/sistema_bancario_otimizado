def menu():
    print("\n" + "=" * 40)
    print(" " * 10 + "BANCO PYTHON")
    print("=" * 40)
    print("[d]  Depositar")
    print("[s]  Sacar")
    print("[e]  Extrato")
    print("[nc] Nova Conta")
    print("[lc] Listar Contas")
    print("[nu] Novo Usuário")
    print("[q]  Sair")
    print("=" * 40)
    return input("Escolha uma opção: ")

def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
        print("\n=== Depósito realizado com sucesso! ===")
    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
    
    return saldo, extrato

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    saldo_excedido = valor > saldo
    limite_excedido = valor > limite
    saque_excedido = numero_saques >= limite_saques
    
    if saldo_excedido:
        print("\n@@@ Operação falhou! Saldo insuficiente. @@@")
    elif limite_excedido:
        print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")
    elif saque_excedido:
        print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1
        print("\n=== Saque realizado com sucesso! ===")
    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

    return saldo, extrato

def exibir_extrato(saldo, /, *, extrato):
    print("\n" + "=" * 40)
    print(" " * 10 + "EXTRATO")
    print("=" * 40)
    print("Não houve movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("=" * 40)

def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def cadastro_usuario(usuarios):
    cpf = input("Informe o CPF: ")
    usuario = filtrar_usuario(cpf, usuarios)
    
    if usuario:
        print("\n@@@ Já existe usuário cadastrado com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (DD-MM-AAAA): ")
    endereco = input("Informe o endereço (logradouro, número - bairro - cidade/sigla estado): ")
    
    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})
    
    print("\n=== Usuário cadastrado com sucesso! ===")

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n=== Conta criada com sucesso! ===")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}

    print("\n@@@ Usuário não encontrado, cadastro de conta encerrado! @@@")

def listar_contas(contas):
    print("\n" + "=" * 40)
    print(" " * 10 + "LISTA DE CONTAS")
    print("=" * 40)
    
    for conta in contas:
        linha = f"""\
Agência:  {conta['agencia']}
C/C:      {conta['numero_conta']}
Titular:  {conta['usuario']['nome']}
"""
        print(linha)
        print("=" * 40)

def realizar_operacao(opcao, saldo, extrato, numero_saques, usuarios, contas, AGENCIA, LIMITE_SAQUES, limite):
    if opcao == "d":
        valor = float(input("Informe o valor do depósito: "))
        saldo, extrato = depositar(saldo, valor, extrato)

    elif opcao == "s":
        valor = float(input("Informe o valor do saque: "))
        saldo, extrato = sacar(
            saldo=saldo,
            valor=valor,
            extrato=extrato,
            limite=limite,
            numero_saques=numero_saques,
            limite_saques=LIMITE_SAQUES,
        )

    elif opcao == "e":
        exibir_extrato(saldo, extrato=extrato)

    elif opcao == "nu":
        cadastro_usuario(usuarios)

    elif opcao == "nc":
        numero_conta = len(contas) + 1
        conta = criar_conta(AGENCIA, numero_conta, usuarios)
        if conta:
            contas.append(conta)

    elif opcao == "lc":
        listar_contas(contas)

    elif opcao == "q":
        return False, saldo, extrato, numero_saques

    else:
        print("\n@@@ Operação inválida, selecione novamente. @@@")

    return True, saldo, extrato, numero_saques

def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []

    continuar = True
    while continuar:
        opcao = menu()
        continuar, saldo, extrato, numero_saques = realizar_operacao(
            opcao, saldo, extrato, numero_saques, usuarios, contas, AGENCIA, LIMITE_SAQUES, limite
        )

main()
