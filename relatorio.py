# responsavel pelo relatorio geral e por cada agencia, também é responsavel por soma o total de saldos
def relatorio_do_banco(agencia_escolhida):
    montante_total__do_banco = sum(lista_saldos)

   # calcula o montante da agencia informada
    montante_agencia = 0
    total_cliente_da_agencia = 0
    # Vai percorre a lista de agencias usando a posição para achar o saldo correto
    for agencias in (len(lista_agencias)):
        if lista_agencias[i] == agencia_alvo:
           montante_agencia += lista_saldos[i]
           total_clientes_agencia += 1
    # Exibir o relatório com os dados dos montantes,contas,agencias e o total de contas no banco na tela
    print("\n" + "="*30)
    print("===== RELATÓRIO BANCÁRIO =====")
    print("="*30)
    print(f"Montante total do banco: R$ {agencia_escolhida}")
    print(f"Total de contas no banco: {len(lista_saldos)}")
    print("-"*30)
    print(f"Agencia pesquisada: {agencia_escolhida}")
    print(f"Montante da Agencia: R$ {montante_agencia}")
    print(f"Contas nesta Agencia: {total_clientes_agencia}")
    print(f"="*30 + "\n")
  
    
