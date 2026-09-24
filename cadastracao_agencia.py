import json

lista_cnpjs = []

def numero_cnpj(cadastro):
    while cadastro in lista_cnpjs:
        cadastro = input('Código já cadastrado, digite outro código: ')
    lista_cnpjs.append(cadastro)
    return True

def salvar_dados():
    with open('codigo_agencia.json', 'w', encoding="utf-8") as f:
        json.dump(lista_cnpjs, f, indent=2)