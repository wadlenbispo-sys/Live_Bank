# Cadastro de agências: a chave é o CNPJ e o código fica dentro do dicionário
import json

ARQUIVO = 'agencias_cadastradas.json'


def carregar_dados():
    """Lê o JSON ao iniciar. Retorna {} se não existir ou estiver inválido."""
    try:
        with open(ARQUIVO, 'r', encoding='utf-8') as f:
            dados = json.load(f)
            return dados if isinstance(dados, dict) else {}
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


lista_agencias = carregar_dados()


def codigo_existe(codigo):
    """Retorna True se já existe uma agência com esse código."""
    codigo = str(codigo)
    return any(dados['codigo'] == codigo for dados in lista_agencias.values())


def cadastra_agencia(cnpj, codigo):
    """Cadastra a agência. Retorna False se o CNPJ ou o código já existirem."""
    cnpj = str(cnpj)
    codigo = str(codigo)
    if cnpj in lista_agencias or codigo_existe(codigo):
        return False

    lista_agencias[cnpj] = {'codigo': codigo}
    return True

def aplicar_rendimento(cnpj, taxa):
    """Aplica rendimento a todas as contas da agência especificada."""
    cnpj = str(cnpj)
    if cnpj not in lista_agencias:
        print("Agência não encontrada.")
        return

    # Carregar contas correntes
    try:
        with open('contas_correntes.json', 'r', encoding='utf-8') as f:
            contas = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("Não há contas cadastradas.")
        return

    # Aplicar rendimento
    for numero, dados in contas.items():
        if dados.get('agencia') == cnpj:
            saldo_atual = float(dados.get('saldo', 0))
            novo_saldo = saldo_atual * (1 + taxa / 100)
            dados['saldo'] = round(novo_saldo, 2)

    # Salvar contas atualizadas
    with open('contas_correntes.json', 'w', encoding='utf-8') as f:
        json.dump(contas, f, indent=2, ensure_ascii=False)
        
def salvar_dados():
    with open(ARQUIVO, 'w', encoding='utf-8') as f:
        json.dump(lista_agencias, f, indent=2, ensure_ascii=False)