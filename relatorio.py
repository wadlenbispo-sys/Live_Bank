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
    clientes = carregar_arquivo_json('clientes.json')

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
    contas_poupanca = carregar_arquivo_json('contas_poupanca.json')
    contas_correntes = carregar_arquivo_json('contas_correntes.json')
    contas_salario = carregar_arquivo_json('contas_salario.json')

    print('\n--- Contas cadastradas ---')
    if not (contas_poupanca or contas_correntes or contas_salario):
        print('Nenhuma conta cadastrada.')
        return
    print('\nContas Poupança:')
    if contas_poupanca:
        for i, (cnpj, dados) in enumerate(contas_poupanca.items(), start=1):
            print(f"{i}. CNPJ: {cnpj} - Código: {dados.get('Codigo', 'N/A')} - Saldo: {dados.get('Saldo', 0.0)}")
    else:
        print('Nenhuma conta poupança cadastrada.')

    print('\nContas Correntes:')
    if contas_correntes:
        for i, (cnpj, dados) in enumerate(contas_correntes.items(), start=1):
            print(f"{i}. CNPJ: {cnpj} - Código: {dados.get('Codigo', 'N/A')} - Saldo: {dados.get('Saldo', 0.0)}")
    else:
        print('Nenhuma conta corrente cadastrada.')

    print('\nContas Salário:')
    if contas_salario:
        for i, (cnpj, dados) in enumerate(contas_salario.items(), start=1):
            print(f"{i}. CNPJ: {cnpj} - Código: {dados.get('Codigo', 'N/A')} - Saldo: {dados.get('Saldo', 0.0)}")
    else:
        print('Nenhuma conta salário cadastrada.')

def gerar_relatorio_completo():
    print('=' * 55)
    print('RELATÓRIO GERAL - LIVE_BANK')
    print('=' * 55)
    relatorio_clientes()
    relatorio_agencias()
    relatorio_contas()
    print('=' * 55)