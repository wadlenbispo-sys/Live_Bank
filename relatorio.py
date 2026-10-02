# Relatório geral do Live_Bank
# Lê os arquivos JSON gerados pelos outros módulos e exibe um resumo formatado

import json


def carregar_json(nome_arquivo):
    """Lê um arquivo JSON na pasta do projeto. Retorna lista vazia se não existir ou estiver vazio/corrompido."""
    try:
        with open(nome_arquivo, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def relatorio_clientes():
    nomes = carregar_json('nomes.json')
    cpfs = carregar_json('cpfs.json')
    clientes = carregar_json('clientes.json')

    print('\n--- Clientes cadastrados ---')

    if clientes:
        if isinstance(clientes, dict):
            i = 1
            for cpf in clientes.keys():
                nome = clientes[cpf].get('nome', 'N/A')
                print(f'{i}. {nome} - CPF: {cpf}')
                i += 1
        return

    if not nomes:
        print('Nenhum cliente cadastrado.')
        return

    i = 1
    for nome in nomes:
        cpf = cpfs[i - 1] if i - 1 < len(cpfs) else 'N/A'
        print(f'{i}. {nome} - CPF: {cpf}')
        i += 1


def relatorio_agencias():
    cnpjs = carregar_json('cnpjs.json')
    codigos = carregar_json('codigo_agencia.json')
    agencias = carregar_json('agencias_cadastradas.json')

    print('\n--- Agências cadastradas ---')

    if agencias:
        if isinstance(agencias, dict):
            i = 1
            for codigo in agencias.keys():
                print(f'{i}. Agência: {codigo}')
                i += 1
        return

    if not cnpjs:
        print('Nenhuma agência cadastrada.')
        return

    i = 1
    for cnpj in cnpjs:
        codigo = codigos[i - 1] if i - 1 < len(codigos) else 'N/A'
        print(f'{i}. CNPJ: {cnpj} - Código: {codigo}')
        i += 1


def relatorio_contas():
    numeros = carregar_json('numero_contas.json')
    agencias = carregar_json('agencias.json')
    saldos = carregar_json('saldos.json')
    contas = carregar_json('contas.json')

    print('\n--- Contas cadastradas ---')

    if contas:
        if isinstance(contas, dict):
            total_banco = 0
            total_por_agencia = {}
            i = 1
            for numero in contas.keys():
                agencia = contas[numero].get('agencia', 'N/A')
                saldo = float(contas[numero].get('saldo', 0))
                total_banco += saldo
                total_por_agencia[agencia] = total_por_agencia.get(agencia, 0) + saldo
                print(f'{i}. Conta: {numero} - Agência: {agencia} - Saldo: R$ {saldo:.2f}')
                i += 1

            print('\n--- Montante por agência ---')
            for agencia, total_agencia in total_por_agencia.items():
                print(f'Agência {agencia}: R$ {total_agencia:.2f}')

            print(f'\nMontante total do banco: R$ {total_banco:.2f}')
        return

    if not numeros:
        print('Nenhuma conta cadastrada.')
        return

    total_banco = 0
    total_por_agencia = {}

    i = 1
    for numero in numeros:
        agencia = agencias[i - 1] if i - 1 < len(agencias) else 'N/A'
        saldo = saldos[i - 1] if i - 1 < len(saldos) else 0
        total_banco += saldo
        total_por_agencia[agencia] = total_por_agencia.get(agencia, 0) + saldo
        print(f'{i}. Conta: {numero} - Agência: {agencia} - Saldo: R$ {saldo:.2f}')
        i += 1

    print('\n--- Montante por agência ---')
    for agencia, total_agencia in total_por_agencia.items():
        print(f'Agência {agencia}: R$ {total_agencia:.2f}')

    print(f'\nMontante total do banco: R$ {total_banco:.2f}')


def gerar_relatorio_completo():
    print('=' * 55)
    print('RELATÓRIO GERAL - LIVE_BANK')
    print('=' * 55)
    relatorio_clientes()
    relatorio_agencias()
    relatorio_contas()
    print('=' * 55)
