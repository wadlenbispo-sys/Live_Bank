#Menu de opções 
import cadastracao_cliente,cadastracao_agencia,cadastracao_conta,relatorio

def ler_numero(texto):
    """Lê um número decimal. Retorna None se o valor for inválido."""
    try:
        return float(input(texto).replace(',', '.'))
    except ValueError:
        print('Valor inválido. Digite apenas números.')
        return None
    
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
  print('8 - Para ver o relatório de clientes')
  print('9 - Para ver o relatório do banco')


  opcao = 0
  while opcao != 7:
      opcao = int(input('Digite a opção desejada: '))
      if opcao == 1:
         nome = input('Digite o nome do cliente: ')
         senha = input('Digite a senha do cliente: ')
         cpf = input('Digite o CPF do cliente (somente números): ')
         cpf = ''.join(filter(str.isdigit, cpf))  # Remove caracteres não numéricos
         if not cadastracao_cliente.validar_cpf(cpf):
            print('CPF inválido. Tente novamente.')
         else:
            if cadastracao_cliente.cadastra_cliente(nome, senha, cpf):
               cadastracao_cliente.salvar_dados()
               print('Cliente cadastrado com sucesso!')
            else:
               print('CPF já cadastrado. Tente novamente.')
         
      if opcao == 2:
         if not cadastracao_cliente.lista_clientes:
            print('Não é possível cadastrar uma agência sem clientes. Cadastre um cliente primeiro.')
         else:
            cnpj = input('Digite o CNPJ da agência: ')
            codigo = input('Digite o código da agência: ')
            if cadastracao_agencia.cadastra_agencia(cnpj, codigo):
               cadastracao_agencia.salvar_dados()
               print('Agência cadastrada com sucesso!')
            else:
               print('CNPJ ou código já cadastrado. Tente novamente.')
 
      if opcao == 3:
         if not cadastracao_agencia.lista_agencias:
            print('Não é possível cadastrar uma conta sem agências. Cadastre uma agência primeiro.')
         else:
            numero = input('Digite o número da conta: ')
            agencia = input('Digite o CNPJ da agência: ')
            codigo = input('Digite o código da agência: ')
            if not cadastracao_agencia.codigo_existe(codigo):
               print('Agência não encontrada. Cadastre a agência primeiro.')
               return
 
            tipo = input('Tipo da conta (1 - corrente, 2 - salário, 3 - poupança): ')
            if tipo not in cadastracao_conta.TIPOS:
               print('Tipo de conta inválido. Escolha 1, 2 ou 3.')
               return
 
            saldo = ler_numero('Digite o saldo inicial: ')
            if saldo is None:
               return
            if saldo < 0:
               print('O saldo inicial não pode ser negativo.')
               return
 
            if cadastracao_conta.cadastracao_contas( numero,agencia,saldo, cadastracao_conta.TIPOS[tipo]):
               cadastracao_conta.salvar_dados()
               print('Conta cadastrada com sucesso!')
            else:
               print('Número de conta já cadastrado.')


      if opcao == 4:
         conta_numero = input('Digite o número da conta para depósito: ')
         valor = ler_numero('Digite o valor do depósito: ')
         if valor is None:
            return
         resultado = cadastracao_conta.deposito(conta_numero, valor)
         print(resultado)
         cadastracao_conta.salvar_dados()

      if opcao == 5:
         if not cadastracao_conta.contas_correntes:
            print('Não é possível realizar um saque sem contas cadastradas. Cadastre uma conta primeiro.')
         else:
            conta = input('Número da conta: ')
            valor = ler_numero('Valor do saque: ')
            if valor is None:
               return
            print(cadastracao_conta.saque(conta, valor))
            cadastracao_conta.salvar_dados()

      if opcao == 6:
         if not cadastracao_conta.contas_correntes:
            print('Não é possível realizar uma transferência sem contas cadastradas. Cadastre uma conta primeiro.')
         else:
            origem = input('Número da conta de origem: ')
            destino = input('Número da conta de destino: ')
            valor = ler_numero('Valor da transferência: ')
            if valor is None:
               return
            resultado = cadastracao_conta.transferencia(origem, destino, valor)
            print(resultado)
            cadastracao_conta.salvar_dados()
      if opcao == 8:
         print(cadastracao_conta.aplicar_rendimento(input('Digite o CNPJ da agência para aplicar o rendimento: '), ler_numero('Digite a taxa de rendimento (%): ')))
         cadastracao_conta.salvar_dados()
      if opcao == 9:
         relatorio.gerar_relatorio_completo()

      elif opcao not in [1,2,3,4,5,6,7,8,9]:
        print('desculpe para prossequir precisa cadastra')

  print('Volte logo, Até mais!')