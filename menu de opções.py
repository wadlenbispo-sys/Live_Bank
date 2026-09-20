#Menu de opções 
def menu_de_opcoes():
  print('============= Seja Bem-vindo ao Live_Bank =============')
  print('='*55)
  print('1 - Para cadastro do cliente ou um novo cliente')
  print('2 - Para fazer o cadastro da agencia, (obs:.só é possivel realizar essa operação com um cliente)')
  print('3 - Para fazer o cadastro da conta, (obs:.só é possivel realizar com agencia)')
  print('4 - Para fazer um deposito, (obs:.só é possivel realizar com conta)')
  print('5 - Para fazer um saque, (obs:.só é possivel realizar com conta)')
  print('6 - Para fazer uma transferencia, (obs:.só é possivel com conta)')
  print('7 - Para sair do banco')


  opcao = 0
  while opcao != 7:
      opcao = int(input('Digite a opção desejada: '))
      if opcao == 1:
         cadastro_cliente()

      if opcao == 2:
         cadastro_agencia()

      if opcao == 3:
         cadastro_conta()

      if opcao == 4:
         realizar_deposito()

      if opcao == 5:
         realizar_saque()

      if opcao == 6:
         realizar_transferencia()

      elif opcao not in [1,2,3,4,5,6,7]:
        print('desculpe para prossequir precisa cadastra')

  print('Volte logo, Até mais!')
menu_de_opcoes()
