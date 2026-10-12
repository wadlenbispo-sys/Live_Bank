#Menu de opções 
import conta_salario, conta_poupanca
import cadastracao_cliente, cadastracao_agencia, conta_corrente, relatorio

def ler_numero(texto):
    """Lê um número decimal. Retorna None se o valor for inválido."""
    try:
        return float(input(texto).replace(',', '.'))
    except ValueError:
        print('Valor inválido. Digite apenas números.')
        return None
    
def operacoes_conta_corrente(cnpj, codigo):
    """Submenu de operações. Termina quando o usuário digita 0."""
    escolha = ''
    while escolha != '0':
        print('\n1 - Depósito | 2 - Saque | 3 - Aplicar rendimento | 0 - Voltar')
        escolha = input('Escolha: ').strip()

        if escolha in ('1', '2', '3'):
            if escolha == '3':
                valor = ler_numero('Taxa de rendimento (%): ')
            else:
                valor = ler_numero('Digite o valor: ')

            if valor is None or valor <= 0:
                print('Valor inválido. Tente novamente.')
            else:
                if escolha == '1':
                    ok, msg = conta_corrente.deposito(codigo, valor)
                elif escolha == '2':
                    ok, msg = conta_corrente.saque(codigo, valor)
                else:
                    ok, msg = conta_corrente.aplicar_rendimento(cnpj, valor)

                print(msg)
                if ok:
                    conta_corrente.salvar_dados()
        elif escolha != '0':
            print('Opção inválida.')

def menu_de_opcoes():
  print('============= Seja Bem-vindo ao Live_Bank =============')
  print('='*55)
  print('1 - Para cadastro do cliente ou um novo cliente')
  print('2 - Para cadastro da agência ou uma nova agência')
  print('3 - Para cadastro da conta corrente ou uma nova conta corrente, com depósito, saque e rendimento')
  print('4 - Para cadastro da conta salário ou uma nova conta salário')
  print('5 - Para cadastro da conta poupança ou uma nova conta poupança')
  print('6 - Para gerar relatório de clientes cadastrados')
  print('7 - Para gerar relatório de agências cadastradas')
  print('8 - Para gerar relatório de contas cadastradas')
  print('9 - Para sair do sistema')

  opcao = 0
  while opcao != 9:
      opcao = int(input('Digite a opção desejada: '))
      if opcao == 1:
         nome = input('Digite o nome do cliente: ')
         senha = input('Digite a senha do cliente: ')
         cpf = input('Digite o CPF do cliente: ')
         cidade = input('Digite a cidade do cliente: ')
         estado = input('Digite o estado do cliente: ')
         cpf = ''.join(filter(str.isdigit, cpf))  # Remove caracteres não numéricos
         if not cadastracao_cliente.validar_cpf(cpf):
            print('CPF inválido. Tente novamente.')
         else:
            if cadastracao_cliente.cadastra_cliente(nome, senha, cpf, cidade, estado):
               cadastracao_cliente.salvar_dados()
               print('Cliente cadastrado com sucesso!')
            else:
               print('CPF já cadastrado. Tente novamente.')
         
      if opcao == 2:
         if not cadastracao_cliente.lista_clientes:
            print('Não é possível cadastrar uma agência sem clientes. Cadastre um cliente primeiro.')
         else:
            nome = input('Digite o nome do sócio: ')
            cpf = input('Digite o CPF do sócio da agência: ')
            cnpj = input('Digite o CNPJ da agência: ')
            codigo = input('Digite o código da agência: ')
            cidade = input('Digite a cidade da agência: ')
            estado = input('Digite o estado da agência: ')
            if cadastracao_agencia.cadastra_agencia(nome, cpf, cnpj, codigo,cidade, estado):
               cadastracao_agencia.salvar_dados()
               print('Agência cadastrada com sucesso!')
            else:
               print('CNPJ ou código já cadastrado. Tente novamente.')
 
      if opcao == 3:
         if not cadastracao_agencia.lista_agencias:
            print('Não é possível cadastrar uma conta corrente sem agências. Cadastre uma agência primeiro.')
         else:
            cnpj = input('Digite o CNPJ da agência: ')
            codigo = input('Digite o código da conta: ')
            numero_conta = input('Digite o número da conta: ')
            cidade = input('Digite a cidade da conta: ')
            estado = input('Digite o estado da conta: ')
            saldo_inicial = ler_numero('Digite o saldo inicial da conta: ')

            if saldo_inicial is None or saldo_inicial < 0:
               print('Saldo inicial inválido.')
            elif not conta_corrente.cadastra_conta_corrente(
                    cnpj, codigo, numero_conta, cidade, estado, saldo_inicial):
               print('CNPJ ou código já cadastrado. Tente novamente.')
            else:
               conta_corrente.salvar_dados()
               print('Conta corrente cadastrada com sucesso!')
               operacoes_conta_corrente(cnpj, codigo)

      if opcao == 4:
         if not conta_corrente.lista_contas_correntes:
            print('Não é possível cadastrar uma conta salário sem contas correntes. Cadastre uma conta corrente primeiro.')
         else:
            cnpj = input('Digite o CNPJ da agência: ')
            codigo = input('Digite o código da conta: ')
            numero_conta = input('Digite o número da conta: ')
            cidade = input('Digite a cidade da conta: ')
            estado = input('Digite o estado da conta: ')
            saldo_inicial = ler_numero('Digite o saldo inicial da conta: ')

            if saldo_inicial is None or saldo_inicial < 0:
               print('Saldo inicial inválido.')
            elif conta_salario.cadastra_conta_salario(
               cnpj, codigo, numero_conta, cidade, estado, saldo_inicial):
               conta_salario.salvar_dados()
               print('Conta salário cadastrada com sucesso!')
            else:
               print('CNPJ ou código já cadastrado. Tente novamente.')

      if opcao == 5:
         if not conta_poupanca.lista_contas_correntes:
            print('Não é possível cadastrar uma conta salário sem contas correntes. Cadastre uma conta corrente primeiro.')
         else:
            cnpj = input('Digite o CNPJ da agência: ')
            codigo = input('Digite o código da conta: ')
            numero_conta = input('Digite o número da conta: ')
            cidade = input('Digite a cidade da conta: ')
            estado = input('Digite o estado da conta: ')
            saldo_inicial = ler_numero('Digite o saldo inicial da conta: ')

            if saldo_inicial is None or saldo_inicial < 0:
               print('Saldo inicial inválido.')
            elif conta_poupanca.cadastra_conta_poupanca(
                    cnpj, codigo, numero_conta, cidade, estado, saldo_inicial):
               conta_poupanca.salvar_dados()
               print('Conta salário cadastrada com sucesso!')
            else:
               print('CNPJ ou código já cadastrado. Tente novamente.')
               
      if opcao == 6:
         relatorio.relatorio_clientes()
      if opcao == 7:
         relatorio.relatorio_agencias()
      if opcao == 8:
         relatorio.relatorio_contas()
      if opcao == 9:
         print('Obrigado por utilizar o Live_Bank!, Até logo!')
      elif opcao not in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
         print('Opção inválida. Digite um número de 1 a 9.')
