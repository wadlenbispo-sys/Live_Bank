# verificação dos dados do cliente e armazenamento
lista_nomes = []
lista_senhas = []
lista_cpfs = []

def cadastra_cliente(nome,senha,cpf):
    if cpf in lista_cpfs:
       return False
    else :
      lista_nomes.append(nome)
      lista_senhas.append(senha)
      lista_cpfs.append(cpf)
      return True


import json
def salvar_dados():
    with open('nomes.json', 'w', encoding="utf-8") as f:
        json.dump(lista_nomes, f, indent=2)
    with open('senhas.json', 'w', encoding="utf-8") as f:
        json.dump(lista_senhas, f, indent=2)
    with open('cpfs.json', 'w', encoding="utf-8") as f:
        json.dump(lista_cpfs, f, indent=2)