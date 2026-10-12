import json

ARQUIVO = 'agencias.json'

def carregar_dados():
    """Lê o JSON ao iniciar. Retorna {} se estiver vazio/corrompido."""
    try:
        with open(ARQUIVO, 'r', encoding='utf-8') as f:
            dados = json.load(f)
            return dados if isinstance(dados, dict) else {}
    except (FileNotFoundError, json.JSONDecodeError):
        return {}
    
lista_agencias = carregar_dados()

def cadastra_agencia(nome,cpf,cnpj, codigo, cidade=None, estado=None):
    """Cadastra a agência. Retorna False se o CNPJ ou o código já existirem."""
    cnpj = str(cnpj)
    codigo = str(codigo)
    if cnpj in lista_agencias or any(dados['Codigo'] == codigo for dados in lista_agencias.values()):
        return False
    lista_agencias[cpf] = {'CNPJ do Sócio': cnpj, 'Nome do Sócio': nome, 'Codigo': codigo, 'Cidade': cidade, 'Estado': estado}
    return True

def salvar_dados():
    with open(ARQUIVO, 'w', encoding='utf-8') as f:
        json.dump(lista_agencias, f, indent=2, ensure_ascii=False)