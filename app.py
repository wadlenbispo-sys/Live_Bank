import os
import json
import re
from flask import Flask, render_template, request, redirect, url_for, flash
from functools import reduce

app = Flask(__name__, template_folder='teste4_templates')
app.secret_key = "troque-esta-chave"
ARQUIVO = os.path.join(os.path.dirname(__file__), 'dados.json')

TIPOS_VALIDOS = {
    'corrente': 'Conta Corrente',
    'poupanca': 'Conta Poupança',
    'salario': 'Conta Salário',
}
PERMISSOES = {
    'corrente': {'saque', 'deposito','transferencia'},
    'poupanca': {'deposito', 'rendimento'},
    'salario': {'saque'},
}

TEXTO_OPERACAO = {
    'saque': 'Saque',
    'deposito': 'Depósito',
    'rendimento': 'Rendimento',
    'transferencia': 'Transferência'
}

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
                        # | Armazenamento de Dados |
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
def carregar_dados():
    """Lê o JSON. Se não existir ou estiver corrompido, devolve a estrutura vazia."""
    dados = {}
    try:
        with open(ARQUIVO, 'r', encoding='utf-8') as f:
            lido = json.load(f)
            if isinstance(lido, dict):
                dados = lido
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    for chave in ('clientes', 'agencias', 'contas'):
        if not isinstance(dados.get(chave), dict):
            dados[chave] = {}
    return dados


def salvar_dados(dados):
    with open(ARQUIVO, 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
                     # | Funções Auxiliares |
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
def somente_digitos(texto):
    return re.sub(r'\D', '', texto or '')

def validar_cpf(cpf):
    """Valida o CPF pelos dígitos verificadores."""
    if len(cpf) != 11 or not cpf.isdigit() or cpf == cpf[0] * 11:
        return False
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    d1 = (soma * 10) % 11 % 10
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    d2 = (soma * 10) % 11 % 10
    return cpf[-2:] == f"{d1}{d2}"

def ler_valor():
    """Lê o campo 'valor' do formulário. Retorna None se for inválido ou <= 0."""
    try:
        valor = float(request.form.get('valor', '').replace(',', '.'))
    except ValueError:
        return None
    return valor if valor > 0 else None


def erro(mensagem):
    flash(mensagem, 'erro')


def ok(mensagem):
    flash(mensagem, 'ok')


@app.template_filter('moeda')
def moeda(valor):
    texto = f"{float(valor):,.2f}"
    return "R$ " + texto.replace(',', 'X').replace('.', ',').replace('X', '.')


@app.template_filter('cpf')
def formatar_cpf(valor):
    v = str(valor)
    return f"{v[:3]}.{v[3:6]}.{v[6:9]}-{v[9:]}" if len(v) == 11 else v


@app.template_filter('cnpj')
def formatar_cnpj(valor):
    v = str(valor)
    if len(v) != 14:
        return v
    return f"{v[:2]}.{v[2:5]}.{v[5:8]}/{v[8:12]}-{v[12:]}"

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
                            # | Início |
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
@app.route('/')
@app.route('/dashboard')
def index():
    dados = carregar_dados()
    contas = list(dados['contas'].items())
    saldo_total = round(sum(conta['saldo'] for _, conta in contas), 2)
    maior_conta = max(contas, key=lambda item: item[1]['saldo'], default=None)
    saldos_por_tipo = {}
    for tipo, nome in TIPOS_VALIDOS.items():
        contas_tipo = [conta for _, conta in contas if conta['tipo'] == tipo]
        saldos_por_tipo[tipo] = {
            'nome': nome,
            'quantidade': len(contas_tipo),
            'saldo': round(sum(conta['saldo'] for conta in contas_tipo), 2),
        }
    return render_template('index.html',
                           total_clientes=len(dados['clientes']),
                           total_agencias=len(dados['agencias']),
                           total_contas=len(contas),
                           tem_clientes=bool(dados['clientes']),
                           tem_agencias=bool(dados['agencias']),
                           saldo_total=saldo_total,
                           saldo_medio=round(saldo_total / len(contas), 2) if contas else 0,
                           maior_conta=maior_conta,
                           saldos_por_tipo=saldos_por_tipo,
                           maior_saldo_tipo=max(
                               (item['saldo'] for item in saldos_por_tipo.values()),
                               default=0))

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
                            # | Clientes |
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
@app.route('/clientes')
def clientes():
    dados = carregar_dados()
    return render_template('clientes.html', clientes=dados['clientes'])


@app.route('/clientes/cadastrar', methods=['POST'])
def cadastrar_cliente():
    nome = request.form.get('nome', '').strip()
    cpf = somente_digitos(request.form.get('cpf'))
    senha = request.form.get('senha', '')
    cidade = request.form.get('cidade', '').strip()
    estado = request.form.get('estado', '').strip().upper()

    if not nome or not cidade or len(estado) != 2:
        erro("Preencha nome, cidade e UF (2 letras).")
        return redirect(url_for('clientes'))
    if not validar_cpf(cpf):
        erro("CPF inválido. Tente novamente.")
        return redirect(url_for('clientes'))
    if len(senha) < 4 or len(senha) > 15:
        erro("A senha deve ter 4~15 caracteres.")
        return redirect(url_for('clientes'))

    dados = carregar_dados()
    if cpf in dados['clientes']:
        erro("CPF já cadastrado.")
        return redirect(url_for('clientes'))

    dados['clientes'][cpf] = {
        'nome': nome,
        'senha': senha,  
        'cidade': cidade,
        'estado': estado,
    }

    dados['clientes'] = dict(sorted(dados['clientes'].items(),key = lambda item: item[1]['nome']))
    salvar_dados(dados)
    ok("Cliente cadastrado com sucesso!")
    return redirect(url_for('clientes'))


@app.route('/clientes/deletar/<cpf>', methods=['POST'])
def deletar_cliente(cpf):
    dados = carregar_dados()
    if cpf not in dados['clientes']:
        erro("Cliente não encontrado.")
    elif any(a['socio_cpf'] == cpf for a in dados['agencias'].values()):
        erro("Não é possível excluir: o cliente é sócio de uma agência.")
    elif any(c['cliente_cpf'] == cpf for c in dados['contas'].values()):
        erro("Não é possível excluir: o cliente possui contas.")
    else:
        del dados['clientes'][cpf]
        salvar_dados(dados)
        ok("Cliente removido.")
    return redirect(url_for('clientes'))

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
                            # | Agencias |
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
@app.route('/agencias')
def agencias():
    dados = carregar_dados()
    return render_template('agencias.html',
                           agencias=dados['agencias'],
                           clientes=dados['clientes'])


@app.route('/agencias/cadastrar', methods=['POST'])
def cadastrar_agencia():
    socio_cpf = request.form.get('socio_cpf', '')
    cnpj = somente_digitos(request.form.get('cnpj'))
    codigo = request.form.get('codigo', '').strip()
    cidade = request.form.get('cidade', '').strip()
    estado = request.form.get('estado', '').strip().upper()

    dados = carregar_dados()
    if socio_cpf not in dados['clientes']:
        erro("Ausência de um Cliente sócio! Cadastre um cliente primeiro.")
    elif len(cnpj) != 14:
        erro("CNPJ inválido: informe 14 dígitos.")
    elif not codigo or not cidade or len(estado) != 2:
        erro("Preencha código, cidade e UF (2 letras).")
    elif cnpj in dados['agencias'] or any(agencia['codigo'] == codigo for agencia in dados['agencias'].values()):
        erro("CNPJ ou código já cadastrado.")
    else:
        dados['agencias'][cnpj] = {
            'codigo': codigo,
            'socio_cpf': socio_cpf,
            'cidade': cidade,
            'estado': estado,
        }
        dados['agencias'] = dict(sorted(dados['agencias'].items(),key = lambda item: item[1]['socio_cpf']))
        salvar_dados(dados)
        ok("Agência cadastrada com sucesso!")
    return redirect(url_for('agencias'))


@app.route('/agencias/deletar/<cnpj>', methods=['POST'])
def deletar_agencia(cnpj):
    dados = carregar_dados()
    if cnpj not in dados['agencias']:
        erro("Agência não encontrada.")
    elif any(c['agencia_cnpj'] == cnpj for c in dados['contas'].values()):
        erro("Não é possível excluir: a agência possui contas.")
    else:
        del dados['agencias'][cnpj]
        salvar_dados(dados)
        ok("Agência removida.")
    return redirect(url_for('agencias'))

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
                            # | Contas |
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
@app.route('/contas')
def contas():
    dados = carregar_dados()
    return render_template('contas.html',
                           contas=dados['contas'],
                           clientes=dados['clientes'],
                           agencias=dados['agencias'],
                           nomes=TIPOS_VALIDOS,
                           permissoes=PERMISSOES)


@app.route('/contas/cadastrar', methods=['POST'])
def cadastrar_conta():
    tipo = request.form.get('tipo')
    cliente_cpf = request.form.get('cliente_cpf')
    agencia_cnpj = request.form.get('agencia_cnpj')
    numero_conta = request.form.get('numero_conta','').strip()

    try:
        saldo = round(float((request.form.get('saldo_inicial') or '0').replace(',', '.')), 2)
    except ValueError:
        saldo = -1

    dados = carregar_dados()
    if tipo not in TIPOS_VALIDOS:
        erro("Conta Inválida! Selecione um tipo de conta válido.")
    elif any(conta['cliente_cpf'] == cliente_cpf and conta['tipo'] == tipo for conta in dados['contas'].values()):
        erro("Tipo de conta já cadastrada! Selecione outro tipo de conta.")
    elif cliente_cpf not in dados['clientes']:
        erro("Cliente inexistente! Selecione um cliente cadastrado.")
    elif agencia_cnpj not in dados['agencias']:
        erro("Agência inexistente! Selecione uma agência cadastrada.")
    elif numero_conta in dados['contas']:  
        erro("O Nº da conta já cadastrado! Selecione outro Número.")
    elif saldo < 0:
        erro("Saldo inicial inválido! Tente novamente.")
    else:
        dados['contas'][numero_conta] = {
            'numero_conta': numero_conta,
            'tipo': tipo,
            'cliente_cpf': cliente_cpf,
            'agencia_cnpj': agencia_cnpj,
            'saldo': saldo,
        }
        salvar_dados(dados)
        ok("Conta cadastrada com sucesso!")
    return redirect(url_for('contas'))

@app.route('/contas/<numero_conta>/<operacao>', methods=['POST'])
def operar_conta(numero_conta, operacao):
    """Saque, depósito ou rendimento, conforme as PERMISSOES do tipo da conta."""
    if operacao not in TEXTO_OPERACAO:
        erro("Operação inválida.")
        return redirect(url_for('contas'))

    valor = ler_valor()
    if valor is None:
        erro("O valor informado é inválido.")
        return redirect(url_for('contas'))

    
    dados = carregar_dados()
    conta = dados['contas'].get(numero_conta)
    numero_destino = request.form.get('conta_destino','').strip()
    conta_destino = dados['contas'].get(numero_destino)if operacao == 'transferencia' else None
    if not conta:
        erro("Conta não encontrada.")
    elif operacao not in PERMISSOES.get(conta['tipo'], set()):
        erro(f"Este tipo de conta não permite {TEXTO_OPERACAO[operacao].lower()}.")
    elif operacao == 'transferencia' and not conta_destino:
        erro("Conta de destino não encontrada.")
    elif operacao == 'transferencia' and numero_destino == numero_conta:
        erro("A conta de destino deve ser diferente da conta de origem.")
    elif operacao == 'transferencia' and 'deposito' not in PERMISSOES.get(conta_destino['tipo'], set()):
        erro("A conta de destino não aceita transferências.")
    elif operacao in ('saque', 'transferencia') and conta['saldo'] < valor:
        erro(f"Saldo insuficiente para realizar {TEXTO_OPERACAO[operacao].lower()}.")
    else:
        if operacao == 'saque':
            conta['saldo'] = round(conta['saldo'] - valor, 2)
        elif operacao == 'deposito':
            conta['saldo'] = round(conta['saldo'] + valor, 2)
        elif operacao == 'transferencia':
            conta['saldo'] = round(conta['saldo'] - valor, 2)
            conta_destino['saldo'] = round(conta_destino['saldo'] + valor, 2)
        else:
            conta['saldo'] = round(conta['saldo'] * (1 + valor / 100), 2)
        salvar_dados(dados)
        ok(f"{TEXTO_OPERACAO[operacao]} realizado com sucesso!")
    return redirect(url_for('contas'))


@app.route('/contas/deletar/<numero_conta>', methods=['POST'])
def deletar_conta(numero_conta):
    dados = carregar_dados()
    if numero_conta in dados['contas']:
        del dados['contas'][numero_conta]
        salvar_dados(dados)
        ok("Conta removida.")
    else:
        erro("Conta não encontrada.")
    return redirect(url_for('contas'))

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
                            # | Relatório |
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
@app.route('/relatorio')
def relatorio():
    dados = carregar_dados()
    registros = {}
    for chave, nome in TIPOS_VALIDOS.items():
        documentos_filtrados = filter(lambda item: item[1]['tipo'] == chave, dados['contas'].items())
        modelo_conta = dict(documentos_filtrados)
        total_contas = round(sum(map(lambda conta: conta['saldo'], modelo_conta.values())), 2)
        saldo_total = round(reduce(lambda sigma,conta: sigma + conta['saldo'],modelo_conta.values(),0),2)
        saldo_maior = max(map(lambda conta: conta['saldo'], modelo_conta.values()), default=0)
        saldo_menor = min(map(lambda conta: conta['saldo'], modelo_conta.values()), default=0) 
        media = round(saldo_total / total_contas, 2) if total_contas else 0

        registros[chave] = {
            'nome': nome,
            'contas': modelo_conta,
            'total': total_contas,
            'saldo_geral': saldo_total,
            'maior_saldo': saldo_maior,
            'menor_saldo': saldo_menor,
            'media': media
        }
    total_geral = round(sum(registro['total'] for registro in registros.values()), 2)
    return render_template('relatorio.html',
                               clientes = dados['clientes'],
                               agencias = dados['agencias'],
                               registros = registros,
                               total_geral = total_geral)
    
if __name__ == '__main__':
    print("Servidor iniciado em http://127.0.0.1:5003")
    app.run(host='127.0.0.1', port=5003, debug=True)
