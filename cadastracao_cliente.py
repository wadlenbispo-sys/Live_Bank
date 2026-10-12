# Função para carregar os dados do arquivo JSON

import json

ARQUIVO = 'lista_clientes.json'


def carregar_dados():
    """Lê o JSON ao iniciar. Retorna {} se estiver vazio/corrompido."""
    try:
        with open(ARQUIVO, 'r', encoding='utf-8') as f:
            dados = json.load(f)
            return dados if isinstance(dados, dict) else {}
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

# Lista de clientes carregada do arquivo JSON

lista_clientes = carregar_dados()

def cadastra_cliente(nome, senha, cpf):
    cpf = str(cpf)
    if cpf in lista_clientes:
        return False

    lista_clientes[cpf] = {
        'nome': nome,
        'senha': senha
    }
    return True

def buscar_cpf(cpf):
    """Busca um cliente pelo CPF. Retorna o cliente se encontrado, None caso contrário."""
    return lista_clientes.get(str(cpf))

def validar_cpf(cpf):
    """Valida o CPF. Retorna True se válido, False caso contrário."""
    cpf = str(cpf)
    if len(cpf) != 11 or cpf == cpf[0] * 11 or not cpf.isdigit():
        return False
    # Calcula o primeiro dígito verificador
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    digito1 = (soma * 10) % 11
    if digito1 == 10:
        digito1 = 0

  # Calcula o segundo dígito verificador
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    digito2 = (soma * 10) % 11
    if digito2 == 10:
        digito2 = 0

    return cpf[-2:] == f"{digito1}{digito2}"

# Salvar os dados no arquivo JSON

def salvar_dados():
    with open(ARQUIVO, 'w', encoding='utf-8') as f:
        json.dump(lista_clientes, f, indent=2, ensure_ascii=False)