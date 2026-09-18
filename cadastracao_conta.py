lista_numero_contas = []
lista_agencias = []
lista_saldos = []
lista_cpfs = []

def cadastracao_contas(numero_conta,agencia,saldo):
    if numero_conta in lista_numero_contas:
       return False
    if agencia in lista_agencias:
       return False
    if saldo in lista_saldos:
       return False
    else :
      lista_numero_contas.append(numero_conta)
      lista_agencias.append(agencia)
      lista_saldos.append(saldo)
      return True