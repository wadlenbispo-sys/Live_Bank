import json

ARQUIVO = 'contas_poupanca.json'

def carregar_dados():
    """Lê o JSON ao iniciar. Retorna {} se não existir ou estiver inválido."""
    try:
        with open(ARQUIVO, 'r', encoding='utf-8') as f:
            dados = json.load(f)
            return dados if isinstance(dados, dict) else {}
    except (FileNotFoundError, json.JSONDecodeError):
        return {}
    
lista_contas_poupanca = carregar_dados()

def codigo_existe(codigo):
    """Retorna True se já existe uma conta com esse código."""
    codigo = str(codigo)
    return any(dados.get('Codigo') == codigo for dados in lista_contas_poupanca.values())

def codigo_existe(codigo):
    """Retorna True se já existe uma conta com esse código."""
    codigo = str(codigo)
    return any(dados.get('Codigo') == codigo for dados in lista_contas_poupanca.values())

def cadastra_conta_poupanca(cnpj, codigo, numero_conta, cidade=None, estado=None, saldo_inicial=0.0):
    """Cadastra a conta poupança. Retorna False se o CNPJ ou o código já existirem."""
    cnpj = str(cnpj)
    codigo = str(codigo)
    if cnpj in lista_contas_poupanca or codigo_existe(codigo):
        return False

    lista_contas_poupanca[cnpj] = {'Codigo': codigo, 'Numero_conta': numero_conta, 'Cidade': cidade, 'Estado': estado, 'Saldo': saldo_inicial}
    return True

def guardar_poupanca(cnpj, valor):
    """Realiza um depósito na conta poupança especificada pelo CNPJ."""
    cnpj = str(cnpj)
    if cnpj not in lista_contas_poupanca:
        return "Conta não encontrada."
    else:
        try:
            valor = float(valor)
            if valor <= 0:
                return "Valor de depósito deve ser positivo."
        except ValueError:
            return "Valor inválido."

        # Carregar contas poupança
        try:
            with open('contas_poupanca.json', 'r', encoding='utf-8') as f:
                contas = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return "Não há contas cadastradas."

        # Atualizar saldo
        for numero, dados in contas.items():
            if dados.get('agencia') == cnpj:
                saldo_atual = float(dados.get('saldo', 0))
                novo_saldo = saldo_atual + valor
                dados['saldo'] = round(novo_saldo, 2)

    # Salvar as alterações no arquivo JSON
    def salvar_dados():
        with open('contas_poupanca.json', 'w', encoding='utf-8') as f:
            json.dump(contas, f, indent=2, ensure_ascii=False) 

def salvar_dados():
    """Salva os dados das contas poupança no arquivo JSON."""
    with open(ARQUIVO, 'w', encoding='utf-8') as f:
        json.dump(lista_contas_poupanca, f, indent=2, ensure_ascii=False)