import json

ARQUIVO = 'agencias_cadastradas.json'

def carregar_dados():
    """Lê o JSON ao iniciar. Retorna {} se estiver vazio/corrompido."""
    try:
        with open(ARQUIVO, 'r', encoding='utf-8') as f:
            dados = json.load(f)
            return dados if isinstance(dados, dict) else {}
    except (FileNotFoundError, json.JSONDecodeError):
        return {}
    
lista_agencias = carregar_dados()

def numero_cnpj(cadastro,codigo):
    cadastro = str(cadastro)
    while cadastro in lista_agencias:
        cadastro = input('Código já cadastrado, digite outro código: ')
    lista_agencias[cadastro] = {'codigo': codigo}
    return True

def salvar_dados():
    with open(ARQUIVO, 'w', encoding='utf-8') as f:
        json.dump(lista_agencias, f, indent=2, ensure_ascii=False)