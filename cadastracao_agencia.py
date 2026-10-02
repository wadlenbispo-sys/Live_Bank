import json

lista_agencias = {}


def numero_cnpj(cadastro):
    cadastro = str(cadastro)
    while cadastro in lista_agencias:
        cadastro = input('Código já cadastrado, digite outro código: ')
    lista_agencias[cadastro] = {'codigo': cadastro}
    return True


def salvar_dados():
    with open('agencias_cadastradas.json', 'w', encoding='utf-8') as f:
        json.dump(lista_agencias, f, indent=2, ensure_ascii=False)

    with open('codigo_agencia.json', 'w', encoding='utf-8') as f:
        json.dump(list(lista_agencias.keys()), f, indent=2, ensure_ascii=False)