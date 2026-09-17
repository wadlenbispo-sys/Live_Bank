# verificação dos dados do cliente e armazenamento
lista_nomes = []
lista_senhas = []
lista_cpfs = []

def cadastra_cliente(nome,senha,cpf):
    if nome in lista_nomes:
       return False
    if senha in lista_senhas:
       return False
    if cpf in lista_cpfs:
       return False
    else :
      lista_nomes.append(nome)
      lista_senhas.append(senha)
      lista_cpfs.append(cpf)
      return True
    
