import json

lista_contas = {}


# responsavel por cadastra conta do cliente
def cadastracao_contas(numero_conta, agencia, saldo):
    numero_conta = str(numero_conta)
    if numero_conta in lista_contas:
        return False

    lista_contas[numero_conta] = {
        'agencia': agencia,
        'saldo': float(saldo)
    }
    return True


# responsavel por realizar o saque
def saque(numero_conta, valor_de_saque):
    numero_conta = str(numero_conta)
    if numero_conta not in lista_contas:
        return 'Conta não encontrada!'

    conta = lista_contas[numero_conta]
    if valor_de_saque <= 0:
        return 'Não houve saque!'
    if valor_de_saque > conta['saldo']:
        return 'Saldo insuficiente!'

    conta['saldo'] -= valor_de_saque
    return 'Saque realizado!'


# responsavel por realizar deposito
def deposito(numero_conta, valor_do_deposito):
    numero_conta = str(numero_conta)
    if numero_conta not in lista_contas:
        return 'Conta não encontrada!'

    conta = lista_contas[numero_conta]
    if valor_do_deposito <= 0:
        return 'Não houve depósito!'

    conta['saldo'] += valor_do_deposito
    return 'Depósito realizado!'


# responsavel por realizar transferencia
def transferencia(numero_conta_origem, numero_conta_destino, valor_de_transferencia):
    numero_conta_origem = str(numero_conta_origem)
    numero_conta_destino = str(numero_conta_destino)

    if numero_conta_origem not in lista_contas or numero_conta_destino not in lista_contas:
        return 'Conta não encontrada!'

    origem = lista_contas[numero_conta_origem]
    destino = lista_contas[numero_conta_destino]

    if valor_de_transferencia <= 0:
        return 'Valor de transferência inválido!'

    if valor_de_transferencia > origem['saldo']:
        return '!erro: você tentou transferir um valor maior do que o valor atual'

    origem['saldo'] -= valor_de_transferencia
    destino['saldo'] += valor_de_transferencia
    return 'transferência concluída!'


# salvar em formato json
def salvar_dados():
    with open('contas.json', 'w', encoding='utf-8') as f:
        json.dump(lista_contas, f, indent=2, ensure_ascii=False)

    with open('numero_contas.json', 'w', encoding='utf-8') as f:
        json.dump(list(lista_contas.keys()), f, indent=2, ensure_ascii=False)

    with open('agencias.json', 'w', encoding='utf-8') as f:
        json.dump({numero: dados['agencia'] for numero, dados in lista_contas.items()}, f, indent=2, ensure_ascii=False)

    with open('saldos.json', 'w', encoding='utf-8') as f:
        json.dump({numero: dados['saldo'] for numero, dados in lista_contas.items()}, f, indent=2, ensure_ascii=False)
