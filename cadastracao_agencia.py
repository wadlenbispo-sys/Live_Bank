import json

lista_cnpjs = []

def numero_cnpj(cadastro):
    while cadastro in lista_cnpjs:
        cadastro = input('Código já cadastrado, digite outro código: ')
    lista_cnpjs.append(cadastro)
    return True

#listar agencias cadastradas
def listar_agencias():
    lista_agencias = set()
    for i in range(len(lista_cnpjs)):
        lista_agencias.add((lista_cnpjs[i]))
    return lista_agencias

def salvar_dados():
    with open('codigo_agencia.json', 'w', encoding="utf-8") as f:
        json.dump(lista_cnpjs, f, indent=2)