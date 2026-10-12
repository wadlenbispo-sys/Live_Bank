# Cadastro de agências: a chave é o CNPJ e o código fica dentro do dicionário
import json

ARQUIVO = 'contas_correntes.json'


def carregar_dados():
    """Lê o JSON ao iniciar. Retorna {} se não existir ou estiver inválido."""
    try:
        with open(ARQUIVO, 'r', encoding='utf-8') as f:
            dados = json.load(f)
            return dados if isinstance(dados, dict) else {}
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

lista_contas_correntes = carregar_dados()

def codigo_existe(codigo):
    """Retorna True se já existe uma conta com esse código."""
    codigo = str(codigo)
    return any(dados.get('Codigo') == codigo for dados in lista_contas_correntes.values())

def cadastra_conta_corrente(cnpj, codigo, numero_conta, cidade=None, estado=None, saldo_inicial=0.0):
    """Cadastra a conta corrente. Retorna False se o CNPJ ou o código já existirem."""
    cnpj = str(cnpj)
    codigo = str(codigo)
    if cnpj in lista_contas_correntes or codigo_existe(codigo):
        return False

    lista_contas_correntes[cnpj] = {'Codigo': codigo, 'Numero_conta': numero_conta, 'Cidade': cidade, 'Estado': estado, 'Saldo': saldo_inicial}
    return True

def deposito(codigo, valor):
    if valor <= 0:
        return False, 'O valor do depósito deve ser maior que zero.'
    for cnpj,dados in lista_contas_correntes.items():
        if dados["Codigo"] == codigo:
            dados["Saldo"] += valor
            return True, f'Depósito de R$ {valor:.2f} realizado com sucesso.'
    return False, 'Conta não encontrada.'

def saque(codigo, valor):
    if valor <= 0:
        return False, 'O valor do saque deve ser maior que zero.'
    for cnpj,dados in lista_contas_correntes.items():
        if dados["Codigo"] == codigo:
            if dados["Saldo"] < valor:
                return False, 'Saldo insuficiente.'
            dados["Saldo"] -= valor
            return True, f'Saque de R$ {valor:.2f} realizado com sucesso.'
    return False, 'Conta não encontrada.'

def aplicar_rendimento(cnpj, taxa):
    encontrou = False
    for cnpj,dados in lista_contas_correntes.items():
        if dados["CNPJ"] == cnpj:
            dados["Saldo"] *= (1 + taxa / 100)
            encontrou = True
    if not encontrou:
        return False, 'Agência não encontrada.'
    return True, f'Rendimento de {taxa}% aplicado com sucesso.'

def salvar_dados():
    """Salva os dados das contas correntes no arquivo JSON."""
    with open(ARQUIVO, 'w', encoding='utf-8') as f:
        json.dump(lista_contas_correntes, f, indent=2, ensure_ascii=False)