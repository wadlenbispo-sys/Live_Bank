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

    print('\n--- Clientes cadastrados ---')
    if not nomes:
        print('Nenhum cliente cadastrado.')
        return

    for i, nome in enumerate(nomes):
        cpf = cpfs[i] if i < len(cpfs) else 'N/A'
        print(f'{i + 1}. {nome} - CPF: {cpf}')


def relatorio_agencias():
    cnpjs = carregar_json('cnpjs.json')
    codigos = carregar_json('codigo_agencia.json')

    print('\n--- Agências cadastradas ---')
    if not cnpjs:
        print('Nenhuma agência cadastrada.')
        return

    for i, cnpj in enumerate(cnpjs):
        codigo = codigos[i] if i < len(codigos) else 'N/A'
        print(f'{i + 1}. CNPJ: {cnpj} - Código: {codigo}')


def relatorio_contas():
    numeros = carregar_json('numero_contas.json')
    agencias = carregar_json('agencias.json')
    saldos = carregar_json('saldos.json')

    print('\n--- Contas cadastradas ---')
    if not numeros:
        print('Nenhuma conta cadastrada.')
        return

    total_banco = 0
    total_por_agencia = {}

    for i, numero in enumerate(numeros):
        agencia = agencias[i] if i < len(agencias) else 'N/A'
        saldo = saldos[i] if i < len(saldos) else 0
        total_banco += saldo
        total_por_agencia[agencia] = total_por_agencia.get(agencia, 0) + saldo
        print(f'{i + 1}. Conta: {numero} - Agência: {agencia} - Saldo: R$ {saldo:.2f}')

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
