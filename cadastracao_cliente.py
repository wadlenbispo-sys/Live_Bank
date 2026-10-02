# verificação dos dados do cliente e armazenamento
import json

lista_clientes = {}


def cadastra_cliente(nome, senha, cpf):
    cpf = str(cpf)
    if cpf in lista_clientes:
        return False

    lista_clientes[cpf] = {
        'nome': nome,
        'senha': senha
    }
    return True


def salvar_dados():
    with open('clientes.json', 'w', encoding='utf-8') as f:
        json.dump(lista_clientes, f, indent=2, ensure_ascii=False)

    with open('nomes.json', 'w', encoding='utf-8') as f:
        json.dump({cpf: dados['nome'] for cpf, dados in lista_clientes.items()}, f, indent=2, ensure_ascii=False)

    with open('senhas.json', 'w', encoding='utf-8') as f:
        json.dump({cpf: dados['senha'] for cpf, dados in lista_clientes.items()}, f, indent=2, ensure_ascii=False)

    with open('cpfs.json', 'w', encoding='utf-8') as f:
        json.dump(list(lista_clientes.keys()), f, indent=2, ensure_ascii=False)