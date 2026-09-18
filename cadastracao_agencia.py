def codigo_agencia():
    while True:
        if codigo_agencia.isdigit() and len(codigo_agencia) == 4:
            return codigo_agencia
        print("Invalido!, digite novamente com apenas numeros e 4 digitos")
