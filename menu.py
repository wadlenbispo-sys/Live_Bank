#Menu de opções 
import cadastracao_cliente,cadastracao_agencia,cadastracao_conta,relatorio


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
  print('8 - Para ver o relatório do banco')


  opcao = 0
  while opcao != 7:
      opcao = int(input('Digite a opção desejada: '))
      if opcao == 1:
         cadastracao_cliente.cadastra_cliente(input(),input(),input())
         cadastracao_cliente.salvar_dados()

      if opcao == 2:
         cadastracao_agencia.numero_cnpj(input())
         cadastracao_agencia.salvar_dados()

      if opcao == 3:
         cadastracao_conta.cadastracao_contas(input(),int(input()),int(input()))
         cadastracao_conta.salvar_dados()

      if opcao == 4:
         resultado = cadastracao_conta.deposito(input('Número da conta: '),float(input('Valor do depósito: ')))
         print(resultado)
         cadastracao_conta.salvar_dados()

      if opcao == 5:
         resultado = cadastracao_conta.saque(input('Número da conta: '),float(input('Valor do saque: ')))
         print(resultado)
         cadastracao_conta.salvar_dados()

      if opcao == 6:
         resultado = cadastracao_conta.transferencia(input('Número da conta de origem: '),input('Número da conta de destino: '),float(input('Valor da transferência: ')))
         print(resultado)
         cadastracao_conta.salvar_dados()

      if opcao == 8:
         relatorio.gerar_relatorio_completo()

      elif opcao not in [1,2,3,4,5,6,7,8]:
        print('desculpe para prossequir precisa cadastra')

  print('Volte logo, Até mais!')
menu_de_opcoes()
