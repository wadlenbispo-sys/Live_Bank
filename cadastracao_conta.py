lista_numero_contas = []
lista_agencias = []
lista_saldos = []

def cadastracao_contas(numero_conta,agencia,saldo):
    if numero_conta in lista_numero_contas:
       return False
    else :
      lista_numero_contas.append(numero_conta)
      lista_agencias.append(agencia)
      lista_saldos.append(saldo)
      return True

import json
def salvar_dados():
   with open('numero_contas.json', 'w', encoding="utf-8") as f:
      json.dump(lista_numero_contas, f, indent=2)
   with open('agencias.json', 'w', encoding="utf-8") as f:
      json.dump(lista_agencias, f, indent=2)
   with open('saldos.json', 'w', encoding="utf-8") as f:
      json.dump(lista_saldos, f, indent=2)