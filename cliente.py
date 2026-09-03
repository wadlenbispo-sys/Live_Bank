# dados pessoais do cliente;

# cada variavel está atribuindo ao usuario seus respectivos valores pessoais
def user_nome(nome_do_usuario):

   return nome_do_usuario

def user_senha(senha__do_usuario):

  return senha_do_usuario

def user_cpf(cpf_do_usuario):

  return cpf_do_usuario
  
# verificação de idade do cliente
def user_idade(idade_do_cliente):
  
  if idade_do_cliente >= 18:
     return  idade_do_cliente,"idade valida"
  else :
     return "idade fora das condições, voce pode ser menor de idade!!
