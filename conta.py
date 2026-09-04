#account_atributo para atributo da conta.
account_name = ""
account_password = ""
account_balance = 0

#atribuir valores
def criar_conta(nome, senha, saldo):
    account_name = nome
    account_password = senha
    account_balance = saldo

def realizar_deposito(valor):
    account_balance += valor

def realizar_saque(valor):
    account_balance -= valor
