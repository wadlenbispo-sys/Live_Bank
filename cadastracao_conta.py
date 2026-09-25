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
def saque(posição_do_cliente,valor_de_saque):
    if valor_de_saque <= 0:
        return "Não houver saque!"
    if valor_de_saque > lista_saldos[posição_do_cliente]:
        return "saldo insuficiente!"
    else:
        novo_valor[posição_do_cliente] -= valor_de_saque
        return f"Seu saque de: R${valor_de_saque} foi realizado!"
             
      
# responsavel por realizar deposito
def deposito(posição_do_cliente,valor_do_deposito):
    if valor_do_deposito <= 0:
       return "Não houver depósito"
    else:
       lista_saldos[posição_do_cliente] += valor_do_deposito
       return f"Seu depósito de: R${valor_do_deposito} foi realizado!onde "
        
# responsavel por realizar transferencia
def transferencia(posição_de_envio,posição_do_recebo,valor_de_transferencia):
    if valor_de_transferencia <= 0:
        return "ocorreu um erro!.tente enviar um valor positivo!"
    if valor_de_transferencia > lista_saldos[posição_de_envio]:
       return "!erro: você tentou transferir um valor maior do que o valor atual"
    else:
        lista_saldos[posição_de_envio] -= valor_de_transferencia
        lista_saldos[posição_do_recebo] += valor_de_transferencia
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
