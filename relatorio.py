# Relatório geral do Live_Bank
# Lê os arquivos JSON gerados pelos outros módulos e exibe um resumo formatado

import json


def carregar_arquivo_json(nome_arquivo):
    """Lê um arquivo JSON. Retorna {} se não existir ou estiver vazio/corrompido."""
    try:
        with open(nome_arquivo, 'r', encoding='utf-8') as f:
            dados = json.load(f)
            return dados if isinstance(dados, dict) else {}
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def relatorio_clientes():
    clientes = carregar_arquivo_json('lista_clientes.json')

    print('\n--- Clientes cadastrados ---')
    if not clientes:
        print('Nenhum cliente cadastrado.')
        return

    for i, (cpf, dados) in enumerate(clientes.items(), start=1):
        print(f"{i}. {dados.get('nome', 'N/A')} - CPF: {cpf}")


def relatorio_agencias():
    agencias = carregar_arquivo_json('agencias_cadastradas.json')

    print('\n--- Agências cadastradas ---')
    if not agencias:
        print('Nenhuma agência cadastrada.')
        return

    for i, (cnpj, dados) in enumerate(agencias.items(), start=1):
        print(f"{i}. CNPJ: {cnpj} - Código: {dados.get('codigo', 'N/A')}")


def relatorio_contas():
    contas = carregar_arquivo_json('contas_correntes.json')

    print('\n--- Contas cadastradas ---')
    if not contas:
        print('Nenhuma conta cadastrada.')
        return

    total_banco = 0
    total_por_agencia = {}

    for i, (numero, dados) in enumerate(contas.items(), start=1):
        agencia = dados.get('agencia', 'N/A')
        saldo = float(dados.get('saldo', 0))
        tipo = dados.get('tipo', 'corrente')

        total_banco += saldo
        total_por_agencia[agencia] = total_por_agencia.get(agencia, 0) + saldo
        print(f'{i}. Conta {tipo}: {numero} - Agência: {agencia} - Saldo: R$ {saldo:.2f}')

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