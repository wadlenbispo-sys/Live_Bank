lista_numero_contas = []
lista_agencias = []
lista_saldos = []
# responsavel por cadastra conta do cliente
def cadastracao_contas(numero_conta,agencia,saldo):
    if numero_conta in lista_numero_contas:
       return False
    else :
      lista_numero_contas.append(numero_conta)
      lista_agencias.append(agencia)
      lista_saldos.append(saldo)
      return True
        
# responsavel por realizar o saque        
def saque(numero_conta,valor_de_saque):
    if numero_conta not in lista_numero_contas:
        return "Conta não encontrada!"
    indice = lista_numero_contas.index(numero_conta)
    if valor_de_saque <= 0:
        return "Não houve saque!"
    if valor_de_saque > lista_saldos[indice]:
        return "Saldo insuficiente!"
    lista_saldos[indice] -= valor_de_saque
    return "Saque realizado!"

# responsavel por realizar deposito
def deposito(numero_conta,valor_do_deposito):
    if numero_conta not in lista_numero_contas:
        return "Conta não encontrada!"
    indice = lista_numero_contas.index(numero_conta)
    if valor_do_deposito <= 0:
       return "Não houve depósito!"
    lista_saldos[indice] += valor_do_deposito
    return "Depósito realizado!"
        
# responsavel por realizar transferencia
def transferencia(numero_conta_origem,numero_conta_destino,valor_de_transferencia):
    if numero_conta_origem not in lista_numero_contas or numero_conta_destino not in lista_numero_contas:
        return "Conta não encontrada!"
    indice_origem = lista_numero_contas.index(numero_conta_origem)
    indice_destino = lista_numero_contas.index(numero_conta_destino)
    
    if valor_de_transferencia <= 0:
        return "Valor de transferência inválido!"
    
    if valor_de_transferencia > lista_saldos[indice_origem]:
       return "!erro: você tentou transferir um valor maior do que o valor atual"
    lista_saldos[indice_origem] -= valor_de_transferencia
    lista_saldos[indice_destino] += valor_de_transferencia
    return "transferência concluída!"
        
# salvar em formato json
import json
def salvar_dados():
   with open('numero_contas.json', 'w', encoding="utf-8") as f:
      json.dump(lista_numero_contas, f, indent=2)
   with open('agencias.json', 'w', encoding="utf-8") as f:
      json.dump(lista_agencias, f, indent=2)
   with open('saldos.json', 'w', encoding="utf-8") as f:
      json.dump(lista_saldos, f, indent=2)
