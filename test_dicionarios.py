import cadastracao_cliente
import conta_corrente

def verificar(condicao, mensagem):
    if not condicao:
        raise ValueError(mensagem)

def test_cliente_em_dicionario():
    cadastracao_cliente.lista_clientes = {}
    verificar(cadastracao_cliente.cadastra_cliente('Ana', '123', '111') is True, 'Cliente não foi cadastrado.')
    verificar(cadastracao_cliente.lista_clientes['111'] == {'nome': 'Ana', 'senha': '123'}, 'Estrutura do cliente incorreta.')
    verificar(cadastracao_cliente.cadastra_cliente('Maria', '456', '111') is False, 'CPF duplicado não foi bloqueado.')

def test_conta_em_dicionario():
    conta_corrente.contas_correntes = {}
    verificar(conta_corrente.cadastra_conta_corrente('001', '1001', 250.0) is True, 'Conta não foi cadastrada.')
    verificar(conta_corrente.contas_correntes['1001'] == {'agencia': '001', 'saldo': 250.0}, 'Estrutura da conta incorreta.')
    verificar(conta_corrente.deposito('1001', 50.0) == 'Depósito realizado!', 'Depósito não foi concluído.')
    verificar(conta_corrente.contas_correntes['1001']['saldo'] == 300.0, 'Saldo da conta incorreto após depósito.')
